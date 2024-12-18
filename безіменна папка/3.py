import time
import random
from functools import wraps
import logging


logging.basicConfig(
    filename="sensor_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Генератори сенсорів
def temperature_sensor():
    while True:
        yield random.uniform(-10, 40)  # Температура в градусах Цельсія
        time.sleep(1)

def pressure_sensor():
    while True:
        yield random.uniform(950, 1050)  # Тиск в гПа
        time.sleep(1)

def humidity_sensor():
    while True:
        yield random.uniform(20, 100)  # Вологість у відсотках
        time.sleep(1)


class SensorSystem:
    def __init__(self):
        self.handlers = {}

    def sensor_handler(self, sensor_type):
        def decorator(func):
            self.handlers[sensor_type] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def process_data(self, sensor_type, data):
        if sensor_type in self.handlers:
            self.handlers[sensor_type](data)
        else:
            logging.info(f"No handler for sensor type: {sensor_type}, data: {data}")

system = SensorSystem()



@system.sensor_handler("temperature")
def handle_temperature(data):
    logging.info(f"Temperature: {data:.2f} °C")
    if data > 35:
        logging.warning("High temperature alert!")

@system.sensor_handler("pressure")
def handle_pressure(data):
    logging.info(f"Pressure: {data:.2f} hPa")
    if data < 960:
        logging.warning("Low pressure alert!")

@system.sensor_handler("humidity")
def handle_humidity(data):
    logging.info(f"Humidity: {data:.2f}%")
    if data > 90:
        logging.warning("High humidity alert!")



if __name__ == "__main__":
    sensors = {
        "temperature": temperature_sensor(),
        "pressure": pressure_sensor(),
        "humidity": humidity_sensor(),
    }
    
    try:
        while True:
            for sensor_type, sensor_gen in sensors.items():
                data = next(sensor_gen)
                system.process_data(sensor_type, data)
    except KeyboardInterrupt:
        print("Зупинено користувачем.")