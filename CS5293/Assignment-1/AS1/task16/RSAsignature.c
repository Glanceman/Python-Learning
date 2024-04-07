#include <stdio.h>
#include <openssl/bn.h>
#include<stdbool.h> 
#include<string.h>
#define NBITS 256
void printBN(char *msg, BIGNUM *a)
{
    /* Use BN_bn2hex(a) for hex string
     * Use BN_bn2dec(a) for decimal string */
    char *number_str = BN_bn2hex(a);
    printf("%s %s\n", msg, number_str);
    OPENSSL_free(number_str);
}

bool Verify(BIGNUM* e, BIGNUM* M,BIGNUM* sign,BIGNUM* n, BN_CTX *ctx){
    BIGNUM *res = BN_new();
    BN_mod_exp(res,sign,e,n,ctx);
    printBN("Message from orignal  : ",M);
    printBN("Message from Signature : ",res);
    char *res_str = BN_bn2hex(res);
    char *m_str = BN_bn2hex(M);
    if(memcmp(res_str,m_str,sizeof(res_str))==0){
        return true;
    }
    return false;
}

BIGNUM* Sign(BIGNUM* d, BIGNUM* M,BIGNUM* n, BN_CTX *ctx){
    BIGNUM *sign = BN_new();
    BN_mod_exp(sign,M,d,n,ctx);
    return sign;
}

int main()
{
    BN_CTX *ctx = BN_CTX_new();
    BIGNUM *e = BN_new();
    BIGNUM *n = BN_new();
    BIGNUM *d = BN_new();
    
    BN_hex2bn(&n, "AE1CD4DC432798D933779FBD46C6E1247F0CF1233595113AA51B450F18116115");
    BN_hex2bn(&d, "74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D");
    BN_hex2bn(&e, "010001");
    BIGNUM *M = BN_new();
    BN_hex2bn(&M, "4C61756E63682061206D6973736C652E"); // hex : Launch a missile.
    BIGNUM* sign = BN_new();
    BN_hex2bn(&sign, "643D6F34902D9C7EC90CB0B2BCA36C47FA37165C0005CAB026C0542CBDB6802F");
    bool result = Verify(e,M,sign,n,ctx);
    if(result==true){
        printf("Verify successful\n");
    }else{
        printf("Verify failure\n");
    }

    printf("Corrupted\n");
    BIGNUM* sign2 = BN_new();
    BN_hex2bn(&sign2, "643D6F34902D9C7EC90CB0B2BCA36C47FA37165C0005CAB026C0542CBDB6803F");
    result = Verify(e,M,sign2,n,ctx);
    if(result==true){
        printf("Verify successful\n");
    }else{
        printf("Verify failure\n");
    }
    return 0;
}