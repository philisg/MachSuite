import pandas as pd
import matplotlib.pyplot as plt
import os
pd.set_option('display.max_columns' , None) #prevents trailing elipses
pd.set_option('display.max_rows'    , None)

try:
    # Automatic detection of folder and benchmark
    directory       = os.getcwd()
    directoryList   = directory.split('\\')
    Benchmark       = directoryList[3] + "_" + directoryList[4]
    print("Checking ", Benchmark)
except:
    # Manual input of directory if not in the correct folder
    Benchmark       = input("Which benchmark? Format:(benchmark_benchmark):")
    splited         = Benchmark.split("_")
    directory       = "Z:\Documents\MachSuite"
    newDirectory    = directory+"\\"+splited[0]+"\\"+splited[1]
    os.chdir(newDirectory)



Address             = ""
Number_of_cycles    = 0
DataPoints          = []

with open(Benchmark+'_search_for_address.txt','r') as f:
    Address   = f.readline()
    # Get number of cycles in simulation
    Cycletext = f.readline()
    for word in Cycletext.split():
        if word.isdigit():
            Number_of_cycles = int(word)

    for line in f:
        line = line.strip()
        DataPoints.append(line)


Scale       = 100
Part        = Number_of_cycles/Scale
GraphDict   = {}

for i in range(0,Scale):
    GraphDict[i] = 0
    for k in range(0,len(DataPoints)):
        if int(DataPoints[k]) >= i*Part and  int(DataPoints[k]) <= (i+1)*Part:
            if i in GraphDict:
                GraphDict[i] += 1

Address = Address.strip('\n')

plt.rcParams.update({'font.size': 18})
fig         = plt.figure(figsize=(10, 8))
ax          = fig.add_axes([0,0,1,1])
y           = [el[1] for el in GraphDict.items()]
Default_x   = [el for el in range(0,Scale+1)]
x           = [int(el*Part) for el in range(0,Scale+1)]
ax.bar(Default_x,y)
plt.title(Address)
plt.autoscale(enable=True, axis=y)
plt.ylabel("Apperance")
plt.xlabel("Cycle")
plt.xticks(rotation=90)
plt.xticks(Default_x,x)
plt.locator_params(axis='x', nbins=10)
# plt.show()
plt.savefig(Benchmark+Address+'plot.png', bbox_inches='tight')
