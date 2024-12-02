import time
import socket
import json
from threading import Thread

from temperature import read_temperature
from muscle_activity import get_muscle_activity
from pulse import get_pulse
from load_cell import get_load_cell


def send_data(data, host, port):
    """
    Отправляет данные через сокет
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            data_json = json.dumps(data)  # Сериализация в JSON
            data_bytes = data_json.encode('utf-8')  # Кодирование в байты
            s.sendall(data_bytes)
    except Exception as e:
        print(f"Ошибка отправки данных: {e}")


if __name__ == '__main__':
    while True:
        results = {}

        temp = Thread(target=read_temperature, args=(results,))
        musc = Thread(target=get_muscle_activity, args=(results,))
        pulse = Thread(target=get_pulse, args=(results,))
        load_cell = Thread(target=get_load_cell, args=(results,))

        temp.start()
        musc.start()
        pulse.start()
        load_cell.start()

        temp.join()
        musc.join()
        pulse.join()
        load_cell.join()

        print(results)

        # host =
        # port = 
        # send_data(results, host, port)
