#include <stdio.h>
#include <stdlib.h>

#include "rocc.h"
#include "encoding.h"
#include "compiler.h"
#include "RoCCTester.h"


/* instruction			roccinst	src2		    src1	        dst	  custom-N
  configure			    2			-	            config	        -	  0
  one input&output	    2			src2(O)		    src1(I)	        -	  1
  input #2			    2			src1(I)		    -               -     2 (Used when we have two inputs)
  input length #1|#2	2			src2(lenI2)	    src1(lenI1)	    -     3

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
        //printf("%d: \t%lx, \t%lx\n",k,config1,config2);
        ROCC_INSTRUCTION_SS(0,config1, config2, 0);
    }
    printf("Config Sent!!\n");
}

int main () {


    printf("Starting program!\n");

    int a = 30, b = 5, sum = 2;
    printf("Adresses: a: %p, b: %p \n", &a,&b);

    asm volatile ("fence");
    
    send_config();

    ROCC_INSTRUCTION_SS(0,&a,&b,0);
    ROCC_INSTRUCTION_SS(0,&a,&b,1);
    ROCC_INSTRUCTION_S(0,&sum,2);
    ROCC_INSTRUCTION_SS(0,45,55,3);

    // ROCC_INSTRUCTION_DSS(0,sum,c,b,0);
    // printf("Second instruction sent to accelerator\n");

    asm volatile ("fence" ::: "memory");

    printf("Program Done!\n");

    return 0;
}