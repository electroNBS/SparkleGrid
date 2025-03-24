import graphene
from graphene_django import DjangoObjectType
from .models import MeasurementsOne

class MeasurementsType(DjangoObjectType):
    class Meta:
        model = MeasurementsOne

class Query(graphene.ObjectType):
    all_measurements = graphene.List(MeasurementsType)

    def resolve_all_measurements(self, info):
        return MeasurementsOne.objects.all() # Corrected model name

class CreateMeasurement(graphene.Mutation):
    class Arguments:
        sensdata = graphene.Float(required=True)

    measurement = graphene.Field(MeasurementsType)

    def mutate(self, info, sensdata):
        measurement = MeasurementsOne.objects.create(sensdata=sensdata) # Corrected model name
        return CreateMeasurement(measurement=measurement)

class UpdateMeasurement(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        sensdata = graphene.Float(required=True)

    measurement = graphene.Field(MeasurementsType)

    def mutate(self, info, id, sensdata):
        measurement = MeasurementsOne.objects.get(pk=id) # Corrected model name
        measurement.sensdata = sensdata
        measurement.save()
        return UpdateMeasurement(measurement=measurement)

class DeleteMeasurement(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        measurement = MeasurementsOne.objects.get(pk=id) # Corrected model name
        measurement.delete()
        return DeleteMeasurement(ok=True)

class Mutation(graphene.ObjectType):
    create_measurement = CreateMeasurement.Field()
    update_measurement = UpdateMeasurement.Field()
    delete_measurement = DeleteMeasurement.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)