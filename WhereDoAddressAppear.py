#!/usr/bin/python

import sys

Benchmark = sys.argv[1]+"_"+sys.argv[2]

# Benchmark = raw_input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark = input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark = "aes_aes"

WantedAddress = sys.argv[3]
# WantedAddress = raw_input("xxxxxxxxxxxxxxxx: Which address are we searching for?\n")
# WantedAddress = "ffffffc000003710"
SearchLine = "pc=["+WantedAddress+"]"
LastCycle = 0
SearchList = []

with open(Benchmark+"_outputlog.txt", 'r') as f:
    for line in f:
        if type(line) is str:
            ActualCycles = 0
            CycleString = line.strip("C0: [")
            CycleString = CycleString.split(" ")
            try:
                Cycle = int(CycleString[0])
            except:
                continue
            
            LastCycle = Cycle

            DevidedLine = line.split(" ")
            for i in DevidedLine:
                if SearchLine in i:
                    SearchList.append(Cycle)
                    break
            
# Create a file
file = open(Benchmark+'_search_for_address.txt','w')
k = WantedAddress + "\n"
file.writelines(k)

k = "Number of simulated cycles: " +  str(LastCycle) + " \n" 
file.writelines(k)

for ele in SearchList:
    l = "{}\n".format(ele)
    file.writelines(l)

f.close()

