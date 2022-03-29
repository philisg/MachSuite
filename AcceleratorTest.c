#include <stdlib.h>
#include <stdio.h>

int main(void){

    int A = 0;
    int B = 5;
    int sum = 0;
    int result = 0;
    int k = 0;

    printf("Starting!");

    loop1: for(int i = 0; i < 1000; i++){
        //DFGLoop: loop
        A += B;
        B = B/2;
        sum = A + B;
        result = sum;    
    }

    loop2: for(int i = 0; i < 100; i++){
        for(k = 0; k < 50; k++)
            result = sum/B;
            sum += k;
    }

    printf("Finished");
    return 0;
}