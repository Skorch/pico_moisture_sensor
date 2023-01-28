import main_sensor
from machine import Pin

debug_pin = Pin(18, Pin.IN)

print("running program")
main_sensor.run()
