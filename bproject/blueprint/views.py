from django.shortcuts import render
from django.http import HttpResponse
from .models import Device, DeviceData
from rest_framework.decorators import api_view
from rest_framework import status

from datetime import datetime

import json


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Welcome to the Blueprint system!")


@api_view(["POST"])
def state_report(request):
    received_json=json.loads(request.body.decode('utf-8')) #This is a working alternative
    device = Device.objects.get(serial_number=received_json["serial_number"])
    cpu = received_json["cpu"]
    memory = received_json["memory"]
    datapoint = DeviceData(datetime=datetime.now(), device=device, cpu=cpu, memory=memory)
    datapoint.save()
    return HttpResponse("Accepted", status=status.HTTP_201_CREATED)


def visualize(request, device_id):
    device = Device.objects.get(serial_number=device_id)
    device_state = DeviceData.objects.filter(device=device).last()
    context = {
        "device_state": device_state
    }
    return render(request, 'bproject/index.html', context=context)
    # return HttpResponse("Hello, world. Welcome to the Visualize endpoint! {}".format(str(device_state.memory)))


def device_state(request, device_id):
    device = Device.objects.get(serial_number=device_id)
    device_state = DeviceData.objects.filter(device=device).last()

    # output = '; '.join([s.cpu for s in device_state])
    return HttpResponse("Hello, world. Welcome to the device state endpoint! {}".format(str(device_state)))

