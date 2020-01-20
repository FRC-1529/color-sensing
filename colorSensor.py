import time
import board
import busio
import adafruit_tcs34725
import numpy as np



i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 50

global latch_counter
latch_counter = 0
latch = 0

global color_detected
color_detected = 0 # red=1, yel=2, grn=3, blu=4
global last_color_detected
last_color_detected = 0

red = np.array([170, 100, 85], dtype=np.uint16)
grn = np.array([95, 170, 120], dtype=np.uint16)
blu = np.array([100, 200, 220], dtype=np.uint16)
yel = np.array([270, 280, 145], dtype=np.uint16)

def Count():
    global latch_counter
    global last_color_detected
    # asks if it saw this color before, if so, then it increments the counter, if not, then it resets it
    if last_color_detected == color_detected:
        latch_counter += 1
    else:
        latch_counter = 0
    #assigns current color to last color for future loops
    last_color_detected = color_detected

def Detect():
    global color_detected
    detected_list = ('r', 'g', 'b', 'c')
    x = list(detected_list)
   
    x[0] = sensor.color_raw[0]
    x[1] = sensor.color_raw[1]
    x[2] = sensor.color_raw[2]
    x[3] = sensor.color_raw[3]
    #print('r:{0}, g:{1}, b:{2}, c:{3}'.format(x[0], x[1], x[2], x[3]))
    
    
    if x[0] > (yel[0] -  20) and x[0] < (yel[0] + 20) and x[1] > (yel[1] - 20) and x[1] < (yel[1] + 20) and x[2] > (yel[2] - 20) and x[2] < (yel[2] + 20):
        color_detected = 2

    elif x[0] > (red[0] - 20) and x[0] < (red[0] + 20) and x[1] > (red[1] - 20) and x[1] < (red[1] + 20) and x[2] > (red[2] - 20) and x[2] < (red[2] + 20):
        color_detected = 1
        
    elif x[0] > (grn[0] - 20) and x[0] < (grn[0] + 20) and x[1] > (grn[1] - 20) and x[1] < (grn[1] + 20) and x[2] > (grn[2] - 20) and x[2] < (grn[2] + 20):
        color_detected = 3
        
    elif (x[0] > (blu[0] - 20)) and (x[0] < (blu[0] + 20)) and (x[1] > (blu[1] - 20)) and (x[1] < (blu[1] + 20)) and (x[2] > (blu[2] - 20)) and (x[2] < (blu[2] + 20)):
        color_detected = 4


    

while True:
    Detect()
    Count()
    
    if latch_counter == 3:
        if color_detected == 1:
            print('I see RED')
        elif color_detected == 3:
            print('I see GREEN')
        elif color_detected == 4:
            print('I see BLUE')
        elif color_detected == 2:
            print('I see YELLOW')