import pandas as pd
# import sys
import os

pd.set_option('display.max_columns', None) #prevents trailing elipses
pd.set_option('display.max_rows', None)

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

From_range_hex = input("From range in hex: ")
To_range_hex = input("To range in hex: ")

# To make the print go to a file
# sys.stdout=open(Benchmark+"_RangeChecker_output.txt", "w")
# Get number of lines in simulation
f = open(Benchmark+'_plain_histogram_output.txt','r')
text=f.readline()
Number_of_lines = 0
for word in text.split():
   if word.isdigit():
       Number_of_lines = int(word)

# Get number of cycles in simulation
text=f.readline()
Number_of_cycles = 0
for word in text.split():
   if word.isdigit():
       Number_of_cycles = int(word)

# print("Number of lines:"+ str(Number_of_lines))
# print("Number of cycles:"+ str(Number_of_cycles))

data = pd.read_csv(Benchmark+'_plain_histogram_output.txt', sep=';', skiprows=2)

PC  =[]
PC  = data.loc[:,["PC","PCcount","PCcycles"]]
dfPC = pd.DataFrame(PC, columns=['PC', 'PCcount','PCcycles'])
dfPC.sort_values(by=['PC'], inplace=True, ascending=False, ignore_index=True)

From_range_int  = int(From_range_hex,16)
To_range_int    = int(To_range_hex,16)

Range_cycles = 0

for i in range(0,len(dfPC)-1):
    if ((int(dfPC.iloc[i][0],16) >= From_range_int) and (int(dfPC.iloc[i][0],16) <= To_range_int)):
        Range_cycles += int(dfPC.iloc[i][2])

Percent_of_runtime = (Range_cycles/Number_of_cycles)*100

print('Cycles in range {} to {}: {} = {}%'.format(From_range_hex,To_range_hex,Range_cycles,Percent_of_runtime))
# sys.stdout.close()

