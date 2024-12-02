#  датчик пульса
import spidev
import time

# Настройка SPI
SPI_BUS = 0  # SPI шина
SPI_DEVICE = 0  # SPI устройство (по умолчанию 0)
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1350000  # Скорость SPI


def read_adc(channel):
    """
    Считывает данные с указанного канала MCP3008.

    :param channel: Номер канала (0-7)
    :return: 10-битное значение (0-1023)
    """
    if channel < 0 or channel > 7:
        raise ValueError("Номер канала должен быть в диапазоне 0-7.")

    # Команда для чтения: [Start Bit, SGL/DIFF, D2, D1, D0]
    cmd = [1, (8 + channel) << 4, 0]
    adc_response = spi.xfer2(cmd)  # Передаём команду и получаем ответ
    adc_value = ((adc_response[1] & 3) << 8) + adc_response[2]  # Собираем 10-битное значение
    return adc_value


def adc_to_voltage(adc_value, vref=3.3):
    """
    Преобразует значение АЦП в напряжение.

    :param adc_value: Значение АЦП (0-1023)
    :param vref: Референсное напряжение (по умолчанию 3.3V)
    :return: Напряжение в Вольтах
    """
    return (adc_value / 1023.0) * vref


def get_pulse(metrics):
    # значение, записываемое в словарь при ошибке выполнения
    error_value = -1

    try:
        # print("Считывание данных с датчика пульса...")
        # Считываем данные с канала 0 (CH0)
        adc_value = read_adc(0)
        voltage = adc_to_voltage(adc_value)

        # print(f"ADC значение: {adc_value}, Напряжение: {voltage:.2f} В")
        metrics['value_pulse'] = adc_value
        metrics['voltage_pulse'] = voltage

        time.sleep(0.1)  # Задержка между измерениями
    except KeyboardInterrupt:
        metrics['value_pulse'] = error_value
        metrics['voltage_pulse'] = error_value
        print("\nОстановка программы.")
    except Exception as e:
        metrics['value_pulse'] = error_value
        metrics['voltage_pulse'] = error_value
        print(f"Ошибка при чтении датчик пульса: {e}")
    finally:
        spi.close()
        # print("SPI соединение закрыто.")
