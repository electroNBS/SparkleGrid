# import time
# import ADS1256
# import RPi.GPIO as GPIO

# # Define the samples per second (SPS)
# samples_per_second = ADS1256.ADS1256_DRATE_E['ADS1256_1000SPS']
# # Calculate the time interval in nanoseconds for the given SPS
# time_interval_ns = int(1e9 / samples_per_second)

# try:
#     ADC = ADS1256.ADS1256()
#     ADC.ADS1256_init()
#     ADC.ADS1256_ConfigADC(ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1'], samples_per_second)
    
#     # Initialize a list to store the last read time in nanoseconds for each channel
#     last_read_time_ns = [time.time_ns()] * 8
    
#     # Initialize a counter for each channel
#     counters = [0] * 8
    
#     while True:
#         ADC_Value = ADC.ADS1256_GetAll()
#         current_time_ns = time.time_ns()
        
#         # Print the ADC values and sampling rates for each channel
#         for i in range(8):
#             # Increment the counter for the channel
#             counters[i] += 1
            
#             # Calculate the time elapsed since the last read
#             time_elapsed_ns = current_time_ns - last_read_time_ns[i]
            
#             # If the time elapsed is greater than the interval, update the last read time and reset the counter
#             if time_elapsed_ns >= time_interval_ns:
#                 sampling_rate = counters[i] * 1e9 / time_elapsed_ns
#                 print(f"{i} ADC = {ADC_Value[i]*5.0/0x7fffff:.6f}, Sampling Rate = {sampling_rate:.2f} SPS")
#                 last_read_time_ns[i] = current_time_ns
#                 counters[i] = 0
        
#         # Move the cursor up 8 lines to overwrite the previous output
#         print ("\33[9A")

# except Exception as e:
#     GPIO.cleanup()
#     print(f"\\r\\nProgram ended due to {e}")
#     exit()
import time
import ADS1256
import RPi.GPIO as GPIO


try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
    samples_per_second = ADS1256.ADS1256_DRATE_E['ADS1256_1000SPS']
    while(1):
        ADC_Value = ADC.ADS1256_GetAll()
        print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
        print ("1 ADC = %lf"%(ADC_Value[1]*5.0/0x7fffff))
        print ("2 ADC = %lf"%(ADC_Value[2]*5.0/0x7fffff))
        print ("3 ADC = %lf"%(ADC_Value[3]*5.0/0x7fffff))
        print ("4 ADC = %lf"%(ADC_Value[4]*5.0/0x7fffff))
        print ("5 ADC = %lf"%(ADC_Value[5]*5.0/0x7fffff))
        print ("6 ADC = %lf"%(ADC_Value[6]*5.0/0x7fffff))
        print ("7 ADC = %lf"%(ADC_Value[7]*5.0/0x7fffff))
        print ("\33[9A")

        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()