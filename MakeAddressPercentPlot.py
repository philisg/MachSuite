import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
pd.set_option('display.max_columns' , None) #prevents trailing elipses
pd.set_option('display.max_rows'    , None)

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

Benchmark = input("which benchmark?")

# To make the print go to a file
sys.stdout=open(Benchmark+"_python_percentage_output.txt", "w")
# Get number of lines in simulation
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

print("Number of lines:"  + str(Number_of_lines))
print("Number of cycles:" + str(Number_of_cycles))

data = pd.read_csv(Benchmark+'_plain_histogram_output.txt', sep=';', skiprows=2)

PC      = []
PC      = data.loc[:,["PC","PCcount","PCcycles"]]
# Inst    = []
# Inst    = data.loc[:,["inst","instcount","instcycles"]]
dfPC    = pd.DataFrame(PC, columns=['PC', 'PCcount','PCcycles'])
dfPC.sort_values(by=['PCcount'], inplace=True, ascending=False, ignore_index=True)
print(dfPC[:200])


# The code below is to make the PC ranges. We check the how many times each PC have been run up against its
# neightbor. If the neightbor has appeared approx the same amount of time, it will create a range.

# The search lenght of the range creator. 
searchLength    = len(dfPC)/2
PercentageArray = []
CheckingArray   = []
i               = 0

if searchLength > 100:
    while i < searchLength:
        PCAppearance    = 0
        LowestAddr      = ""
        HighestAddr     = ""
        CycleCount      = 0
        # PC_in_Range     = []
        for k in range(1,100):
            if (int(dfPC.iloc[i][1]) > int(dfPC.iloc[i+k][1])-9) and (int(dfPC.iloc[i][1]) < int(dfPC.iloc[i+k][1])+9):
                if PCAppearance == 0:
                    PCAppearance    = int(dfPC.iloc[i][1]) + int(dfPC.iloc[i+k][1])
                    LowestAddr      = int(dfPC.iloc[i][0],16)
                    HighestAddr     = LowestAddr
                    CycleCount      = int(dfPC.iloc[i][2])+int(dfPC.iloc[i+k][2])
                    # PC_in_Range.append(dfPC.iloc[i][0])
                else:
                    PCAppearance    += int(dfPC.iloc[i+k][1])
                    CycleCount      += int(dfPC.iloc[i+k][2])
                if LowestAddr > int(dfPC.iloc[i+k][0],16):
                    LowestAddr      = int(dfPC.iloc[i+k][0],16)
                if HighestAddr < int(dfPC.iloc[i+k][0],16):
                    HighestAddr     = int(dfPC.iloc[i+k][0],16)
                # PC_in_Range.append(dfPC.iloc[i+k][0])
            else:
                if PCAppearance != 0:
                    addressRange = str(hex(LowestAddr) + " \n- " + hex(HighestAddr))
                    PercentageArray.append([addressRange,(PCAppearance/Number_of_lines)*100,(CycleCount/Number_of_cycles)*100])
                    # PercentageArray[dfPC.iloc[i][0]] = (PCAppearance/Number_of_lines)*100
                    # print("PCAppearance: ", PCAppearance, " add k:",k)
                    i = i + (k-1)
                    
                break
        # CheckingArray.append(PC_in_Range)
        i += 1
else:
    while i < searchLength:
        PCAppearance    = 0
        LowestAddr      = ""
        HighestAddr     = ""
        CycleCount      = 0
        # PC_in_Range     = []
        for k in range(1,len(dfPC)-i):
            if (int(dfPC.iloc[i][1]) > int(dfPC.iloc[i+k][1])-9) and (int(dfPC.iloc[i][1]) < int(dfPC.iloc[i+k][1])+9):
                if PCAppearance == 0:
                    PCAppearance    = int(dfPC.iloc[i][1]) + int(dfPC.iloc[i+k][1])
                    LowestAddr      = int(dfPC.iloc[i][0],16)
                    HighestAddr     = LowestAddr
                    CycleCount      = int(dfPC.iloc[i][2])+int(dfPC.iloc[i+k][2])
                    # PC_in_Range.append(dfPC.iloc[i][0])
                else:
                    PCAppearance    += int(dfPC.iloc[i+k][1])
                    CycleCount      += int(dfPC.iloc[i+k][2])
                if LowestAddr > int(dfPC.iloc[i+k][0],16):
                    LowestAddr      = int(dfPC.iloc[i+k][0],16)
                if HighestAddr < int(dfPC.iloc[i+k][0],16):
                    HighestAddr     = int(dfPC.iloc[i+k][0],16)
                # PC_in_Range.append(dfPC.iloc[i+k][0])
            else:
                if PCAppearance != 0:
                    addressRange = str(hex(LowestAddr) + " \n- " + hex(HighestAddr))
                    PercentageArray.append([addressRange,(PCAppearance/Number_of_lines)*100,(CycleCount/Number_of_cycles)*100])
                    # PercentageArray[dfPC.iloc[i][0]] = (PCAppearance/Number_of_lines)*100
                    # print("PCAppearance: ", PCAppearance, " add k:",k)
                    i = i + (k-1)
                    
                break
        # CheckingArray.append(PC_in_Range)
        i += 1

dfPercentArray = pd.DataFrame(PercentageArray, columns=['PC', 'PCcount','PCcycles'])
dfPercentArray.sort_values(by=['PCcycles'], inplace=True, ascending=False, ignore_index=True)
# print(CheckingArray[:10])
print("----------------------------------------------------------------------------")
print(dfPercentArray)
plt.rcParams.update({'font.size': 45})
values = pd.DataFrame(dfPercentArray[:5])
fig = plt.figure(figsize=(10, 8))
ax = fig.add_axes([0,0,1,1])
y = [el[2] for el in values.values]
X = [el[0] for el in values.values]
ax.bar(X,y)
# plt.xlabel("PC")
plt.ylabel("Runtime %")
plt.autoscale(enable=True, axis=y)
plt.xticks(rotation=90)
# plt.show()
plt.savefig(Benchmark+'_pc_percentage_plot.png', bbox_inches='tight')

sys.stdout.close()

