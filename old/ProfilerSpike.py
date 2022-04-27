#!/usr/bin/python

ThisPCDict = {}
# Number of lines read from simulated benchmark
NumberOfLines = 0
NumberOfCycles = 0
# Name of benchmark to profile
# Benchmark = raw_input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark = input("which Benchmark? (format: \"benchmark_benchmark\") ")
Benchmark = "aes_aes"
skip = 0
with open(Benchmark+"_spike_output.txt", 'r') as f:
    for line in f:
        if type(line) is str:
            NumberOfLines += 1
            line = line.strip("core 0: ")
            try:
                x = line.split(" ")                
                tx = x[0]
                x = tx.split("x")
                PC = x[1]
                if PC in ThisPCDict:
                    # update +1
                    count = ThisPCDict.get(PC)
                    ThisPCDict[PC] = [count[0] + 1,count[1] + 1]
                else:
                    # add to dict
                    ThisPCDict[PC] = [1, 1]
            except:
                continue
# Create file to put text in
file = open(Benchmark+'_plain_histogram_output.txt','w')
# Number of lines read from benchmark file
k = "Number of simulated lines: " +  str(NumberOfLines) + " \n" 
file.writelines(k)
# Number of cycles read from benchmark file
k = "Number of simulated cycles: " +  str(NumberOfLines) + " \n" 
file.writelines(k)
# Make header
k = "{:1};{:1};{:1};\n".format('PC','PCcount','PCcycles')
file.writelines(k)
for c1 in ThisPCDict:
        ValuesPC = ThisPCDict.get(c1)
        l ="{:1};{:1};{:1};\n".format(c1,ValuesPC[0],ValuesPC[1])
        file.writelines(l)

# Close file
f.close()
