#!/usr/bin/python
import scd30
import socket
import time
from statistics import mean
import os

address = os.environ['MINITSDB_IP']
port = int(os.environ['MINITSDB_PORT'])
sensor_path = '/dev/ttyscd30'

sensor = scd30.SCD30(sensor_path)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interval = 2
# number of averages for boxcar
N = 4

co2_list = [0] * N
temp_list = [0] * N
hum_list = [0] * N

i = 0
buffer_full = False

if (intv_is := sensor.measurement_interval) != interval:
    print(f'measurement interval was {intv_is}s, setting to {interval}')
    sensor.measurement_interval = interval

while True:
    while not sensor.get_ready():
        time.sleep(0.5)
    co2, temp, hum = sensor.read()
    co2_list[i] = co2
    temp_list[i] = temp
    hum_list[i] = hum
    i += 1
    if i == N:
        i = 0
        buffer_full = True
    if buffer_full:
        packet = 'name:sensor loc:m_hadiko|'
        packet += f'name:co2 {mean(co2_list):0.0f}|'
        packet += f'name:temperature {mean(temp_list):0.2f}|'
        packet += f'name:humidity {mean(hum_list):0.2f}|'
        packet += f'{int(time.time())}'
        packet = packet.encode()
        try:
            sock.sendto(packet, (address, port))
        except:
            pass
