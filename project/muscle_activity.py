#датчик мышечной активности
import RPi.GPIO as GPIO
import time

# Настройка GPIO
CLK_PIN = 11  # IO CLOCK
DATA_PIN = 13  # DATA OUT
CS_PIN = 24  # CS

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.OUT)
GPIO.setup(DATA_PIN, GPIO.IN)
GPIO.setup(CS_PIN, GPIO.OUT)

def read_adc():
    """
    Считывает данные с TLC549IP.
    Возвращает 8-битное значение (0-255).
    """
    GPIO.output(CS_PIN, GPIO.LOW)  # Активируем чип (CS = 0)
    time.sleep(0.001)  # Небольшая задержка для стабильности

    result = 0
    for i in range(8):  # 8-битное чтение
        GPIO.output(CLK_PIN, GPIO.HIGH)  # Поднимаем CLK
        time.sleep(0.001)  # Задержка для формирования сигнала
        GPIO.output(CLK_PIN, GPIO.LOW)  # Опускаем CLK

        # Считываем бит с DATA_PIN
        bit = GPIO.input(DATA_PIN)
        result = (result << 1) | bit  # Сдвигаем результат влево и добавляем новый бит

    GPIO.output(CS_PIN, GPIO.HIGH)  # Деактивируем чип (CS = 1)
    return result


def get_muscle_activity(metrics):
    # значение, записываемое в словарь при ошибке выполнения
    error_value = -1

    try:
        # print("Начинаем чтение данных с датчика EMG...")
        value = read_adc()
        voltage = (value / 255.0) * 3.3  # Преобразование в напряжение (если VCC = 3.3V)
        # print(f"ADC значение: {value}, Напряжение: {voltage:.2f} В")
        metrics['value_muscle_activity'] = value
        metrics['voltage_muscle_activity'] = voltage
        time.sleep(0.1)  # Пауза между измерениями
    except KeyboardInterrupt:
        metrics['value_muscle_activity'] = error_value
        metrics['voltage_muscle_activity'] = error_value
        print("\nОстановка программы.")
    except Exception as e:
        metrics['value_muscle_activity'] = error_value
        metrics['voltage_muscle_activity'] = error_value
        print(f"Ошибка при чтении мышечной активности: {e}")
    finally:
        GPIO.cleanup()