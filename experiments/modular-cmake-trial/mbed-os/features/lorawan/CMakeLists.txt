add_library(lorawan
  LoRaWANInterface.cpp
  LoRaWANStack.cpp
  lorastack/mac/LoRaMac.cpp
  lorastack/mac/LoRaMacChannelPlan.cpp
  lorastack/mac/LoRaMacCommand.cpp
  lorastack/mac/LoRaMacCrypto.cpp
  lorastack/phy/LoRaPHY.cpp
  lorastack/phy/LoRaPHYAS923.cpp
  lorastack/phy/LoRaPHYAU915.cpp
  lorastack/phy/LoRaPHYCN470.cpp
  lorastack/phy/LoRaPHYCN779.cpp
  lorastack/phy/LoRaPHYEU433.cpp
  lorastack/phy/LoRaPHYEU868.cpp
  lorastack/phy/LoRaPHYIN865.cpp
  lorastack/phy/LoRaPHYKR920.cpp
  lorastack/phy/LoRaPHYUS915.cpp
  system/LoRaWANTimer.cpp
)

target_link_libraries(lorawan rtos)

target_include_directories(lorawan
    PUBLIC
        .
        system
        lorastack/phy
        lorastack/mac
        lorastack
)
