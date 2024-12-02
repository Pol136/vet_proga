# тензодатчик
import RPi.GPIO as GPIO
import time

# Настройка GPIO
GPIO.setmode(GPIO.BCM)

# Определение пинов для первого АЦП
ADC1_CLK_PIN = 9  # IO CLOCK
ADC1_DATA_PIN = 12  # DATA OUT
ADC1_CS_PIN = 23  # CS

# Определение пинов для второго АЦП
ADC2_CLK_PIN = 10  # IO CLOCK
ADC2_DATA_PIN = 16  # DATA OUT
ADC2_CS_PIN = 18  # CS

# Настройка пинов первого АЦП
GPIO.setup(ADC1_CLK_PIN, GPIO.OUT)
GPIO.setup(ADC1_DATA_PIN, GPIO.IN)
GPIO.setup(ADC1_CS_PIN, GPIO.OUT)

# Настройка пинов второго АЦП
GPIO.setup(ADC2_CLK_PIN, GPIO.OUT)
GPIO.setup(ADC2_DATA_PIN, GPIO.IN)
GPIO.setup(ADC2_CS_PIN, GPIO.OUT)


def read_adc(clk_pin, data_pin, cs_pin):
    """
    Считывает 8-битное значение с АЦП TLC549IP.

    :param clk_pin: GPIO номер для IO CLOCK
    :param data_pin: GPIO номер для DATA OUT
    :param cs_pin: GPIO номер для CS
    :return: Значение АЦП (0-255)
    """
    # Активируем чип (CS = LOW)
    GPIO.output(cs_pin, GPIO.LOW)
    time.sleep(0.001)  # Небольшая задержка для стабильности

    result = 0
    for i in range(8):
        # Генерируем положительный фронт CLOCK
        GPIO.output(clk_pin, GPIO.HIGH)
        time.sleep(0.001)  # Задержка для стабилизации сигнала

        # Читаем бит данных
        bit = GPIO.input(data_pin)
        result = (result << 1) | bit

        # Генерируем отрицательный фронт CLOCK
        GPIO.output(clk_pin, GPIO.LOW)
        time.sleep(0.001)  # Задержка между битами

    # Деактивируем чип (CS = HIGH)
    GPIO.output(cs_pin, GPIO.HIGH)
    return result


def adc_to_voltage(adc_value, vcc=3.3):
    """
    Преобразует значение АЦП в напряжение.

    :param adc_value: Значение АЦП (0-255)
    :param vcc: Напряжение питания АЦП (по умолчанию 3.3V)
    :return: Напряжение в Вольтах
    """
    return (adc_value / 255.0) * vcc


def get_load_cell(metrics):
    # значение, записываемое в словарь при ошибке выполнения
    error_value = -1

    try:
        print("Начинаем чтение данных с двух тензодатчиков...")

        # Чтение с первого АЦП
        adc1_value = read_adc(ADC1_CLK_PIN, ADC1_DATA_PIN, ADC1_CS_PIN)
        voltage1 = adc_to_voltage(adc1_value)

        # Чтение со второго АЦП
        adc2_value = read_adc(ADC2_CLK_PIN, ADC2_DATA_PIN, ADC2_CS_PIN)
        voltage2 = adc_to_voltage(adc2_value)

        # print(f"Тензодатчик 1 - ADC: {adc1_value}, Напряжение: {voltage1:.2f} В")
        # print(f"Тензодатчик 2 - ADC: {adc2_value}, Напряжение: {voltage2:.2f} В")
        # print("-" * 40)

        metrics['value1_load_cell'] = adc1_value
        metrics['value2_load_cell'] = adc2_value
        metrics['voltage1_load_cell'] = voltage1
        metrics['voltage2_load_cell'] = voltage2

        time.sleep(0.5)  # Пауза между измерениями

    except KeyboardInterrupt:
        metrics['value1_load_cell'] = error_value
        metrics['value2_load_cell'] = error_value
        metrics['voltage1_load_cell'] = error_value
        metrics['voltage2_load_cell'] = error_value
        print("\nОстановка программы пользователем.")
    except Exception as e:
        metrics['value1_load_cell'] = error_value
        metrics['value2_load_cell'] = error_value
        metrics['voltage1_load_cell'] = error_value
        metrics['voltage2_load_cell'] = error_value
        print(f"Произошла ошибка: {e}")
    finally:
        GPIO.cleanup()
        # print("GPIO очищены. Программа завершена.")
