from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Record

def index(request):
    latest_record = Record.objects.order_by('-date')[0]
    context = {
        'record': latest_record,
    }
    return render(request, 'WeatherApp/index.html', context)

def all(request):
    records = Record.objects.all()
    context = {}

    if request.GET.get('start') is not None:
        start = request.GET.get('start')
        start_datetime = datetime.strptime(start, "%Y-%m-%d")
        records = records.filter(date__gte = start_datetime)
        context |= {"start": start_datetime}

    if request.GET.get('end') is not None:
        end = request.GET.get('end')
        end_datetime = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        records = records.filter(date__lte = end_datetime)
        context |= {"end": end_datetime}

    if request.GET.get('orderby') is not None:
        order = request.GET.get('orderby')
        records = records.order_by(order)
        context |= {"order": order}

    if request.GET.get('min_temp') is not None:
        min_temp = float(request.GET.get('min_temp'))
        records = records.filter(temperature__gte = str(min_temp))
        context |= {"min_temp": min_temp}

    if request.GET.get('max_temp') is not None:
        max_temp = float(request.GET.get('max_temp')) + 0.1
        records = records.filter(temperature__lte = str(max_temp))
        context |= {"max_temp": max_temp}

    if request.GET.get('min_press') is not None:
        min_press = float(request.GET.get('min_press'))
        records = records.filter(pressure__gte = str(min_press))
        context |= {"min_press": min_press}

    if request.GET.get('max_press') is not None:
        max_press = float(request.GET.get('max_press')) + 0.1
        records = records.filter(pressure__lte = str(max_press))
        context |= {"max_press": max_press}

    context |= { "records": records }

    return render(request, 'WeatherApp/all.html', context)

def about(request):
    return render(request, 'WeatherApp/about.html')

def graphs(request):
    now = datetime.now()

    if request.GET.get('from') is not None:
        if request.GET.get('from') == '24h':
            records = Record.objects.filter('date' > datetime.now() - datetime.timedelta(days=1))
    else:
        records = Record.objects.order_by('-date')

    context = {
        "records": records,
    }
    return render(request, 'WeatherApp/graphs.html', context)
