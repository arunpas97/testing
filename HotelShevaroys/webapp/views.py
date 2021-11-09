from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django_user_agents.utils import get_user_agent
# from webapp.forms import PaymentDetailsForm
import requests
import razorpay
import urllib
from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime , date,timedelta
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
# import pandas as pd 


# Payment Gateway
#old
#client = razorpay.Client(auth=("rzp_live_BStJ1GMUmGrT7O", "u1mRJzIb8Pwcjf3CfEVt9I6O"))
#new 22.01.2021
client = razorpay.Client(auth=("rzp_live_J8nQ5tgrIyEcQI", "Q4hlENYykxUtKGzAvKiYXv6K"))

# Create your views here.

def index(request):
	user_agent = get_user_agent(request)
	obj1 = Room.objects.all().order_by('-price')
	# print(datetime.now().strftime("%d/%m/%Y"))

	#curentr date
	cdate=datetime.now().strftime("%d/%m/%Y")
	a=datetime.now()+timedelta(days=-1)
	#Yesterday date
	pdate = a.strftime("%d/%m/%Y")
	print("Curent date : ",cdate, "pdate :",pdate)
	get=Reservation.objects.filter(Q(payment_status=True ) & (Q(bookOut=cdate) or Q(bookOut=pdate) ))
	# print(get)
	for i in get:
		if Room.objects.get(roomname=i.roomname):
			r=Room.objects.get(roomname=i.roomname)
			r.size = int(r.size) + int(i.noofroom)
			n=confom(user=i.user, resvno=i.id, name=i.name, phone=i.phone,email=i.email,roomname=i.roomname, roomamt=i.roomamt, noofroom=i.noofroom,adult=i.adult, exper=i.exper,kids=i.kids,bookIn=i.bookIn, bookOut=i.bookOut,amount=i.amount, t=i.t, tamount=i.tamount ,razorpayid=i.razorpayid, razorpay_payment_id=i.razorpay_payment_id)
			n.save()
			r.save()
		i.delete()

	if request.method =="POST":
		try:
			# print("request.POST")
			rr = []

			#for finding the reserved rooms on this time period for excluding from the query set
			for i in Reservation.objects.all():
				if str(i.bookIn) < str(request.POST['bookIn']) and str(i.bookOut) < str(request.POST['bookOut']):
					pass
				elif str(i.bookIn) > str(request.POST['bookIn']) and str(i.bookOut) > str(request.POST['bookOut']):
					pass
				else:
					rr.append(i.id)
			print("rr",rr)
			room = Room.objects.all().filter(capacity= int(request.POST['adult'])).exclude(id__in=rr)
			print("Room",room)
			if len(room) == 0:
				messages.warning(request,"Sorry No Rooms Are Available on this time period")
				return render(request,'index.html',locals())
		except Exception as e:
			return render(request,'index.html',locals())
	
	return render(request,"index.html",locals())

def room(request):
	user_agent = get_user_agent(request)
	obj1 = Room.objects.all().order_by('-price')

	return render(request,'room.html',locals())

def hall(request):
	return render(request,'hall.html',locals())
def service(request):
	return render(request,'service.html',locals())
def about(request):
	return render(request,'about.html',locals())
def gallery(request):
	return render(request,'gallery.html',locals())	
def contact(request):
	return render(request,'contact.html',locals())

# Rooms

def room_detail(request,roomname):
	user_agent = get_user_agent(request)
	obj2 = Room.objects.get(roomname=roomname)
	a=str(obj2.img.url)
	obj1 = Room.objects.all()
	for i in obj1:
		print(i.roomname)
		if Room.objects.get(roomname="Standard Room"):
			r=Room.objects.get(roomname="Standard Room")
			aa=str(r.img.url)

		if Room.objects.get(roomname="Bougainvilla Room"):
			r=Room.objects.get(roomname="Bougainvilla Room")
			b=str(r.img.url)
		if Room.objects.get(roomname="Rose Room"):
			r=Room.objects.get(roomname="Rose Room")
			c=str(r.img.url)
		if Room.objects.get(roomname="Dahlia Room"):
			obj=Room.objects.get(roomname="Dahlia Room")
			d=str(obj.img.url)
		if Room.objects.get(roomname="Orchid Room"):
			obj=Room.objects.get(roomname="Orchid Room")
			e=str(obj.img.url)
		if Room.objects.get(roomname="Deluxe Villa"):
			obj=Room.objects.get(roomname="Deluxe Villa")
			f=str(obj.img.url)
		if Room.objects.get(roomname="Luxury Villa"):
			obj=Room.objects.get(roomname="Luxury Villa")
			g=str(obj.img.url)

	return render(request,'rooms/room.html',locals())

