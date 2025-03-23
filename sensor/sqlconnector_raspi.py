import psycopg2
from psycopg2 import OperationalError
import numpy as np
import time
import datetime
import serial

# Initialize the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', baudrate=9600)  # Adjust the port as needed

# Constants for the sine wave
AMPLITUDE = 240
NOISE_LEVEL = 0
SAMPLES = 1000

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

    # Calculate THD and PF
    #thd = calculate_thd(voltage_array[:, 0])  # Assuming voltage data is in the first column
    # pf = calculate_power_factor(voltage_array[:, 0], current_array)  # Assuming you have current data

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



# def calculate_power_factor(voltage_array, current_array):
#     # Assuming you have the current data as well (current_array)
#     # Compute the displacement power factor (PF)
#     apparent_power = np.abs(np.mean(voltage_array) * np.mean(current_array))
#     real_power = np.mean(voltage_array * current_array)
#     displacement_pf = real_power / apparent_power

#     # Compute the distortion power factor (PF_THD)
#    # thd_percentage = calculate_thd(voltage_array) / 100
#     distortion_pf = np.cos(np.arccos(displacement_pf) - np.arccos(thd_percentage))

#     # Compute the total power factor (PF_Tot)
#     total_pf = displacement_pf * distortion_pf
#     return total_pf


# def calculate_thd(voltage_array):
#     # Compute the FFT of the voltage array
#     signal_fft = np.fft.fft(voltage_array)
#     N_harmonics = 10  # Number of harmonics to consider (adjust as needed)

#     # Find the index of the maximum amplitude in the FFT result (fundamental frequency)
#     max_amplitude_idx = np.argmax(np.abs(signal_fft))
#     fundamental_amplitude = np.abs(signal_fft[max_amplitude_idx])

#     # Calculate the THD numerator (exclude DC component)
#     thd_numerator = np.sqrt(np.sum(np.square(np.abs(signal_fft[1:N_harmonics+1]))))

#     # Compute the THD percentage
#     thd_percentage = (thd_numerator / fundamental_amplitude) * 100
#     return thd_percentage
import datetime
import numpy as np


def get_arduino_data():
    try:
        # Read data from the Arduino
        arduino_data = ser.readline().decode().strip()  # Assuming the Arduino sends data as a string
        arduino_data = eval(arduino_data)  # Convert the string to a Python list
        print(arduino_data)
    # Default values for sensor data
    except Exception as e:
        # Handle other unexpected errors
        print(f"Error: {e}")
        arduino_data = [0, [[0.0, 0.0]]]  # Default values for sensor data

    


    # Create a NumPy array initialized with zeros and size 1000
    formatted_voltage_array = np.zeros((1000, 2))  # Assuming 2 columns (value, delta time)
    

    try:
        arduino_data_values = np.array(arduino_data[1])  # Extract the actual data from Arduino
        # Update the NumPy array with actual data, handling potential index errors
        formatted_voltage_array[:len(arduino_data_values), :] = arduino_data_values
        sensor_id = arduino_data[0]
            
        if sensor_id == 1:
            stype = "Voltage"
            sname = "Voltage Sensor"
        elif sensor_id == 2:
            stype = "Current"
            sname = "Current Sensor"
        # Add more sensors
        else:
            # Default values if sensor_id is not recognized
            stype = "Voltage"
            sname = "Undefined Sensor, define in the backend."
    except IndexError as e:
        # Handle index errors caused by corrupted Arduino data
        print(f"Error updating NumPy array: {e}")
        return np.zeros((1000, 2)), start_time, 20,"Voltage", "Voltage"

    start_time = datetime.datetime.now(datetime.timezone.utc)
    print(formatted_voltage_array)
    formatted_voltage_array = formatted_voltage_array / 10  # Divide all values by 10 to adjust the gain
 # Round the values to two decimal places

    formatted_voltage_array = np.round(formatted_voltage_array, decimals=2)

    return formatted_voltage_array, start_time, sensor_id, sname, stype
# Replace with your actual database credentials
connection = create_connection("localhost", "sensor2", "microgrid", "sensors")

try:
    while True:
        max_id = get_max_id(connection) + 1
        voltage_array, start_time, sensor_id, sname, stype = get_arduino_data()  # Arduino
        print(voltage_array)
        insert_voltage_array(max_id, connection, voltage_array, start_time, sensor_id, sname, stype)
        max_id += 1
        print(f"Inserted a batch of {SAMPLES} values into the database at t={start_time}")
        
        time.sleep(1)  # Wait for 1 second before the next batch
except Exception as e:
        # Handle index errors caused by corrupted Arduino data
        print(f"Error updating NumPy array: {e}")

except KeyboardInterrupt:
    print("Exiting...")
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")
