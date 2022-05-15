from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
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

    # print(plot)
    return plot

def PrintData(Benchmark, plot):
    print("Benchmark: \t initial setup: \t Configuration: \t Calculation: \t Base number of cycles:")
    print("{:1}\t {:1} \t \t \t {:1} \t \t {:1} \t \t {:1}".format(Benchmark, plot[0], plot[1], plot[2], Base_Number_Of_Cycles))

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
            "stream6x6result",
            "streamDouble4x3result",
            "streamDouble6x6result"]

# plot1 = MakeGraphData(Benchmark[0], True)
# plot2 = MakeGraphData(Benchmark[1])
# plot3 = MakeGraphData(Benchmark[2])
# plot4 = MakeGraphData(Benchmark[3])
# plot5 = MakeGraphData(Benchmark[4])
# plot6 = MakeGraphData(Benchmark[5])
# plot7 = MakeGraphData(Benchmark[6])
# plot8 = MakeGraphData(Benchmark[7])
# plot9 = MakeGraphData(Benchmark[8])


# # # plot = {}
# # # for i in Benchmark:
# # #     if "Base" in i:
# # #         plot[i] = MakeGraphData(i,True)
# # #     else:
# # #         plot[i] = MakeGraphData(i)



# y = {}
# for i in  range(0,3):
#     y[i] = np.array([   plot1[i], 
#                         plot2[i],
#                         plot3[i], 
#                         plot4[i], 
#                         plot5[i], 
#                         plot6[i], 
#                         plot7[i],
#                         plot8[i],
#                         plot9[i]])

# x = Benchmark

Computation102Array = {
                        "Base": 611,
                        "Buffer 2x2": 564,
                        "Buffer 4x3": 670,
                        "Buffer 6x6": 684,
                        "Stream 2x2": 512,
                        "Stream 4x3": 496,
                        "Stream 6x6": 510,
                        ""          : 0,
                        "Base parallel": 175,
                        "Parallel stream 4x3": 214,
                        "Parallel stream 6x6": 149
                        }

Computation501Array = {
                        "Base": 2043,
                        "Buffer 2x2": 3334,
                        "Buffer 4x3": 3300,
                        "Buffer 6x6": 3386,
                        "Stream 2x2": 2491,
                        "Stream 4x3": 2470,
                        "Stream 6x6": 2544,
                        ""          : 0,
                        "Base parallel": 1386,
                        "Parallel stream 4x3": 1019,
                        "Parallel stream 6x6": 739
                        }

Computation1002Array = {
                        "Base": 3924,
                        "Buffer 2x2": 6782,
                        "Buffer 4x3": 6860,
                        "Buffer 6x6": 6848,
                        "Stream 2x2": 5099,
                        "Stream 4x3": 5175,
                        "Stream 6x6": 5159,
                        ""          : 0,
                        "Base parallel": 2736,
                        "Parallel stream 4x3": 2531,
                        "Parallel stream 6x6": 1466
                        }

Computation2001Array = {
                        "Base": 10592,
                        "Buffer 2x2": 13560,
                        "Buffer 4x3": 13428,
                        "Buffer 6x6": 13326,
                        "Stream 2x2": 10200,
                        "Stream 4x3": 10081,
                        "Stream 6x6": 9994,
                        ""          : 0,
                        "Base parallel": 7878,
                        "Parallel stream 4x3": 4250,
                        "Parallel stream 6x6": 2827
                        }

ConfigurationArray = {  "Base": 1,
                        "Buffer 2x2": 514,
                        "Buffer 4x3": 1407,
                        "Buffer 6x6": 3841,
                        "Stream 2x2": 514,
                        "Stream 4x3": 1407,
                        "Stream 6x6": 3841,
                        ""          : 0,
                        "Base parallel": 1,
                        "Parallel stream 4x3": 1407,
                        "Parallel stream 6x6": 3841
                    }

configSize = {  "Base": 0,
                "2x2": 256,
                "4x3": 704,
                "6x6": 1920
                }

configTime = {  "Base": 1,
                "2x2": 514,
                "4x3": 1407,
                "6x6": 3841
                }

