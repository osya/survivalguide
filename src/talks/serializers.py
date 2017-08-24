#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers

from talks.models import TalkList, Talk


class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('id', 'name',)


class TalkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkList
        fields = ('id', 'name', 'talks')

    talks = TalkSerializer(many=True)
