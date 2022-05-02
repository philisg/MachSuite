#include <stdio.h>
#include <stdlib.h>


void array_gen(int len , int array[]){
    int arraysum = 0;
    for(int i = 0; i< len; i++){
        array[i] = rand() % 100;
        arraysum += array[i];   
        // printf("Array[%d] = %d, Sum is: %d\n", i,array[i], arraysum);
    }
    printf("Arraysum is: %d\n", arraysum);
}

int main () {

    asm ("nop"); //Marking start of program
    
    int ComputeLength = 100;
    int array1[] = {1,2,3,4,5,6};
    // printf("Starting program!\n");

    array_gen(ComputeLength,array1);

    int sum = 0;

    asm("nop"); //Marking start of configuration

    asm("nop"); //Marking the starting of computation
    for (int i = 0; i < ComputeLength; i++) {
        //DFGLoop: loop
        sum += array1[i];
    }

    asm("nop"); //Marking end of computation
    printf("Program Done! Sum is: %d\n", sum);
    return 0;
}