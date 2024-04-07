/* stack.c */
/* This program has a buffer overflow vulnerability. */
/* Our task is to exploit this vulnerability */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* Changing this size will change the layout of the stack. */
#ifndef BUFSIZE
#define BUFSIZE 33
#endif
int bof(char *str)
{
    char buffer[BUFSIZE];
    /* The following statement has a buffer overflow problem */
    strcpy(buffer, str);

    register char *ebp asm("ebp");
    printf("address of buffer is %p\n", &buffer); // %p means hex
    printf("address of ebp is %p\n", ebp);
    return 1;
}

int main(int argc, char **argv)
{
    char str[517];
    FILE *badfile;
    /* Change the size of the dummy array to randomize the parameters */
    char dummy[BUFSIZE];
    memset(dummy, 0, BUFSIZE);
    badfile = fopen("badfile", "r");
    fread(str, sizeof(char), 517, badfile);
    bof(str);
    printf("Returned Properly\n");
    return 1;
}