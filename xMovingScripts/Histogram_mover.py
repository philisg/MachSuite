import os

# This is a script for moving histograms from their own folder into a common folder

def movingFunction(arg1,arg2):
    try:
        os.rename('Z:/Documents/MachSuite/{}/{}/{}_{}_plain_histogram_output.txt'.format(arg1,arg2,arg1,arg2), "Z:/Documents/MachSuite/old/Histograms/{}_{}_plain_histogram_output.txt".format(arg1,arg2))
        print("Found file {} {}".format(arg1,arg2))
    
    except:
        print("Could not find file {} {}".format(arg1,arg2))

movingFunction("aes","aes")
movingFunction("bfs","bulk")
movingFunction("bfs","queue")
movingFunction("fft","strided")
movingFunction("fft","transpose")
movingFunction("gemm","blocked")
movingFunction("gemm","ncubed")
movingFunction("kmp","kmp")
movingFunction("md","grid")
movingFunction("md","knn")
movingFunction("nw","nw")
movingFunction("sort","radix")
movingFunction("sort","merge")
movingFunction("spmv","crs")
movingFunction("spmv","ellpack")
movingFunction("stencil","stencil3d")
movingFunction("stencil","stencil2d")
movingFunction("viterbi","viterbi")


