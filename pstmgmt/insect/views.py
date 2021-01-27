from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'index.html')

# Create your views here.
def add(request):
    return render(request, 'addProduct.html')

def viewDetails(request):
    return render(request, 'allProducts.html')

def add_new_insect(request):
    return render(request, 'addProduct.html')
