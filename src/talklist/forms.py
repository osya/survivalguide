#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from talklist.models import TalkList


class TalkListForm(forms.ModelForm):
    """
    Form for creating new TalkList
    """

    class Meta:
        fields = ('name', )
        model = TalkList

    def __init__(self, *args, **kwargs):
        super(TalkListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout('name', FormActions(Submit('submit', 'Submit')))
