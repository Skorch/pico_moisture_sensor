from machine import Pin
import mqtt_client
import moisture
import wifi
from lib.datetime import datetime, timezone, timedelta
import time
import machine
import moisture_led

print(dir(moisture_led))



SENSOR_TYPE = "moisture"
DEBUG = False
SLEEP_SECONDS = 5 if DEBUG else 60

deep_sleep = True

wlan_client = None

dip_pins = [
    Pin(19, Pin.IN),
    Pin(20, Pin.IN),
    Pin(21, Pin.IN)
    
]

done_pin_number = 13

led_pin_number = 0


np = moisture_led.setup_led(led_pin_number)
done_pin = Pin(done_pin_number, Pin.OUT)


def dip_value():
    
    dip_values = list(map(lambda p: str(p.value()), dip_pins))
    return int("".join(dip_values), 2)

def event_template(sensor_type, sensor_id, system_id, sensor_ts, metric_name, metric_value): 
    return {
        "sensor_id": sensor_id,
        "sensor_type": sensor_type, 
        "system_id": system_id,
        "metric_name": metric_name,
        "metric_value": metric_value,
        "timestamp": sensor_ts
    }


def create_message(channel, percent_moist):
    
    tz1 = timezone(timedelta(hours=-8))
    
    sensor_id = dip_value()
    
    system_id = f"pico_moisture_{sensor_id:03}"
    
    return event_template(SENSOR_TYPE, f"{SENSOR_TYPE}_{channel}", system_id, datetime.now(tz1).isoformat(' '), "humidity", percent_moist)



def setup():
    global wlan_client, mqtt
    
    if not wlan_client or not wlan_client.active():
        ssid, pwd = wifi.get_ssid()
        
        wlan_client = wifi.connect(ssid, pwd)
        mqtt = mqtt_client.setup()


debug_pin_number = 18
debug_pin = Pin(debug_pin_number, Pin.IN)

moisture_channel = 0

def run(debug = False):
    
    x = 0
    done_pin.value(0)
    try:
        
        
        while not debug or x<3:
            
            
            if debug_pin.value():
                print("Debug Pin")
                
                print("signalling lowpower chip to sleep")
                done_pin.value(1)
                
                break


            # get moisture level and turn on LED
            channel, avg_sensor_value, percent_moist = moisture.get_data(moisture_channel)
            if percent_moist >= 40:
                moisture_led.on_good()
            elif percent_moist >= 20:
                moisture_led.on_water_soon()
            else:
                moisture_led.on_water_now()

            
            try:
                setup()
                
                message = create_message(channel, percent_moist)
                
                print(message)
                    
                    
                mqtt_client.send_message(mqtt_client.mqtt_client, mqtt_client.MQTT_TOPIC, message)

                moisture_led.off(led_pin_number)
                
                if deep_sleep:

                    print("signalling lowpower chip to sleep")
                    done_pin.value(1)

                else:
                    print(f"time.sleep for {SLEEP_SECONDS} seconds")                
                    time.sleep(SLEEP_SECONDS)
                
                x+=1
            
            except Exception as ex:
                print(ex)
                moisture_led.blink_error()
                time.sleep(10)
                continue

    except KeyboardInterrupt:
        print("shutting down")
    
    

# setup()
# run()

if __name__ == "__main__":
    run(True)
    print("done")