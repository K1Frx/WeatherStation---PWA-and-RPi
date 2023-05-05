from django.shortcuts import render
from .models import Record

def index(request):
    latest_record = Record.objects.order_by('-date')[0]
    context = {
        'record': latest_record,
    }
    return render(request, 'WeatherApp/index.html', context)

def all(request):
    records = Record.objects.order_by('-date')
    context = {
        "records": records,
    }
    return render(request, 'WeatherApp/all.html', context)

def about(request):
    return render(request, 'WeatherApp/about.html')

def graphs(request):
    records = Record.objects.order_by('-date')
    context = {
        "records": records,
    }
    return render(request, 'WeatherApp/graphs.html', context)
