#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import utc

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit

from talk.models import Talk


class TalkForm(forms.ModelForm):
    """
    Form for creating new Talks
    """

    class Meta:
        fields = ('talklist', 'name', 'host', 'when', 'room')
        model = Talk

    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout('name', 'host', 'when', 'room', Field('talklist', type='hidden'),
                                    FormActions(Submit('create', 'Create')))

    def clean_when(self):
        when = self.cleaned_data.get('when')
        pycon_start = datetime.datetime(2014, 4, 11).replace(tzinfo=utc)
        pycon_end = datetime.datetime(2014, 4, 13, 17).replace(tzinfo=utc)
        if not pycon_start < when < pycon_end:
            raise ValidationError("'when' is outside of PyCon")
        return when

    def save(self, commit=True):
        super(TalkForm, self).save()
        return self.instance
