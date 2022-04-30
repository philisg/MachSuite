import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import os
import numpy as np

Sections = ["Configuration", "Program start", "Computation"]
Base_Number_Of_Lines = 0
Base_Number_Of_Cycles = 0


def groupTheData(datasource):
    SectionDict = {}
    SectionSpace = -2
    SectionName = "Configuration"
    for i in range(len(datasource)):
        k = datasource.iloc[i][0]
        if "Section:" in k:
            k = k.lstrip("Section: ")
            # print(k)
            SectionDict[SectionName] = datasource[SectionSpace+2:i]
            SectionName = k
            SectionSpace = i
        if i == len(datasource)-1:
            SectionDict[SectionName] = datasource[SectionSpace+2:i]
    return SectionDict

def GetNumberOfLinesAndCycles(Benchmark, IsBaseBench=False):
    f = open(Benchmark+'_plain_histogram_output.txt','r')
    text = f.readline()
    Number_of_lines = 0
    for word in text.split():
        if word.isdigit():
            Number_of_lines = int(word)

    # Get number of cycles in simulation
    text = f.readline()
    Number_of_cycles = 0
    for word in text.split():
        if word.isdigit():
            Number_of_cycles = int(word)
        
    if IsBaseBench:
        global Base_Number_Of_Cycles
        Base_Number_Of_Cycles = Number_of_cycles

    return Number_of_lines, Number_of_cycles

def MakeGraphData(Benchmark, IsBaseBench=False):
    Number_of_lines, Number_of_cycles = GetNumberOfLinesAndCycles(Benchmark, IsBaseBench)

    # print("Number of lines:"  + str(Number_of_lines))
    print("Number of cycles: " + str(Number_of_cycles) + " for Benchmark: " + Benchmark)

    data = pd.read_csv(Benchmark+'_plain_histogram_output.txt', sep=';', skiprows=4)

    PC      = []
    PC      = data.loc[:,["PC","PCcount","PCcycles"]]
    dfPC    = pd.DataFrame(PC, columns=['PC', 'PCcount','PCcycles'])
    SectionDict = groupTheData(dfPC)
    plot = {0: 1, 1 : 1, 2 :1}
    for k in plot:
        for i in SectionDict[Sections[k]]["PCcycles"]:
            plot[k] += int(i)

    return plot


##################################################################################################
# try:
#     # Automatic detection of folder and benchmark
#     directory       = os.getcwd()
#     directoryList   = directory.split('\\')
#     Benchmark       = directoryList[3] + "_" + directoryList[4]
#     print("Checking ", Benchmark)
# except:
#     # Manual input of directory if not in the correct folder
#     Benchmark       = input("Which benchmark? Format:(benchmark_benchmark):")
#     splited         = Benchmark.split("_")
#     directory       = "Z:\Documents\MachSuite"
#     NewDirectory    = directory+"\\"+splited[0]+"\\"+splited[1]
#     os.chdir(NewDirectory)
Benchmark = [   
            "Base_result", 
            "2x2result",
            "4x3result",
            "6x6result",
            "stream2x2result",
            "stream4x3result",
            "stream6x6result"]


plot1 = MakeGraphData(Benchmark[0], True)
plot2 = MakeGraphData(Benchmark[1])
plot3 = MakeGraphData(Benchmark[2])
plot4 = MakeGraphData(Benchmark[3])
plot5 = MakeGraphData(Benchmark[4])
plot6 = MakeGraphData(Benchmark[5])
plot7 = MakeGraphData(Benchmark[6])

# plot = {}
# for i in Benchmark:
#     if "Base" in i:
#         plot[i] = MakeGraphData(i,True)
#     else:
#         plot[i] = MakeGraphData(i)


y = {}
for i in  range(0,3):
    y[i] = np.array([   plot1[i]/Base_Number_Of_Cycles, 
                        plot2[i]/Base_Number_Of_Cycles,
                        plot3[i]/Base_Number_Of_Cycles, 
                        plot4[i]/Base_Number_Of_Cycles, 
                        plot5[i]/Base_Number_Of_Cycles, 
                        plot6[i]/Base_Number_Of_Cycles, 
                        plot7[i]/Base_Number_Of_Cycles])

x = Benchmark

plt.title("CGRA performance")
plt.bar(x, y[0])
plt.bar(x, y[1], bottom=y[0])
plt.bar(x, y[2], bottom=y[0]+y[1])
plt.legend(["configuration", "Program", "Configuration"])
plt.show()
