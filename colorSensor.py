import time
import board
import busio
import adafruit_tcs34725
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 100

def DetectControlPanelColor():
    colors = sensor.color_rgb_bytes
    r = np.floor(colors[0]/20)
    g = np.floor(colors[1]/20)
    b = np.floor(colors[2]/20)
    if ( r > 0 and g == 0 and b == 0):
        return [1, 0, 0, 0]
    if (r == 0 and g > 0 and b == 0):
        return [0, 1, 0, 0]
    if (r == 0 and g >= 0 and b > 0):
        return [0, 0, 1, 0]
    if (r > 0 and g > 0 and b == 0):
        return [0, 0, 0, 1]
    return [0, 0, 0, 0]

def DetectionToColorName(det):
    if (det[0]): return "Red"
    elif (det[1]): return "Green"
    elif (det[2]): return "Cyan"
    elif (det[3]): return "Yellow"
    else: return "No Color Detected"
    
while True:
    colordet = DetectControlPanelColor()
    print(DetectionToColorName(colordet))