def stdroom(request):
	return render(request,'rooms/stdroom.html',locals())
def bouvilla(request):
	return render(request,'rooms/bouvilla.html',locals())
def deluxeroom(request):
	return render(request,'rooms/deluxeroom.html',locals())
def dhaliaroom(request):
	return render(request,'rooms/dhaliaroom.html',locals())
def luxuryroom(request):
	return render(request,'rooms/luxuryroom.html',locals())
def roseroom(request):
	return render(request,'rooms/roseroom.html',locals())
def orchidroom(request):
	return render(request,'rooms/orchidroom.html',locals())

def register(request):
	user_agent = get_user_agent(request)
	if request.method == "POST":
		name = request.POST['name']
		mobile = request.POST['mobile']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		try:
			username = email
			usr = User.objects.create_user(username, email, pass1)
			usr.first_name = name
			usr.last_name = ""
			usr.save()
			obj = Profile(user=usr, name=name, mobile=mobile, email=email,pass1=pass1)
			obj.save()
			
			messages.success(request, 'Account Created Successfully:)')
			return redirect('login')
		except:
			messages.error(request, 'Username already exist Please enter another unique username!')
			return redirect('register')
	return render(request,"accounts/register.html",locals())

def Login(request):
	user_agent = get_user_agent(request)
	if request.method == 'POST':
		uname = request.POST['email']
		pass1 = request.POST['pass1']

		user = authenticate(username=uname, password=pass1)
		if user is not None:
			login(request, user)
			obj = Profile.objects.get(user = request.user)
			if obj.radmin_status == True:
				print(">>>>>>>>>>>>>>>> Reception admin",obj.radmin_status)
				messages.success(request, 'Welcome to Hotel Shevaroys, Reception Admin !!!')
				return redirect('superadmin1')
			if obj.admin_status == False & obj.radmin_status == False:
				messages.success(request, f'Welcome to Hotel Shevaroys !!!')
				print("Normal")
				return redirect('index')
			
			else:
				print(">>>>>>>>>>>>>>>>admin",obj.admin_status)
				messages.success(request, 'Welcome Hotel Shevaroys, Super Admin!!!')
				return redirect('superadmin')
		else:
			messages.error(request, 'Invalid credentials, Please try again! or Signup before login if not Registered!')
			return redirect('login')
	return render(request,"accounts/login.html",locals())

def Logout(request):
	user_agent = get_user_agent(request)
	if request.user.is_authenticated:
		logout(request)
		messages.success(request, 'You are Successfully Logged Out!')
		return redirect('index')

from datetime import datetime
date_format = "%d/%m/%Y"

def room_view(request,roomname):
	user_agent = get_user_agent(request)
	user = Profile.objects.get(user=request.user)
	r = Room.objects.get(roomname=roomname)

	return render(request,'room_view.html', locals())

