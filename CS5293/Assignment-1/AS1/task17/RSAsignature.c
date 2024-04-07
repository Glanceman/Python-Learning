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
    //BIGNUM *d = BN_new();
    
    BN_hex2bn(&n, "d081c13923c2b1d1ecf757dd55243691202248f7fcca520ab0ab3f33b5b08407f6df4e7ab0fb98223d01ac56fb716db2eeb9a00f5277ab9893be338aeb875ec7aab0ca698f43086a3f22bf333946d594f2e24c0522d9678091f1044a0e9b7ca2c9d26cfd3c0984bdfd6b149a811de78a83ef6116754798133b0d901698bf8ae22732539999c3fb961c35f762ed8cbd4971d24343a1a1e3212a2370a8753db26c4606616f1867e4297eb23cc1c55f091e6e444eec2199581548f455482ab734b405e37c498c0058de3a96cc39dc613355ce2a2e3fd19962e8aae6347631aaaf79299678cb8114af69dafb04b9598344aa094fb4d42c019d9b94316b2da1cfc1e5");
    //BN_hex2bn(&d, "74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D");
    BN_hex2bn(&e, "10001");
    BIGNUM *M = BN_new();
    BN_hex2bn(&M, "7b1ec178808eab709eaf188128ba253a4abbfdcbdc62a62c85ebcc64bfa53f37"); // hex : Launch a missile.
    BIGNUM* sign = BN_new();
    BN_hex2bn(&sign, "5133b9b9335c850ef78a48d23832480c2756475b0d3b1ae3eaac52890ce1c4ad6a9d18ba7901a7564fb0d6f16ed0a22c7326602554bc15bfccd4df9fc0d72f340c24fe86aeaa0fb9aee6096ea3fd321e79ee47b0957be587c0421011dd87e07f20a7743056f179af99c5bde7f12aa16e898af1c71ca0cf2ca0e316b9815d4b5e333eec15a896c5bc0b579af19ed884bdaa021cd1af3840ce857b87632d82206c396b57e6c6b8ca31880ad9036fd83556e4d369e4ff2f13c942fec1ffc3fdfaa00df13e716acf62ccfb20aeb6b3088da440edd580a990e1a76ecbc92b4706c5c1bd1b722cc807f4c93036cb70635b89d69112ff4e5d1974468f92e3e35651aec0");
    
    bool result = Verify(e,M,sign,n,ctx);
    if(result==true){
        printf("Verify successful\n");
    }else{
        printf("Verify failure\n");
    }

    return 0;
}