from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def web_user(request):
    context ={
        
    }
    return render(request, 'web_users/index.html', context)