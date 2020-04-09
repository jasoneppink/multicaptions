CC=g++
CFLAGS=-fno-exceptions -fno-rtti
DEPS=src/config.h src/interface.h src/Noritake_VFD_GU3000.h
OBJS=outputvfd.o Noritake_VFD_GU3000.o linux_serial.o

all: outputvfd
clean:
	rm -rf *.o outputvfd
outputvfd: $(OBJS) 
	$(CC) $(OBJS) -ooutputvfd `/usr/lib/arm-linux-gnueabihf/ImageMagick-6.9.10/bin-q16/Magick++-config --cppflags --cxxflags --ldflags --libs`
outputvfd.o: outputvfd.cpp $(DEPS)
	#TODO: find a better way to link Magick++-config
	$(CC) $(CFLAGS) -c outputvfd.cpp `/usr/lib/arm-linux-gnueabihf/ImageMagick-6.9.10/bin-q16/Magick++-config --cppflags --cxxflags --ldflags --libs`
Noritake_VFD_GU3000.o: src/Noritake_VFD_GU3000.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
linux_serial.o: src/linux_serial.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<