def bookroom(request,roomname,price):
	user_agent = get_user_agent(request)
	user = Profile.objects.get(user=request.user)
	r = Room.objects.get(roomname=roomname)
	if request.method == "POST":
		name=request.POST['name']
		phone=request.POST['phone']
		email=request.POST['email']
		roomname=request.POST['roomname']
		roomamt=request.POST['roomamt']
		noofroom=request.POST['noofroom']
		if int(noofroom) <= r.size:
			adult=request.POST['adult']
			exper=request.POST['exper']
			kids=request.POST['kids']
			bookIn=request.POST['bookIn']

			if bookIn == r.date_disable:
				messages.warning(request,'{} Full on {}. Please Book Room for different date or Book different Room.'.format(r.roomname,bookIn))
				return redirect('room')
			elif bookIn == r.date_disable1:
				messages.warning(request,'{} Full on {}. Please Book Room for different date or Book different Room.'.format(r.roomname,bookIn))
				return redirect('room')
			elif bookIn == r.date_disable2:
				messages.warning(request,'{} Full on {}. Please Book Room for different date or Book different Room.'.format(r.roomname,bookIn))
				return redirect('room')

			bookOut=request.POST['bookOut']
			
			a=datetime.strptime(str(bookIn), date_format)
			b=datetime.strptime(str(bookOut), date_format)
			delta = b - a
			delta.days
			amount=(delta.days) * int(roomamt) * int(noofroom)
			print('#########amount',amount)
			if amount > 1000 & amount > 7499:
				t=round(amount*0.12)
			elif amount >7500:
				t=round(amount*0.18)
			else:
				t=0
			tamount= round(amount + t)
			ttamount=tamount*100

			pre_bookIn = datetime.strftime(datetime.date(a) - timedelta(hours=24), date_format)
			print('@@@@@@@@@@pre_bookIn:',pre_bookIn)

			# Maximum Price for Perticular date
			if r.max_price_date1 == bookIn:
				amount=(delta.days) * int(r.price2) * int(noofroom)
				print('$$$$$$$$amount',amount)
				ttamount = amount*100
				messages.warning(request,"You are Selected Special date. So your Room rent is {}".format(amount))
				print('!!!!!!!!ttamount',ttamount)
			elif r.max_price_date2 == bookIn:
				amount=(delta.days) * int(r.price2) * int(noofroom)
				print('$$$$$$$$amount',amount)
				ttamount = amount*100
				messages.warning(request,"You are Selected Special date. So your Room rent is {}".format(amount))
				print('!!!!!!!!ttamount',ttamount)

			# Restrict Adult capacity
			if noofroom == "2":
				adult = r.capacity*2
			elif noofroom == "3":
				adult = r.capacity*3
			elif noofroom == "4":
				adult = r.capacity*4
			elif noofroom == "5":
				adult = r.capacity*5
			else:
				adult = r.capacity

			# Add extra amount for extra person
			if exper == "1":
				ttamount = ttamount+80000 # in paise ₹.800.00
			elif exper == "2":
				ttamount = ttamount+160000 # in paise ₹.1,600.00
			elif exper == "3":
				ttamount = ttamount+240000 # in paise ₹.2,400.00
			elif exper == "4":
				ttamount = ttamount+320000 # in paise ₹.3,200.00
			elif exper == "5":
				ttamount = ttamount+400000 # in paise ₹.4,000.00
			else:
				ttamount = ttamount+0

			# Razorpay Payment Integration
			data = {
	                'amount':ttamount,
	                'currency': 'INR',
	                'receipt': str(id),
	                'payment_capture':'0',
	                'notes': {
	                    'name': name
	                }
	            }
			
			
			resp = client.order.create(data=data)
			print(resp)
			print("razorpay_order :",resp['id'])
			
			no=resp['id']
			am=resp['amount']
			n=name
			rn=roomname
			p=phone
			e=email


			context = {'id': resp['id'],'amount': resp['amount'],'name': name,'roomname': roomname,
	            'phone':phone,'email':email }

			booking = Reservation(user=request.user, name=name, phone=phone, 
	        	email=email,roomname=roomname, roomamt=roomamt, noofroom=noofroom,
	        	adult=adult, exper=exper,kids=kids,bookIn=bookIn, bookOut=bookOut,
	        	amount=amount, t=t, tamount=tamount ,razorpayid=resp['id'],pre_bookIn=pre_bookIn)
			booking.save()

				
			
			# print(".............Reservation Conform.........")
			# messages.success(request, 'You Room Successfully Booked!')
			# return redirect('payment', context=context )
			return redirect('payment', no=no, n=n, rn=rn, am=am, p=p , e=e )
						
		else:
			messages.success(request, 'Your Room Counts are High... Available Room Count : {}'.format(r.size))
			return redirect('room')

		
		# return redirect('payment', { 'context':context } )
		# return render('booking/payment.html', context=context )
		# return render(request,'booking/payment.html',context)
		#return render(request,'booking/success.html',context=context)
		# return redirect('payment',context)
		
	return render(request, 'booking/bookroom.html', locals())


