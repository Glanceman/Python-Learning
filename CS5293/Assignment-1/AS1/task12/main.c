
#include <stdio.h>
#include <openssl/bn.h>
#define NBITS 256
void printBN(char *msg, BIGNUM *a)
{
    /* Use BN_bn2hex(a) for hex string
     * Use BN_bn2dec(a) for decimal string */
    char *number_str = BN_bn2hex(a);
    printf("%s %s\n", msg, number_str);
    OPENSSL_free(number_str);
}
int main()
{
    BN_CTX *ctx = BN_CTX_new();
    BIGNUM *p = BN_new();
    BIGNUM *q = BN_new();
    BIGNUM *e = BN_new();
    BIGNUM *n = BN_new();
    BIGNUM *one = BN_new();
    BN_hex2bn(&one, "1");
    // assign  p q e
    BN_hex2bn(&p, "F7E75FDC469067FFDC4E847C51F452DF");
    BN_hex2bn(&q, "E85CED54AF57E53E092113E62F436F4F");
    BN_hex2bn(&e, "0D88C3");
    //compute n
    BN_mul(n, p, q, ctx);
    //compute phi(m)
    BIGNUM *phi = BN_new();
    BIGNUM *pMinusOne = BN_new();
    BIGNUM *qMinusOne = BN_new();
    BN_sub(pMinusOne, p, one);
    BN_sub(qMinusOne, q, one);
    BN_mul(phi, pMinusOne, qMinusOne, ctx);
    // find d
    BIGNUM *d = BN_new();
    BN_mod_inverse(d, e, phi, ctx);
    printBN("SK= ",d);
    return 0;
}