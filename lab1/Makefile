ASFLAGS := -m32
CFLAGS  := -m32 -g -std=c99 -Wall -Werror -D_GNU_SOURCE
LDFLAGS := -m32
LDLIBS  := -lcrypto

ifeq ($(wildcard /usr/bin/execstack),)
  ifneq ($(wildcard /usr/sbin/execstack),)
    ifeq ($(filter /usr/sbin,$(subst :, ,$(PATH))),)
      PATH := $(PATH):/usr/sbin
    endif
  endif
endif

all = zookld zookfs zookfs-exstack zookfs-ssp zookd zookd-exstack zookd-ssp shellcode.bin
all: $(all)

%-exstack: %
	cp $< $@
	execstack -s $@

zookld: zookld.o http.o

zookd: zookd.o http.o

zookfs: zookfs.o http.o

zookd-ssp: zookd-ssp.o http-ssp.o

zookfs-ssp: zookfs-ssp.o http-ssp.o

%.o: %.c
	$(CC) $< -c -o $@ $(CFLAGS) -fno-stack-protector

%-ssp.o: %.c
	$(CC) $< -c -o $@ $(CFLAGS)

%.bin: %.o
	objcopy -S -O binary -j .text $< $@

clean:
	rm -f *.o *.pyc *.bin $(all)

check-bugs:
	./check-bugs.py bugs.txt

check-crash: bin.tar.gz exploit-2a.py exploit-2b.py shellcode.bin
	tar xf bin.tar.gz
	./check-part2.sh zook-exstack.conf ./exploit-2a.py
	./check-part2.sh zook-exstack.conf ./exploit-2b.py

check-exstack: bin.tar.gz exploit-3.py shellcode.bin
	tar xf bin.tar.gz
	./check-part3.sh zook-exstack.conf ./exploit-3.py

check-libc: bin.tar.gz exploit-4a.py exploit-4b.py shellcode.bin
	tar xf bin.tar.gz
	./check-part3.sh zook.conf ./exploit-4a.py
	./check-part3.sh zook.conf ./exploit-4b.py

check: check-bugs check-crash check-exstack check-libc

lab%-handin.tar.gz: clean
	tar cf - `find . -type f | grep -v '^\.*$$' | grep -v '/CVS/' | grep -v '/\.svn/' | grep -v '/\.git/' | grep -v 'lab[0-9].*\.tar\.gz'` | gzip > $@

handin: lab1-handin.tar.gz
	@echo "Please visit http://css.csail.mit.edu/6.858/2012/labs/handin.html"
	@echo "and upload $<.  Thanks!"

submit: lab1-handin.tar.gz
	./submit.py $<

.PHONY: check check-bugs check-exstack check-libc handin

