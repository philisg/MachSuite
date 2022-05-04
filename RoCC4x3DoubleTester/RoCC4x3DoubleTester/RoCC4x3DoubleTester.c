#include <stdio.h>
#include <stdlib.h>

#include "rocc.h"
#include "encoding.h"
#include "compiler.h"
#include "RoCC4x3Tester.h"

#define ComputeLength 102


/* instruction		    roccinst	src1		    src2	        dst	  custom-N
  configure			    0			config          config	        -	  0
  one input&output	    0			src1(O)		    src2(O)	        -	  1 output = src2, input = src1
  input #2			    0			src2(I)		    -               -     2 (Used when we have two inputs)
  input length #1	    0			src1(lenI1)	    0         	    -     3

  * ROCC_INSTRUCTION_SS(0,src1,src2, instruction)
  * configure: configure the CGRA with a mapping (`busy` while configuring)
  * one input: when the configuration demands a single input (pointer)
  * two inputs: setup two inputs for the configuration
  * input length: we tell the CGRA how long the input is, so that it knows
                  when it's done.
          (`busy` and starts the computation, `!busy` when completed)
  It's based on the following roccinst+opcode->RISC-V mapping:
  funct7		rs2		rs1		xd	xs1	xs2	rd	opcode
  roccinst	src2	src1				dst	custom-0/1/2/3 */

void send_config(){
    unsigned long int config1 = 0;
    unsigned long int config2 = 0;

    for(int k = 0; k < 11; k=k+2){
        for(int i = 0; i < 8; i ++){
            config1 = config1 << 8;
            config1 = config1 | cgra_configuration[i+(8*k)];
            config2 = config2 << 8;
            config2 = config2 | cgra_configuration[i+(8*k)+8];
        }
        ROCC_INSTRUCTION_SS(0,config1, config2, 0);
    }
    // printf("Config Sent!!\n");
}

void array_gen(int array[]){
    int arraysum = 0;
    int a, b;
    for(int i = 0; i< ComputeLength/2; i++){
        a = rand() % 100;
        b = rand() % 100;
        // c = rand() % 100;
        array[i] = a | (b << 16);
        // array[i+1] = c;
        arraysum += a + b;     
        printf("Array[%d] = %d with address 1: %p, 2:%p , Sum is: %d, a:  %d, b: %d\n", i,array[i], &array[i], &array[i+1], arraysum, a,b);
    }
    printf("Arraysum is: %d\n", arraysum);

}

int main () {

    asm ("nop"); //Marking start of program

    int array1[ComputeLength];
    // printf("Starting program!\n");
    
    array_gen(array1);

    int sum = 0;

    // printf("Addresses: array1: %p, sum has the value: %d with address: %p \n", &array1,sum,&sum);

    asm volatile ("fence");

    asm("nop"); //Marking start of configuration

    // Send the config first
    send_config();

    // Send the first input and output address
    ROCC_INSTRUCTION_SS(0,&array1,&sum,1); 

    asm("nop"); //Marking the starting of computation
    
    // Send the array length. This need to be the same for array1 and array2 in this configuration
    // This will also start the calculation
    ROCC_INSTRUCTION_SS(0,ComputeLength,0,3);

    asm("nop"); //Marking end of computation

    // if not here, the Sum will not be available to CPU (Datarace)
    ROCC_INSTRUCTION_SS(0,&array1, &sum,1);

    asm volatile ("fence" ::: "memory");

    printf("Program Done! Sum is: %d\n", sum);
    return 0;
}