# темпа
from w1thermsensor import W1ThermSensor
import time

sensor = W1ThermSensor()


def read_temperature(metrics):
    # значение, записываемое в словарь при ошибке выполнения
    error_value = -1

    try:
        # Считываем температуру
        temperature = sensor.get_temperature()  # По умолчанию в градусах Цельсия
        # print(f"Температура: {temperature:.2f} °C")
        metrics['temperature'] = temperature
        time.sleep(1)  # Пауза между считываниями (1 секунда)
    except KeyboardInterrupt:
        metrics['temperature'] = error_value
        print("\nОстановка программы.")
    except Exception as e:
        metrics['temperature'] = error_value
        print(f"Ошибка при чтении температуры: {e}")
