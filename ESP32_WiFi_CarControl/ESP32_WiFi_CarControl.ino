#include <Arduino.h>
#ifdef ESP32
#include <WiFi.h>
#include <AsyncTCP.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#endif
#include <ESPAsyncWebServer.h>

#include <iostream>
#include <sstream>

struct MOTOR_PINS
{
  int pinEn;  
  int pinIN1;
  int pinIN2;    
};

std::vector<MOTOR_PINS> motorPins = 
{
  {25, 32, 33},  //LEFT_MOTOR Pins (EnA, IN1, IN2)
  {26, 27, 14},  //RIGHT_MOTOR  Pins (EnB, IN3, IN4)
};

#define UP 1
#define DOWN 2
#define LEFT 3
#define RIGHT 4
#define STOP 0

#define RIGHT_MOTOR 0
#define LEFT_MOTOR 1

#define FORWARD 1
#define BACKWARD -1

#define LED_PIN 2  // Example LED pin

#define INITIAL_SPEED 110
#define MIN_DISTANCE_TAG 40

bool state = 0;

const int PWMFreq = 1000; /* 1 KHz */
const int PWMResolution = 8;
const int PWMSpeedChannel = 4;

const char* ssid     = "MyWiFiCar";
const char* password = "12345678";

AsyncWebServer server(80);
AsyncWebSocket wsCarInput("/CarInput");

const char* htmlHomePage PROGMEM = R"HTMLHOMEPAGE(
<!DOCTYPE html>
<html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <style>
    .arrows {
      font-size:40px;
      color:red;
    }
    td.button {
      background-color:black;
      border-radius:25%;
      box-shadow: 5px 5px #888888;
    }
    td.button:active {
      transform: translate(5px,5px);
      box-shadow: none; 
    }

    .noselect {
      -webkit-touch-callout: none; /* iOS Safari */
        -webkit-user-select: none; /* Safari */
         -khtml-user-select: none; /* Konqueror HTML */
           -moz-user-select: none; /* Firefox */
            -ms-user-select: none; /* Internet Explorer/Edge */
                user-select: none; /* Non-prefixed version, currently
                                      supported by Chrome and Opera */
    }

    .slidecontainer {
      width: 100%;
    }

    .slider {
      -webkit-appearance: none;
      width: 100%;
      height: 20px;
      border-radius: 5px;
      background: #d3d3d3;
      outline: none;
      opacity: 0.7;
      -webkit-transition: .2s;
      transition: opacity .2s;
    }

    .slider:hover {
      opacity: 1;
    }
  
    .slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: red;
      cursor: pointer;
    }

    .slider::-moz-range-thumb {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: red;
      cursor: pointer;
    }

    </style>
  
  </head>
  <body class="noselect" align="center" style="background-color:white">
     
    <h1 style="color: teal;text-align:center;">Hash Include Electronics</h1>
    <h2 style="color: teal;text-align:center;">WiFi Tank Control</h2>
    
    <table id="mainTable" style="width:400px;margin:auto;table-layout:fixed" CELLSPACING=10>
      <tr>
        <td></td>
        <td class="button" ontouchstart='sendButtonInput("MoveCar","1")' ontouchend='sendButtonInput("MoveCar","0")'><span class="arrows" >&#8679;</span></td>
        <td></td>
      </tr>
      <tr>
        <td class="button" ontouchstart='sendButtonInput("MoveCar","3")' ontouchend='sendButtonInput("MoveCar","0")'><span class="arrows" >&#8678;</span></td>
        <td class="button"></td>    
        <td class="button" ontouchstart='sendButtonInput("MoveCar","4")' ontouchend='sendButtonInput("MoveCar","0")'><span class="arrows" >&#8680;</span></td>
      </tr>
      <tr>
        <td></td>
        <td class="button" ontouchstart='sendButtonInput("MoveCar","2")' ontouchend='sendButtonInput("MoveCar","0")'><span class="arrows" >&#8681;</span></td>
        <td></td>
      </tr>
      <tr/><tr/>
      <tr/><tr/>
      <tr/><tr/>
      <tr>
        <td style="text-align:left;font-size:25px"><b>Speed:</b></td>
        <td colspan=2>
         <div class="slidecontainer">
            <input type="range" min="0" max="255" value="150" class="slider" id="Speed" oninput='sendButtonInput("Speed",value)'>
          </div>
        </td>
      </tr>       
    </table>
  
    <script>
      var webSocketCarInputUrl = "ws:\/\/" + window.location.hostname + "/CarInput";      
      var websocketCarInput;
      
      function initCarInputWebSocket() 
      {
        websocketCarInput = new WebSocket(webSocketCarInputUrl);
        websocketCarInput.onopen    = function(event)
        {
          var speedButton = document.getElementById("Speed");
          sendButtonInput("Speed", speedButton.value);
        };
        websocketCarInput.onclose   = function(event){setTimeout(initCarInputWebSocket, 2000);};
        websocketCarInput.onmessage = function(event){};        
      }
      
      function sendButtonInput(key, value) 
      {
        var data = key + "," + value;
        websocketCarInput.send(data);
      }
    
      window.onload = initCarInputWebSocket;
      document.getElementById("mainTable").addEventListener("touchend", function(event){
        event.preventDefault()
      });      
    </script>
  </body>    
