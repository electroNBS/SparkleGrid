import time
import ADS1256
import RPi.GPIO as GPIO
import psycopg2
from psycopg2 import OperationalError
import numpy as np
import datetime

# Function to create a database connection
def create_connection(host_name, user_name, password, db_name):
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=user_name,
            password=password,
            host=host_name,
            port="5432"
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to get the max id from the table
def get_max_id(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM microgrid_back_measurementssix;")
    max_id = cursor.fetchone()[0]
    cursor.close()
    return max_id if max_id else 0

# Function to calculate RMS value
def calculate_rms(data_array):
    return np.sqrt(np.mean(np.square(data_array)))

def insert_voltage_array(curr_id, connection, voltage_array, start_time, sensor_id, sname, stype):
    cursor = connection.cursor()

    # Calculate RMS value for the voltage array
    rms_value = calculate_rms(voltage_array[:, 0])  # Assuming the voltage is in the first column

    # Prepare the voltage array for insertion
    voltage_list = voltage_array.tolist()
    timestamp = start_time.isoformat()
    query = """
    INSERT INTO microgrid_back_measurementssix(id, sensor_id, sensdata, time, rmsvalue, sname, stype, thd, pf)
    VALUES (%s, %s, %s::numeric[], %s, %s, %s, %s, %s, %s);
    """
    voltage_array_str = str(voltage_list).replace('[', '{').replace(']', '}')
    cursor.execute(query, (curr_id, sensor_id, voltage_array_str, timestamp, rms_value, sname, stype, 0, 0))
    connection.commit()
    cursor.close()

# Function to read data from the ADS1256
def read_ads1256_data(ADC, num_samples):
    voltage_values = []
    for i in range(num_samples):
        ADC_Value = ADC.ADS1256_GetChannalValue(7)
        sensor_value = ADC_Value * 5.0 / 0x7fffff  # Assuming reading from channel 7
        delta_time = i  # Delta time is the index of the sample
        voltage_values.append([sensor_value, delta_time])  # Add the voltage value with delta time
    return np.array(voltage_values)
# Replace with your actual database credentials
connection = create_connection("localhost", "postgres", "microgrid", "sensors")

# Initialize the ADS1256 ADC
ADC = ADS1256.ADS1256()
ADC.ADS1256_init()

try:
    while True:
        max_id = get_max_id(connection) + 1
        voltage_array = read_ads1256_data(ADC, num_samples=1000)  # Read 1000 samples
        start_time = datetime.datetime.now(datetime.timezone.utc)
        sensor_id = 1  # Assuming the sensor ID is 1
        sname = "Voltage Sensor"
        stype = "Voltage"
        insert_voltage_array(max_id, connection, voltage_array, start_time, sensor_id, sname, stype)
        max_id += 1
        print(f"Inserted a batch of 1000 values into the database at t={start_time}")
        time.sleep(1)  # Wait for 1 second before the next batch
except KeyboardInterrupt:
    print("Exiting...")
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")
