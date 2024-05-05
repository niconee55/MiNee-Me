int pinD = 4;  
int pinF = 5;  
int pinA = 6;
int pinB = 7;  
int pinG = 8;  
int pinE = 9;
int pinC = 10;  

bool playD = true;
bool playF = true;
bool playA = true;
bool playB = true;
bool playG = true;
bool playE = true;
bool playC = true;

void setup() {
  Serial.begin(31250);
  pinMode(pinC, OUTPUT);  
  pinMode(pinD, OUTPUT); 
  pinMode(pinE, OUTPUT);     
  pinMode(pinF, OUTPUT); 
  pinMode(pinG, OUTPUT);  
  pinMode(pinA, OUTPUT); 
  pinMode(pinB, OUTPUT);     
}

void loop() {
  // while(1);
  String data = Serial.readStringUntil('\n');
  if (data == "start"){
    digitalWrite(pinC, LOW);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, LOW);
    digitalWrite(pinG, LOW);
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
    Serial.print("start");
  }
  if (data == "end"){
    digitalWrite(pinC, LOW);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, LOW);
    digitalWrite(pinG, LOW);
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
    Serial.print("end");
  }

  int notes[10]; // assume most notes played at once is 10
  int index = 0;
  char* ptr = strtok((char*)data.c_str(), ",");
  while (ptr != NULL) {
    notes[index++] = atoi(ptr);
    ptr = strtok(NULL, ",");
  }
  int length = index;
  int* duplicateArray = nullptr;
  int* uniqueArray = nullptr;
  int dupCount = 0;
  int uniqueCount = 0;


  getDups(notes, length, duplicateArray, uniqueArray, dupCount, uniqueCount);

  for (int i = 0; i < dupCount; i++) {
      playNote(duplicateArray[i]);
  }
  delay(100);
  for (int i = 0; i < uniqueCount; i++) {
    playNote(uniqueArray[i]);
  }
}

void getDups(int notes[], int length, int* &duplicateArray, int* &uniqueArray, int &dupCount, int &uniqueCount) {
    bool isUnique[length];  // To track if a note is unique
    int dupSize = 0;  // Track number of duplicates
    int uniqueSize = 0;  // Track number of unique elements

    for (int i = 0; i < length; i++) {
        bool duplicateFound = false;
        
        // Check if the current note is a duplicate
        for (int j = 0; j < i; j++) {
            if (notes[i] == notes[j]) {
                duplicateFound = true;
                break;
            }
        }

        if (duplicateFound) {
            dupSize++;
        } else {
            isUnique[uniqueSize++] = true;  // Mark as unique
        }
    }

    // Create arrays to store duplicates and unique elements
    duplicateArray = new int[dupSize];
    uniqueArray = new int[uniqueSize];

    int dupIndex = 0;
    int uniqueIndex = 0;

    for (int i = 0; i < length; i++) {
        bool duplicateFound = false;
        
        for (int j = 0; j < i; j++) {
            if (notes[i] == notes[j]) {
                duplicateFound = true;
                break;
            }
        }

        if (duplicateFound) {
            duplicateArray[dupIndex++] = notes[i];
        } else {
            uniqueArray[uniqueIndex++] = notes[i];
        }
    }

    dupCount = dupSize;
    uniqueCount = uniqueSize;
}

void playNote(int note) {
  switch(note) {
    case 60: // C4 (middle C)
      playC = checkNote(pinC, playC);
      break;
    case 62: // D4
      playD = checkNote(pinD, playD);
      break;
    case 64: // E4
      playE = checkNote(pinE, playE);
      break;
    case 65: // F4
      playF = checkNote(pinF, playF);
      break;
    case 67: // G4
      playG = checkNote(pinG, playG);
      break;
    case 69: // A4
      playA = checkNote(pinA, playA);
      break;
    case 71: // B4
      playB = checkNote(pinB, playB);
      break;
  }
}

bool checkNote(int pin, bool play){
  if (play) {
    digitalWrite(pin, HIGH);
  } else {
    digitalWrite(pin, LOW);
  }
  return !play;
}