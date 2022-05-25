from django.shortcuts import render, redirect
from .models import *
from products.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Google Calendar

from pprint import pprint
from .google import create_service, convert_to_RFC_datetime
import pathlib

print(pathlib.Path().resolve(),"***************")

CLIENT_SECRET_FILE =str(pathlib.Path().resolve())+'\events\credentials.json'
API_NAME = 'Calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
calander_id_chicago = 'ibrahim.murad009@gmail.com'


def calendar(request):
    return render(request,'events/calendar.html')

@login_required(login_url='login')
def get_events(request):
    events_obj = events.objects.filter(status="confirmed")
    events_obj_tentative = events.objects.filter(status="tentative")
    events_obj_late = events.objects.filter(status="late")
    context = {
        'events_obj':events_obj,
        'events_obj_tentative':events_obj_tentative,
        'events_obj_late':events_obj_late
    }
    return render(request,'events/events.html',context)

@login_required(login_url='login')
def view_event(request,id):
    event_obj = events.objects.get(id=id)
    products_obj = event_products.objects.filter(event=event_obj)
    context = {
        'products': products_obj,
        'event': event_obj
    }
    return render(request, 'events/event_detail.html',context)

@login_required(login_url='login')
def add_events(request):
    if request.user.is_superuser:
        products_obj = products.objects.all()
        if request.method == 'POST':
            client_name = request.POST.get('cl_name')
            event_location = request.POST.get('event_location')
            shipment_date = request.POST.get('shipment_date')
            return_date = request.POST.get('return_date')
            status = request.POST.get('status')

            product_ids = request.POST.get('product_ids')
            product_quantities = request.POST.get('product_quantities')
            temp_ids = product_ids.split(",")
            temp_quantities = product_quantities.split(",")

            print(return_date,"***********")

            #Create Event
            temp_shipment_date = shipment_date.split('-')
            temp_return_date = return_date.split('-')
            event_request_body = {
                'start':{
                    'dateTime': convert_to_RFC_datetime(int(temp_shipment_date[0]), int(temp_shipment_date[1]), int(temp_shipment_date[2]), 00, 00),
                    'timeZone': 'Asia/Taipei'
                },
                'end':{
                    'dateTime': convert_to_RFC_datetime(int(temp_return_date[0]), int(temp_return_date[1]), int(temp_return_date[2]), 00, 00),
                    'timeZone': 'Asia/Taipei'
                },
                'summary': client_name+"'s Event",
                'description': 'Shipment Date:'+shipment_date+' Return Date:'+return_date+' Location:'+event_location+' Status:'+status,
            }

            event = service.events().insert(calendarId=calander_id_chicago, body=event_request_body).execute()
            print(event)

            eventID = event['id']

            event_obj = events.objects.create(
                client_name=client_name,
                event_location=event_location,
                shipment_date=shipment_date,
                return_date=return_date,
                status=status, 
                google_event_id = eventID,      
                )
            event_obj.save()
            for x in range(len(temp_quantities)):
                if temp_quantities[x] != "" and int(temp_quantities[x]) > 0:
                    product_obj = products.objects.get(id=temp_ids[x])
                    if (int(product_obj.quantity_left) - int(temp_quantities[x])) > 0:
                        event_products_obj = event_products.objects.create(
                            quantity=temp_quantities[x],
                            event_products=product_obj,
                            event=event_obj
                        )
                        product_obj.quantity_left -= int(temp_quantities[x])

                        product_obj.save()
                        event_products_obj.save()
                    else:
                        event_obj.delete()
                        context = {
                            'products': products_obj,
                            'msg': "Out of range"
                        }
                        return render(request, 'events/add_events.html',context)
            return redirect('events')
        context = {
            'products': products_obj
        }
        return render(request, 'events/add_events.html',context)
    else:
        return redirect('events')


