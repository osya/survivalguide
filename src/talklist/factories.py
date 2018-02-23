#!/usr/bin/env python
# -*- coding: utf-8 -*-
import factory

from factory_user import UserFactory, random_string_generator
from talklist.models import TalkList


# pragma pylint: disable=R0903
class TalkListFactory(factory.DjangoModelFactory):
    class Meta:
        model = TalkList

    user = factory.SubFactory(UserFactory, password=random_string_generator())
    name = factory.Sequence(lambda n: 'TalkList %03d' % n)
# pragma pylint: enable=R0903
