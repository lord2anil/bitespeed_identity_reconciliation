from django.db import models

# Create your models here.


class Contact(models.Model):
    phonenumber = models.TextField(null=True,blank=True,db_index=True)
    email = models.TextField(null=True,blank=True,db_index=True)
    linkedId = models.IntegerField(null=True,blank=True)
    linkprecedence = models.TextField(choices=( ("primary", "primary"),("secondary", "secondary")),default="primary")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True,null=True)
    
        
    

    