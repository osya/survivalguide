#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import utc
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field
import datetime

from talks.models import TalkList, Talk


class TalkListForm(forms.ModelForm):
    """
    Form for creating new TalkList
    """
    class Meta:
        fields = ('name',)
        model = TalkList

    def __init__(self, *args, **kwargs):
        super(TalkListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'name',
                ButtonHolder(
                        Submit('submit', 'Submit', css_class='btn btn-primary')
                )
        )


class TalkForm(forms.ModelForm):
    """
    Form for creating new Talks
    """
    class Meta:
        fields = ('talk_list', 'name', 'host', 'when', 'room')
        model = Talk

    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'name', 'host', 'when', 'room',
                Field('talk_list', type="hidden"),
                ButtonHolder(
                        Submit('create', 'Create')
                )
        )

    def clean_when(self):
        when = self.cleaned_data.get('when')
        pycon_start = datetime.datetime(2014, 4, 11).replace(tzinfo=utc)
        pycon_end = datetime.datetime(2014, 4, 13, 17).replace(tzinfo=utc)
        if not pycon_start < when < pycon_end:
            raise ValidationError("'when' is outside of PyCon")
        return when

    def save(self):
        super(TalkForm, self).save()
        return self.instance
