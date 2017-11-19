#include <string.h>
#include <stdlib.h>
#include <iostream>

#include "../src/config.h"
#include "../src/Noritake_VFD_GU3000.h"
Noritake_VFD_GU3000 vfd;

int main(int argc, char **argv) {
  std::string type = argv[1]; //"sub" = subtitle, "info" = meta info (display language)
  std::string lang = argv[2]; //3-character language code
  //text = argv[3];

  // argc = number of arguments, argv = character input
  // helpful: https://stackoverflow.com/questions/4176326/arguments-to-main-in-c

  vfd.GU3000_init();
//  vfd.GU3000_setScreenBrightness(100);
  vfd.GU3000_setFontSize(_8x16Format, 1, 1);

  if(lang == "chi") {
    vfd.GU3000_useMultibyteChars(true);
    vfd.GU3000_setMultibyteCharset(2);
  } else if (lang == "eng") {
    vfd.GU3000_setCharset(CP850);
  } else if (lang == "spa") {
    vfd.GU3000_setCharset(CP850);
  } else if (lang == "fre") {
    vfd.GU3000_setCharset(CP850);
  }


  //split \n into new strings
  //based on this: https://stackoverflow.com/questions/18429273/in-c-how-to-split-a-string-on-n-into-lines

  char **res  = NULL;
  char *p = strtok (argv[3], "\n");
  int n_spaces = 0, i;
  while (p) {
      res = (char**)realloc (res, sizeof (char*) * ++n_spaces);
      if (res == NULL)
        exit (-1);
      res[n_spaces-1] = (char*)malloc(sizeof(char)*strlen(p));
      strcpy(res[n_spaces-1],p);
    p = strtok (NULL, "\n");
  }

  // print the result
  if(type == "info") {
    //center the info, assumes 8-pixel wide, 16 pixels tall
    vfd.GU3000_setCursor((256 - strlen(res[0]) * 8) / 2, 24);
    vfd.println(res[0]);
    vfd.GU3000_wait(2);
  } else if (type == "sub") {
    for (i = 0; i < (n_spaces+1); ++i)
      vfd.println(res[i]);
  }

  // free res
  // *****this is causing a segmentation fault, I believe
  for(i = 0; i < n_spaces; i++)
    free(res[i]);
  free(res);

}
