
forTheBenchmark()
{
	cd $1
	cd $2
	rm $1
	export CC=riscv64-unknown-elf-gcc
	make
	riscv64-unknown-elf-objdump -S $1 &> $1_$2_objdump_S.txt
	cd ../..
}

echo "Starting script"
forTheBenchmark aes aes
forTheBenchmark bfs bulk
forTheBenchmark bfs queue
forTheBenchmark fft strided
forTheBenchmark fft transpose
forTheBenchmark gemm blocked
forTheBenchmark gemm ncubed
forTheBenchmark kmp kmp
forTheBenchmark md grid
forTheBenchmark md knn
forTheBenchmark nw nw
forTheBenchmark sort merge 
forTheBenchmark sort radix
forTheBenchmark spmv crs
forTheBenchmark spmv ellpack
forTheBenchmark stencil stencil2d
forTheBenchmark stencil stencil3d
forTheBenchmark viterbi viterbi
