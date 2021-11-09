from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from webapp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
# from webapp.forms import PaymentDetailsForm
import requests
import razorpay

from .forms import *


# Payment Gateway
# client = razorpay.Client(auth=("rzp_live_BStJ1GMUmGrT7O", "u1mRJzIb8Pwcjf3CfEVt9I6O"))
key = 'rzp_live_BStJ1GMUmGrT7O'
secret = 'u1mRJzIb8Pwcjf3CfEVt9I6O'

# razorpay_client = razorpay.Client(auth=(key, secret))
 


# Create your views here.
def index(request):
	obj1 = Room.objects.all()
	if Room.objects.get(roomname="Standard Room"):
		obj=Room.objects.get(roomname="Standard Room")
		a=str(obj.img.url[14:])
	elif Room.objects.get(roomname="Bougainvilla Room"):
		obj=Room.objects.get(roomname="Bougainvilla Room")
		a=str(obj.img.url[14:])
	elif Room.objects.get(roomname="Rose Room"):
		obj=Room.objects.get(roomname="Rose Room")
		a=str(obj.img.url[14:])
	elif Room.objects.get(roomname="Dahlia Room"):
		obj=Room.objects.get(roomname="Dahlia Room")
		a=str(obj.img.url[14:])
	elif Room.objects.get(roomname="Orchid Room"):
		obj=Room.objects.get(roomname="Orchid Room")
		a=str(obj.img.url[14:])
	elif Room.objects.get(roomname="Deluxe Villa"):
		obj=Room.objects.get(roomname="Deluxe Villa")
		a=str(obj.img.url[14:])
	elif Room.objects.get(roomname="Luxury Villa"):
		obj=Room.objects.get(roomname="Luxury Villa")
		a=str(obj.img.url[14:])
	if request.method =="POST":
		# rr = []

		# #for finding the reserved rooms on this time period for excluding from the query set
		# for i in Reservation.objects.all():
		# 	if str(i.bookIn) < str(request.POST['bookIn']) and str(i.bookOut) < str(request.POST['bookOut']):
		# 		pass
		# 	elif str(i.bookIn) > str(request.POST['bookIn']) and str(i.bookOut) > str(request.POST['bookOut']):
		# 		pass
		# 	else:
		# 		rr.append(i.id)
		# print(",,,,,,,,,,,,,, rr :",rr)
		# room = Room.objects.all().filter(capacity= int(request.POST['adult']) ).exclude(id__in=rr)
		# print(",,,,,,,,,,,,,, room :",room)
		# if len(room) == 0:
		# 	messages.warning(request,"Sorry No Rooms Are Available on this time period")
		# 	return render(request,'index.html',locals())
		try:
			print("request.POST")
			rr = []

			#for finding the reserved rooms on this time period for excluding from the query set
			for i in Reservation.objects.all():
				if str(i.bookIn) < str(request.POST['bookIn']) and str(i.bookOut) < str(request.POST['bookOut']):
					pass
				elif str(i.bookIn) > str(request.POST['bookIn']) and str(i.bookOut) > str(request.POST['bookOut']):
					pass
				else:
					rr.append(i.id)
			print(rr)
			room = Room.objects.all().filter(capacity= int(request.POST['adult'])).exclude(id__in=rr)
			print(room)
			if len(room) == 0:
				messages.warning(request,"Sorry No Rooms Are Available on this time period")
				return render(request,'index.html',locals())
		except Exception as e:
			return render(request,'index.html',locals())
	
	return render(request,"index.html",locals())

def room(request):
	obj1 = Room.objects.all()
	if Room.objects.get(roomname="Standard Room"):
		obj=Room.objects.get(roomname="Standard Room")
		a=str(obj.img.url[14:])
	# elif Room.objects.get(roomname="Bougainvilla Room"):
	# 	obj=Room.objects.get(roomname="Bougainvilla Room")
	# 	a=str(obj1.img.url[14:])
	# elif Room.objects.get(roomname="Rose Room"):
	# 	obj=Room.objects.get(roomname="Rose Room")
	# 	a=str(obj1.img.url[14:])
	# elif Room.objects.get(roomname="Standard Room"):
	# 	obj=Room.objects.get(roomname="Standard Room")
	# 	a=str(obj1.img.url[14:])
	# elif Room.objects.get(roomname="Standard Room"):
	# 	obj=Room.objects.get(roomname="Standard Room")
	# 	a=str(obj1.img.url[14:])
	# elif Room.objects.get(roomname="Standard Room"):
	# 	obj=Room.objects.get(roomname="Standard Room")
	# 	a=str(obj1.img.url[14:])
	# elif Room.objects.get(roomname="Standard Room"):
	# 	obj=Room.objects.get(roomname="Standard Room")
	# 	a=str(obj1.img.url[14:])
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
	obj1 = Room.objects.get(roomname=roomname)
	a=str(obj1.img.url[14:])
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
			messages.error(request, 'Account Created Successfully!')
			return redirect('login')
		except:
			messages.error(request, 'Username already exist please enter another unique username!')
			return redirect('register')
	return render(request,"accounts/register.html",locals())

