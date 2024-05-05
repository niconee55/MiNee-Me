int solenoidPin1 = 7;  
int solenoidPin2 = 6;  
int solenoidPin3 = 5;   
int solenoidPin4 = 4;    
void setup() 
{
  pinMode(solenoidPin1, OUTPUT);  
  pinMode(solenoidPin2, OUTPUT); 
  pinMode(solenoidPin3, OUTPUT);     
  pinMode(solenoidPin4, OUTPUT);    
}

void loop() 
{
  digitalWrite(solenoidPin1, HIGH);
  digitalWrite(solenoidPin3, HIGH);
  digitalWrite(solenoidPin4, HIGH); 
  digitalWrite(solenoidPin2, HIGH);    //Switch Solenoid ON
  delay(500);                          //Wait 1 Second
  digitalWrite(solenoidPin1, LOW);
  digitalWrite(solenoidPin4, LOW);
  digitalWrite(solenoidPin3, LOW); 
  digitalWrite(solenoidPin2, LOW);        //Switch Solenoid OFF
  delay(500);    
 }