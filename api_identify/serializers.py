from rest_framework import serializers

    
class response_Contact(serializers.Serializer):
    primaryContactId = serializers.IntegerField()
    emails = serializers.ListField( allow_empty=True,allow_null=True,required=None)
    phonenumbers = serializers.ListField(allow_null=True,allow_empty=True,required=None)
    secondaryContactIds = serializers.ListField(child=serializers.IntegerField(),allow_empty=True,allow_null=True)