from django.shortcuts import render, redirect
from .models import *
from products.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.views import generic
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='login'), name='dispatch')
class CalendarView(generic.ListView):
    model = events
    template_name = 'events/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

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

            event_obj = events.objects.create(
                client_name=client_name,
                event_location=event_location,
                shipment_date=shipment_date,
                return_date=return_date,
                status=status,    
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

        events_obj = events.objects.distinct().filter(
            Q(shipment_date__gte = search_date_low_range) &
            Q(shipment_date__lte=search_date_heigh_range) |
            Q(return_date__gte = search_date_low_range) &
            Q(return_date__lte=search_date_heigh_range)

        )

        context={
            'search_date_low_range':search_date_low_range,
            'search_date_heigh_range':search_date_heigh_range,
            'events_obj':events_obj
        }
        return render(request, 'events/search.html',context)
    return render(request, 'events/search.html')