</html>
)HTMLHOMEPAGE";


void rotateMotor(int motorNumber, int motorDirection)
{
  if (motorDirection == FORWARD)
  {
    
    digitalWrite(motorPins[motorNumber].pinIN1, HIGH);
    digitalWrite(motorPins[motorNumber].pinIN2, LOW);    
  }
  else if (motorDirection == BACKWARD)
  {
    digitalWrite(motorPins[motorNumber].pinIN1, LOW);
    digitalWrite(motorPins[motorNumber].pinIN2, HIGH);     
  }
  else
  {
    digitalWrite(motorPins[motorNumber].pinIN1, LOW);
    digitalWrite(motorPins[motorNumber].pinIN2, LOW);       
  }
}

void moveCar(int inputValue)
{
  Serial.printf("Got value as %d\n", inputValue);  
  switch(inputValue)
  {

    case UP:
      rotateMotor(RIGHT_MOTOR, FORWARD);
      rotateMotor(LEFT_MOTOR, FORWARD);                  
      break;
  
    case DOWN:
      rotateMotor(RIGHT_MOTOR, BACKWARD);
      rotateMotor(LEFT_MOTOR, BACKWARD);  
      break;
  
    case LEFT:
      rotateMotor(RIGHT_MOTOR, FORWARD);
      rotateMotor(LEFT_MOTOR, BACKWARD);  
      break;
  
    case RIGHT:
      rotateMotor(RIGHT_MOTOR, BACKWARD);
      rotateMotor(LEFT_MOTOR, FORWARD); 
      break;
 
    case STOP:
      rotateMotor(RIGHT_MOTOR, STOP);
      rotateMotor(LEFT_MOTOR, STOP);    
      break;
  
    default:
      rotateMotor(RIGHT_MOTOR, STOP);
      rotateMotor(LEFT_MOTOR, STOP);    
      break;
  }
}

// Function to set motor speed and direction
void setMotorSpeed(int motorIndex, int speed, bool direction) {
  analogWrite(motorPins[motorIndex].pinEn, abs(speed)); // Set speed  
  
  if (direction) {
    digitalWrite(motorPins[motorIndex].pinIN1, HIGH);
    digitalWrite(motorPins[motorIndex].pinIN2, LOW);
  } else {
    digitalWrite(motorPins[motorIndex].pinIN1, LOW);
    digitalWrite(motorPins[motorIndex].pinIN2, HIGH);
  }

  //ledcWrite(PWMSpeedChannel, abs(speed));
}

bool tagDetected(int d, int x, int KP, int KD)
{
  static int mystate = 0;
  bool result;
  Serial.printf("my state: %d\n", mystate);

  switch(mystate){
      case 0:
        if (d<MIN_DISTANCE_TAG)
        {
          mystate = 1;
          moveCar(STOP);
        }
        else{
          moveTowardsTag(d, x, KP, KD);
        }
        break;

      case 1:
        result = faceTheTag(d, x, KP, KD);
        if(result)
        {
          mystate = 0;
          moveCar(STOP);
          return true;
        }
        break;

  }
  return false;

}

bool faceTheTag(int d, int x, int KP, int KD)
{
  // PID constants (tune these values based on your system)
  float Kp = 40;
  // float Ki = 0;
  float Kd = 0.01;

  // float Kp = KP / 100;
  // float Kd = KD / 100;

  // PID variables
  static float prev_error = 0;
  static float integral = 0;

  float error = (float)x/100;           // Calculate the error
  //if (x<0) error*= -1;
  integral += error;             // Calculate the integral
  float derivative = error - prev_error;  // Calculate the derivative
  

  if (abs(error) <= 2.5)
  {
    prev_error = 0;
    return true;
  }

  // Calculate the PID output
  float output = Kp * error  + Kd * derivative;

  // Control the motors based on the PID output
  int leftMotorSpeed = constrain(-output, -255, 255); // Constrain speed to -255 to 255
  int rightMotorSpeed = constrain(output, -255, 255); // Reverse for the right motor

  bool leftDirection = leftMotorSpeed >= 0; // Determine direction based on sign
  bool rightDirection = rightMotorSpeed >= 0;



  // Set motor speeds
  setMotorSpeed(0, leftMotorSpeed, leftDirection);
  setMotorSpeed(1, rightMotorSpeed, rightDirection);
  delay(100);
  moveCar(STOP);

  // Update previous error
  prev_error = error;

  return false;
}


