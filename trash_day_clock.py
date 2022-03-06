from adafruit_ht16k33.segments import Seg7x4
from datetime import datetime
from datetime import timedelta
import board
import holidays
import RPi.GPIO as GPIO
import sys
import time

us_holidays = holidays.US()
trash_holidays = [ # these are the only holidays that affect trash pickup
    'New Year\'s Day',
    'New Year\'s Day (Observed)',
    'Memorial Day',
    'Independence Day',
    'Independence Day (Observed)',
    'Labor Day',
    'Thanksgiving',
    'Christmas Day',
    'Christmas Day (Observed)'
]

i2c = board.I2C()
display = Seg7x4(i2c)
BLUE_LED = 17
GREEN_LED = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

def is_holiday(date):
    return bool(set(trash_holidays) & set(us_holidays.get_list(date)))

def is_recycle_week(now):
    known_recycle_date = datetime(2022,2,24,0,0,0)
    return ((now - known_recycle_date).days / 7) % 2 < 1

def leds_on(is_recycle_week):
    GPIO.output(BLUE_LED, True)
    if is_recycle_week:
        GPIO.output(GREEN_LED, True)

def process_leds(now):
    GPIO.output(BLUE_LED, False)
    GPIO.output(GREEN_LED, False)
    weekday = now.weekday() # trash only picked up on Thu or Fri
    if weekday == 3: # Thu
        if not is_holiday(now):
            leds_on(is_recycle_week(now))
    elif weekday == 4: # Fri
        if is_holiday(now + timedelta(days = - 1)):
            leds_on(is_recycle_week(now - 1))

def update_time(now):
    display.colon = now.second % 2 # blink colon on even seconds
    display.print(now.strftime("%H%M"))

print('Press Ctrl-C to quit.')

try:
    while(True):
        now = datetime.now()
        process_leds(now)
        update_time(now)
        time.sleep(1)
except KeyboardInterrupt:
    print() # prevents errors in the console when stopping with ctrl-c
finally:
    GPIO.cleanup()
    sys.exit(0)
