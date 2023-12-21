from django.contrib import admin

from board.models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'title', 'category')
    list_filter = ('created_at', 'created_by', 'title', 'category')
    search_fields = ('title',)


admin.site.register(Ad, AdAdmin)
