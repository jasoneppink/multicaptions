CC=g++
CFLAGS=-fno-exceptions -fno-rtti
DEPS=../src/config.h ../src/interface.h ../src/Noritake_VFD_GU3000.h
OBJS=test.o Noritake_VFD_GU3000.o linux_serial.o

all: test
clean:
	rm -rf *.o test
test: $(OBJS) 
	$(CC) $(OBJS) -otest
test.o: test.cpp $(DEPS)
	$(CC) $(CFLAGS) -c test.cpp
Noritake_VFD_GU3000.o: ../src/Noritake_VFD_GU3000.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
linux_serial.o: ../src/linux_serial.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