@login_required(login_url='login')
def edit_events(request,id):
    if request.user.is_superuser:
        events_obj = events.objects.get(id=id)
        event_products_obj = event_products.objects.filter(event=events_obj)
        all_products_obj = products.objects.all()
        products_list = []
        for p in all_products_obj:
            chk = False
            for event_p in event_products_obj:
                if p.id == event_p.event_products.id:
                    temp = {
                        'id': p.id,
                        'event_id':event_p.id,
                        'name': p.name,
                        'quantity':p.quantity,
                        'quantity_left':p.quantity_left,
                        'quantity_client_have': event_p.quantity
                    }
                    products_list.append(temp)
                    chk = True
                    break
            if chk == False:
                temp = {
                    'id': p.id,
                    'event_id':'no',
                    'name': p.name,
                    'quantity':p.quantity,
                    'quantity_left':p.quantity_left,
                    'quantity_client_have': 0
                }
                products_list.append(temp) 
        if request.method == 'POST':
            msg = False
            client_name = request.POST.get('cl_name')
            event_location = request.POST.get('event_location')
            shipment_date = request.POST.get('shipment_date')
            return_date = request.POST.get('return_date')
            status = request.POST.get('status')

            #update
            temp_shipment_date = shipment_date.split('-')
            temp_return_date = return_date.split('-')
            event_request_body = {
                'start':{
                    'dateTime': convert_to_RFC_datetime(int(temp_shipment_date[0]), int(temp_shipment_date[1]), int(temp_shipment_date[2]), 00, 00),
                    'timeZone': 'Asia/Taipei'
                },
                'end':{
                    'dateTime': convert_to_RFC_datetime(int(temp_return_date[0]), int(temp_return_date[1]), int(temp_return_date[2]), 00, 00),
                    'timeZone': 'Asia/Taipei'
                },
                'summary': client_name+"'s Event",
                'description': 'Shipment Date:'+shipment_date+' Return Date:'+return_date+' Location:'+event_location+' Status:'+status,
            }

            service.events().update(
                        calendarId=calander_id_chicago,
                        eventId=events_obj.google_event_id,
                        body=event_request_body).execute()

            events_obj.client_name = client_name
            events_obj.event_location = event_location
            events_obj.shipment_date = shipment_date
            events_obj.return_date = return_date
            events_obj.status = status
            events_obj.save()


            event_ids = request.POST.get('event_ids')
            product_ids = request.POST.get('product_ids')
            product_quantities = request.POST.get('product_quantities')

            temp_ids = product_ids.split(",")
            temp_quantities = product_quantities.split(",")
            temp_event_ids = event_ids.split(",")

            for x in range(len(temp_ids)-1):
                try:
                    temp_events = event_products.objects.get(id=temp_event_ids[x])
                    if temp_events.quantity != int(temp_quantities[x]):
                        print(temp_events.event_products.quantity_left,"left one**********")
                        print(temp_events.quantity,"add more")
                        temp_events.event_products.quantity_left += int(temp_events.quantity)
                        temp_events.event_products.save()
                        temp_events.delete()

                        if temp_quantities[x] != "" and int(temp_quantities[x]) > 0:
                            product_obj = temp_events.event_products
                            if (int(product_obj.quantity_left) - int(temp_quantities[x])) > 0:
                                create_event_products_obj = event_products.objects.create(
                                    quantity=temp_quantities[x],
                                    event_products=product_obj,
                                    event=events_obj
                                )
                                product_obj.quantity_left -= int(temp_quantities[x])
                                product_obj.save()
                                create_event_products_obj.save()
                            else:
                                msg = True
                except:
                    product_obj = products.objects.get(id=temp_ids[x])
                    if (int(product_obj.quantity_left) - int(temp_quantities[x])) > 0:
                        create_event_products_obj = event_products.objects.create(
                            quantity=temp_quantities[x],
                            event_products=product_obj,
                            event=events_obj
                        )
                        product_obj.quantity_left -= int(temp_quantities[x])

                        product_obj.save()
                        create_event_products_obj.save()
                    else:
                        msg = True

            if msg:
                context = {
                    'events_obj':events_obj,
                    'event_products_obj':event_products_obj,
                    'products': products_list,
                    'msg':msg
                }
                return render(request, 'events/edit_events.html',context)   
            else:
                return redirect('events')         
                
        context = {
            'events_obj':events_obj,
            'event_products_obj':event_products_obj,
            'products': products_list,
        }
        return render(request, 'events/edit_events.html',context)
    else:
        return redirect('events')

@login_required(login_url='login')
def delete_events(request,id):
    if request.user.is_superuser:
        events_obj = events.objects.get(id=id)
        #Delete Event
        service.events().delete(
            calendarId=calander_id_chicago,
            eventId=events_obj.google_event_id).execute()

        event_products_obj = event_products.objects.filter(event=events_obj)
        for e in event_products_obj:
            e.event_products.quantity_left = int(e.quantity) + e.event_products.quantity_left
            e.event_products.save()
        events_obj.delete()
    return redirect('events')

@login_required(login_url='login')
def search(request):
    if request.method == 'POST' and request.POST.get('search_date'):
        search_date = request.POST.get('search_date')
        events_obj = events.objects.distinct().filter(
            Q(shipment_date__lte = search_date) &
            Q(return_date__gte=search_date)
        )
        context={
            'search_date':search_date,
            'events_obj':events_obj
        }
        return render(request, 'events/search.html',context)
    if request.method == 'POST' and request.POST.get('search_date_low_range') and request.POST.get('search_date_heigh_range'):
        search_date_low_range = request.POST.get('search_date_low_range')
        search_date_heigh_range = request.POST.get('search_date_heigh_range')

        print(search_date_low_range,search_date_heigh_range,"*************")

        events_obj = events.objects.distinct().filter(
            Q(shipment_date__lte = search_date_low_range) &
            Q(return_date__lte=search_date_heigh_range) |
            Q(shipment_date__gte = search_date_low_range) &
            Q(return_date__gte=search_date_heigh_range) |
            Q(shipment_date__lte = search_date_low_range) &
            Q(return_date__gte=search_date_heigh_range)
        )
        context={
            'search_date_low_range':search_date_low_range,
            'search_date_heigh_range':search_date_heigh_range,
            'events_obj':events_obj
        }
        return render(request, 'events/search.html',context)
    return render(request, 'events/search.html')
