# -*- coding: utf-8 -*-
# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# Copyright (c) 2021 Pawel Granat
# Changed:
# Upgraded to python3
# Upgraged to circuitpython oled driver instead of old one (deprecated)
# Added weather - current and forecast




    
# Import all board pins.
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import time
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps


# i2c = busio.I2C(board.SCL1, board.SDA1)  # QT Py RP2040 STEMMA connector
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

# Import the SSD1306 module.
import adafruit_ssd1306
from adafruit_extended_bus import ExtendedI2C as i2c

# Create the I2C interface.
# Selectable i2c bus
i2c = i2c(5)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)



# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = display.width
height = display.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('Montserrat-Light.ttf', 12)
# changed to newer
font2 = ImageFont.truetype('fa-solid-900.ttf', 14)
font_icon = ImageFont.truetype('fa-solid-900.ttf', 20)
font_text_small = ImageFont.truetype('Montserrat-Medium.ttf', 8)

start_time = time.time()
# Forecast download interval
secondsday = 86400
# Current weather download interval
secondshour = 3600



#Forecast - icons dependent on 
def forecast():
    owm = OWM('your')
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=52.185942, lon=20.990242)
    curcond = one_call.forecast_daily[0].status
    if curcond == "Snow":
      foricon=chr(62172) # OK
    elif curcond == "Thunderstorm":
      foricon=chr(61671) # OK
    elif curcond == "Drizzle":
      foricon=chr(63293) # OK
    elif curcond == "Rain":
      foricon=chr(63293) # OK
    elif curcond == "Mist":
      foricon=chr(63327)   # OK
    elif curcond == "Smoke":
      foricon=chr(63327)  # OK
    elif curcond == "Haze":
      foricon=chr(63327)  # OK
    elif curcond == "Dust":
      foricon=chr(63327) # OK
    elif curcond == "Fog":
      foricon=chr(63327)   #OK
    elif curcond == "Sand":
     foricon=chr(63327) #OK
    elif curcond == "Dust":
      foricon=chr(63327) # OK
    elif curcond == "Ash": 
      foricon=chr(63327) # OK
    elif curcond == "Squall":
      foricon=chr(63278) # OK
    elif curcond == "Tornado":
      foricon=chr(63278) # OK
    elif curcond == "Clear":
      foricon=chr(61829)
    elif curcond == "Clouds":
      foricon=chr(61634)
    else:
      foricon=chr(61953)
      
    fortmp = one_call.forecast_daily[0].temperature('celsius').get('day', None) 
    fortmp = str(fortmp)+" C"
    return fortmp,foricon

#Current weather
def current_weather():
    owm = OWM('yourapikey')
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=52.185942, lon=20.990242)
    outtmp=one_call.current.temperature('celsius').get('temp', None)
    outtmp=str(outtmp)+" C"
    outhum=one_call.current.humidity
    outhum=str(outhum)+" %"
    return outtmp, outhum

fortmp,foricon = forecast()
outtmp, outhum = current_weather()

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    #Download forecast data once per day
    if elapsed_time > secondsday:
        fortmp,foricon = forecast()
    #Download current temp once per hour
    if elapsed_time > secondshour:
        outtmp, outhum = current_weather()
        
        
        
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -3"
    Temperature = subprocess.check_output(cmd, shell = True )
    Temperature = Temperature.decode('utf-8')
    Temperature=str(Temperature)+" C"
    
    # Icons
    # Icon temperature -> 1 column up -> Current temperature
    draw.text((x, top+5),    chr(62152),  font=font_icon, fill=255)
    
    # Icon dependent on forecast -> 2 column up -> Weather forecast
    draw.text((x+60, top+5), foricon,  font=font_icon, fill=255)
    
    # Icon droplet -> 1 column down -> Current humidity
    draw.text((x, top+30), chr(62657),  font=font2, fill=255)
    
    # Icon Computer -> 2 column down -> Temp CPU 
    draw.text((x+60, top+30), chr(63231),  font=font2, fill=255)
    
    # Icon Wifi -> Sam dol
    #draw.text((x, top+52), chr(61931),  font=font2, fill=255)
       
  # Text temperature 
    draw.text((x+15, top+5), outtmp,  font=font, fill=255)
  # Text forecsat
    draw.text((x+80, top+5),    fortmp,  font=font, fill=255)
  # Text humidity
    draw.text((x+20, top+30),   outhum,  font=font, fill=255)
  # Text cpu usage  
    draw.text((x+80, top+30),      Temperature, font=font, fill=255)
  
   # Text IP addresss  
    #draw.text((x+20, top+55),      str(IP),  font=font_text_small, fill=255)
    
   # Display image.

    display.image(image)
    display.show()
    time.sleep(5)
