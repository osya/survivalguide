#!/usr/bin/env python
# -*- coding: utf-8 -*-
import factory

from factory_user import UserFactory, random_string_generator
from talk.models import Talk
from talklist.factories import TalkListFactory


# pragma pylint: disable=R0903
class TalkFactory(factory.DjangoModelFactory):
    class Meta:
        model = Talk

    user = factory.SubFactory(UserFactory, password=random_string_generator())
    talklist = factory.SubFactory(TalkListFactory)
    name = factory.Sequence(lambda n: 'Talk %03d' % n)
# pragma pylint:enable=R0903
