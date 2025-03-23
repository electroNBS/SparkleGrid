import time
import ADS1256
import RPi.GPIO as GPIO
import psycopg2
from psycopg2 import OperationalError
import numpy as np
import datetime
import threading

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

    # Calculate delta time
    delta_time = np.diff(voltage_array[:, 1]) / 1000.0  # Assuming time is in milliseconds

    # Calculate RMS value for the voltage array
    rms_value = calculate_rms(voltage_array[:, 0])

    # Prepare the voltage array for insertion
    timestamp = start_time.isoformat()
    query = """
    INSERT INTO microgrid_back_measurementssix(id, sensor_id, sensdata, time, rmsvalue, sname, stype, thd, pf)
    VALUES (%s, %s, %s::numeric[], %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (curr_id, sensor_id, voltage_array.tolist(), timestamp, rms_value, sname, stype, 0, 0))
    connection.commit()
    cursor.close()

def read_ads1256_data(ADC, buffer, buffer_lock):
    while True:
        ADC_Value = ADC.ADS1256_GetChannalValue(7)
        sensor_value = ADC_Value * 5.0 / 0x7fffff
        with buffer_lock:
            buffer[0] = sensor_value  # Update the latest value in the buffer

def main():
    connection = create_connection("localhost", "postgres", "microgrid", "sensors")

    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
    ADC.ADS1256_ConfigADC(ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256.ADS1256_DRATE_E['ADS1256_2000SPS'])

    buffer = [0.0]  # Buffer to store the latest sensor value
    buffer_lock = threading.Lock()
    voltage_buffer = np.zeros((1000, 2))  # Buffer to store 1000 values for one second

    adc_thread = threading.Thread(target=read_ads1256_data, args=(ADC, buffer, buffer_lock))
    adc_thread.daemon = True
    adc_thread.start()

    max_id = get_max_id(connection) + 1
    sensor_id = 1
    sname = "Voltage Sensor"
    stype = "Voltage"

    start_time = time.perf_counter()
    try:
        while True:
            current_time = time.perf_counter_ns()
            elapsed_time = current_time - start_time
           

            if elapsed_time >= 1000000:  # Every 1 second
                start_time = current_time
                timestamp = datetime.datetime.now(datetime.timezone.utc)
                for i in range(1000):
                    with buffer_lock:
                        latest_value = buffer[0]
                    voltage_buffer[i] = [latest_value, i]  # Store both value and time
                    
                    
                    
                
                insert_voltage_array(max_id, connection, voltage_buffer, timestamp, sensor_id, sname, stype)
                print(f"Inserted a batch of 1000 values into the database at t={timestamp}")
                max_id += 1

            # Sleep very briefly to yield to other threads
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("Exiting...")
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    main()
