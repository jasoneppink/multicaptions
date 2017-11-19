CC=g++
CFLAGS=-fno-exceptions -fno-rtti
DEPS=../src/config.h ../src/interface.h ../src/Noritake_VFD_GU3000.h
OBJS=imagetest.o Noritake_VFD_GU3000.o linux_serial.o

all: imagetest
clean:
	rm -rf *.o imagetest
imagetest: $(OBJS) 
	$(CC) $(OBJS) -oimagetest
imagetest.o: imagetest.cpp $(DEPS)
	$(CC) $(CFLAGS) -c imagetest.cpp
Noritake_VFD_GU3000.o: ../src/Noritake_VFD_GU3000.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
linux_serial.o: ../src/linux_serial.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
