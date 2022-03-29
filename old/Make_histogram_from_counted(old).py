import pandas as pd
import matplotlib.pyplot as plt
import numpy as NP
import sys
Benchmark = input("Which benchmark? format: \"benchmark_benchmark\" ")

# To make the print go to a file
sys.stdout=open(Benchmark+"_python_output.txt", "w")
# Get number of lines in simulation
f = open(Benchmark+'_plain_histogram_output.txt','r')
text=f.readline()
Number_of_lines = 0
for word in text.split():
   if word.isdigit():
       Number_of_lines = int(word)
    
print("Number of lines:"+ str(Number_of_lines))
data = pd.read_csv(Benchmark+'_plain_histogram_output.txt', sep=';', skiprows=1)

PC =[]
PC = data.loc[:,["PC","count"]]
Inst = []
Inst = data.loc[:,["inst","count.1"]]
dfPC = pd.DataFrame(PC, columns=['PC', 'count'])
dfPC.sort_values(by=['count'], inplace=True, ascending=False, ignore_index=True)
dfInst = pd.DataFrame(Inst, columns=['inst', 'count.1'])
dfInst.sort_values(by=['count.1'], inplace=True, ascending=False, ignore_index=True)

df = pd.DataFrame(zip(dfPC,dfInst), columns=['PC', 'instruction'])
values = pd.DataFrame(dfPC[:10])
fig = plt.figure(figsize=(10, 5))
ax = fig.add_axes([0,0,1,1])
y = [(el[1]/Number_of_lines)*100 for el in values.values]
X = [el[0] for el in values.values]
ax.bar(X,y)
plt.title("PC")
plt.xlabel("PC")
plt.ylabel("%")
plt.ylim([0,30])
plt.xticks(rotation=-20)
# plt.show()
plt.savefig(Benchmark+'_pc_plot.png', bbox_inches='tight')
ToPrint = pd.DataFrame(dfPC)
toprintx = [el[0] for el in ToPrint.values]
toprintXpart = [(el[1]/Number_of_lines)*100 for el in ToPrint.values]
print(dfPC[:10])
print("% of each PC address:")
# for i in range(10):
    # print(i, "=", X[i], "=", y[i],"%")

for i in range(300):
    print(i, "=", toprintx[i], "=",toprintXpart[i],"%")

values = pd.DataFrame(dfInst[:10])
fig = plt.figure(figsize=(10, 5))
ax = fig.add_axes([0,0,1,1])
y = [(el[1]/Number_of_lines)*100 for el in values.values]
X = [el[0] for el in values.values]
ax.bar(X,y)
plt.title("Instruction")
plt.xlabel("Instruction")
plt.ylabel("%")
plt.ylim([0,30])
plt.xticks(rotation=-20)
# plt.show()
plt.savefig(Benchmark+'_instruction_plot.png', bbox_inches='tight')

ToPrint = pd.DataFrame(dfInst)
toprintx = [el[0] for el in ToPrint.values]
toprintXpart = [(el[1]/Number_of_lines)*100 for el in ToPrint.values]

print(dfInst[:10])
print("% of each instruction address:")
# for i in range(10):
#     print(i, "=", X[i], "=", y[i], "%")

for i in range(300):
    print(i, "=", toprintx[i], "=",toprintXpart[i],"%")

sys.stdout.close()

