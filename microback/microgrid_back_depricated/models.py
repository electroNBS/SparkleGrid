from django.db import models
from django.contrib.postgres.fields import ArrayField

class NestedDecimalArrayField(ArrayField):
    def __init__(self, *args, **kwargs):
        kwargs['base_field'] = ArrayField(models.DecimalField(max_digits=5, decimal_places=2), size=2)
        super().__init__(*args, **kwargs)

class MeasurementModel(models.Model):
    sensor_id = models.PositiveIntegerField()
    sensdata = NestedDecimalArrayField()
    time = models.DateTimeField(auto_now_add=True)
    rmsvalue = models.DecimalField(max_digits=5, decimal_places=2)
    pf = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Power Factor')
    thd = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Total Harmonic Distortion')
    sname = models.CharField(max_length=50, verbose_name='Sensor Name')
    stype = models.CharField(max_length=50, verbose_name='Sensor Type', choices=[('Current', 'Current'), ('Voltage', 'Voltage')])

    class Meta:
        abstract = True

    def __str__(self):
        return f"Sensor ID: {self.sensor_id}, Sensdata: {self.sensdata}, Time: {self.time}, RMS: {self.rmsvalue}, PF: {self.pf}, THD: {self.thd}, Name: {self.sname}, Type: {self.stype}"

class MeasurementsOne(MeasurementModel):
    pass

class MeasurementsTwo(MeasurementModel):
    pass

class MeasurementsThree(MeasurementModel):
    pass

class MeasurementsFour(MeasurementModel):
    pass

class MeasurementsFive(MeasurementModel):
    pass

class MeasurementsSix(MeasurementModel):
    pass
