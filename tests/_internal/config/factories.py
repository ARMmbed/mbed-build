#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import factory

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_source import ConfigSource


class ConfigSourceFactory(factory.Factory):
    class Meta:
        model = ConfigSource

    namespace = factory.Faker("slug")
    file = factory.Faker("file_path", extension="json")
    config = factory.Dict({})
    target_overrides = factory.Dict({})


class ConfigFactory(factory.Factory):
    class Meta:
        model = Config

    settings = factory.Dict({})
    target = factory.Dict(
        {"components": set(), "device_has": set(), "extra_labels": set(), "features": set(), "macros": set()}
    )