CCodeConfigTime = { "Base": 1,
                    "Buffer 2x2": 63,
                    "Buffer 4x3": 121,
                    "Buffer 6x6": 226,
                    "Stream 2x2": 63,
                    "Stream 4x3": 121,
                    "Stream 6x6": 226,
                    ""          : 0,
                    "Base parallel": 1,
                    "Parallel stream 4x3": 121,
                    "Parallel stream 6x6": 226
                    }


yCCodeConfig    = np.array([el[1] for el in CCodeConfigTime.items()])
yConfigTime     = np.array([el[1] for el in ConfigurationArray.items()])
y102            = np.array([el[1] for el in Computation102Array.items()])
y501            = np.array([el[1] for el in Computation501Array.items()])
y1002           = np.array([el[1] for el in Computation1002Array.items()])
y2001           = np.array([el[1] for el in Computation2001Array.items()])

t = [i for i in Computation102Array]

plt.figure(1)
plt.title("Benchmark result. Array length = 102")
plt.ylabel("Cycles")
plt.bar(t, y102, label='Comp')
plt.bar(t, yCCodeConfig, bottom=y102, label='Code config')
bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+y102, label='Config')
plt.bar_label(bars)
# plt.axis([-0.5,6.5, 9000, 18500])
plt.legend()
plt.xticks(rotation=40)
plt.savefig('OverAll_performance_102_plot.png', bbox_inches='tight')

plt.figure(2)
plt.title("Benchmark result. Array length = 501")
plt.ylabel("Cycles")
plt.bar(t, y501, label='Comp')
plt.bar(t, yCCodeConfig, bottom=y501, label='Code config')
bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+y501, label='Config')
plt.bar_label(bars)
# plt.axis([-0.5,6.5, 9000, 18500])
plt.legend()
plt.xticks(rotation=40)
plt.savefig('OverAll_performance_501_plot.png', bbox_inches='tight')

plt.figure(3)
plt.title("Benchmark result. Array length = 1002")
plt.ylabel("Cycles")
plt.bar(t, y1002, label='Comp')
plt.bar(t, yCCodeConfig, bottom=y1002, label='Code config')
bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+y1002, label='Config')
plt.bar_label(bars)
# plt.axis([-0.5,6.5, 9000, 18500])
plt.legend()
plt.xticks(rotation=40)
plt.savefig('OverAll_performance_1002_plot.png', bbox_inches='tight')

plt.figure(4)
plt.title("Benchmark result. Array length = 2001")
plt.ylabel("Cycles")
plt.bar(t, y2001, label='Comp')
plt.bar(t, yCCodeConfig, bottom=y2001, label='Code config')
bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+y2001, label='Config')
plt.bar_label(bars)
# plt.axis([-0.5,6.5, 9000, 18500])
plt.legend()
plt.xticks(rotation=40)
plt.savefig('OverAll_performance_2001_plot.png', bbox_inches='tight')




# yShort = np.array([el[1] for el in Computation102Array.items()])
# t = [i for i in Computation102Array]

# plt.figure(1)
# plt.rcParams.update({'font.size': 12})
# plt.title("CGRA performance Array length = 102")
# plt.ylabel("Cycles")
# bars = plt.bar(t, yShort)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Array_102_computation_performance_plot.png', bbox_inches='tight')


# yShortPar = np.array([el[1] for el in Computation102ArrayPar.items()])
# t = [i for i in Computation102ArrayPar]

# plt.figure(2)
# plt.title("CGRA performance Array length = 102 Parallel")
# plt.ylabel("Cycles")
# bars = plt.bar(t, yShortPar)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Array_102_para_computation_performance_plot.png', bbox_inches='tight')


# yMed = np.array([el[1] for el in Computation501Array.items()])
# t = [i for i in Computation501Array]

# plt.figure(3)
# plt.title("CGRA performance Array length = 501")
# plt.ylabel("Cycles")
# bars = plt.bar(t, yMed)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Array_501_computation_performance_plot.png', bbox_inches='tight')

