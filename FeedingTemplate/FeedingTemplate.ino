#include <SimpleModbusSlave.h>

//30мс пропуск между мосфетом и реле
#define LED 13
#define PWM_M 5
#define UP_M A3
#define DOWN_M A2
#define END_SWITCH 4
#define CURRENT A0

//CONFIGURABLE
#define MODBUS_ID 1

#define MAX_UP_TIME 15000
#define MAX_DOWN_TIME 8000
boolean endSwitchStopValue = false;
int time_for_motion_down = MAX_DOWN_TIME;
int time_for_motion_up = MAX_UP_TIME;
//END OF CONFIGURABLE

enum
{
  // just add or remove registers and your good to go...
  // The first register starts at address 0
  ENABLING,// OUT is avaliable 0 -not calibrated, 1 good - 2 not good
  ROTATION,// IN direction, 2 - up, 3 - down, 1 - stop, 4 - calibration
  STATE_NOW,//1 - stopped; 4 - moving, 2 - up, 3 - down
  LAST_COMMAND, //last change
  DOWN_TIME,
  UP_tiME,
  MAX_SPEED,
  HOLDING_REGS_SIZE // leave this one
  // total number of registers for function 3 and 16 share the same register array
  // i.e. the same address space
};

unsigned long motion_started = 0;
int rotation_cmd = 0;
unsigned int holdingRegs[HOLDING_REGS_SIZE]; // function 3 and 16 register array
volatile boolean end_found;
volatile boolean started = 0;


