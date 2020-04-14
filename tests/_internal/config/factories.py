#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from factory import Factory, Faker

from mbed_build._internal.config.config_source import ConfigSource


class ConfigSourceFactory(Factory):
    class Meta:
        model = ConfigSource

    name = Faker("name")
    file = Faker("file_path", extension="json")
    config = {
        "event-loop-size": 1024,
        "event_loop_thread_stack_size": {"help": "Define event-loop thread stack size.", "value": 6144},
        "http-resume-maximum-download-time-secs": {
            "help": "Period for HTTP-resume actions after which resume gives up and terminates.",
            "macro_name": "ARM_UC_HTTP_RESUME_MAXIMUM_DOWNLOAD_TIME_SECS",
            "value": "(7*24*60*60)",
        },
    }
    target_overrides = {
        "*": {"target.boot-stack-size": "0x400"},
        "STM": {"idle-thread-stack-size-debug-extra": 128},
    }
