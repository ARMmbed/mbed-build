add_library(events
  source/EventQueue.cpp
  source/equeue.c
  source/equeue_mbed.cpp
  source/equeue_posix.c
  source/mbed_shared_queues.cpp
)

target_link_libraries(events rtos)
target_include_directories (events
    PUBLIC
        source
        internal
        .
)
