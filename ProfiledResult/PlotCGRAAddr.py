
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

Benchmark1 = "Base_result"
Benchmark2 = "2x2result"
Benchmark3 = "stream2x2result"
Benchmark4 = "6x6result"



# To make the print go to a file
# sys.stdout=open(Benchmark+"_python_percentage_output.txt", "w")
# Get number of lines in simulation


plot1 = MakeGraphData(Benchmark1, True)
plot2 = MakeGraphData(Benchmark2)
plot3 = MakeGraphData(Benchmark3)
plot4 = MakeGraphData(Benchmark4)

y0 = np.array([plot1[0]/Base_Number_Of_Cycles, plot2[0]/Base_Number_Of_Cycles, plot3[0]/Base_Number_Of_Cycles, plot4[0]/Base_Number_Of_Cycles])
y1 = np.array([plot1[1]/Base_Number_Of_Cycles, plot2[1]/Base_Number_Of_Cycles, plot3[1]/Base_Number_Of_Cycles, plot4[1]/Base_Number_Of_Cycles])
y2 = np.array([plot1[2]/Base_Number_Of_Cycles, plot2[2]/Base_Number_Of_Cycles, plot3[2]/Base_Number_Of_Cycles, plot4[2]/Base_Number_Of_Cycles])
x = np.array([Benchmark1, Benchmark2, Benchmark3, Benchmark4])

plt.title("CGRA performance")
plt.bar(x, y0)
plt.bar(x, y1, bottom=y0)
plt.bar(x, y2, bottom=y0+y1)
plt.legend(["configuration", "Program", "Configuration"])
plt.show()

