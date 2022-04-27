#include <stdio.h>
#include <stdlib.h>

#include "rocc.h"
#include "encoding.h"
#include "compiler.h"
#include "RoCCTester.h"


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

    for(int k = 0; k < 14; k=k+2){
        for(int i = 0; i < 8; i ++){
            config1 = config1 << 8;
            config1 = config1 | cgra_configuration[i+(8*k)];
            config2 = config2 << 8;
            config2 = config2 | cgra_configuration[i+(8*k)+8];
        }
        ROCC_INSTRUCTION_SS(0,config1, config2, 0);
    }
    printf("Config Sent!!\n");
}

int main () {


    printf("Starting program!\n");

    int sum = 2;
    int array1[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
    int array2[] = {5,6,7,8,7,10,11,11,11,11,11,12,13,14,15,16,17,18,19,20};

    printf("Adresses: array1: %p, array2: %p, sum has value: %d with adress: %p \n", &array1,&array2, sum, &sum);


    asm volatile ("fence");
    // Send the config first
    send_config();

    // Send the first input and output address
    ROCC_INSTRUCTION_SS(0,&array1, &sum,1);

    // Send the #2 input address
    // ROCC_INSTRUCTION_S(0,&array2,2);

    // Send the array length. This need to be the same for array1 and array2 in this configuration
    // This will also start the calculation
    ROCC_INSTRUCTION_SS(0,19,19,3);


    asm volatile ("fence" ::: "memory");

    for(int i = 0; i < 1000; i++){}

    printf("Program Done! sum is: %d\n", sum);

    return 0;
}