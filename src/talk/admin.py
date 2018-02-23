from django.contrib import admin

from talk.models import Talk


class TalkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Talk, TalkAdmin)
