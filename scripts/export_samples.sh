

TARGETS="NUCLEO_F413ZH DISCO_H747I CY8CKIT_062_BLE K64F"

if [ ! -e 'mbed-os' ] ; then
  echo "ERROR: This script must be run in a directory containing an mbed-os"
  exit 1
fi

for t in $TARGETS
do
  echo "Exporting for target $t..."
  mbed export -m $t -i cmake_gcc_arm
  mv CMakeLists.txt example_cmakelists/CMakeLists.txt.$t
done

echo "All done"

#mbed export -m NUCLEO_F413ZH -i cmake_gcc_arm
#mv CMakeLists.txt CMakeLists.txt.NUCLEO_F413ZH
#mbed export -m DISCO_H747I -i cmake_gcc_arm
#mv CMakeLists.txt CMakeLists.txt.DISCO_H747I
#mbed export -m CY8CKIT_062_BLE -i cmake_gcc_arm
#mv CMakeLists.txt CMakeLists.txt.CY8CKIT_062_BLE
#mbed export -m K64F -i cmake_gcc_arm
#mv CMakeLists.txt CMakeLists.txt.K64F