# yMedPar = np.array([el[1] for el in Computation501ArrayPar.items()])
# t = [i for i in Computation501ArrayPar]

# plt.figure(4)
# plt.title("CGRA performance Array length = 501 Parallel")
# plt.ylabel("Cycles")
# bars = plt.bar(t, yMedPar)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Array_501_para_computation_performance_plot.png', bbox_inches='tight')


# yLong = np.array([el[1] for el in Computation2001Array.items()])
# t = [i for i in Computation2001Array]

# plt.figure(5)
# plt.title("CGRA performance Array length = 2001")
# plt.ylabel("Cycles")
# bars = plt.bar(t, yLong)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 7500, 18500])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Array_2001_computation_performance_plot.png', bbox_inches='tight')

# yLongPar = np.array([el[1] for el in Computation2001ArrayPar.items()])
# t = [i for i in Computation2001ArrayPar]

# plt.figure(6)
# plt.title("CGRA performance Array length = 2001 Parallel")
# plt.ylabel("Cycles")
# bars = plt.bar(t, yLongPar)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Array_2001_Para_computation_performance_plot.png', bbox_inches='tight')

# yConfigTime = np.array([el[1] for el in ConfigurationArray.items()])
# t = [i for i in ConfigurationArray]
# plt.figure(7)
# plt.title("CGRA performance configuration")
# plt.ylabel("Cycles")

# bars = plt.bar(t, yConfigTime)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Configuration_performance_plot.png', bbox_inches='tight')

# yConfigTimePar = np.array([el[1] for el in ConfigurationArrayPar.items()])
# t = [i for i in ConfigurationArrayPar]
# plt.figure(8)
# plt.title("CGRA performance configuration Parallel")
# plt.ylabel("Cycles")

# bars = plt.bar(t, yConfigTimePar)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('Configuration_Para_performance_plot.png', bbox_inches='tight')

# yConfigSize = np.array([el[1] for el in configSize.items()])
# t = [i for i in configSize]
# # plt.rcParams.update({'font.size': 20})
# plt.figure(9)
# plt.title("CGRA Configuration size")
# plt.ylabel("Bits")

# bars = plt.bar(t, yConfigSize)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# plt.axis([-0.5,3.5, 0, 2300])
# plt.bar_label(bars)
# plt.savefig('Config_size_plot.png', bbox_inches='tight')

# yConfigCycles = np.array([el[1] for el in configTime.items()])
# t = [i for i in configTime]
# plt.figure(18)
# plt.title("CGRA Configuration Time")
# plt.ylabel("Cycles")

# bars = plt.bar(t, yConfigCycles)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# plt.axis([-0.5,3.5, 0, 4500])
# plt.bar_label(bars)
# plt.savefig('Config_time_plot.png', bbox_inches='tight')



# yCCodeConfig = np.array([el[1] for el in CCodeConfigTime.items()])
# t = [i for i in CCodeConfigTime]
# plt.rcParams.update({'font.size': 12})
# plt.figure(10)
# plt.title("CGRA C Code configuration time")
# plt.ylabel("Cycles")

# bars = plt.bar(t, yCCodeConfig)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('CCode_Config_plot.png', bbox_inches='tight')

# yCCodeConfigPar = np.array([el[1] for el in CCodeConfigTimePar.items()])
# t = [i for i in CCodeConfigTimePar]
# plt.figure(11)
# plt.title("CGRA C Code configuration time Parallel")
# plt.ylabel("Cycles")

# bars = plt.bar(t, yCCodeConfigPar)
# # plt.bar(x, y[1], bottom=y[0])
# # plt.bar(x, y[2], bottom=y[0]+y[1])
# # plt.axis([-0.5,6.5, 0.18, 0.24])
# plt.bar_label(bars)
# plt.xticks(rotation=40)
# plt.savefig('CCode_Config_Para_plot.png', bbox_inches='tight')



# t = [i for i in Computation102Array]

# # Plot_Maker(t, yShort,yCCodeConfig,yConfigTime,102,"Serial")

# w = 0.6

