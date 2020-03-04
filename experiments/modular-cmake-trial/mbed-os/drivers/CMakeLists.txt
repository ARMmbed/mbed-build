add_library(drivers
  source/AnalogIn.cpp
  source/AnalogOut.cpp
  source/BusIn.cpp
  source/BusInOut.cpp
  source/BusOut.cpp
  source/CAN.cpp
  source/DigitalIn.cpp
  source/DigitalInOut.cpp
  source/DigitalOut.cpp
  source/Ethernet.cpp
  source/FlashIAP.cpp
  source/I2C.cpp
  source/I2CSlave.cpp
  source/InterruptIn.cpp
  source/InterruptManager.cpp
  source/MbedCRC.cpp
  source/PortIn.cpp
  source/PortInOut.cpp
  source/PortOut.cpp
  source/PwmOut.cpp
  source/QSPI.cpp
  source/RawSerial.cpp
  source/ResetReason.cpp
  source/SPI.cpp
  source/SPISlave.cpp
  source/Serial.cpp
  source/SerialBase.cpp
  source/SerialWireOutput.cpp
  source/TableCRC.cpp
  source/Ticker.cpp
  source/Timeout.cpp
  source/Timer.cpp
  source/TimerEvent.cpp
  source/UARTSerial.cpp
  source/Watchdog.cpp
  source/usb/AsyncOp.cpp
  source/usb/ByteBuffer.cpp
  source/usb/EndpointResolver.cpp
  source/usb/LinkedListBase.cpp
  source/usb/OperationListBase.cpp
  source/usb/PolledQueue.cpp
  source/usb/TaskBase.cpp
  source/usb/USBAudio.cpp
  source/usb/USBCDC.cpp
  source/usb/USBCDC_ECM.cpp
  source/usb/USBDevice.cpp
  source/usb/USBHID.cpp
  source/usb/USBKeyboard.cpp
  source/usb/USBMIDI.cpp
  source/usb/USBMSD.cpp
  source/usb/USBMouse.cpp
  source/usb/USBMouseKeyboard.cpp
  source/usb/USBSerial.cpp
)

target_link_libraries(drivers platform)
target_link_libraries(drivers events)
target_link_libraries(drivers hal)

target_include_directories (drivers
    PUBLIC 
        .
        source
        source/usb
        internal
)
