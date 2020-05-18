#include <pm2008_i2c.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 4 //온습도센서 핀
#define DHTTYPE DHT22 // Uncomment the type of sensor in use:

uint32_t delayMS;
DHT_Unified dht(DHTPIN, DHTTYPE);

PM2008_I2C pm2008_i2c;

void setup() {

  
  pm2008_i2c.begin();
  Serial.begin(9600);
  pm2008_i2c.command();

  dht.begin(); //온습도 센서 선언
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);

  delayMS = sensor.min_delay / 1000;
  delay(1000);
}

void loop() {
  uint8_t ret = pm2008_i2c.read();
  if (ret == 0) {
    Serial.print(pm2008_i2c.pm1p0_tsi);
    Serial.print("a|");
    Serial.print(pm2008_i2c.pm2p5_tsi);
    Serial.print("b|");
    Serial.print(pm2008_i2c.pm10_tsi);
    Serial.print("c|");
  }
  sensors_event_t event;  
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println("Error reading temperature!");
  }
  else {
    Serial.print(event.temperature);
    Serial.print("d|");
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println("Error reading humidity!");
  }
  else {
    Serial.print(event.relative_humidity);
    Serial.println("e|");
  }
  delay(delayMS);
}
