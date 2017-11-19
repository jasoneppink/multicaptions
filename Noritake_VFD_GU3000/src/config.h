// CPU frequency in Hertz
#define F_CPU                           16000000UL

#ifdef __AVR
	#include <util/delay.h>
	#include <avr/pgmspace.h>
#else
	#include <unistd.h>
	#define _delay_us(x)                usleep(x)
	#define _delay_ms(x)                usleep(x*1000)
	#define pgm_read_byte(p)			(*(uint8_t*)p)
#endif

#define NORITAKE_VFD_WIDTH              256
#define NORITAKE_VFD_HEIGHT             64
#define NORITAKE_VFD_LINES              (NORITAKE_VFD_HEIGHT/8)

//Delay time between the Atmel starting and the VFD module being
//initialized. This is necessary to allow the module's controller
//to initialize. This value will vary depend on the power supply
//and hardware setup. 500 ms is more than enough time for the
//module to start up. This delay will only occur the first time
//the CUY_init() or CUY_reset() method is called.
#define NORITAKE_VFD_RESET_DELAY        500

// SELECT THE INTERFACE TO THE VFD MODULE
// NORITAKE_VFD_INTERFACE:
//  0 = Serial
//  1 = Reversed for future use
//  2 = Linux serial device
#define NORITAKE_VFD_INTERFACE          2

#if NORITAKE_VFD_INTERFACE==0
    //
    //  ASYNCHRONOUS SERIAL INTERFACE OPTIONS
    //
    //  NORITAKE_VFD_BAUD           Baud rate
    //  RXD_PORT & RXD_PIN          Data line (RXD) port & pin
    //  DTR_PORT & DTR_PIN          Busy line (SBUSY) port & pin
    //
    #define NORITAKE_VFD_BAUD       38400
    #define OUT_PIN                 0
    #define OUT_PORT                PORTA
    #define BUSY_PIN                1
    #define BUSY_PORT               PORTA
#elif NORITAKE_VFD_INTERFACE==2
	#define NORITAKE_VFD_BAUD		38400
	#define NORITAKE_VFD_FILE		"/dev/ttyUSB0"
#endif

