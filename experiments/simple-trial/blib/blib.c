#include <stdio.h>

#include "blib.h"
#include "private_blib.h"

void print_from_blib()
{
    printf("Hello from library B %d\n", B_VAR);
}
