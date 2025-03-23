import ADS1256
import RPi.GPIO as GPIO
import psycopg2
import numpy as np
import datetime
import threading, time

# Define a buffer variable to store the latest ADC value
buffer_value = 0.0

# Define a buffer lock for thread-safe operations
buffer_lock = threading.Lock()

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
    except psycopg2.OperationalError as e:
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
    # delta_time = np.diff(voltage_array[:, 1]) / 1000.0  # Assuming time is in milliseconds

    # Calculate RMS value for the voltage array
   
    # rms_value = calculate_rms(voltage_array[:, 0])

    # # Ensure RMS value is within the allowed range, scale if necessary
    # if rms_value >= 1000:
    #     scale_factor = 10 ** (np.floor(np.log10(rms_value)) - 2)
    #     voltage_array[:, 0] = voltage_array[:, 0] / scale_factor
    #     rms_value = calculate_rms(voltage_array[:, 0])

    # # Format the RMS value to 5 significant figures with 2 decimal places
    # rms_value = f"{rms_value:.2f}"


    # Prepare the voltage array for insertion
    timestamp = start_time.isoformat()
    query = """
    INSERT INTO microgrid_back_measurementssix(id, sensor_id, sensdata, time, rmsvalue, sname, stype, thd, pf)
    VALUES (%s, %s, %s::numeric[], %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (curr_id, sensor_id, voltage_array.tolist(), timestamp, 0, sname, stype, 0, 0))
    connection.commit()
    cursor.close()




# Initialize the ADS1256 ADC
ADC = ADS1256.ADS1256()
ADC.ADS1256_init()
ADC.ADS1256_ConfigADC(ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256.ADS1256_DRATE_E['ADS1256_2000SPS'])

# Replace with your actual database credentials
connection = create_connection("localhost", "postgres", "microgrid", "sensors")

# Function to sample ADC at 1000Hz
def sample_adc():
    global buffer_value
    while True:
        start_time = time.time()
        # print(round(time.time_ns()))
        ADC_Value = ADC.ADS1256_GetChannalValue(7)
        with buffer_lock:
            buffer_value = ADC_Value * 5.0 / 0x7fffff
        
        # Sleep until the next sampling period
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        sleep_time = max(0, (1.0 / 2000) - elapsed_time)
        time.sleep(sleep_time)

# Thread to handle sampling
sampling_thread = threading.Thread(target=sample_adc)
sampling_thread.daemon = True
sampling_thread.start()
# time_arr=[]
# Function to collect samples at 1000Hz
def collect_samples():
    global buffer_value
    voltage_values = []
    for _ in range(1000):  # Collect 1000 samples
        with buffer_lock:
            # Format buffer_value to 5 significant figures with 2 decimal places
            formatted_value = format(buffer_value, '.5g')
            voltage_values.append([formatted_value, _])
            # time_arr.append(time.time_ns())
        time.sleep(1.0 / 1000)  # Collect at 1000Hz
    # print(time_arr)
    return np.array(voltage_values)


# Function to handle periodic database insertion
def database_insertion_task():
    while True:
        start_time = datetime.datetime.now(datetime.timezone.utc)
        voltage_array = collect_samples()
        
        max_id = get_max_id(connection) + 1
        sensor_id = 1  # Assuming the sensor ID is 1
        sname = "Voltage Sensor"
        stype = "Voltage"
        
        insert_voltage_array(max_id, connection, voltage_array, start_time, sensor_id, sname, stype)
        print(f"Inserted a batch of 1000 values into the database at t={start_time}")

# Thread to handle database insertion
db_thread = threading.Thread(target=database_insertion_task)
db_thread.daemon = True
db_thread.start()

# Main loop to keep the script running
try:
    while True:
        time.sleep(0.0001)  # Small sleep to reduce CPU usage while keeping the main loop active
except KeyboardInterrupt:
    print("Exiting...")
finally:
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")
