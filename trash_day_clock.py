from adafruit_ht16k33.segments import Seg7x4
from datetime import datetime
from datetime import timedelta
import board
import holidays
import RPi.GPIO as GPIO
import time

us_holidays = holidays.US()
trash_holidays = [ # only holidays that affect trash pickup
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
known_recycle_date = datetime(2022, 2, 24, 0, 0, 0)
i2c = board.I2C()
display = Seg7x4(i2c)
BLUE_LED = 17
GREEN_LED = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

def is_holiday(date):
    return bool(set(trash_holidays) & set(us_holidays.get_list(date)))

def is_recycle_week(date):
    return ((date - known_recycle_date).days / 7) % 2 < 1

def leds_on(is_recycle_week):
    GPIO.output(BLUE_LED, True)
    if is_recycle_week:
        GPIO.output(GREEN_LED, True)

def process_leds(now):
    weekday = now.weekday() # Thu or Fri are only trash days
    if weekday == 3: # Thu
        if not is_holiday(now):
            leds_on(is_recycle_week(now))
            return
    elif weekday == 4: # Fri
        previous_day = now + timedelta(days = - 1)
        if is_holiday(previous_day):
            leds_on(is_recycle_week(previous_day))
            return
    GPIO.output(BLUE_LED, False)
    GPIO.output(GREEN_LED, False)

def update_time(now):
    display.colon = now.second % 2 # colon on even seconds
    display.print(now.strftime("%H%M"))

while(True):
    now = datetime.now()
    process_leds(now)
    update_time(now)
    time.sleep(1)
