import csv
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import json_script
from .models import Record

def offline(request):
    return render(request, 'WeatherApp/offline.html')

def index(request):
    latest_record = Record.objects.order_by('-date')[0]
    context = {
        'record': latest_record,
    }
    return render(request, 'WeatherApp/index.html', context)

def export(request):
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

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['id', 'date', 'temperature', 'pressure', 'comment'])  # Replace with your actual column names

    # Write the data rows
    for row in records:
        writer.writerow([row.id, row.date, row.temperature, row.pressure, row.comment])  # Replace with your actual column names

    return response

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

    temperatures = []
    dates = []
    pressures = []

    if request.GET.get('type') is not None:
        if request.GET.get('type') == "24h":
            records = Record.objects.filter(date__gt=now - timedelta(days=1)).order_by('date')
            records_copy = {}
            for record in records:
                dates.append(record.date.strftime('%H:%M'))
                temperatures.append(record.temperature)
                pressures.append(record.pressure)
        elif request.GET.get('type') == "7d":
            records = Record.objects.filter(date__gt=now - timedelta(days=7)).order_by('date')
            records_copy = {}
            for record in records:
                dates.append(record.date.strftime('%d.%m - %H:%M'))
                temperatures.append(record.temperature)
                pressures.append(record.pressure)
        elif request.GET.get('type') == "30d":
            records = Record.objects.filter(date__gt=now - timedelta(days=30)).order_by('date')
            print(records)
            records_copy = {}
            i = 0
            temp_sum = 0
            press_sum = 0
            for record in records:
                if i != 3:
                    temp_sum += record.temperature
                    press_sum += record.pressure
                    i += 1
                else:
                    temp_sum += record.temperature
                    press_sum += record.pressure
                    temperature = temp_sum / 4
                    pressure = press_sum / 4
                    date = record.date.strftime('%d.%m - %H:%M')
                    dates.append(date)
                    temperatures.append(temperature)
                    pressures.append(pressure)
                    i = 0

    elif request.GET.get('start') is not None and request.GET.get('end') is not None:
        start = request.GET.get('start')
        start_datetime = datetime.strptime(start, "%Y-%m-%d")
        records = records.filter(date__gte = start_datetime)

        end = request.GET.get('end')
        end_datetime = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        records = records.filter(date__lte = end_datetime)

        for record in records:
            dates.append(record.date.strftime('%d.%m - %H:%M'))
            temperatures.append(record.temperature)
            pressures.append(record.pressure)

    
    else:
        records = Record.objects.filter(date__gt=now - timedelta(days=7)).order_by('date')
        records_copy = {}
        for record in records:
            dates.append(record.date.strftime('%d.%m - %H:%M'))
            temperatures.append(record.temperature)
            pressures.append(record.pressure)

    #records is dictionary like:
    #records = {
    #   'date',
    #   'temperature',
    #   'pressure',
    # }

    # dates = []
    # temperatures = []
    # pressures = []

    # for record in records:
    #     print(record['temperature'])
    #     dates.append(record['date'])
    #     temperatures.append(record['temperature'])
    #     pressures.append(record['pressure'])
    # context = {
    #     'records': json.dumps(records),
    #     'dates': dates,
    #     'temperatures': temperatures,
    #     'pressures': pressures,
    # }

    context = {
        'dates': json.dumps(dates),
        'temperatures': json.dumps(temperatures),
        'pressures': json.dumps(pressures),
    }

    return render(request, 'WeatherApp/graphs.html', context)
