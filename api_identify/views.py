from django.shortcuts import render 
from .models import *
from .serializers import *
from django.http import HttpResponse 
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class identity(APIView):
  def post(self,request):
        serializer = request_data(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        phonenumber = serializer.validated_data['phonenumber']
        common_email = Contact.objects.filter(Q(email=email))
        common_phonenumber = Contact.objects.filter(phonenumber=phonenumber)
        already_exists = Contact.objects.filter(Q(email=email) & Q(phonenumber=phonenumber))
        primary_phone = common_phonenumber.filter(linkprecedence="primary")
        primary_email = common_email.filter(linkprecedence="primary")
        response = {
            "primaryContactId": "",
            "emails":[],
            "phonenumbers" : [],
            "secondaryContactIds":[]
        }
        if already_exists.exists():
            already_exists_obj = already_exists.first()
            if already_exists_obj.linkprecedence == "primary":
                response["primaryContactId"] = already_exists_obj.id
                response["emails"] = list(Contact.objects.filter(linkedId=already_exists_obj.id).values_list("email",flat=True).distinct())
                response["phonenumbers"] = list(Contact.objects.filter(linkedId=already_exists_obj.id).values_list("phonenumber",flat=True).distinct())
                response["secondaryContactIds"] = list(Contact.objects.filter(linkedId=already_exists_obj.id).values_list("id",flat=True).distinct())
            else:
                response["primaryContactId"] = already_exists_obj.linkedId
                response["emails"] = list(Contact.objects.filter(linkedId=already_exists_obj.linkedId).values_list("email",flat=True).distinct())
                response["phonenumbers"] = list(Contact.objects.filter(linkedId=already_exists_obj.linkedId).values_list("phonenumber",flat=True).distinct())
                response["secondaryContactIds"] = list(Contact.objects.filter(linkedId=already_exists_obj.linkedId).values_list("id",flat=True).distinct())
            print(response)
        else:
            if primary_email.exists() and primary_phone.exists():
                if primary_email.first().createdAt > primary_phone.first().createdAt:
                    obj = primary_email.first()
                    obj.linkedId = primary_phone.first().id
                    obj.linkprecedence = "secondary"
                    obj.save()
                    response["primaryContactId"] = primary_phone.first().id
                    response["emails"] = list(Contact.objects.filter(linkedId=primary_phone.first().id).values_list("email",flat=True).distinct())
                    response["phonenumbers"] = list(Contact.objects.filter(linkedId=primary_phone.first().id).values_list("phonenumber",flat=True).distinct())
                    response["secondaryContactIds"] = list(Contact.objects.filter(linkedId=primary_phone.first().id).values_list("id",flat=True).distinct())
                else:
                    obj = primary_phone.first()
                    obj.linkedId = primary_email.first().id
                    obj.linkprecedence = "secondary"
                    obj.save()
                    response["primaryContactId"] = primary_email.first().id
                    response["emails"] = list(Contact.objects.filter(linkedId=primary_email.first().id).values_list("email",flat=True).distinct())
                    response["phonenumbers"] = list(Contact.objects.filter(linkedId=primary_email.first().id).values_list("phonenumber",flat=True).distinct())
                    response["secondaryContactIds"] = list(Contact.objects.filter(linkedId=primary_email.first().id).values_list("id",flat=True).distinct())
            elif common_email.exists():
                primary_common_email = Contact.objects.filter((Q(linkprecedence="primary") & Q(email=email)) | Q(id = common_email.first().linkedId)).first()
                if phonenumber is not None:
                    contact = Contact(
                        phonenumber=phonenumber,
                        email=email,
                        linkedId = primary_common_email.id,
                        linkprecedence = "secondary"
                    )
                    print(contact)
                    contact.save()
                response["primaryContactId"] = primary_common_email.id
                response["emails"] = list(Contact.objects.filter(linkedId=primary_common_email.id).values_list("email",flat=True).distinct()) + [primary_common_email.email]
                response["phonenumbers"] = list(Contact.objects.filter(linkedId=primary_common_email.id).values_list("phonenumber",flat=True).distinct()) 
                response["secondaryContactIds"] = list(Contact.objects.filter(linkedId=primary_common_email.id).values_list("id",flat=True).distinct())
            elif common_phonenumber.exists():
                primary_common_phonenumber = Contact.objects.filter((Q(linkprecedence="primary") & Q(phonenumber=phonenumber)) | Q(id = common_phonenumber.first().linkedId)).first()
                if email is not None:
                    contact = Contact(
                        phonenumber=phonenumber,
                        email=email,
                        linkedId = primary_common_phonenumber.id,
                        linkprecedence = "secondary"
                    )
                    print(contact)
                    contact.save()
                response["primaryContactId"] = primary_common_phonenumber.id
                response["emails"] = list(Contact.objects.filter(linkedId=primary_common_phonenumber.id).values_list("email",flat=True).distinct()) + [primary_common_phonenumber.email]
                response["phonenumbers"] = list(Contact.objects.filter(linkedId=primary_common_phonenumber.id).values_list("phonenumber",flat=True).distinct())
                response["secondaryContactIds"] = list(Contact.objects.filter(linkedId=primary_common_phonenumber.id).values_list("id",flat=True).distinct())
            else:
                obj = Contact.objects.create(email=email,phonenumber=phonenumber)
                response["primaryContactId"] = obj.id
                response["emails"] = [obj.email]
                response["phonenumbers"] = [obj.phonenumber]
                response["secondaryContactIds"] = []
        serializer = response_Contact(data = response)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response (str(serializer.errors))
    
