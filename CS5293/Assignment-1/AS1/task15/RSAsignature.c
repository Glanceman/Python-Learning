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
    char *res_str = BN_bn2hex(res);
    char *m_str = BN_bn2hex(M);
    if(strcmp(res_str,m_str)==0){
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
    
    BN_hex2bn(&n, "DCBFFE3E51F62E09CE7032E2677A78946A849DC4CDDE3A4D0CB81629242FB1A5");
    BN_hex2bn(&d, "74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D");
    BN_hex2bn(&e, "010001");
    BIGNUM *M1 = BN_new();
    BN_hex2bn(&M1, "2049206F776520796F752024323030302E"); // hex : I owe you $2000.
    BIGNUM* sign1 = Sign(d,M1,n,ctx);
    printBN(" I owe you $2000 ", sign1);

    BIGNUM *M2 = BN_new();
    BN_hex2bn(&M2, "2049206F776520796F752024333030302E"); // hex : I owe you $3000.
    BIGNUM* sign2= Sign(d,M2,n,ctx);
    printBN(" I owe you $3000 ", sign2);

    return 0;
}