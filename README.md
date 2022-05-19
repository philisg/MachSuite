# MachSuite

[![build status](https://travis-ci.org/breagen/MachSuite.svg?branch=master)](https://travis-ci.org/breagen/MachSuite)

MachSuite is a benchmark suite intended for accelerator-centric research.

There is a Makefile in the top direcrory as well as one within each benchmark
subdirectory.

We suggest running the benchmarks locally (from their own directory) for now.

Also, our validation approach does is not portable across machines.
For now, the final check to see if the output is correct is not performed.
We are working on fixing it. However, this should not change the computation
or behavior of the benchmarks at all.

The benchmarks used for the Master thesis is the benchmarks named with RoCC<xxxxx>Tester and Sum. The initial though was to use the MachSuite benchmarks to test the performance, but we discovered that this was a little bit hard to do at this point in time.


## Licensing

All code is open source (BSD-compatible) and free to use and distribute. Please
look in the LICENSE file for details.

## Citing

If you use the code, we would appreciate it if you cite the following paper:

> Brandon Reagen, Robert Adolf, Sophia Yakun Shao, Gu-Yeon Wei, and David Brooks.
> *"MachSuite: Benchmarks for Accelerator Design and Customized Architectures."*
  2014 IEEE International Symposium on Workload Characterization.

For any questions/concerns, please email [reagen@fas.harvard.edu](reagen@fas.harvard.edu)

Enjoy!!
