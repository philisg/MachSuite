BENCHMARKS=\
	RoCC2x2DoubleTester/RoCC2x2DoubleTester \
	RoCC2x2Tester/RoCC2x2Tester \
	RoCC4x3DoubleTester/RoCC4x3DoubleTester \
	RoCC4x3Tester/RoCC4x3Tester \
	RoCC6x6DoubleTester/RoCC6x6DoubleTester \
	RoCC6x6Tester/RoCC6x6Tester
#FIXME\
	backprop/backprop \

CFLAGS=-g -Og -O3 -Wall -Wno-unused-label

.PHONY: build run generate all test clean

build:
	@( for b in $(BENCHMARKS); do $(MAKE) CFLAGS="$(CFLAGS)" -C $$b; done )



### For regression tests
all: clean build generate run


clean:
	@( for b in $(BENCHMARKS); do $(MAKE) -C $$b clean || exit ; done )
