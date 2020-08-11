import datetime
import statistics

from django.shortcuts import render
from django.http import JsonResponse
from metno_locationforecast import Place, Forecast
from core.models import City


def forecast(request):
    if not 'city' in request.GET:
        return JsonResponse({'message': 'Parameter "city" is required'}, status=400)
    if not 'days' in request.GET:
        return JsonResponse({'message': 'Parameter "days" is required'}, status=400)

    try:
        days = int(request.GET['days'])
    except ValueError:
        return JsonResponse({'message': 'Parameter "days" must be between 1 and 10'}, status=400)

    if not 0 < days <= 10:
        return JsonResponse({'message': 'Parameter "days" must be between 1 and 10'}, status=400)

    # Fetch (lat, lon) for given city.
    try:
        city = City.objects.get(name=request.GET['city'])
    except City.MultipleObjectsReturned:
        # XXX: Unfortunately the data we're using contains what appears to be
        # duplicates. Use the first result as a workaround for now.
        city = City.objects.filter(name=request.GET['city']).first()
    except City.DoesNotExist:
        return JsonResponse(
            {'message': 'City "{}" could not be found'.format(request.GET['city'])}, status=400)

    # Get weather for the given city.
    city = Place(city.name, city.lat, city.lon)
    forecast = Forecast(city,
        'metno-locationforecast/1.0 https://github.com/Rory-Sullivan/metno-locationforecast')
    forecast.update()

    # Collect temperature and humidity values for calculations and limit data
    # to the number of days given in the request.
    t, h = [], []
    for interval in forecast.data.intervals:
        if interval.end_time <= datetime.datetime.now() + datetime.timedelta(days=days):
            t.append(interval.variables['air_temperature'].value)
            h.append(interval.variables['relative_humidity'].value)

    temperature_min = min(t)
    temperature_max = max(t)
    temperature_average = statistics.mean(t)
    temperature_median = statistics.median(t)

    humidity_min = min(h)
    humidity_max = max(h)
    humidity_average = statistics.mean(h)
    humidity_median = statistics.median(h)

    return JsonResponse({
        'temperature_min': temperature_min,
        'temperature_max': temperature_max,
        'temperature_average': round(temperature_average, 2),
        'temperature_median': round(temperature_median, 2),
        'humidity_min': humidity_min,
        'humidity_max': humidity_max,
        'humidity_average': round(humidity_average, 2),
        'humidity_median': round(humidity_median, 2),
    })
