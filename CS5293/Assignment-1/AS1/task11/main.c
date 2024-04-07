#include <stdio.h>
#include <string.h>
unsigned char x[200] = {
    "ContentP"
};

unsigned char y[200] = {
    "ContentP"
};
int main()
{
    if(memcmp(x, y, sizeof(x))==0){
        printf("Normal\n");
    }else{
        printf("Malicious\n");
    } 
    return 0;
}