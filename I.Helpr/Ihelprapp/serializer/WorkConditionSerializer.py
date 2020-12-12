from rest_framework import serializers 
from Ihelprapp.models import Work_Condition

class WorkConditionSerializer(serializers.ModelSerializer):
    type_of_service = serializers.CharField()
    work_period = serializers.CharField()
    begin_work_time = serializers.TimeField()
    end_work_time = serializers.TimeField()
    location = serializers.CharField()
    gender = serializers.CharField()
    payrate = serializers.IntegerField()

    class Meta:
        model = Work_Condition
        fields = ('type_of_service',
                  'work_period',
                  'begin_work_time',
                  'end_work_time',
                  'location',
                  'gender', 
                  'payrate')

