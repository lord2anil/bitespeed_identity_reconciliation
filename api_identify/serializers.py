from rest_framework import serializers

class request_data(serializers.Serializer):
    email = serializers.CharField(required=False,allow_null = True)
    phonenumber = serializers.CharField(required=False,allow_null = True)
    
    
class response_Contact(serializers.Serializer):
    primaryContactId = serializers.IntegerField()
    emails = serializers.ListField(child=serializers.EmailField())
    phonenumbers = serializers.ListField()
    secondaryContactIds = serializers.ListField(child=serializers.IntegerField())