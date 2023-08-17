from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def reserve(request):
    return render(request, 'reserve.html')