# plt.figure(12)
# plt.title("Benchmark result. Array length = 102. Serial")
# plt.ylabel("Cycles")
# plt.bar(t, yShort, label='Comp')
# plt.bar(t, yCCodeConfig, bottom=yShort, label='Code config')
# bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+yShort, label='Config')
# plt.bar_label(bars)
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_102_plot.png', bbox_inches='tight')

# plt.figure(13)
# plt.title("Benchmark result. Array length = 501. Serial")
# plt.ylabel("Cycles")
# plt.bar(t, yMed, label='Comp')
# plt.bar(t, yCCodeConfig, bottom=yMed, label='Code config')
# bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+yMed, label='Config')
# plt.bar_label(bars)
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_501_plot.png', bbox_inches='tight')

# plt.figure(14)
# plt.title("Benchmark result. Array length = 2001. Serial")
# plt.ylabel("Cycles")
# plt.bar(t, yLong, label='Comp')
# plt.bar(t, yCCodeConfig, bottom=yLong, label='Code config')
# bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+yLong, label='Config')
# plt.bar_label(bars)
# plt.axis([-0.5,6.5, 9000, 18500])
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_2001_plot.png', bbox_inches='tight')

# t = [i for i in Computation102ArrayPar]
# w = 0.6

# plt.figure(15)
# plt.title("Benchmark result. Array length = 102. Parallel")
# plt.ylabel("Cycles")
# plt.bar(t, yShortPar, label='Comp')
# plt.bar(t, yCCodeConfigPar, bottom=yShortPar, label='Code config')
# bars = plt.bar(t, yConfigTimePar, bottom=yCCodeConfigPar+yShortPar, label='Config')
# plt.bar_label(bars)
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_Para_102_plot.png', bbox_inches='tight')

# plt.figure(16)
# plt.title("Benchmark result. Array length = 501. Parallel")
# plt.ylabel("Cycles")
# plt.bar(t, yMedPar, label='Comp')
# plt.bar(t, yCCodeConfigPar, bottom=yMedPar, label='Code config')
# bars = plt.bar(t, yConfigTimePar, bottom=yCCodeConfigPar+yMedPar, label='Config')
# plt.bar_label(bars)
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_Para_501_plot.png', bbox_inches='tight')

# plt.figure(17)
# plt.title("Benchmark result. Array length = 2001. Parallel")
# plt.ylabel("Cycles")
# plt.bar(t, yLongPar, label='Comp')
# plt.bar(t, yCCodeConfigPar, bottom=yLongPar, label='Code config')
# bars = plt.bar(t, yConfigTimePar, bottom=yCCodeConfigPar+yLongPar, label='Config')
# plt.bar_label(bars)
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_Para_2001_plot.png', bbox_inches='tight')

# yLongmed = np.array([el[1] for el in Computation1002Array.items()])
# t = [i for i in Computation1002Array]

# plt.figure(19)
# plt.title("Benchmark result. Array length = 1002. Serial")
# plt.ylabel("Cycles")
# plt.bar(t, yLongmed, label='Comp')
# plt.bar(t, yCCodeConfig, bottom=yLongmed, label='Code config')
# bars = plt.bar(t, yConfigTime, bottom=yCCodeConfig+yLongmed, label='Config')
# plt.bar_label(bars)
# plt.axis([-0.5,6.5, 9000, 18500])
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_1002_plot.png', bbox_inches='tight')

# yLongmedPar = np.array([el[1] for el in Computation1002ArrayPar.items()])
# t = [i for i in Computation1002ArrayPar]


# plt.figure(20)
# plt.title("Benchmark result. Array length = 1002. Parallel")
# plt.ylabel("Cycles")
# plt.bar(t, yLongmedPar, label='Comp')
# plt.bar(t, yCCodeConfigPar, bottom=yLongmedPar, label='Code config')
# bars = plt.bar(t, yConfigTimePar, bottom=yCCodeConfigPar+yLongmedPar, label='Config')
# plt.bar_label(bars)
# plt.legend()
# plt.xticks(rotation=40)
# plt.savefig('OverAll_performance_Para_1002_plot.png', bbox_inches='tight')