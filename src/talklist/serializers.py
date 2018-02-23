#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from talk.models import Talk
from talk.serializers import TalkUpdateSerializer
from talklist.models import TalkList


class TalkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkList
        fields = ('id', 'name', 'talks', 'user')
        read_only_fields = ('user', )

    talks = TalkUpdateSerializer(many=True)
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')

    def create(self, validated_data):
        talks_data = validated_data.pop('talks', None)
        talklist = TalkList.objects.create(**validated_data)
        for talk_data in talks_data:
            Talk.objects.create(talklist=talklist, **talk_data)
        return talklist

    def update(self, instance, validated_data):
        if 'talks' in validated_data:
            talks_data = validated_data.pop('talks')
            if talks_data:
                talks_to_delete = instance.talks.exclude(pk__in=[item.get('id', None) for item in talks_data])

                for item in talks_data:
                    item_id = item.get('id', None)
                    if item_id:
                        talk_item = Talk.objects.get(id=item_id, talklist=instance)
                        talk_item.name = item.get('name', talk_item.name)
                        talk_item.save()
                    else:
                        Talk.objects.create(talklist=instance, **item)
            else:
                talks_to_delete = instance.talks.all()
            # Delete talks which are not exists in validated_data
            if talks_to_delete:
                talks_to_delete.delete()

        super(self.__class__, self).update(instance, validated_data)
        return instance
