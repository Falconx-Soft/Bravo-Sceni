from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import events,event_products

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(shipment_date__day=day)
		d = ''
		for event in events_per_day:
			d += f"<li data-toggle='modal' data-target='#exampleModalLive{event.id}' class='evnet-list'> {event.client_name} </li><div id='exampleModalLive{event.id}' class='modal fade' tabindex='-1' role='dialog' aria-labelledby='exampleModalLive{event.id}Label' aria-hidden='true'><div class='modal-dialog' role='document'><div class='modal-content'><div class='modal-header'><h5 style='margin: 0px; line-height: 1.5; font-size: 18px;' id='exampleModalLive{event.id}Label'>Event</h5></div><div class='modal-body'><p><b>Client name:</b> {event.client_name}</p><p><b>Event location:</b> {event.event_location}</p><p><b>Shipment date:</b> {event.shipment_date}</p><p><b>Return date:</b> {event.return_date}</p><p><b>Status:</b> {event.status}</p><p style='text-align: center;'>----Products----</p>"

			products = event_products.objects.filter(event=event)

			for p in products:
				d += f"<p><b>{p.event_products.name}:</b> {p.quantity}</p>"

			d += "</div><div class='modal-footer'><button type='button' class='btn  btn-secondary' data-dismiss='modal'>Close</button></div></div></div></div>"

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events_obj = events.objects.filter(shipment_date__year=self.year, shipment_date__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events_obj)}\n'
		return cal