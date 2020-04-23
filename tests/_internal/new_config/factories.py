#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import factory

from mbed_build._internal.new_config.source import Source


class SourceFactory(factory.Factory):
    class Meta:
        model = Source

    name = factory.Faker("slug")
    config = factory.Dict({})
    target_overrides = factory.Dict({})
