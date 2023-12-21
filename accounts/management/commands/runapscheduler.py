import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.db.models import F, Subquery
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from accounts.models import Subscription, EmailVerify
from board.models import Ad

logger = logging.getLogger(__name__)


def newsletter():
    logger.debug(f'Run sending at: {datetime.datetime.now()}')

    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    last_week = today - datetime.timedelta(days=7)

    last_sending_obj = DjangoJobExecution.objects.filter(
        job_id='sending_new_posts',
        status='Executed'
    ).order_by('-run_time').first()

    last_sending = last_sending_obj.run_time if last_sending_obj else last_week

    last_ads = (Ad.objects
                           .filter(created_at__gt=last_sending)
                           )

    subscriptions = Subscription.objects.filter(
        category__in=Ad.objects.filter(created_at__gt=last_sending).values('category')
    ).distinct()
    emails = []
    for subscription in subscriptions:
        linked_ads = last_ads.filter(category=subscription.category)
        for i in linked_ads:
            emails.append((i, subscription.user.email))

    sending_dict = dict()
    for ad, email in emails:
        if email in sending_dict:
            sending_dict[email].append(ad)
        else:
            sending_dict[email] = [ad]

    subject = f'Новые объявления с {last_sending.strftime("%x")}'
    text_content = (
        'Новые объявления на портале:\n'
    )
    html_content = (
        'Новые объявления на портале:<br>'
    )
    for mail, ads in sending_dict.items():
        msg = EmailMultiAlternatives(
            subject,
            text_content + '\n'.join([f'http://127.0.0.1{i.get_absolute_url()}' for i in ads]),
            None,
            [mail]
        )

        msg.attach_alternative(
            html_content + '<br>'.join(
                [f'<a href="http://127.0.0.1{i.get_absolute_url()}">{i.title}</a>' for i in ads]),
            "text/html"
        )
        msg.send()


def clear_email_verify():
    logger.debug('run clear_email_verify')
    # Код действителен в течении 5 минут
    last_minutes = datetime.datetime.now() - datetime.timedelta(minutes=5)
    email_verify = EmailVerify.objects.filter(sent__lt=last_minutes)
    for i in email_verify:
        i.delete()


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            newsletter,
            trigger=CronTrigger(hour='18', day_of_week='fri'),
            id="newsletter",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'newsletter'.")

        scheduler.add_job(
            clear_email_verify,
            trigger=CronTrigger(second='*/5'),
            id="clear_email_verify",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'clear_email_verify'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
