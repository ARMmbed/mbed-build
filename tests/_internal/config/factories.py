#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import factory

from mbed_build._internal.config.assemble_build_config import BuildConfig
from mbed_build._internal.config.config import Config, Option
from mbed_build._internal.config.source import Source


class SourceFactory(factory.Factory):
    class Meta:
        model = Source

    human_name = factory.Faker("name")
    config = factory.Dict({})
    config_overrides = factory.Dict({})
    cumulative_overrides = factory.Dict({})
    macros = factory.List([])


class OptionFactory(factory.Factory):
    class Meta:
        model = Option

    value = "0"
    macro_name = "MACRO_NAME"
    help_text = factory.Faker("text")
    set_by = "libname"
    key = "key"


class ConfigFactory(factory.Factory):
    class Meta:
        model = Config

    options = factory.Dict({})


class BuildConfigFactory(factory.Factory):
    class Meta:
        model = BuildConfig

    config = factory.SubFactory(ConfigFactory)
    macros = set()
