from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import MeasurementsOne, MeasurementsTwo, MeasurementsFive, MeasurementsThree, MeasurementsFour, MeasurementsSix

@csrf_exempt
def hello_world(request):
    return HttpResponse("hello world")

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
            latest_measurement = model_class.objects.filter(sensor_id=sensor_id).order_by('-time').first()
            if latest_measurement:
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