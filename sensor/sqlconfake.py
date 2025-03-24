
import psycopg2
from psycopg2 import OperationalError
import numpy as np
import time
import random
import datetime

# Constants for the sine wave
AMPLITUDE = 240
NOISE_LEVEL = 100
SAMPLES = 1000

# Variable to specify sensor_id
sensor_id = 6  # Replace with the desired sensor ID

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
    # Updated table name to 'measurements_one' as defined in GridSense models
    cursor.execute("SELECT MAX(id) FROM measurements_six;")
    max_id = cursor.fetchone()[0]
    cursor.close()
    return max_id if max_id else 0

# Function to calculate RMS value
def calculate_rms(data_array):
    return np.sqrt(np.mean(np.square(data_array)))

# Function to insert a new record into the measurements table
def insert_voltage_array(curr_id, connection, voltage_array, start_time):
    cursor = connection.cursor()

    # Calculate RMS value for the voltage array
    rms_value = calculate_rms(voltage_array[:, 0])  # Assuming the voltage is in the first column
    print(rms_value)

    # **Explicitly convert rms_value to a Python float**
    rms_value_float = float(rms_value)


    # Prepare the voltage array for insertion
    voltage_list = voltage_array.tolist()
    timestamp = start_time.isoformat()

    query = """
    INSERT INTO measurements_six(id, sensor_id, sensdata, time, rmsvalue, sname, stype, thd, pf)
    VALUES (%s, %s, %s::numeric[], %s, %s, %s, %s, %s, %s);
    """
    print("parameterized query being used")
    print(query)


    cursor.execute(query, (
        curr_id,
        sensor_id,
        voltage_list, # Pass the Python list directly, psycopg2 will handle conversion for parameterized queries
        timestamp,
        rms_value_float, # Use the explicitly converted Python float here
        'Voltage', # Corrected typo and using single quotes as string literals in SQL
        'Voltage', # Corrected typo and using single quotes as string literals in SQL
        0,
        0
    ))
    connection.commit()
    cursor.close()

# Function to generate synthetic sine wave data with disturbances
def generate_synthetic_data():
    start_time = datetime.datetime.now(datetime.timezone.utc)
    time_array = np.linspace(0, 1, SAMPLES, endpoint=False)
    voltage_array = AMPLITUDE * np.sin(2 * np.pi * 50 * time_array)
    noise = np.random.uniform(-NOISE_LEVEL, NOISE_LEVEL, SAMPLES)
    voltage_array += noise
    formatted_voltage_array = np.column_stack((np.round(voltage_array, 2), (time_array * 1000).astype(int)))
    return formatted_voltage_array, start_time

# Replace with your actual database credentials
connection = create_connection("localhost", "gridsense_user", "microgrid", "gridsense_db")

try:
    while True:
        max_id = get_max_id(connection) + 1
        voltage_array, start_time = generate_synthetic_data()
        print(voltage_array)
        insert_voltage_array(max_id, connection, voltage_array, start_time)
        max_id += 1
        print(f"Inserted a batch of {SAMPLES} values into the database. at t={start_time}")

        time.sleep(1)  # Wait for 1 second before the next batch

except KeyboardInterrupt:
    print("Exiting...")
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")