add_library (rtos
  source/ConditionVariable.cpp
  source/EventFlags.cpp
  source/Kernel.cpp
  source/Mutex.cpp
  source/RtosTimer.cpp
  source/Semaphore.cpp
  source/TARGET_CORTEX/TOOLCHAIN_GCC_ARM/mbed_boot_gcc_arm.c
  source/TARGET_CORTEX/mbed_boot.c
  source/TARGET_CORTEX/mbed_rtos_rtx.c
  source/TARGET_CORTEX/mbed_rtx_handlers.c
  source/TARGET_CORTEX/mbed_rtx_idle.cpp
  source/TARGET_CORTEX/rtx4/cmsis_os1.c
  source/TARGET_CORTEX/rtx5/RTX/Config/RTX_Config.c
  source/TARGET_CORTEX/rtx5/RTX/Source/TOOLCHAIN_GCC/TARGET_RTOS_M4_M7/irq_cm4f.S
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_delay.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_evflags.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_evr.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_kernel.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_lib.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_memory.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_mempool.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_msgqueue.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_mutex.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_semaphore.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_system.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_thread.c
  source/TARGET_CORTEX/rtx5/RTX/Source/rtx_timer.c
  source/TARGET_CORTEX/rtx5/Source/os_systick.c
  source/TARGET_CORTEX/rtx5/Source/os_tick_ptim.c
  source/ThisThread.cpp
  source/Thread.cpp
)

target_link_libraries(rtos platform)
target_link_libraries(rtos drivers)

target_include_directories (rtos
    PUBLIC
  source/TARGET_CORTEX/rtx5/RTX/Source
  source/TARGET_CORTEX/rtx5/RTX/Include
  source/TARGET_CORTEX/rtx5/RTX/Config
  source/TARGET_CORTEX/rtx5/RTX
  source/TARGET_CORTEX/rtx5/Include
  source/TARGET_CORTEX/rtx5
  source/TARGET_CORTEX/rtx4
  source/TARGET_CORTEX
  source
  .
)
