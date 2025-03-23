# views.py
#from django.shortcuts import render
#from .models import Measurements

#def print_measurements(request):
    # Query the database to retrieve data from Measurements
#    measurements = Measurements.objects.all()
    
    # Print the data
#    for measurement in measurements:
#        print(f"Sensdata: {measurement.sensdata}, Time: {measurement.time}")
    
#    return render(request, 'measurements.html', {'measurements': measurements})
# microback/micro_back/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from .models import MeasurementsOne
from .models import MeasurementsTwo,MeasurementsFive,MeasurementsThree, MeasurementsFour, MeasurementsSix
@csrf_exempt
def hello_world(request):
    return HttpResponse("hello world")

# View to fetch all measurements

@csrf_exempt
def measurements_by_sensor_id(request, table_no, sensor_id):
    if request.method == 'GET':
        model_mapping = {
            1: MeasurementsOne,
            2: MeasurementsTwo,
            3: MeasurementsThree,
            4: MeasurementsFour,
            5: MeasurementsFive,
            6: MeasurementsSix
        }
        if table_no in model_mapping:
            model_class = model_mapping[table_no]
            # Fetch the latest measurement
            latest_measurement = model_class.objects.filter(sensor_id=sensor_id).order_by('-time').first()
            if latest_measurement:
                # Assuming 'sensdata' is now an array field in your model
                data = {
                    'sensdata': latest_measurement.sensdata,
                    'time': latest_measurement.time,
                    'rms': latest_measurement.rmsvalue,
                    'pf': latest_measurement.pf,
                    'thd': latest_measurement.thd,
                    'sname': latest_measurement.sname,
                    'stype': latest_measurement.stype,
                }
                return JsonResponse({'measurements': data})
            else:
                return JsonResponse({'error': 'No measurements found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)




