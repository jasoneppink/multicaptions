#include <U8g2lib.h>

U8G2_T6963_240X64_F_8080 u8g2(U8G2_R0, 11, 5, 10, 4, 9, 3, 8, 2, /*enable=lcd_7*/ 12, /*cs= lcd_5 */ 13, /*dc=lcd 8 c/d */ 7, /*reset=pin10 green*/ 6); // Connect RD with +5V, FS0 and FS1 with GND

String inputString;                     //holds incoming subtitle data
boolean stringComplete = false;         //whether the line of text is complete and ready to be printed to the display

String language;                        //holds incoming language data
String languageCode;                    //current language (three characters in ISO 639-2B format e.g. "eng")
String displayLanguage;                 //language to display on screen
boolean newLanguage = false;            //whether a language has been detected

String launchState = "blank";           //is display default blank ("blank"), shows subtitles ("subtitles"), or shows instructions (custom)
String displayLaunchState;              //default text to display on screen
boolean newLaunchState = false;         //whether instructions have been detected to return to launch state

unsigned long displayPause;             //test for whether subtitles are temporarily disabled while language name is displayed 

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
  
  //Default to Latin characters (English, French, Spanish, etc.)
  u8g2.setFont(u8g2_font_helvR10_tf);
  
  //clear the internal memory
  u8g2.clear();

  //print "Ready..."
  u8g2.setCursor(x, line1_y);
  u8g2.print("Ready...");
  u8g2.sendBuffer();
  u8g2.clearBuffer();
}


void loop() {
  //switch to the correct font based on language
  if (newLanguage) {
    //Serial is sent as "{LANGUAGE[display language][3-letter language code]}" e.g. {LANGUAGEEnglisheng} or {LANGUAGEespañolspa}
    displayLanguage = language.substring(8, language.length()-3);
    languageCode = language.substring(language.length()-3, language.length());
    
    if(languageCode=="eng" || languageCode=="fre" || languageCode=="hat" || languageCode=="spa") {
      u8g2.setFont(u8g2_font_helvR10_tf);
    } else if(languageCode=="ara") {
      u8g2.setFont(u8g2_font_unifont_t_arabic);
    } else if(languageCode=="ben") {
      //no Bengali font yet
    } else if(languageCode=="chi") {
      u8g2.setFont(u8g2_font_unifont_t_chinese2);
    } else if(languageCode=="kor") {
      //no Korean font yet
    } else if(languageCode=="rus") {
      u8g2.setFont(u8g2_font_unifont_t_cyrillic);
    } else if(languageCode=="urd") {
      //no Urdu font yet
    } 
  
    //print the new language
    printCenteredText(displayLanguage);
    displayPause = millis();
    newLanguage = false;
  }

  if (newLaunchState) {
    //Serial is sent as "{DEFAULT[display instructions]}" e.g. {DEFAULTblank} or {DEFAULTsubtitles}
    displayLaunchState = launchState.substring(7, launchState.length());
   
    if (displayLaunchState == "blank") {
      u8g2.clear();
    } else if (displayLaunchState != "subtitles") {
      printCenteredText(displayLaunchState);
    }
    newLaunchState = false;
  }

  //if we're not paused on a display language
  if((millis() - displayPause) > 500) {
    //print the lines when everything has arrived via serialEvent()
    if (stringComplete) {
        u8g2.clearBuffer();
     
        //clear the internal memory
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
  //otherwise clear out any text that may have come in during the display language pause
  } else {
    line1 = "";
    line2 = "";
    stringComplete = false;
  }
}

void printCenteredText(String text) {
    u8g2.clearBuffer();
    char textChar[text.length()+1];
    text.toCharArray(textChar, text.length()+1);
    int textWidth = u8g2.getUTF8Width(textChar);
    u8g2.setCursor((240-textWidth)/2, 36);
    u8g2.print(text);
    u8g2.sendBuffer(); 
}

/*
SerialEvent occurs whenever new data comes in the
hardware serial RX. This routine is run between each
time loop() runs, so using delay inside loop can delay
response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    //get the new byte:
    char inChar = (char)Serial.read();

    //detect language
    if (inChar == '{') {
      //indicates beginning of new instruction string, so clear what came before
      inputString == "";
    } else if(inChar == '}') {
      //indicates end of new instruction string
      if (inputString.substring(0,8) == "LANGUAGE") {
        newLanguage = true;
        language = inputString;
      } else if(inputString.substring(0,7) == "DEFAULT") {
        newLaunchState = true;
        launchState = inputString;
      }
      //clear string
      inputString = "";
    } else {
      //add character to the inputString:
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


