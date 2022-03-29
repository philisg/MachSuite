#!/usr/bin/python

from fcntl import I_ATMARK
import sys

from sympy import false, true
ThisInstDict    = {}
ThisPCDict      = {}

# Number of lines read from simulated benchmark
NumberOfLines   = 0
LastCycleCount  = 0
NumberOfCycles  = 0
StartAddress = {"aes_aes":"00000000000113ac",
"bfs_bulk":"00000000000103f8",
"bfs_queue":"0000000000010436",
"fft_strided":"0000000000010406",
"fft_transpose":"000000000001165e",
"gemm_blocked":"000000000001041c",
"gemm_ncubed":"000000000001039a",
"kmp_kmp":"000000000001044a",
"md_grid":"00000000000105ce",
"md_knn":"0000000000010410",
"nw_nw":"0000000000010528",
"sort_merge":"00000000000105a0",
"sort_radix":"0000000000010a84",
"spmv_crs":"00000000000103b8",
"spmv_ellpack":"00000000000103fa",
"stencil_stencil2d":"0000000000010434",
"stencil_stencil3d":"00000000000107a8",
"viterbi_viterbi":"00000000000104d6"}

EndAddress = {"aes_aes":"000000000001158a",
"bfs_bulk":"000000000001072c",
"bfs_queue":"000000000001076a",
"fft_strided":"00000000000106a4",
"fft_transpose":"0000000000011896",
"gemm_blocked":"0000000000010630",
"gemm_ncubed":"00000000000105ae",
"kmp_kmp":"0000000000010640",
"md_grid":"0000000000010c70",
"md_knn":"0000000000010746",
"nw_nw":"000000000001077a",
"sort_merge":"000000000001077c",
"sort_radix":"0000000000010c76",
"spmv_crs":"000000000001064e",
"spmv_ellpack":"0000000000010662",
"stencil_stencil2d":"000000000001063c",
"stencil_stencil3d":"000000000001097e",
"viterbi_viterbi":"0000000000010744"}

# Name of benchmark to profile
# Benchmark       = raw_input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark     = input("which Benchmark? (format: \"benchmark_benchmark\") ")
# Benchmark     = "aes_aes"

Benchmark       = sys.argv[1]+"_"+sys.argv[2]
skip            = 3
ReadingLineNumber = 0
LastLoopPC      = "0"
LastLoopInst    = "0"
StartLine       = 0
Done_analyzing  = false
# If we dont know the starting point, analyze all.
if StartAddress[Benchmark] == " ":
    StartLine = 1

with open(Benchmark+"_outputlog.txt", 'r') as f:
    for line in f:
        if type(line) is str:
            if StartLine == 0:
                linesplit = line.split("] ")
                for i in linesplit:
                    if "pc=[" in i:
                        value = i.split("[")
                        if value[1] == StartAddress[Benchmark]:
                            StartLine = 1
                        break
            else:
                if Done_analyzing: break

                ActualCycles    = 0
                CycleString     = line.strip("C0: [")
                CycleString     = CycleString.split(" ")
                try:
                    CurrentCycle = int(CycleString[0])
                except:
                    continue
                
                if LastCycleCount == 0:
                    LastCycleCount = CurrentCycle
                ActualCycles    = CurrentCycle - LastCycleCount
                NumberOfCycles  += ActualCycles
                LastCycleCount  = CurrentCycle

                NumberOfLines += 1
                x = line.split("] ")
                for i in x:                
                    if "pc=[" in i:
                        value   = i.split("[")
                        i       = value[1]
                        if EndAddress != " " and i == EndAddress[Benchmark]:
                            Done_analyzing = true
                            break
                        if LastLoopPC in ThisPCDict:
                            # update +1
                            count                   = ThisPCDict.get(LastLoopPC)
                            ThisPCDict[LastLoopPC]  = [count[0] + 1,count[1] + ActualCycles]
                        else:
                            # add to dict
                            ThisPCDict[LastLoopPC]   = [1, ActualCycles]
                        LastLoopPC = i
                    if "inst=[" in i:
                        value   = i.split("[")
                        i       = value[1]
                        if LastLoopInst in ThisInstDict:
                            # update +1
                            count                       = ThisInstDict.get(LastLoopInst)
                            ThisInstDict[LastLoopInst]  = [count[0] + 1, count[1]+ActualCycles]
                        else:
                            # add to dict
                            ThisInstDict[LastLoopInst] = [1, ActualCycles]
                        LastLoopInst = i
                        break
                
                


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
