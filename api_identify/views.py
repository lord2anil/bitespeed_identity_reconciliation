
from .models import *
from .serializers import *
from django.http import HttpResponse 
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.

class identity(APIView):


  
  def find_phonenumber_data(self,phonenumber,all_data, filter_data):

    phonenumber_rows=[]
    for x in all_data:
        if phonenumber ==x.phonenumber:
            phonenumber_rows.append(x)

          
    if len(phonenumber_rows)==0:
        return all_data,filter_data
    new_all_data=[]
    for x in phonenumber_rows:
        filter_data.append(x)
        
    for x in all_data:
        p=0
        for y in phonenumber_rows:
            if y.phonenumber==x.phonenumber:
                p=1
                break
        if p==0:
            new_all_data.append(x)

    all_data=new_all_data

    for x in filter_data:
        all_data,filter_data=self.find_email_data(x.email,all_data,filter_data)
    return all_data,filter_data
  def find_email_data(self,email,all_data=[], filter_data=[]):

    
    email_rows=[]
    for x in all_data:
        if email ==x.email:
            email_rows.append(x)

    if len(email_rows)==0:
        return all_data,filter_data

    new_all_data=[]
    for x in email_rows:
        filter_data.append(x)
    for x in all_data:

        p=0
        for y in email_rows:
            if y.email==x.email:
                p=1
                break
        if p==0:
            new_all_data.append(x)
    
    all_data=new_all_data
    for x in filter_data:
        all_data,filter_data=self.find_phonenumber_data(x.phonenumber,all_data,filter_data)
    return all_data,filter_data

        

        
    
  def post(self,request):
        data = request.data
        
        email = data['email']
        ## validate the email
        try:
            validate_email(email)
        except ValidationError as e:
            return Response("Please enter a valid email")

        phonenumber = data['phonenumber']
        if (email is None and phonenumber is None) or (email == "" and phonenumber == "")   :
            return Response("Please enter either email or phonenumber")
        common_email = Contact.objects.filter(email=email).all()
        common_phonenumber = Contact.objects.filter(phonenumber=phonenumber).all()
        
        response = {
            "primaryContactId": "",
            "emails":[],
            "phonenumbers" : [],
            "secondaryContactIds":[]
        }
        if (email == "" or email is None )and len(common_phonenumber)==0:
            print("here")
            contact_1=Contact.objects.create(email=email,phonenumber=phonenumber)
            contact_1.save()
            response["primaryContactId"]=contact_1.id
            response["emails"]=[]
            response["phonenumbers"].append(phonenumber)
            response["secondaryContactIds"]=[]
            serializer = response_Contact(data = response)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response (str(serializer.errors))
        elif ( phonenumber == "" or phonenumber is None) and len(common_email)==0:
            contact_1=Contact.objects.create(email=email,phonenumber=phonenumber)
            contact_1.save()
            response["primaryContactId"]=contact_1.id
            response["emails"].append(email)
            response["phonenumbers"]=[]
            response["secondaryContactIds"]=[]
            serializer = response_Contact(data = response)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response (str(serializer.errors))
        
        if len(common_email)==0 and len(common_phonenumber)==0 and email is not None and email!="" and phonenumber is not None and phonenumber!="":

            contact_1=Contact.objects.create(email=email,phonenumber=phonenumber)
            contact_1.save()
            response["primaryContactId"]=contact_1.id
            response["emails"].append(email)
            response["phonenumbers"].append(phonenumber)
            response["secondaryContactIds"]=[]
            serializer = response_Contact(data = response)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response (str(serializer.errors))
        elif len(common_email)==0 and len(common_phonenumber)!=0  and email is not None and email!="":
            contact_1=Contact.objects.create(email=email,phonenumber=phonenumber,linkprecedence="secondary")
            contact_1.save()
        elif len(common_email)!=0 and len(common_phonenumber)==0 and phonenumber is not None and phonenumber!="":
            contact_1=Contact.objects.create(email=email,phonenumber=phonenumber,linkprecedence="secondary")
            contact_1.save()
            
         
        all_data=Contact.objects.all()
        filter_data=[]
        if email is not None and email!="":
            all_data,filter_data=self.find_email_data(email,all_data,filter_data)
        if phonenumber is not None and phonenumber!="":
            all_data,filter_data=self.find_phonenumber_data(phonenumber,all_data,filter_data)
        
        # for x in filter_data:
        #     print(x.email,x.phonenumber)

        # print(filter_data)
        ## sort the based on created time, oldest first
        filter_data.sort(key=lambda x: x.created_at)    
        print(filter_data)
        primary_contact_id=filter_data[0].id

        response["primaryContactId"]=primary_contact_id
        for x in filter_data:
                response["emails"].append(x.email)
                response["phonenumbers"].append(x.phonenumber)
                if x.id!=primary_contact_id:
                  response["secondaryContactIds"].append(x.id)
        
        ## upadate the link precedence of all secondary contacts to secondary in the database
        primary_contact=Contact.objects.get(id=primary_contact_id)
        primary_contact.linkprecedence="primary"
        primary_contact.save()
        for id_1 in response["secondaryContactIds"]:
            if id_1 is not None:
                secondary_contact=Contact.objects.get(id=id_1)
                secondary_contact.linkprecedence="secondary"
                secondary_contact.save()

            
            


        # print(response)
        serializer = response_Contact(data = response)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response (str(serializer.errors))
    