bool moveTowardsTag(int d, int x, int KP, int KD)
{
  // PID constants (tune these values based on your system)
  //float Kp = 6.0;
  // float Ki = 0;
  // float Kd = 0.01;

  float Kp = KP / 100;
  float Kd = KD / 100;

  // PID variables
  static float prev_error = 0;
  static float integral = 0;

  //test
  float error = (float)x / 100;

  //float error = sqrt(abs(x));           // Calculate the error
  //if (x<0) error*= -1;
  integral += error;             // Calculate the integral
  float derivative = error - prev_error;  // Calculate the derivative
  
  if (abs(error) <= 2.5){
    prev_error = 0;
    Serial.printf("return true face to tag \n");
    //return true;
  }
    

  // Calculate the PID output
  float output = Kp * error  + Kd * derivative;
  //float output = 600;

  // Control the motors based on the PID output
  int leftMotorSpeed = constrain(INITIAL_SPEED-output, -255, 255); // Constrain speed to -255 to 255
  int rightMotorSpeed = constrain(INITIAL_SPEED+output, -255, 255); // Reverse for the right motor

  bool leftDirection = leftMotorSpeed >= 0; // Determine direction based on sign
  bool rightDirection = rightMotorSpeed >= 0;
  Serial.printf("speeds: left: %d, right: %d, output: %f\n", leftMotorSpeed, rightMotorSpeed, output);

  // ledcWrite(PWMSpeedChannel, 200);


  // Set motor speeds
  setMotorSpeed(0, leftMotorSpeed, leftDirection);
  setMotorSpeed(1, rightMotorSpeed, rightDirection);
  // setMotorSpeed(0, 233, true);
  // setMotorSpeed(1, 66, true);
  // delay(100);
  // moveCar(STOP);

  // Update previous error
  prev_error = error;

  return false;
}

void handleRoot(AsyncWebServerRequest *request) 
{
  request->send_P(200, "text/html", htmlHomePage);
}

void handleNotFound(AsyncWebServerRequest *request) 
{
    request->send(404, "text/plain", "File Not Found");
}

void onCarInputWebSocketEvent(AsyncWebSocket *server, 
                      AsyncWebSocketClient *client, 
                      AwsEventType type,
                      void *arg, 
                      uint8_t *data, 
                      size_t len)
{
  bool result;                  
  switch (type) 
  {
    case WS_EVT_CONNECT:
      Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
      break;
    case WS_EVT_DISCONNECT:
      Serial.printf("WebSocket client #%u disconnected\n", client->id());
      moveCar(STOP);
      break;
    case WS_EVT_DATA: 
             AwsFrameInfo *info;
             info = (AwsFrameInfo*)arg;
            //AwsFrameInfo *info = (AwsFrameInfo*)arg;
            if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
                std::string myData = "";
                myData.assign((char *)data, len);
                std::istringstream ss(myData);
                std::string key, value1, value2, value3, value4;
                std::getline(ss, key, ',');
                std::getline(ss, value1, ',');
                std::getline(ss, value2, ',');
                std::getline(ss, value3, ',');
                std::getline(ss, value4, ',');


                //Serial.printf("Key [%s] Value[%s]\n", key.c_str(), value.c_str()); 
                // int valueInt = atoi(value.c_str());
                int valueInt1 = atoi(value1.c_str());
                int valueInt2 = atoi(value2.c_str());
                int valueInt3 = atoi(value3.c_str());
                int valueInt4 = atoi(value4.c_str());

                if (key == "MoveCar" && state == 0) {
                    moveCar(valueInt1); 
                    Serial.printf("move car %d \n",valueInt1)  ;    
                }
                else if (key == "Speed" && state == 0) {
                    ledcWrite(PWMSpeedChannel, valueInt1);
                    Serial.printf("speed %d\n",valueInt1);
                }
                // New LED control logic based on WebSocket message
                else if (key == "TAG") {
                    // if (valueInt > 0) {
                    //     digitalWrite(LED_PIN, HIGH);  // Turn the LED on
                    // } else {
                    //     digitalWrite(LED_PIN, LOW);   // Turn the LED off
                    // }
                    Serial.printf("message recieved %d %d %d %d \n",valueInt1,valueInt2,valueInt3,valueInt4);
                    state = 1;
                    result = tagDetected(valueInt1,valueInt2,valueInt3,valueInt4);
                    if (result)
                    {
                      state = 0;
                      client->text("DOOOOOOOOOOOOOOOOOOOOOOOOOOOOONE");
                    }
                }
            }
            break;
    
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
    default:
      break;  
  }
}

void setUpPinModes()
{
  //Set up PWM
  ledcSetup(PWMSpeedChannel, PWMFreq, PWMResolution);
      
  for (int i = 0; i < motorPins.size(); i++)
  {
    pinMode(motorPins[i].pinEn, OUTPUT);    
    pinMode(motorPins[i].pinIN1, OUTPUT);
    pinMode(motorPins[i].pinIN2, OUTPUT);  

    /* Attach the PWM Channel to the motor enb Pin */
    ledcAttachPin(motorPins[i].pinEn, PWMSpeedChannel);
  }
  moveCar(STOP);
  pinMode(LED_PIN, OUTPUT);
}


void setup(void) 
{
  setUpPinModes();
  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.on("/", HTTP_GET, handleRoot);
  server.onNotFound(handleNotFound);
      
  wsCarInput.onEvent(onCarInputWebSocketEvent);
  server.addHandler(&wsCarInput);

  server.begin();
  Serial.println("HTTP server started");

  digitalWrite(LED_PIN, HIGH);

}

void loop() 
{
  wsCarInput.cleanupClients();
}
