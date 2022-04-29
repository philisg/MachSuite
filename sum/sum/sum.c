#include <stdio.h>
#include <stdlib.h>


void array_gen(int len , int array[]){
    int arraysum = 0;
    for(int i = 0; i < len; i++){
        array[i] = rand() % 100;
        arraysum += array[i];   
        printf("Array[%d] = %d, Sum is: %d\n", i,array[i], arraysum);
    }
}
// Simple accumulation
int main() {
    asm("nop"); //Marking start of program
    asm("nop"); //Marking start of configuration
    
    int a[]= {1,2};
    int sum = 0;

    array_gen(100,a);
    // int i;
    asm("nop"); //Marking start of Computation
    for (int i = 0; i < 100; i++) {
        //DFGLoop: loop
        sum += a[i];
    }
    // printf("sum = %d\n", sum);

    asm("nop"); //Marking end of computation
    return sum;
}

