from django.core.management.base import BaseCommand
from api_identify.models import Contact
from datetime import datetime, time

class Command(BaseCommand):
    help = 'Insert data into the database'

   
    def handle(self, *args, **kwargs):

        Contact.objects.create(phonenumber='1234567890',email='a8208226@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        Contact.objects.create(phonenumber='12345342890',email='a8242308226@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        Contact.objects.create(phonenumber='1234567890',email='a82082vc26@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        Contact.objects.create(phonenumber='122434567890',email='a82dg08226@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        Contact.objects.create(phonenumber='1234567890',email='a82082dfg26@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        Contact.objects.create(phonenumber='1234523490',email='a8208dfg226@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        Contact.objects.create(phonenumber='1234567890',email='a8208226@gmail.com',linkprecedence='primary',created_at=datetime.now(),updated_at=datetime.now())
        
       
                    
            




        



        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
