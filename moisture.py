
from time import sleep
import machine

# import lcd

callibration = {
    0:(24487, 42338),
    1:(21434, 42735)
}
samplerate = 200

sensors = {
    0: machine.ADC(26),
    1: machine.ADC(27)
}


def Average(lst):
    return sum(lst) / len(lst)

def get_reading(channel):
    samples = []
    sensor = sensors[channel]
    print(f"getting channel {channel} {sensor}")
    for _ in range(samplerate):
        sensor_value = sensor.read_u16()
        samples.append(sensor_value)
        
    avg_sensor_value = Average(samples) 
    cal_min = callibration[channel][0]
    cal_max = callibration[channel][1]
    percent_moist = int(100*max(min((cal_max - avg_sensor_value) / (cal_max - cal_min), 1.0), 0.0))
    
    return (channel, avg_sensor_value, percent_moist)
            

    
def get_data(channel):

    return get_reading(channel)

if __name__ == "__main__":

    try:

        while True:
            text_line_1 = ""
            text_line_2 = ""
            for channel, sensor_value, percent_moist in get_data():
                print(f"channel {channel}: {percent_moist}% {sensor_value}")        
                
                text_line_1 += f"{'C'+str(channel+1):3} "
                text_line_2 += f"{str(percent_moist) + '%':3} "
                
                sleep(1)

            # lcd.write(f"{text_line_1}\n{text_line_2}")


    except KeyboardInterrupt:
        machine.reset()

