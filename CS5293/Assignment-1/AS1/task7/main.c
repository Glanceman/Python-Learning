#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>


void print_hex(unsigned char *array, int length) {
    int i;
    for (i = 0; i < length; i++) {
        printf("%02x ", array[i]);
    }
}


int main() {
    FILE *fp;
    char line[16];
    size_t blocksize = 16;

    unsigned char plaintext[] = "This is a top secret";

    unsigned char cyhertext[] = {0x76,0x4a,0xa2,0x6b,0x55,0xa4,0xda,0x65,0x4d,0xf6,0xb1,0x9e,0x4b,0xce,0x00,0xf4,0xed,0x05,0xe0,0x93,0x46,0xfb,0x0e,0x76,0x25,0x83,0xcb,0x7d,0xa2,0xac,0x93,0xa2};

    fp = fopen("words.txt", "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    int i=0;
    while (fgets(line, sizeof(line), fp)) {
        char padKey[16];
        memset(padKey, 0x23, sizeof(padKey));
        //copy the to padword
        for (int i =0; i< 16; i++){
            if(line[i]=='\n'){
                break;
            }
            padKey[i]=line[i];
        }
        //char padKey[16]="immoral#########";
        AES_KEY enc_key;
        AES_set_encrypt_key(padKey, sizeof(padKey)*8, &enc_key);
        size_t length = (sizeof(plaintext)+ blocksize)/blocksize * blocksize;
        unsigned char aes_out[length];
        unsigned char iv[] = {0xaa,0xbb,0xcc,0xdd,0xee,0xff,0x00,0x99,0x88,0x77,0x66,0x55,0x44,0x33,0x22,0x11};
        AES_cbc_encrypt(plaintext,aes_out,sizeof(plaintext),&enc_key,iv,AES_ENCRYPT);

        if(strncmp(aes_out,cyhertext,32)==0){
            printf("Found: ");
            printf("key = %.16s ", padKey);
            print_hex(aes_out,length);
            printf("\n");
        }

        // if(i<3){
        //     print_hex(iv,16);
        //     printf("key = %.16s ", padKey);
        //     printf("length = %li |" ,length);
        //     //printf("cypher = %.21s ", aes_out);
        //     print_hex(aes_out,length);
        //     printf("\n");
        // }
        i++;
        //break;
    }

    fclose(fp);
    return 0;
}