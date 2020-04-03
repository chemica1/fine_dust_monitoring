
// 공기청정기 위 등에서 먼지를 가라앉힌 후 voltage값 개별적으로 측정 필요
// 4/1 0.65V로 관측, 3M 측정기와 대조
#define no_dust 0.54
// 60초 이동평균
#define MAX 60

//이동평균을 위한 원형큐 변수 선언
int front=0;
int rear=0;
float queue[MAX];

//아두이노-센서간에 핀 설정
int dustout=A0;
int v_led=7;

// 센서로 읽은 값 변수 선언
float vo_value=0;

// 센서로 읽은 값을 전압으로 측정 변수
float sensor_voltage=0;

// 실제 미세 먼지 밀도 변수
float dust_density=0;

// 미세 먼지 밀도 이동평균값 변수
float moving_average=0;


void setup()
{
 Serial.begin(9600); // 통신 속도 9600bps로 시리얼 통신 시작
 pinMode(v_led,OUTPUT); // 적외선 led 출력으로 설정
}

void loop()
{
 // 미세 먼지 센서 동작
 digitalWrite(v_led,LOW); // 적외선 LED ON
 delayMicroseconds(280); // 280us동안 딜레이
 vo_value=analogRead(dustout); // 데이터를 읽음
 delayMicroseconds(40); // 320us - 280us
 digitalWrite(v_led,HIGH); // 적외선 LED OFF
 delayMicroseconds(9680); // 10ms(주기) -320us(펄스 폭) 한 값

 sensor_voltage=get_voltage(vo_value);
 dust_density=get_dust_density(sensor_voltage);
 moving_average=get_moving_average(dust_density);
 
 Serial.print("Dust Density = ");
 Serial.print(moving_average);
 Serial.println(" [ug/m^3]");

 delay(1000);
}

float get_voltage(float value)
{
 // 아날로그 값을 전압 값으로 바꿈
 float V= value * 5.0 / 1024; 
 return V; 
}

float get_dust_density(float voltage)
{
 // 데이터 시트에 있는 미세 먼지 농도(ug) 공식 기준
 float dust=(voltage-no_dust) / 0.005;
 return dust;
}

float get_moving_average(float dust_density)
{ 
 //이동평균 함수
 float tmp = 0.0;
 if(IsFull() == true) deleteq();
 addq(dust_density);
 for(int i = 0; i<60; i++)
 {
   tmp = tmp + queue[i];
 }
 return (tmp/60.0);
}


//큐 관련 함수
int IsEmpty(void)
{
  if(front==rear)//front와 rear가 같으면 큐는 비어있는 상태 
      return true;
  else return false;
}

int IsFull(void)
{
  int tmp=(rear+1)%MAX; //원형 큐에서 rear+1을 MAX로 나눈 나머지값이
  if(tmp==front)//front와 같으면 큐는 가득차 있는 상태 
      return true;
  else
      return false;
}

void addq(float value)
{
  if(IsFull()) return false;
  else{
       rear = (rear+1)%MAX;
       queue[rear]=value;
      }
}

int deleteq()
{
  if(IsEmpty());
  else{
      front = (front+1)%MAX;
      return queue[front];
  }
}

// Serial.print("value = ");
// Serial.println(vo_value);
// Serial.print("Voltage = ");
// Serial.print(sensor_voltage);
// Serial.println(" [V]");
// Serial.print("Dust Density = ");
// Serial.print(dust_density);
// Serial.println(" [ug/m^3]");
