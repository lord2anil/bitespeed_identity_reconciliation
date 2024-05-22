from django.db import models

# Create your models here.


class Contact(models.Model):
    phonenumber = models.TextField(db_index=True)
    email = models.TextField(null=True,blank=True,db_index=True)
    linkedId = models.IntegerField(null=True,blank=True)
    linkprecedence = models.TextField(choices=( ("primary", "primary"),("secondary", "secondary")),default="primary")
    createdAt = models.DateTimeField(auto_add_now=True)
    updatedAt = models.DateTimeField(auto_add_now=True)
    deletedAt = models.DateTimeField(blank=True,null=True)
    
        
    

    