import pandas as pd
import matplotlib.pyplot as plt
import numpy as NP
import sys
Benchmark = input("Which benchmark? ")
sys.stdout=open(Benchmark+"_python_output.txt", "w")

data = pd.read_csv(Benchmark+'_outputlog.txt', skiprows=3)
lengde = len(data)
PC = []
Inst = []
for i in range(int(lengde)):
    testline = data.iloc[i,0]
    if type(testline) is str:
        x = testline.split("] ")
        # print(x)
        for k in x:
            if "inst=[" in k:
                Inst.append(k)
            if "pc=[" in k:
                PC.append(k)

print("Total elements of PC: ",len(PC))
print("Total elements of instructions: ",len(Inst))

df = pd.DataFrame(list(zip(PC,Inst)), columns=['PC', 'instruction'])
values = pd.DataFrame(df['PC'].value_counts()[:10])
fig = plt.figure(figsize=(10, 5))
ax = fig.add_axes([0,0,1,1])
X = values.index
y = [(el[0]/len(PC))*100 for el in values.values]
ax.bar(X,y)
plt.title("PC")
plt.xlabel("PC")
plt.ylabel("%")
plt.ylim([0,30])
plt.xticks(rotation=-20)
plt.savefig(Benchmark+'_pc_plot.png', bbox_inches='tight')

print(df['PC'].value_counts()[:10])
print("% of each address:")
for i in range(10):
    print(i, "=", X[i], "=", y[i],"%")

values = pd.DataFrame(df['instruction'].value_counts()[:10])
fig = plt.figure(figsize=(10, 5))
ax = fig.add_axes([0,0,1,1])
X = values.index
y = [(el[0]/len(Inst))*100 for el in values.values]
ax.bar(X,y)
plt.title("Instruction")
plt.xlabel("Instruction")
plt.ylabel("%")
plt.ylim([0,30])
plt.xticks(rotation=-20)
plt.savefig(Benchmark+'_instruction_plot.png', bbox_inches='tight')

print(df['instruction'].value_counts()[:10])
print("% of each address:")
for i in range(10):
    print(i, "=", X[i], "=", y[i], "%")

sys.stdout.close()
