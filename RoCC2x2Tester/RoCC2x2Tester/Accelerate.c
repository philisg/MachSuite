#include <stdio.h>
#include <stdlib.h>
#include "rocc.h"

#define ConfigLength2x2 3
#define ConfigLength4x3 11
#define ConfigLength6x6 29

void send_config(int length){
    unsigned long int config1 = 0;
    unsigned long int config2 = 0;

    for(int k = 0; k < length; k=k+2){
        config1 = cgra_configuration[k];
        config2 = cgra_configuration[k+1];
        ROCC_INSTRUCTION_SS(0,config1, config2, 0);
    }
}

void Accelerate(int InputArray[], int Output, int ComputeLength, int size) {
   
    asm volatile ("fence");
    int length = 0;
    switch (size){
        case 2:
            length = ConfigLength2x2;
            break;
        case 4:
            length = ConfigLength4x3;
            break;
        case 6:
            length = ConfigLength6x6;
            break;
        
        default:
            length = 0;
            printf("Size not set, unable to send configuration to CGRA");
            break;
    } 

    send_config(length);

    //***********************************************************//
    //Declear array here to avoid page fault error in simulation.//
    //***********************************************************//

    // Send the first input and output address
    ROCC_INSTRUCTION_SS(0,&InputArray,&Output,1);
    
    // Send the array length. This will also start the calculation
    ROCC_INSTRUCTION_SS(0,ComputeLength,0,3);

    asm volatile ("fence" ::: "memory");
}