def payment(request,no,n,rn,am,p,e):
	
	# print(type(context))
	# print(context)
	print("Name :",n)
	print("Id:",no)
	print("Room Name:",rn)
	print("Amount :",am)
	print("Phone :",p)
	print("Email: ",e)
	
	# resv = Reservation.objects.get(razorpayid=no)
	# resv.payment_status = True
	# r=Room.objects.get(roomname=resv.roomname)
	# print("no of room insertd >>>>>>>>>>>>>>>>> :",resv.noofroom)
	# r.size = int(r.size) - int(resv.noofroom)
	# r.save()
	# print("Updated RooM Size",r.size)
	# resv.save()

	if request.method == 'POST':
	 	data = request.POST
	 	params_dict = {
	 		'razorpay_order_id': data['razorpay_order_id'],
	 		'razorpay_payment_id': data['razorpay_payment_id'],
	 		'razorpay_signature': data['razorpay_signature']
	 	}

	 	status = client.utility.verify_payment_signature(params_dict)
	 	resv = Reservation.objects.get(razorpayid=data['razorpay_order_id'])
	 	resv.razorpay_payment_id = data['razorpay_payment_id']
	 	resv.payment_status = True
	 	room=Room.objects.get(roomname=resv.roomname)
	 	room.size = int(room.size) - int(resv.noofroom)
	 	room.save()
	 	
	 	resv.save()
	 	n=resv.name
	 	o=resv.id

	 	# Razorpay Auto Capture
	 	payment_id = resv.razorpay_payment_id
	 	payment_amount = int(resv.tamount)*100
	 	payment_currency = "INR"
	 	resp = client.payment.capture(payment_id, payment_amount, {"currency":"payment_currency"})

	 	return redirect('success', n=n,o=o)
	return render(request, 'booking/payment.html' , locals())



def success(request,o,n):
	print("Name",n)
	print("id",o)
	name=n
	oid=o
	print("Name",name)
	print("id",oid)
	user_agent = get_user_agent(request)
	a=Reservation.objects.get(id=oid)
	bi=a.bookIn
	bo=a.bookOut
	inr = "₹"
	email_from = settings.EMAIL_HOST_USER

	data = {
	'id':a.id,
	'name':a.name,
	'adult':a.adult,
	'exper':a.exper,
	'kids':a.kids,
	'roomname':a.roomname,
	'noofroom':a.noofroom,
	'bookIn':a.bookIn,
	'bookOut':a.bookOut,
	'razorpay_payment_id':a.razorpay_payment_id,
	'amount':a.amount,
	't':a.t,
	'tamount':a.tamount,
	}
	
	# Hotel Reservation mail 
	recipient_list = ['frontoffice@hotelshevaroys.com','info@hotelshevaroys.com']
	# recipient_list = ['i18nsolutions@gmail.com','dhanya3196@gmail.com']
	
	subject = 'Reservation : '+str(date.today())
	message = """Hey There is new reservation is done by the customer\n
        ID         			   : """+str(a.id)+"""
        Name       		       : """+str(a.name)+"""
        Adult      		       : """+str(a.adult)+"""
        Extra Persons      	   : """+str(a.exper)+"""
        Kids       		       : """+str(a.kids)+"""
        Room Name   		   : """+str(a.roomname)+"""
        Number of Room         : """+str(a.noofroom)+"""
        Check In               : """+str(a.bookIn)+"""
        Check Out              : """+str(a.bookOut)+"""
        Room Amount            : """+str(inr) +str(a.amount)+"""
        Tax Amount             : """+str(inr) +str(a.t)+"""
        Total Amount           : """+str(inr) +str(a.tamount)+"""
        
        
        Contact Details\n
        Mobile :"""+str(a.phone)+"""
        Email  :"""+str(a.email)+""" """
   

	send_mail( subject, message, email_from, recipient_list )

	# Customer Reservation mail

	mail_html = get_template('confirm_booking_email.html').render(data)
	sender_address = 'reservations@hotelshevaroys.com'
	sender_pass = 'hotelshevaroys@#123'
	receiver_address = a.email
	print('>>>>>>>>>>>>>>>>>>>>',a.email)
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Booking Conformed !'
	message.attach(MIMEText(mail_html, 'html'))
	session = smtplib.SMTP('smtp.zoho.in', 587)
	session.starttls()
	session.login(sender_address, sender_pass)
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()


	messages.success(request, f'Your Booking was Registered Successfully. Please Check Your Email:)')

	 # if request.method == 'POST':
	 # 	data = request.POST
	 # 	print(data)
	 # 	resv = Reservation.objects.get(razorpayid=data['razorpay_order_id'])
	 # 	resv.payment_status = True
	 # 	resv.save()
	return render(request, 'booking/success.html',locals())
	
def mybooking(request):
	user_agent = get_user_agent(request)
	if request.user.is_authenticated == False:
		return redirect('Login')
	user = User.objects.all().get(id=request.user.id)
	
	# a = date.today()
	# a = a.strftime(date_format)
	bookings = Reservation.objects.filter(user=request.user, cancel=False, checkout=False)[::-1]
	if not bookings:
		messages.warning(request,"No Bookings Found")
	return render(request, 'booking/mybooking.html', locals())

