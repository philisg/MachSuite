#!/usr/bin/python

ThisInstDict = {}
ThisPCDict = {}
# Number of lines read from simulated benchmark
NumberOfLines = 0
LastCycleCount = 0
NumberOfCycles = 0
# Name of benchmark to profile
Benchmark = raw_input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark = input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark = "aes_aes"
skip = 3
ReadingLineNumber = 0
with open(Benchmark+"_outputlog.txt", 'r') as f:
    for line in f:
        if type(line) is str:
            
            ActualCycles = 0
            CycleString = line.strip("C0: [")
            CycleString = CycleString.split(" ")
            try:
                CurrentCycle = int(CycleString[0])
            except:
                continue
            
            ActualCycles = CurrentCycle - LastCycleCount
            NumberOfCycles += ActualCycles
            LastCycleCount = CurrentCycle

            NumberOfLines += 1
            x = line.split("] ")
            for i in x:                
                if "pc=[" in i:
                    value = i.split("[")
                    i = value[1]
                    if i in ThisPCDict:
                        # update +1
                        count = ThisPCDict.get(i)
                        ThisPCDict[i] = [count[0] + 1,count[1] + ActualCycles]
                    else:
                        # add to dict
                        ThisPCDict[i] = [1, ActualCycles]
                if "inst=[" in i:
                    value = i.split("[")
                    i = value[1]
                    if i in ThisInstDict:
                        # update +1
                        count = ThisInstDict.get(i)
                        ThisInstDict[i] = [count[0] + 1, count[1]+ActualCycles]
                    else:
                        # add to dict
                        ThisInstDict[i] = [1, ActualCycles]

            
            
            



# Make sure the dicts are equal length
dif = len(ThisInstDict) - len(ThisPCDict)
k = "NA"
if dif < 0:
    dif = -dif
    for i in range(dif):
        ThisInstDict[i]= [k,k]
elif dif > 0:
    for i in range(dif):
        ThisPCDict[i]= [k,k]

# Create file to put text in
file = open(Benchmark+'_plain_histogram_output.txt','w')
# Number of lines read from benchmark file
k = "Number of simulated lines: " +  str(NumberOfLines) + " \n" 
file.writelines(k)
# Number of cycles read from benchmark file
k = "Number of simulated cycles: " +  str(NumberOfCycles) + " \n" 
file.writelines(k)
# Make header
k = "{:1};{:1};{:1};{:1};{:1};{:1}\n".format('PC','PCcount','PCcycles','inst','instcount','instcycles')
file.writelines(k)
for c1, c2 in zip(ThisPCDict, ThisInstDict):
        ValuesPC = ThisPCDict.get(c1)
        ValuesInst = ThisInstDict.get(c2)
        l ="{:1};{:1};{:1};{:1};{:1};{:1}\n".format(c1,ValuesPC[0],ValuesPC[1],c2,ValuesInst[0],ValuesInst[1])
        file.writelines(l)

# Close file
f.close()
