KERN=sum


CFLAGS?=-g -Og -O3 -Wall -Wno-unused-label

SRCS=$(KERN).c 

$(KERN):
	riscv64-unknown-elf-gcc $(CFLAGS) -o $(KERN) $(SRCS) -static

clean:
	rm -f $(KERN) generate output.data