def Login(request):
	if request.method == 'POST':
		uname = request.POST['email']
		pass1 = request.POST['pass1']

		user = authenticate(username=uname, password=pass1)
		if user is not None:
			login(request, user)
			obj = Profile.objects.get(user = request.user)
			if obj.admin_status == False:
				messages.success(request, 'Welcome to Hotel Shevaroys !!!')
				return redirect('index')
			else:
				print(">>>>>>>>>>>>>>>>admin",obj.admin_status)
				messages.success(request, 'Welcome Hotel Shevaroys, Super Admin!!!')
				return redirect('superadmin')
		else:
			messages.error(request, 'Invalid credentials, Please try again! or signup before login if not registered!')
			return redirect('login')
	return render(request,"accounts/login.html",locals())

def Logout(request):
	if request.user.is_authenticated:
		logout(request)
		messages.success(request, 'You are successfully logged out!')
		return redirect('index')

from datetime import datetime
date_format = "%d/%m/%Y"
def bookroom(request,roomname,price):
	user = Profile.objects.get(user=request.user)
	# print(">>>>>>>>>>>>>>",user)
	# ttamount=int(100)
	if request.method == "POST":
		# form = ReservationForm(request.POST)
  #       if form.is_valid():
  #           Reservation = form.save()
		name=request.POST['name']
		phone=request.POST['phone']
		email=request.POST['email']
		roomname=request.POST['roomname']
		roomamt=request.POST['roomamt']
		noofroom=request.POST['noofroom']
		adult=request.POST['adult']
		exper=request.POST['exper']
		kids=request.POST['kids']
		bookIn=request.POST['bookIn']
		bookOut=request.POST['bookOut']
		a=datetime.strptime(str(bookIn), date_format)
		b=datetime.strptime(str(bookOut), date_format)
		delta = b - a
		delta.days
		amount=(delta.days) * int(roomamt) * int(noofroom)
		if amount > 1000 & amount > 7499:
			t=round(amount*0.12)
		elif amount >7500:
			t=round(amount*0.18)
		else:
			t=0
		tamount= round(amount + t)
		ttamount=tamount*100

		print(">>>>>>>>>>>>> No Of days: ",delta.days)
		print(">>>>>>>>>>>>> Room Rent: ",amount)
		print(">>>>>>>>>>>>> tax: ",t)
		print(">>>>>>>>>>>>> total: ",tamount)
		print(">>>>>>>>>>>>> total: ",ttamount)

		 data = {
                'amount':ttamount,
                'currency': 'INR',
                'receipt': str(id),
                'payment_capture':'0',
                'notes': {
                    'name': name
                }
            }
		
		
		razorpay_client = razorpay.Client(auth=(key, secret))
		order = razorpay_client.order.create(dict(amount=ttamount, currency='INR', payment_capture='0'))
		print(order)
		print("razorpay_order :",order['id'])
		payment_id = order['id']
			# print(order)
			# url = 'https://api.razorpay.com/v1/payments/%s/capture' % str(payment_id)
			# resp = requests.post(url, data={'amount':int(ttamount)}, auth=(key, secret))
			# if resp.status_code == 200:
			# 	data = {"body": request.body, "contetn": resp.text}
			# 	RazorpayResponsew.objects.create(response=data,status="Success",user=name,mobile=phone,roomname=roomname, tamount=tamount)
			# 	booking=Reservation(user=request.user, name=name, phone=phone, email=email,
			# 	roomname=roomname, roomamt=roomamt, noofroom=noofroom,adult=adult, exper=exper,kids=kids,
			# 	bookIn=bookIn, bookOut=bookOut,amount=amount, t=t, tamount=tamount ,razorpayid=order['id'])
			# 	booking.save()
			# 	print("Payment Success")
			# 	# print(".............Reservation Conform.........")
			# 	messages.success(request, 'You Room Successfully Booked! % Payment Was Done !!!')
			# 	return render(request, 'index.html',locals())
			# elif resp.status_code == 400:
			# 	data = {"body": request.body, "contetn": resp.text}
			# 	RazorpayResponsew.objects.create(response=data,status="Failed",user=name,mobile=phone,roomname=roomname, tamount=tamount)
			# 	print("Payment UnSuccess")
			# 	messages.success(request, 'You Payment Was Not Done.. We Will Verify Shortly')
			# 	return render(request, 'index.html',locals())
			# else:
			# 	data = {"body": request.body, "contetn": resp.text}
			# 	RazorpayResponsew.objects.create(response=data,status="Pending",user=name,mobile=phone,roomname=roomname, tamount=tamount)
			# 	print("Payment Pending")
			# 	messages.success(request, 'Hmm Failed we will verify shortly')
			# 	return render(request, 'index.html')

		# print(".............Reservation Conform.........")
		# messages.success(request, 'You Room Successfully Booked!')

		return redirect('index')
	
		
	return render(request, 'booking/bookroom.html', locals())


