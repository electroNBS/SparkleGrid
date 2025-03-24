# /home/mgrid/development/microgrid-iot/GridSense/GridSense/admin.py

from django.contrib import admin
from .models import MeasurementsOne, MeasurementsTwo, MeasurementsThree, MeasurementsFour, MeasurementsFive, MeasurementsSix


admin.site.register(MeasurementsOne)
admin.site.register(MeasurementsTwo)
admin.site.register(MeasurementsThree)
admin.site.register(MeasurementsFour)
admin.site.register(MeasurementsFive)
admin.site.register(MeasurementsSix)
