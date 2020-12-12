from rest_framework import serializers 
from Ihelprapp.models import Message, Message_History, Review
from django.db import transaction

 
class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('sender_id',
                  'receiver_id',
                  'message_content'
                  )

                
class MessageHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Message_History
        fields = ('message_status',
                  'owner_id',
                  'other_owner_id')

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('rating',
                  'reviewer_id',
                  'reviewed_user_id',
                  'review_content',
                  'after_service')


    