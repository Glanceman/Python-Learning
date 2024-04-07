#include <stdio.h>
#include <openssl/bn.h>
#include <openssl/aes.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#define KEYSIZE 16

void print_hex(unsigned char *array, int length) {
    int i;
    printf(" ");
    for (i = 0; i < length; i++) {
        printf("%02x ", array[i]);
    }
    printf(" ");
}

int main()
{
    size_t blocksize = 16;
    // range

    for (long second = 1524013729 ; second <= 1524020929; second++)
    {
        unsigned char iv[] = {0x09,0x08,0x07,0x06,0x05,0x04,0x03,0x02,0x01,0x00,0xA2,0xB2,0xC2,0xD2,0xE2,0xF2};
        unsigned char plaintext[] = {0x25,0x50,0x44,0x46,0x2D,0x31,0x2E,0x35,0x0A,0x25,0xD0,0xD4,0xC5,0xD8,0x0A,0x34};
        unsigned char ciphertext[] = {0xD0,0x6B,0xF9,0xD0,0xDA,0xB8,0xE8,0xEF,0x88,0x06,0x60,0xD2,0xAF,0x65,0xAA,0x82};
        srand(second);
        unsigned char key[KEYSIZE];
        printf("key= ");
        for (int j = 0; j < KEYSIZE; j++)
        {
            key[j] = rand() % 256;
            printf("%.2x", (unsigned char)key[j]);
        }
        printf(" ");

        AES_KEY enc_key;
        AES_set_encrypt_key(key, sizeof(key)*8, &enc_key);
        //size_t length = (sizeof(plaintext)+ blocksize)/blocksize * blocksize;
        unsigned char aes_out[sizeof(plaintext)];
        
        AES_cbc_encrypt(plaintext,aes_out,sizeof(ciphertext),&enc_key,iv,AES_ENCRYPT);
        print_hex(plaintext,sizeof(plaintext));
        print_hex(aes_out,sizeof(aes_out));

        if(strncmp(aes_out,ciphertext,sizeof(plaintext))==0){
            printf("Found: ");
            print_hex(aes_out,sizeof(plaintext));
            printf("\n");
            return 0;
        }
        printf("\n");
    }

    printf("fail \n");
    return 0;
}