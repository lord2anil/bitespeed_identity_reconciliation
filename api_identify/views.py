
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


  
  def find_phoneNumber_data(self,phoneNumber,all_data, filter_data):

    phoneNumber_rows=[]
    for x in all_data:
        if phoneNumber ==x.phoneNumber:
            phoneNumber_rows.append(x)

          
    if len(phoneNumber_rows)==0:
        return all_data,filter_data
    new_all_data=[]
    for x in phoneNumber_rows:
        filter_data.append(x)
        
    for x in all_data:
        p=0
        for y in phoneNumber_rows:
            if y.phoneNumber==x.phoneNumber:
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
        all_data,filter_data=self.find_phoneNumber_data(x.phoneNumber,all_data,filter_data)
    return all_data,filter_data

        

        
    
  def post(self,request):
        data = request.data
        
        try :
            email=data['email']
        except:
            email=""
        try :
            phoneNumber=data['phoneNumber']
        except:
            phoneNumber=""
        
        
        ## validate the email
        if email is not None and email!="":
            try:
                validate_email(email)
            except ValidationError as e:
                return Response("Please enter a valid email")

        if (email is None and phoneNumber is None) or (email == "" and phoneNumber == "")   :
            return Response("Please enter either email or phoneNumber")
        common_email = Contact.objects.filter(email=email).all()
        common_phoneNumber = Contact.objects.filter(phoneNumber=phoneNumber).all()
        
        response = {
            "primaryContactId": "",
            "emails":[],
            "phoneNumbers" : [],
            "secondaryContactIds":[]
        }
        if (email == "" or email is None )and len(common_phoneNumber)==0:
            print("here")
            contact_1=Contact.objects.create(email=email,phoneNumber=phoneNumber)
            contact_1.save()
            response["primaryContactId"]=contact_1.id
            response["emails"]=[]
            response["phoneNumbers"].append(phoneNumber)
            response["secondaryContactIds"]=[]
            serializer = response_Contact(data = response)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response (str(serializer.errors))
        elif ( phoneNumber == "" or phoneNumber is None) and len(common_email)==0:
            contact_1=Contact.objects.create(email=email,phoneNumber=phoneNumber)
            contact_1.save()
            response["primaryContactId"]=contact_1.id
            response["emails"].append(email)
            response["phoneNumbers"]=[]
            response["secondaryContactIds"]=[]
            serializer = response_Contact(data = response)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response (str(serializer.errors))
        
        if len(common_email)==0 and len(common_phoneNumber)==0 and email is not None and email!="" and phoneNumber is not None and phoneNumber!="":
            print(email,phoneNumber)
            contact_1=Contact.objects.create(email=email,phoneNumber=phoneNumber)
            contact_1.save()
            response["primaryContactId"]=contact_1.id
            response["emails"].append(email)
            response["phoneNumbers"].append(phoneNumber)
            response["secondaryContactIds"]=[]
            serializer = response_Contact(data = response)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response (str(serializer.errors))
        elif len(common_email)==0 and len(common_phoneNumber)!=0  and email is not None and email!="":
            contact_1=Contact.objects.create(email=email,phoneNumber=phoneNumber,linkprecedence="secondary")
            contact_1.save()
        elif len(common_email)!=0 and len(common_phoneNumber)==0 and phoneNumber is not None and phoneNumber!="":
            contact_1=Contact.objects.create(email=email,phoneNumber=phoneNumber,linkprecedence="secondary")
            contact_1.save()
            
         
        all_data=Contact.objects.all()
        filter_data=[]
        if email is not None and email!="":
            all_data,filter_data=self.find_email_data(email,all_data,filter_data)
        if phoneNumber is not None and phoneNumber!="":
            all_data,filter_data=self.find_phoneNumber_data(phoneNumber,all_data,filter_data)
        
        # for x in filter_data:
        #     print(x.email,x.phoneNumber)

        # print(filter_data)
        ## sort the based on created time, oldest first
        filter_data.sort(key=lambda x: x.created_at)    
        print(filter_data)
        primary_contact_id=filter_data[0].id

        response["primaryContactId"]=primary_contact_id
        for x in filter_data:
                response["emails"].append(x.email)
                response["phoneNumbers"].append(x.phoneNumber)
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
    
