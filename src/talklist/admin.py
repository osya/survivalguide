from django.contrib import admin

# Register your models here.
from talklist.models import TalkList


class TalkListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(TalkList, TalkListAdmin)
