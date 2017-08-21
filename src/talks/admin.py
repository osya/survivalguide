from django.contrib import admin
from .models import TalkList, Talk


class TalkListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(TalkList, TalkListAdmin)


class TalkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Talk, TalkAdmin)
