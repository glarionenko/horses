#include <SimpleModbusSlave.h>

#define  LED 13 
#define PWM_M 5
#define UP_M A2
#define DOWN_M A3

// Using the enum instruction allows for an easy method for adding and 
// removing registers. Doing it this way saves you #defining the size 
// of your slaves register array each time you want to add more registers
// and at a glimpse informs you of your slaves register layout.

//////////////// registers of your slave ///////////////////
enum 
{     
  // just add or remove registers and your good to go...
  // The first register starts at address 0
  ADC_VAL,     
  PWM_VAL,
  PWM_NEW,       
  HOLDING_REGS_SIZE // leave this one
  // total number of registers for function 3 and 16 share the same register array
  // i.e. the same address space
};

unsigned int holdingRegs[HOLDING_REGS_SIZE]; // function 3 and 16 register array
////////////////////////////////////////////////////////////

void setup()
{
  pinMode(PWM_M,OUTPUT);
  pinMode(UP_M,OUTPUT);
  pinMode(DOWN_M,OUTPUT);
  digitalWrite(UP_M,0);
  digitalWrite(DOWN_M,0);
  modbus_configure(&Serial, 4800, SERIAL_8N2, 2, 7, HOLDING_REGS_SIZE, holdingRegs);

  // modbus_update_comms(baud, byteFormat, id) is not needed but allows for easy update of the
  // port variables and slave id dynamically in any function.
  modbus_update_comms(4800, SERIAL_8N2, 2);
  digitalWrite(PWM_M,0);
  pinMode(LED, OUTPUT);
}
int timer1=100;
unsigned long last_update=0;
int now_sp=0;
void loop()
{
  // modbus_update() is the only method used in loop(). It returns the total error
  // count since the slave started. You don't have to use it but it's useful
  // for fault finding by the modbus master.
  
  modbus_update();

  
  
  holdingRegs[ADC_VAL] = 0x1234; // update data to be read by the master to adjust the PWM
  
  switch(holdingRegs[PWM_VAL]){
    case 0:
    analogWrite(PWM_M, 0); // constrain adc value from the arduino master to 255
    delay(1000);
  digitalWrite(UP_M,0); // constrain adc value from the arduino master to 255
  digitalWrite(13, 0);
  now_sp=100;
  break;
  case 1:
  if((now_sp<250)&&(millis()-last_update>timer1)){
    now_sp++;
    last_update=millis();
    }
  analogWrite(PWM_M, now_sp); // constrain adc value from the arduino master to 255
  digitalWrite(UP_M, 1); // constrain adc value from the arduino master to 255
  digitalWrite(13, 1);
  break;
  case 2:
  if((now_sp<250)&&(millis()-last_update>timer1)){
    now_sp++;
    last_update=millis();
    }
  analogWrite(PWM_M, now_sp); // constrain adc value from the arduino master to 255
  digitalWrite(DOWN_M, 1); // constrain adc value from the arduino master to 255
  digitalWrite(13, 1);
  break;
    
  }

    
  /* Note:
     The use of the enum instruction is not needed. You could set a maximum allowable
     size for holdinRegs[] by defining HOLDING_REGS_SIZE using a constant and then access 
     holdingRegs[] by "Index" addressing. 
     I.e.
     holdingRegs[0] = analogRead(A0);
     analogWrite(LED, holdingRegs[1]/4);
  */
  
}
