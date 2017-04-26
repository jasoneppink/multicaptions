#include <U8g2lib.h>

U8G2_T6963_240X64_F_8080 u8g2(U8G2_R0, 10, 11, 12, 13, 6, 7, 8, 9, /*enable=lcd_7 grey*/ 5, /*cs= lcd_5 */ 2, /*dc=lcd 8 c/d purple*/ 4, /*reset=pin10 green*/ 3); // Connect RD with +5V, FS0 and FS1 with GND

String inputString;         // a string to hold incoming data
String language;            // current language (three characters in ISO 639-2B format e.g. "eng")

boolean stringComplete = false;  // whether the string is complete
boolean newLanguage = false; //whether a language has been detected

String line1;
String line2;

//location of text on display
int x = 5;
int line1_y = 20;
int line2_y = 40;

void setup(void) {
  // initialize serial:
  Serial.begin(9600);
  
  u8g2.begin();
  u8g2.enableUTF8Print();
  u8g2.setFontDirection(0);
  
  //Default to English, Spanish, French
  u8g2.setFont(u8g2_font_helvR10_tf);
  
  // clear the internal memory
  //u8g2.firstPage();
  //u8g2.clearBuffer();
  u8g2.clear();
  u8g2.setCursor(x, line1_y);
  u8g2.print("Ready...");

  u8g2.sendBuffer();
  delay(1000);
  u8g2.clearBuffer();
  //u8g2.firstPage();
  
}


void loop() {
  // print the lines when everything has arrived via serialEvent()
  if (newLanguage) {
    if(language=="eng" || language=="spa" || language=="fre") {
      u8g2.setFont(u8g2_font_helvR10_tf);
    } else if(language=="chi") {
      u8g2.setFont(u8g2_font_unifont_t_chinese1);
    } else if(language=="ara") {
      u8g2.setFont(u8g2_font_unifont_t_arabic);
    }
    newLanguage = false;
  }
  
  if (stringComplete) {
      u8g2.clearBuffer();
   
      // clear the internal memory
      u8g2.firstPage();
      do {  
         u8g2.setCursor(x, line1_y);
         u8g2.print(line1);
         line1 = "";

         u8g2.setCursor(x, line2_y);
         u8g2.print(line2);
         line2 = "";
      }

      while ( u8g2.nextPage() );
      stringComplete = false;
  }
}


/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();

    //detect language
    if(inChar == '~') {
      language = inputString;
      inputString = "";
      newLanguage = true;
    } else {
      // add character to the inputString:
      inputString += inChar;
    }
    
    //split into lines
    if (inChar == '\n') {
      line1 = inputString;
      inputString = "";
    } else if (inChar == '\r') {
      if (line1 == "") {
          line1 = inputString;
      } else {
        line2 = inputString;
      }
      inputString = "";
      stringComplete=true;
    }
  }
}