def previous_booking(request):
	user_agent = get_user_agent(request)
	if request.user.is_authenticated == False:
		return redirect('Login')
	user = User.objects.all().get(id=request.user.id)
	bookings = Reservation.objects.filter(user=request.user, checkout=True)[::-1]
	if not bookings:
		messages.warning(request,"No Previous Bookings Found")
	return render(request, 'booking/previous_booking.html', locals())

def cancel_booking_view(request,id):
	user_agent = get_user_agent(request)
	if request.user.is_authenticated == False:
		return redirect('Login')
	user = User.objects.all().get(id=request.user.id)

	obj = Reservation.objects.filter(id = id)

	return render(request,'booking/cancel_booking_view.html',locals())

def cancel_booking(request,id):
	obj = Reservation.objects.get(id = id)

	# a=datetime.strptime(str(obj.bookIn), date_format)
	# b = datetime.strftime(datetime.date(a) - timedelta(1), date_format)
	# print('@@@@@@@@@@@@b',b)
	# print('$$$$$$$$$$$$pre_bookIn',obj.pre_bookIn)
	a = date.today()
	a = a.strftime(date_format)

	print('@@@@@@@@@@@@a',a)
	print('$$$$$$$$$$$$pre_bookIn',obj.pre_bookIn)
	
	if obj.pre_bookIn != a:
		obj.cancel=True
		
		# Razorpay Auto Refund
		ttamount = int(obj.tamount)*100
		payment_id = obj.razorpay_payment_id
		payment_amount = ttamount
		notes = {'name': obj.name}
		resp = client.payment.refund(payment_id, payment_amount)

		obj.save()

		# Cancellation Mail
		mail_html = get_template('cancel_booking_email.html').render({"name": obj.name})
		sender_address = 'reservations@hotelshevaroys.com'
		sender_pass = 'hotelshevaroys@#123'
		receiver_address = obj.email
		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_address
		message['Subject'] = 'Booking Cancelled!'
		message.attach(MIMEText(mail_html, 'html'))
		session = smtplib.SMTP('smtp.zoho.in', 587)
		session.starttls()
		session.login(sender_address, sender_pass)
		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()

		messages.success(request,"Booking Cancelled Successfully! Please Check Your Email!")

		return redirect('cancel_booking_list')
	else:
		print('#############no')
		messages.success(request,"Cannot Cancel Booking before 24 hours!")

		return redirect('mybooking')
	

def cancel_booking_list(request):
	user_agent = get_user_agent(request)
	if request.user.is_authenticated == False:
		return redirect('Login')
	user = User.objects.all().get(id=request.user.id)
	
	bookings = Reservation.objects.filter(user=request.user, cancel=True)[::-1]
	if not bookings:
		messages.warning(request,"No Cancelled Bookings Found")
	return render(request, 'booking/cancel_booking_list.html', locals())

def privacy(request):
	
	return render(request, 'privacy.html', locals())


def feedback(request):
	if request.method == "POST":
		name=request.POST['name']
		email=request.POST['email']
		phone=request.POST['phone']
		feedback=request.POST['feedback']

		booking = Feedback(name=name,email=email,phone=phone,feedback=feedback)
		booking.save()
		messages.success(request,"Feedback Sended Successfully:)")	
		return redirect('index')
	return render(request, 'feedback.html', locals())
	
# class StoreDetails(View):

#     def get(self,request):
#         usr  = request.user
#         prof  = request.user.profile
#         template = 'store.html'
#         form =PaymentDetailsForm()
#         # roomname = request.POST.get('roomname')
#         # amt = request.POST.get('amount')
#         return render(request,template,locals())

#     def post(self,request):
#         usr  = request.user
#         prof  = request.user.profile
#         form = PaymentDetailsForm(request.POST or None)        
#         roomname = request.POST.get('roomname')
#         amt = request.POST.get('amount')
#         # copn = request.POST.get('coupon') 
#         # print("coupon>>>>>",copn) 
#         # if copn == 'PY50':
#         #     amt1 = int(int(amt)*50/100)
#         # else:
#         #     amt1 = int(amt)
        
#         if form.is_valid():
#             obj = form.save()
#             template = 'get.html' 
#         else:
#             form = PaymentDetailsForm()
#             template = 'store.html'
#         return render(request,template,locals())


