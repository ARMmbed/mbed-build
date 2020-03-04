#include <stdio.h>

#include "alib.h"
#include "blib.h"

#include "clib.h"

int main(void) {
    print_from_alib();
    print_from_blib();

#if !defined(CONFIG_PARAM_1)
    #error CONFIG_PARAM_1 is not defined
#endif

    printf("CONFIG_PARAM_1 is '%s'\n", CONFIG_PARAM_1);

    clib_hello();

    return 0;
}
