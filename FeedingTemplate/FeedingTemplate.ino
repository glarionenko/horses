#include <SimpleModbusSlave.h>
#define MODBUS_ID 1
#define LED 13
#define PWM_M 5
#define UP_M A2
#define DOWN_M A3
#define END_SWITCH 3

boolean endSwitchStopValue = true;

enum
{
  // just add or remove registers and your good to go...
  // The first register starts at address 0
  ENABLING,// OUT is avaliable
  ROTATION,// IN direction, 2 - up, 3 - down, 1 - stop
  STATE_NOW,//1 - stopped; 4 - moving, 2 - up, 3 - down
  LAST_COMMAND, //last change
  DOWN_TIME,
  UP_tiME,
  MAX_SPEED,
  HOLDING_REGS_SIZE // leave this one
  // total number of registers for function 3 and 16 share the same register array
  // i.e. the same address space
};

unsigned int holdingRegs[HOLDING_REGS_SIZE]; // function 3 and 16 register array
int rotation_cmd = 0;
void setup()
{
  //объявить пин для датчика холла
  pinMode(END_SWITCH, INPUT);
  pinMode(PWM_M, OUTPUT);
  pinMode(UP_M, OUTPUT);
  pinMode(DOWN_M, OUTPUT);
  digitalWrite(UP_M, 0);
  digitalWrite(DOWN_M, 0);
  digitalWrite(PWM_M, 0);
  pinMode(LED, OUTPUT);
  modbus_configure(&Serial, 4800, SERIAL_8N2, MODBUS_ID, 7, HOLDING_REGS_SIZE, holdingRegs);
  modbus_update_comms(4800, SERIAL_8N2, MODBUS_ID);
  //проверить наличие геркона, если нет, то поискать и сообщить, что его нет в ENABLED =0
  holdingRegs[ENABLING] = 1; //0x1
  //
}
unsigned long motion_started = 0;
int time_for_motion_down = 3000;
int time_for_motion_up = 3000;
boolean checkTime(unsigned long started, int timer) {
  boolean ok = false;
  if (millis() - started < timer) {
    ok = true;
  }
  return ok;
}
boolean checkHall() {
  //добавить повторную проверку
  return digitalRead(END_SWITCH);
}
boolean motion_allowed(int dir) { //3 - down, 2 - up
  boolean allowed = false;
  switch (dir) {
    case 3:
      if (checkTime(motion_started, time_for_motion_down)) {
        allowed = true;
      }
      break;
    case 2:
      if (checkHall && checkTime(motion_started, time_for_motion_up)) {
        allowed = true;
      }
      break;
  }
  return allowed;
}
boolean cmd_changed() {
  boolean changed = false;
  if ((holdingRegs[ROTATION] != 0) && (holdingRegs[ROTATION] != holdingRegs[LAST_COMMAND])) {
    changed = true;
    holdingRegs[LAST_COMMAND] = holdingRegs[ROTATION];
  }
  return changed;
}
void move_it(int _rotation_cmd) {
  switch (_rotation_cmd) {
    case 1:
      analogWrite(PWM_M, 0);
      delay(1000);//время на выключение питания
      digitalWrite(UP_M, 0);
      digitalWrite(DOWN_M, 0);
      digitalWrite(13, 0);
      //now_sp = 100;
      break;
    case 2:
      //      if ((now_sp < 250) && (millis() - last_update > timer1)) {
      //        now_sp++;
      //        last_update = millis();
      //      }
      if (motion_allowed(_rotation_cmd)) {
        analogWrite(PWM_M, 250);//now_sp
        delay(500);
        digitalWrite(UP_M, 1);
        digitalWrite(13, 1);
      }
      break;
    case 3:
      //      if ((now_sp < 250) && (millis() - last_update > timer1)) {
      //        now_sp++;
      //        last_update = millis();
      //      }
      if (motion_allowed(_rotation_cmd)) {
        analogWrite(PWM_M, 250);//now_sp
        delay(500);
        digitalWrite(DOWN_M, 1);
        digitalWrite(13, 1);
      }
      break;

  }

}
void loop()
{
  modbus_update();
  if (cmd_changed()) {
    move_it(holdingRegs[ROTATION]);
  }
}
