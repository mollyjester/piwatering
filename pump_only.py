# coding=UTF8
# TONGLING JQC-3FF-S-Z Relay (5V, 5ma triggering. commutating 10A/250VAC, 15A/125VAC)

import configparser
import datetime
import pigpio
from time import sleep

TIMESTAMP_FORMAT = '%d.%m.%Y'

CONFIG_SECTION_WATERING = 'watering'
CONFIG_OPTION_DURATION = 'duration'
CONFIG_OPTION_INTERVAL = 'interval'
CONFIG_OPTION_LAST = 'last'

CONFIG_SECTION_RELAY = 'relay'
CONFIG_OPTION_PIN = 'pin'

def watering(pi, duration, gpio_pwr):
    if gpio_pwr and duration:
        pi.set_mode(gpio_pwr, pigpio.OUTPUT)
        pi.write(gpio_pwr, 0) # trigger switches on low level
        sleep(duration)
        pi.set_mode(gpio_pwr, pigpio.INPUT)

config = configparser.ConfigParser()

with open('/home/pi/python/watering/config.cfg') as cfgfile:
    config.read_file(cfgfile)

WATERING_INTERVAL = config.getint(CONFIG_SECTION_WATERING, CONFIG_OPTION_INTERVAL)
WATERING_DURATION = config.getint(CONFIG_SECTION_WATERING, CONFIG_OPTION_DURATION)
WATERING_LAST = datetime.datetime.strptime(config.get(CONFIG_SECTION_WATERING, CONFIG_OPTION_LAST), TIMESTAMP_FORMAT)
RELAY_PIN = config.getint(CONFIG_SECTION_RELAY, CONFIG_OPTION_PIN)

pi = pigpio.pi()

if pi.connected:
    try:
        delta = datetime.datetime.today() - WATERING_LAST

        if delta.days >= WATERING_INTERVAL:
            watering(pi, WATERING_DURATION, RELAY_PIN)
            config.set(CONFIG_SECTION_WATERING, CONFIG_OPTION_LAST, datetime.datetime.today().strftime(TIMESTAMP_FORMAT))
        else:
            print('Дней с полива: ' + str(delta.days) + '. Должно быть: ' + str(WATERING_INTERVAL))
    finally:
        #уходя, гасите свет
        pi.set_mode(RELAY_PIN, pigpio.INPUT)
        
        with open('/home/pi/python/watering/config.cfg', 'w') as cfgfile:
            config.write(cfgfile)
