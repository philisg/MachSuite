#!/usr/bin/python


ThisInstDict = {}
ThisPCDict = {}
# Number of lines read from simulated benchmark
NumberOfLines = 0
# Name of benchmark to profile
Benchmark = raw_input("which Benchmark? (format: \"benchmark_benchmark\") ")

with open(Benchmark+"_outputlog.txt", 'r') as f:
    for line in f:
        if type(line) is str:
            NumberOfLines += 1
            x = line.split("] ")
            for i in x:                
                if "pc=[" in i:
                    value = i.split("[")
                    i = value[1]
                    if i in ThisPCDict:
                        # update +1
                        count = ThisPCDict.get(i)
                        ThisPCDict[i] = count + 1
                    else:
                        # add to dict
                        ThisPCDict[i] = 1
                if "inst=[" in i:
                    value = i.split("[")
                    i = value[1]
                    if i in ThisInstDict:
                        # update +1
                        count = ThisInstDict.get(i)
                        ThisInstDict[i] = count + 1
                    else:
                        # add to dict
                        ThisInstDict[i] = 1

# Make sure the dicts are equal length
dif = len(ThisInstDict) - len(ThisPCDict)
k = "NA"
if dif < 0:
    dif = -dif
    for i in range(dif):
        ThisInstDict[i]= k
elif dif > 0:
    for i in range(dif):
        ThisPCDict[i]= k

# Create file to put text in
file = open(Benchmark+'_plain_histogram_output.txt','w')
# Number of lines read from benchmark file
k = "Number of simulated lines: " +  str(NumberOfLines) + " \n" 
file.writelines(k)
# Make header
k = "{:1};{:1};{:1};{:1}\n".format('PC','count','inst','count')
file.writelines(k)
for c1, c2 in zip(ThisPCDict, ThisInstDict):
        l ="{:1};{:1};{:1};{:1}\n".format(c1,ThisPCDict[c1],c2,ThisInstDict[c2])
        file.writelines(l)

# Close file
f.close()
