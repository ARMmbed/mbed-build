#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import factory

from mbed_build._internal.config.source import Source


class SourceFactory(factory.Factory):
    class Meta:
        model = Source

    human_name = factory.Faker("name")
    namespace = factory.Faker("slug")
    config = factory.Dict({})
    config_overrides = factory.Dict({})
    cumulative_overrides = factory.Dict({})
