from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
@csrf_exempt
def login(request):
    return render(request, 'login.html')


@csrf_exempt
def authenticateUser(request):
    return redirect("insect:insect_dashboard")
    # return render(request, 'index.html')