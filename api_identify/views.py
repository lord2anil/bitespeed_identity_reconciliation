from django.shortcuts import render 
from .models import *

from django.http import HttpResponse 
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class identity(APIView):
   pass