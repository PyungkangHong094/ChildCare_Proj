from rest_framework import serializers 
from Ihelprapp.models import Parent_Post
from Ihelprapp.models import Sitter_Post
from .WorkConditionSerializer import *
from django.db import transaction

 
class ParentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parent_Post
        fields = ('writer_id',
                  'writer_name',
                  'title',
                  'content',
                  'work_condition')


class SitterPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sitter_Post
        fields = ('writer_id',
                  'writer_name',
                  'title',
                  'content',
                  'work_condition')
    