#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field
from . import models


class TalkListForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = models.TalkList

    def __init__(self, *args, **kwargs):
        super(TalkListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'name',
                ButtonHolder(
                        Submit('submit', 'Submit', css_class='btn btn-primary')
                )
        )


class CommonFormHelper(FormHelper):
    def __init__(self):
        super(CommonFormHelper, self).__init__()
        self.disable_csrf = True
        self.form_tag = False


class TalkListDetailForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = models.TalkList

    def __init__(self, *args, **kwargs):
        super(TalkListDetailForm, self).__init__(*args, **kwargs)
        self.helper = CommonFormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
                Field('name', readonly=True),
        )
