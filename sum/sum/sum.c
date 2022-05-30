#include <stdio.h>
#include <stdlib.h>

#define ComputeLength 1002


void array_gen(int array[]){
    int arraysum = 0;
    for(int i = 0; i< ComputeLength; i++){
        array[i] = rand() % 65535;
        arraysum += array[i];   
        // printf("Array[%d] = %d, Sum is: %d\n", i,array[i], arraysum);
    }
    printf("Arraysum is: %d\n", arraysum);
}

int main () {

    asm ("nop"); //Marking start of program
    
    int array1[ComputeLength];
    // printf("Starting program!\n");

    array_gen(array1);

    int sum = 0;

    asm("nop"); //Marking start of configuration

    asm("nop"); //Marking the starting of computation
    for (int i = 0; i < ComputeLength; i++) {
        //DFGLoop: loop
        sum += array1[i];
        // sum += array1[i] + array1[i+1] + array1[i+2];
    }

    asm("nop"); //Marking end of computation
    printf("Program Done! Sum is: %d\n", sum);
    return 0;
}