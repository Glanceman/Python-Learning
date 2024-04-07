#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>

#define LEN 32 // 128 bits

void print_hex(unsigned char *array, int length) {
    int i;
    printf(" ");
    for (i = 0; i < length; i++) {
        printf("%02x ", array[i]);
    }
    printf("\n");
}

int main()
{
    unsigned char *key = (unsigned char *)malloc(sizeof(unsigned char) * LEN);
    FILE *random = fopen("/dev/urandom", "r");
    fread(key, sizeof(unsigned char) * LEN, 1, random);
    fclose(random);
    print_hex(key,LEN);
    return 0;
}