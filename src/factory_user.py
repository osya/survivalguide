#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string

import factory
from django.contrib.auth import get_user_model


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# pragma pylint: disable=R0903
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'Agent %03d' % n)
    email = factory.LazyAttributeSequence(lambda o, n: f'{o.username}{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password')


# pragma pylint: enable=R0903
