#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from talk.models import Talk


class TalkSerializer(serializers.ModelSerializer):
    """
        This serializer used for TalkViewSet
    """

    class Meta:
        model = Talk
        fields = ('id', 'talklist', 'name', 'user')

    # Show name instead of id
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')


class TalkUpdateSerializer(serializers.ModelSerializer):
    """
        This serializer used for TalkListSerializer to be able to create new Talks during TalkLIst partial update
    """

    class Meta:
        model = Talk
        # According to 'talklist' field, I suppose that during updating TalkList it will be not possible to change
        # TalkList for talk
        fields = ('id', 'name', 'user')

    # To be possible to make TalkList partial update with creating new talks Talk.id field should be not read_only
    # It is read_only by default as a PK
    id = serializers.IntegerField(label='ID')
    # Show name instead of id
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')
