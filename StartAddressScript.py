import os


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
#     newDirectory    = directory+"\\"+splited[0]+"\\"+splited[1]
#     os.chdir(newDirectory)

Benchmarks = ["aes_aes",
"bfs_bulk",
"bfs_queue",
"fft_strided",
"fft_transpose",
"gemm_blocked",
"gemm_ncubed",
"kmp_kmp",
"md_grid",
"md_knn",
"nw_nw",
"sort_merge",
"sort_radix",
"spmv_crs",
"spmv_ellpack",
"stencil_stencil2d",
"stencil_stencil3d",
"viterbi_viterbi"]

StartAddressDict = {}
EndAddressDict = {}

for i in Benchmarks:
    NameSplit   = i.split("_")
    newPath     = "Z:\Documents\MachSuite\\"+NameSplit[0]+"\\"+NameSplit[1]
    os.chdir(newPath)
    Benchmark   = i
    StartCounter= 0
    EndCounter  = 0
    StartingAddress  = ""
    EndAddress       = ""
    with open(Benchmark+'_objdump_S.txt','r') as f:
        for line in f:
            if "<run_benchmark>" in line:
                if StartCounter == 1:
                    wordSplit = line.split(" ")
                    StartingAddress = wordSplit[0]
                StartCounter += 1
            if "<Benchmark_done_running>" in line:
                if EndCounter == 1:
                    wordSplit = line.split(" ")
                    EndAddress = wordSplit[0]
                EndCounter += 1
    
    StartAddressDict[Benchmark] = StartingAddress
    EndAddressDict[Benchmark] = EndAddress

os.chdir("Z:\Documents\MachSuite\\")
file = open("Start_and_End_Address.txt", "w")
k = "Starting addresses: \n"
file.writelines(k)

for i in StartAddressDict:
    value = StartAddressDict.get(i)
    k = "\"{:1}\":\"{:1}\",\n".format(i,value)
    file.writelines(k)

k = "End addresses: \n"
file.writelines(k)
for i in EndAddressDict:
    value = EndAddressDict.get(i)
    k = "\"{:1}\":\"{:1}\",\n".format(i,value)
    file.writelines(k)