CC=g++
CFLAGS=-fno-exceptions -fno-rtti
DEPS=../src/config.h ../src/interface.h ../src/Noritake_VFD_GU3000.h
OBJS=Demo.o Noritake_VFD_GU3000.o linux_serial.o

all: demo
clean:
	rm -rf *.o demo
demo: $(OBJS) 
	$(CC) $(OBJS) -odemo
Demo.o: Demo.cpp $(DEPS)
	$(CC) $(CFLAGS) -c Demo.cpp
Noritake_VFD_GU3000.o: ../src/Noritake_VFD_GU3000.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
linux_serial.o: ../src/linux_serial.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
