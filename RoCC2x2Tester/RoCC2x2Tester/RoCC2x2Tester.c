#include <stdio.h>
#include <stdlib.h>

#include "rocc.h"
#include "encoding.h"
#include "compiler.h"
#include "RoCC2x2Tester.h"


/* instruction		    roccinst	src2		    src1	        dst	  custom-N
  configure			    0			-	            config	        -	  0
  one input&output	    0			src2(O)		    src1(I)	        -	  1 output = src2, input = src1
  input #2			    0			src1(I)		    -               -     2 (Used when we have two inputs)
  input length #2|#1	0			src2(lenI2)	    src1(lenI1)	    -     3


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

    for(int k = 0; k < 3; k=k+2){
        for(int i = 0; i < 8; i ++){
            config1 = config1 << 8;
            config1 = config1 | cgra_configuration[i+(8*k)];
            config2 = config2 << 8;
            config2 = config2 | cgra_configuration[i+(8*k)+8];
        }
        //printf("%d: \t%lx, \t%lx\n",k,config1,config2);
        ROCC_INSTRUCTION_SS(0,config1, config2, 0);
    }
    printf("Config Sent!!\n");
}

volatile int * a;//[N] = {1,2,3,4,5,6,7,8,9,10};

volatile int * n;

int main () {

    int array1[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
    printf("Starting program!\n");
    
    int tester = 45;
    // int N = *n;
    int sum = 0;
    // int i;

    for(int i = 0; i < 15; i++){
        printf("adress of array1[%d] = %p , Tester is: %d at adress: %p\n", i, &array1[i], tester, &tester);
    }

    int b = 5;
    printf("Adresses: array1: %p, b: %p, Volatile int a: %p, sum has the value: %d with address: %p \n", &array1,&b,&a,sum,&sum);
    // printf("Adresses: N: %p, sum: %p, a: %p \n",&N, &sum, &a);

    asm volatile ("fence");

    ROCC_INSTRUCTION_SS(0,&array1,&sum,1); 
    
    send_config();
    
    ROCC_INSTRUCTION_SS(0,15,15,3);

    ROCC_INSTRUCTION_S(0,&tester,4);

    asm volatile ("fence" ::: "memory");

    printf("Program Done! Sum is: %d, array1{0] is: %d, tester is: %d\n", sum, array1[0],tester);
    return 0;
}