def payment(request):
	# user = Profile.objects.get(user=request.user)
	# a=Reservation.objects.filter(user=user.user)
	# print(len(a))
	# c=a.count()
	# l=a[1] # last Booking Details of the User
	# print(len(a))
	# print("Last Amount",l.tamount)
	# print(l.roomname, l.id)
	# print(">>>>>>>>>>",l)

	# tamount = int(l.tamount)
	# ttamount =tamount*100
	# print(tamount) 
	
	# order_currency = 'INR'
	# # razorpay_client.payment.capture(tamount)
	# order = razorpay_client.order.create(dict(amount=tamount*100, currency=order_currency, payment_capture='1'))
	# print("razorpay_order :",order['id'])
	# l.razorpayid =order['id']
	# l.save()
	# print("++++++++++++++++++++++++",l.razorpayid)
	# payment_id = l.razorpayid
	# print("++++++++++++++++++++++++",payment_id)
	# url = 'https://api.razorpay.com/v1/payments/%s/capture' % str(payment_id)
	# resp = requests.post(url, data={'amount':int(tamount)*100}, auth=(key, secret))
	# if resp.status_code == 200:
	# 	data = {"body": request.body, "contetn": resp.text}
	# 	RazorpayResponsew.objects.create(response=data,status="Success",user=l.name,mobile=l.phone,roomname=l.roomname, tamount=l.tamount)
	# 	print("Payment Success")
	# 	messages.success(request, 'You Payment Was Done !!!')
	# 	return render(request, 'index.html',locals())
	# elif resp.status_code == 400:
	# 	data = {"body": request.body, "contetn": resp.text}
	# 	RazorpayResponsew.objects.create(response=data,status="Failed",user=l.name,mobile=l.phone,roomname=l.roomname, tamount=l.tamount)
	# 	print("Payment UnSuccess")
	# 	messages.success(request, 'You Payment Was Not Done.. We Will Verify Shortly')
	# 	return render(request, 'index.html',locals())
	# else:
	# 	data = {"body": request.body, "contetn": resp.text}
	# 	RazorpayResponsew.objects.create(response=data,status="Pending",user=l.name,mobile=l.phone,roomname=l.roomname, tamount=l.tamount)
	# 	print("Payment Pending")
	# 	messages.success(request, 'Hmm Failed we will verify shortly')
	# 	return render(request, 'index.html')

	return render(request, 'booking/payment.html' , locals())


@csrf_exempt
def success(request):
	if request.method=="POST":
		a=request.POST
		print(a)
	return render(request, 'booking/success.html', locals())
	
def mybooking(request):
	if request.user.is_authenticated == False:
		return redirect('Login')
	user = User.objects.all().get(id=request.user.id)
	print(user)
	bookings = Reservation.objects.all().filter(user=request.user)
	print(bookings)
	if not bookings:
		messages.warning(request,"No Bookings Found")
	return render(request, 'booking/mybooking.html', locals())


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