void setup()
{
  //объявить пин для датчика холла
  pinMode(END_SWITCH, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(PWM_M, OUTPUT);
  pinMode(UP_M, OUTPUT);
  pinMode(DOWN_M, OUTPUT);
  digitalWrite(UP_M, 0);
  digitalWrite(DOWN_M, 0);
  digitalWrite(PWM_M, 0);
  pinMode(LED, OUTPUT);
  modbus_configure(&Serial, 4800, SERIAL_8N2, MODBUS_ID, 7, HOLDING_REGS_SIZE, holdingRegs);
  modbus_update_comms(4800, SERIAL_8N2, MODBUS_ID);
  attachInterrupt(1, myEventListener, RISING);
  calibration();
}

void myEventListener() {

  delayMicroseconds(300);
  if (digitalRead(3)) {
    digitalWrite(PWM_M, 0);
    started = 0;
    end_found = 1;
  }
}

void calibration() {
  int calibration_time = 10000; // максимальное время подъема
  end_found = 0;
  delay(5000*MODBUS_ID);
  unsigned long check_started = millis();
  digitalWrite(DOWN_M, 1);
  tone(PWM_M, 1000);
  delay(300);
  tone(PWM_M, 2000);
  delay(300);
  tone(PWM_M, 3000);
  delay(300);
  noTone(PWM_M);
  //digitalWrite(DOWN_M, 0);
  //move down for 2 sec
  digitalWrite(DOWN_M, 1);
  delay(30);
  analogWrite(PWM_M, 150);
  delay(2000);
  analogWrite(PWM_M, 0);
  delay(30);
  digitalWrite(DOWN_M, 0);
  delay(30);
  digitalWrite(UP_M, 1);
  delay(30);
  while ((end_found == 0) && (millis() - check_started < calibration_time)) {
    analogWrite(PWM_M, 150);
  }
  stop_moving();
  if (end_found) {
    holdingRegs[LAST_COMMAND] = 2;
    holdingRegs[ENABLING] = 1;
    holdingRegs[STATE_NOW] = 2;
  } else {
    holdingRegs[ENABLING] = 2;
  }

}

boolean checkTime(unsigned long started, int timer) {
  boolean ok = false;
  if (millis() - started < timer) {
    ok = true;
  }
  return ok;
}

boolean checkHall() {
  //добавить повторную проверку
  //return digitalRead(END_SWITCH);
  boolean can_move = 0;
  if (digitalRead(END_SWITCH) != endSwitchStopValue) {
    can_move = 1;
  }
  return can_move;
}

boolean motion_allowed(int dir) { //3 - down, 2 - up
  boolean allowed = false;

  switch (dir) {
    case 3:
      if (checkTime(motion_started, time_for_motion_down)) {
        allowed = true;
      } else {
        started = 0;
      }
      break;
    case 2:
      if (checkHall() && checkTime(motion_started, time_for_motion_up)) {
        allowed = true;
      } else {
        started = 0;
      }
      break;
  }
  if (!allowed) {
    stop_moving();
  }
  //allowed = true;
  return allowed;
}

boolean cmd_changed() {
  boolean changed = false;
  if ((holdingRegs[ROTATION] != 0) && (holdingRegs[ROTATION] != holdingRegs[LAST_COMMAND])) {
    changed = true;
    holdingRegs[LAST_COMMAND] = holdingRegs[ROTATION];
    //переключение прерываний

    if ( holdingRegs[LAST_COMMAND] == 2) {
      attachInterrupt(1, myEventListener, RISING);
      delay(5);
    } else if (holdingRegs[LAST_COMMAND] == 3) {
      detachInterrupt(digitalPinToInterrupt(3));
      delay(5);
    }

  }
  return changed;
}
int max_sp = 250;
int min_sp = 120;
int now_sp;
int stop_in = 2000;
int step_time = stop_in / (max_sp - min_sp); // время через которое скорость упадет на 1
int start_stopping_at = 5000;
unsigned long last_update;
boolean in_progress = 0;
void move_it(int _rotation_cmd) {
  switch (_rotation_cmd) {
    case 1:
      stop_moving();
      now_sp = min_sp;
      break;
    case 2:


      if (millis() - motion_started > start_stopping_at) {

        if ((now_sp > min_sp) && (millis() - last_update > step_time)) {
          now_sp--;
          last_update = millis();
        }


      } else {
        now_sp = max_sp;
      }

      if (motion_allowed(_rotation_cmd)) {
        if (!in_progress) {
          digitalWrite(UP_M, 1);
          digitalWrite(13, 1);
          delay(30);
          in_progress = 1;
          holdingRegs[STATE_NOW] = 4;
        }
        analogWrite(PWM_M, now_sp);//now_sp

      } else {
        in_progress = 0;
      }
      break;
    case 3:
      //      if ((now_sp < 250) && (millis() - last_update > timer1)) {
      //        now_sp++;
      //        last_update = millis();
      //      }

      if (motion_allowed(_rotation_cmd)) {
        if (!in_progress) {
          digitalWrite(DOWN_M, 1);
          digitalWrite(13, 1);
          delay(30);
          in_progress = 1;
          holdingRegs[STATE_NOW] = 4;
        }
        analogWrite(PWM_M, 250);

      }
      break;
    case 4:
      calibration();
      break;

  }

}
void stop_moving() {

  analogWrite(PWM_M, 0);
  delay(30);
  digitalWrite(UP_M, 0);
  digitalWrite(DOWN_M, 0);
  digitalWrite(13, 0);
  delay(100);
  in_progress = 0;
  holdingRegs[STATE_NOW] = holdingRegs[LAST_COMMAND];

}
unsigned long last_b;
void loop()
{
  modbus_update();
  /*if(millis()-last_b>500){
    digitalWrite(13,!digitalRead(13));
    last_b=millis();
    }
  */
  if (cmd_changed()) {
    analogWrite(PWM_M, 0);
    delay(30);
    digitalWrite(UP_M, 0);
    digitalWrite(DOWN_M, 0);
    started = 1;
    in_progress = 0;
    motion_started = millis();
  }
  //check it, if not moving
  if (started) {
    move_it(holdingRegs[ROTATION]);
  } else {
    stop_moving();
  }


}
