#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from talks.models import Talk, TalkList


class TalkSerializer(serializers.ModelSerializer):
    """
        This serializer used for TalkViewSet
    """

    class Meta:
        model = Talk
        fields = ('id', 'talk_list', 'name', 'user')

    # Show name instead of id
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')


class TalkUpdateSerializer(serializers.ModelSerializer):
    """
        This serializer used for TalkListSerializer to be able to create new Talks during TalkLIst partial update
    """

    class Meta:
        model = Talk
        # According to 'talk_list' field, I suppose that during updating TalkList it will be not possible to change
        # TalkList for talk
        fields = ('id', 'name', 'user')

    # To be possible to make TalkList partial update with creating new talks Talk.id field should be not read_only
    # It is read_only by default as a PK
    id = serializers.IntegerField(label='ID')
    # Show name instead of id
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')


class TalkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkList
        fields = ('id', 'name', 'talks', 'user')
        read_only_fields = ('user', )

    talks = TalkUpdateSerializer(many=True)
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')

    def create(self, validated_data):
        talks_data = validated_data.pop('talks', None)
        talk_list = TalkList.objects.create(**validated_data)
        for talk_data in talks_data:
            Talk.objects.create(talk_list=talk_list, **talk_data)
        return talk_list

    def update(self, instance, validated_data):
        if 'talks' in validated_data:
            talks_data = validated_data.pop('talks')
            if talks_data:
                talks_to_delete = instance.talks.exclude(pk__in=[item.get('id', None) for item in talks_data])

                for item in talks_data:
                    item_id = item.get('id', None)
                    if item_id:
                        talk_item = Talk.objects.get(id=item_id, talk_list=instance)
                        talk_item.name = item.get('name', talk_item.name)
                        talk_item.save()
                    else:
                        Talk.objects.create(talk_list=instance, **item)
            else:
                talks_to_delete = instance.talks.all()
            # Delete talks which are not exists in validated_data
            if talks_to_delete:
                talks_to_delete.delete()

        super(self.__class__, self).update(instance, validated_data)
        return instance
