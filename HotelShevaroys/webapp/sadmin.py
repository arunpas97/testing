from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django_user_agents.utils import get_user_agent
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from datetime import datetime , date,timedelta
from django.utils import timezone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template


@login_required
def superadmin(request):
    user=Profile.objects.get(user=request.user)
    user.name
    print(">>>>>>>>>>>>>",user.name)
    
    obj1 = Room.objects.all()
    obj2 = Reservation.objects.all()
    obj3 = Profile.objects.all()
    c = confom.objects.all()
    cc=c.count()
    print(" Previous Conformed Booking",cc)
    cb=Reservation.objects.filter(payment_status=True)
    cbc=cb.count()
    print("Succes Payment",cbc)
    ucb=Reservation.objects.filter(payment_status=False)
    ucbc=ucb.count()
    print("failure Payment",ucbc)
    t=cc+cbc+ucbc
    print("Total Counts........: ",t)

    rcount=obj1.count()
    bcount=obj2.count()
    ucount=obj3.count()
    return render(request,"dash/index.html",locals())

@login_required
def srooms(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj1 = Room.objects.all().order_by('price')
    
    return render(request,"dash/rooms.html",locals())

@login_required
def addroom(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    # print("Start if")
    if request.method == "POST":
        print(" if inside Start")
        roomname=request.POST['roomname']
        roomtype=request.POST['roomtype']
        capacity=request.POST['capacity']
        price=request.POST['price']
        # price2=request.POST['price2']
        size=request.POST['size']
        # img=request.FILES['img']
        dis=request.POST['dis']
        status=request.POST['status']

        addroom=Room(roomname=roomname, roomtype=roomtype, capacity=capacity,
            price=price, size=size, img=request.FILES['img'], dis=dis, status=status)
        addroom.save()

        print(".............room added success.........")
        messages.success(request,'New Room Was Added Successfully')
        return redirect('superadmin')  
        
    return render(request, "dash/addroom.html",locals())


#editroom
@login_required
def editroom(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    data1 = Room.objects.get(id=id)
    u=Profile.objects.get(user=request.user)
    if request.method == 'POST':
        roomname=request.POST['roomname']
        roomtype=request.POST['roomtype']
        capacity=request.POST['capacity']
        price=request.POST['price']
        price2=request.POST['price2']
        size=request.POST['size']
        # img=request.FILES['img']
        dis=request.POST['dis']
        status=request.POST['status']
        date_disable=request.POST['date_disable']
        date_disable1=request.POST['date_disable1']
        date_disable2=request.POST['date_disable2']
        max_price_date1=request.POST['max_price_date1']
        max_price_date2=request.POST['max_price_date2']
        data1.roomname =roomname
        data1.roomtype = roomtype
        data1.capacity = capacity
        data1.price = price 
        data1.price2 = price2
        data1.size =size
        # data1.img = request.FILES['img']
        data1.dis = dis
        data1.status = status
        data1.date_disable = date_disable 
        data1.date_disable1 = date_disable1
        data1.date_disable2 = date_disable2
        data1.max_price_date1 = max_price_date1
        data1.max_price_date2 = max_price_date2

        data1.save()
        messages.success(request, 'Room Updates Successfully:)')
        return redirect("srooms")        
    
    return render(request, "dash/editroom.html",locals())

@login_required
def booking(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    if request.method == "POST":
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        roomname=request.POST['roomname']
        noofroom=request.POST['noofroom']
        adult=request.POST['adult']
        exper=request.POST['exper']
        kids=request.POST['kids']
        bookIn=request.POST['bookIn']
        bookOut=request.POST['bookOut']
        amount=request.POST['amount']
        t=request.POST['t']
        tamount=request.POST['tamount']
        razorpayid=request.POST['razorpayid']
        

        booking=Reservation(user=request.user, name=name, phone=phone, email=email,
            roomname=roomname, noofroom=noofroom,adult=adult, exper=exper,kids=kids,
            bookIn=bookIn, bookOut=bookOut,amount=amount,t=t,tamount=tamount,razorpayid=razorpayid,payment_status=True)
        booking.save()
        messages.success(request,'Booking Successfully')
        return render(request,'superadmin')  
        
    return render(request, "dash/booking.html",locals())


#order
@login_required
def bookinglist(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Profile.objects.all()
    obj1 = Reservation.objects.all()
    c=Reservation.objects.filter(payment_status=True, cancel=False, checkout=False)[::-1]
    # count=c.count()

    return render(request, "dash/bookinglist.html",locals())

@login_required
def search_bookinglist(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(payment_status=True) & 
                Q(cancel=False) & 
                Q(checkout=False)
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search) | 
                Q(razorpay_payment_id__icontains=search)
            )
        )[::-1]
        return render(request,'dash/search_bookinglist.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/search_bookinglist.html',{})

@login_required
def checkin_view(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c = Reservation.objects.filter(id = id)
    return render(request,'dash/checkin_view.html',locals())

@login_required
def checkin_conform(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Reservation.objects.get(id = id)
    obj.checkin=True
    obj.checkin_time = datetime.now().time().replace(microsecond=0)
    obj.save()

    # Checkin Mail
    data = {
    'name':obj.name,
    'checkin_time':obj.checkin_time,
    }

    mail_html = get_template('checkin_email.html').render(data)
    sender_address = 'reservations@hotelshevaroys.com'
    sender_pass = 'hotelshevaroys@#123'
    receiver_address = obj.email
    print('!!!!!!!!!!!!',receiver_address)
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Checkin Successfully!'
    message.attach(MIMEText(mail_html, 'html'))
    session = smtplib.SMTP('smtp.zoho.in', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


    messages.success(request,"Booking CheckedIn Successfully!")

    return redirect('bookinglist')

@login_required
def checkout_view(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c = Reservation.objects.filter(id = id)
    return render(request,'dash/checkout_view.html',locals())

@login_required
def checkout_conform(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Reservation.objects.get(id = id)
    obj.checkout=True
    obj.checkout_time = datetime.now().time().replace(microsecond=0)
    obj.save()

    # Checkout mail
    mail_html = get_template('checkout_email.html').render({"name": obj.name})
    sender_address = 'reservations@hotelshevaroys.com'
    sender_pass = 'hotelshevaroys@#123'
    receiver_address = obj.email
    print('!!!!!!!!!!!!',receiver_address)
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'CheckOut Successfully!'
    message.attach(MIMEText(mail_html, 'html'))
    session = smtplib.SMTP('smtp.zoho.in', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    messages.success(request,"Booking Checkedout Successfully!")

    return redirect('prevbooking')

@login_required
def prevbooking(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c=Reservation.objects.filter(checkout=True)[::-1]
    # c=confom.objects.all()[::-1]
    # count=c.count()

    return render(request, "dash/prevbooking.html",locals())

@login_required
def search_prevbooking(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(checkout=True) 
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search) | 
                Q(razorpay_payment_id__icontains=search)
            )
        )[::-1]
        return render(request,'dash/search_prevbooking.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/search_prevbooking.html',{})

@login_required
def unbookinglist(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Profile.objects.all()
    obj1 = Reservation.objects.all()
    c=Reservation.objects.filter(payment_status=False)[::-1]
    # count=c.count()    

    return render(request, "dash/unbookinglist.html",locals())

@login_required
def search_unbookinglist(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(payment_status=False) 
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search)
            )
        )[::-1]
        return render(request,'dash/search_unbookinglist.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/search_unbookinglist.html',{})

@login_required
def cancellist(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c=Reservation.objects.filter(cancel=True)[::-1]
 
    return render(request, "dash/cancellist.html",locals())

@login_required
def search_cancellist(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(cancel=True) 
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search)
            )
        )[::-1]
        return render(request,'dash/search_cancellist.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/search_cancellist.html',{})

@login_required
def sinvoice(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c=Reservation.objects.filter(payment_status=True)
    count=c.count()
    return render(request, "dash/invoice.html",locals())

@login_required
def updateimg(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    if request.method == 'POST':
        room = request.POST['room']
        img = request.FILES['img']
        img2 = request.FILES['img2']
        img3 = request.FILES['img3']
        img4 = request.FILES['img4']

        r=Room.objects.get(roomname=room)
        r.img = img
        r.img2 = img2
        r.img3 = img3
        r.img4 = img4
        r.save()
        messages.success(request,'Room Image Was Changed Successfully!!!')
        return redirect('srooms')

    return render(request, "dash/updateimg.html",locals())

def customer_feedback(request):
    fb = Feedback.objects.all()
    return render(request,"dash/customer_feedback.html",locals())

#Reception User Profile

@login_required
def superadmin1(request):
    user=Profile.objects.get(user=request.user)
    user.name
    print(">>>>>>>>>>>>>",user.name)
    
    obj1 = Room.objects.all()
    obj2 = Reservation.objects.all()
    obj3 = Profile.objects.all()
    c = confom.objects.all()
    cc=c.count()
    print(" Previous Conformed Booking",cc)
    cb=Reservation.objects.filter(payment_status=True)
    cbc=cb.count()
    print("Succes Payment",cbc)
    ucb=Reservation.objects.filter(payment_status=False)
    ucbc=ucb.count()
    print("failure Payment",ucbc)
    t=cc+cbc+ucbc
    print("Total Counts........: ",t)

    rcount=obj1.count()
    bcount=obj2.count()
    ucount=obj3.count()
    return render(request,"dash/admin/index.html",locals())

@login_required
def srooms1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj1 = Room.objects.all().order_by('price')
    
    return render(request,"dash/admin/rooms.html",locals())

# def addroom1(request):
#     # print("Start if")
#     if request.method == "POST":
#         print(" if inside Start")
#         roomname=request.POST['roomname']
#         roomtype=request.POST['roomtype']
#         capacity=request.POST['capacity']
#         price=request.POST['price']
#         size=request.POST['size']
#         # img=request.FILES['img']
#         dis=request.POST['dis']
#         status=request.POST['status']

#         addroom=Room(roomname=roomname, roomtype=roomtype, capacity=capacity,
#             price=price, size=size, img=request.FILES['img'], dis=dis, status=status)
#         addroom.save()

#         print(".............room added success.........")
#         messages.success(request,'New Room Was Added Successfully')
#         return redirect('superadmin')  
        
#     return render(request, "dash/addroom.html",locals())

# #editroom
# def editroom1(request,id):
#     data1 = Room.objects.get(id=id)
#     u=Profile.objects.get(user=request.user)
#     print(u.email)
#     print(">>>>>>>>>>>>>> if start")
#     if request.method == 'POST':
#         print(">>>>>>>>>>>>>> post")
#         roomname=request.POST['roomname']
#         roomtype=request.POST['roomtype']
#         capacity=request.POST['capacity']
#         price=request.POST['price']
#         size=request.POST['size']
#         # img=request.FILES['img']
#         dis=request.POST['dis']
#         status=request.POST['status']
#         print(">>>>>>>>>>>", price)
#         data1.roomname =roomname
#         data1.roomtype = roomtype
#         data1.capacity = capacity
#         data1.price = price 
#         data1.size =size
#         data1.img = request.FILES['img']
#         data1.dis = dis
#         data1.status = status 

#         print(">>>>>>>>>>>", data1.price)
#         data1.save()
#         print(">>>>>>>>>>>>>>>>>>> Room Update Successfully")
#         messages.success(request, 'Room Updates Successfully)')
#         return redirect("srooms")        
    
#     # print("d>>>>>>>>>>>",data1.roomname)
#     return render(request, "dash/editroom.html",locals())

@login_required
def booking1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    if request.method == "POST":
        print("post")
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        roomname=request.POST['roomname']
        noofroom=request.POST['noofroom']
        adult=request.POST['adult']
        exper=request.POST['exper']
        kids=request.POST['kids']
        bi=request.POST['bookIn']
        bookIn= str(bi[3:6]+bi[:3]+bi[6:])
        bo=request.POST['bookOut']
        bookOut=str(bo[3:6]+bo[:3]+bo[6:])
        amount=request.POST['amount']
        t=request.POST['t']
        tamount=request.POST['tamount']
        razorpayid=request.POST['razorpayid']
        

        booking=Reservation(user=request.user, name=name, phone=phone, email=email,
            roomname=roomname, noofroom=noofroom,adult=adult, exper=exper,kids=kids,
            bookIn=bookIn, bookOut=bookOut,amount=amount,t=t,tamount=tamount,razorpayid=razorpayid,payment_status=True)
        
        booking.save()

        print(".............Booking success.........")
        messages.success(request,'Booking Successfully')

        resv = Reservation.objects.get(razorpayid=razorpayid)
        room=Room.objects.get(roomname=resv.roomname)
        room.size = int(room.size) - int(resv.noofroom)
        room.save()
        
        return redirect('bookinglist1')  
        
    return render(request, "dash/admin/booking.html",locals())


#order
@login_required
def bookinglist1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')

    obj = Profile.objects.all()
    obj1 = Reservation.objects.all()
    c=Reservation.objects.filter(payment_status=True, cancel=False, checkout=False)[::-1]
    # count=c.count()

    return render(request, "dash/admin/bookinglist.html",locals())

@login_required
def search_bookinglist1(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(payment_status=True) & 
                Q(cancel=False) & 
                Q(checkout=False)
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search) | 
                Q(razorpay_payment_id__icontains=search)
            )
        )[::-1]
        return render(request,'dash/admin/search_bookinglist.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/admin/search_bookinglist.html',{})


@login_required
def checkin_view1(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c = Reservation.objects.filter(id = id)
    return render(request,'dash/admin/checkin_view.html',locals())

@login_required
def checkin_conform1(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Reservation.objects.get(id = id)
    obj.checkin=True
    obj.checkin_time = datetime.now().time().replace(microsecond=0)
    obj.save()


    data = {
    'name':obj.name,
    'checkin_time':obj.checkin_time,
    }

    # Checkin Mail
    mail_html = get_template('checkin_email.html').render(data)
    sender_address = 'reservations@hotelshevaroys.com'
    sender_pass = 'hotelshevaroys@#123'
    receiver_address = obj.email
    print('!!!!!!!!!!!!',receiver_address)
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Checkin Successfully!'
    message.attach(MIMEText(mail_html, 'html'))
    session = smtplib.SMTP('smtp.zoho.in', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    messages.success(request,"Booking CheckedIn Successfully!")

    return redirect('bookinglist1')

@login_required
def checkout_view1(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c = Reservation.objects.filter(id = id)
    return render(request,'dash/admin/checkout_view.html',locals())

@login_required
def checkout_conform1(request,id):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Reservation.objects.get(id = id)
    obj.checkout=True
    obj.checkout_time = datetime.now().time().replace(microsecond=0)
    obj.save()

    # Checkout Mail
    mail_html = get_template('checkout_email.html').render({"name": obj.name})
    sender_address = 'reservations@hotelshevaroys.com'
    sender_pass = 'hotelshevaroys@#123'
    receiver_address = obj.email
    print('!!!!!!!!!!!!',receiver_address)
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'CheckOut Successfully!'
    message.attach(MIMEText(mail_html, 'html'))
    session = smtplib.SMTP('smtp.zoho.in', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


    messages.success(request,"Booking Checkedout Successfully!")

    return redirect('prevbooking1')

@login_required
def cancellist1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    # obj = Profile.objects.all()
    # obj1 = Reservation.objects.all()
    c=Reservation.objects.filter(cancel=True)[::-1]


    return render(request, "dash/admin/cancellist.html",locals())

@login_required
def search_cancellist1(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(cancel=True) 
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search)
            )
        )[::-1]
        return render(request,'dash/admin/search_cancellist.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/admin/search_cancellist.html',{})


@login_required
def prevbooking1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    # obj = Profile.objects.all()
    c = Reservation.objects.filter(checkout=True)[::-1]
    # c=confom.objects.all()[::-1]
    # count=c.count()
   
    return render(request, "dash/admin/prevbooking.html",locals())

@login_required
def search_prevbooking1(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(checkout=True) 
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search) | 
                Q(razorpay_payment_id__icontains=search)
            )
        )[::-1]
        return render(request,'dash/admin/search_prevbooking.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/admin/search_prevbooking.html',{})

@login_required
def unbookinglist1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    obj = Profile.objects.all()
    obj1 = Reservation.objects.all()
    c=Reservation.objects.filter(payment_status=False)[::-1]
    # count=c.count()
    return render(request, "dash/admin/unbookinglist.html",locals())

@login_required
def search_unbookinglist1(request):
    if request.method == 'POST':
        search = request.POST['search']
        obj = Reservation.objects.all().filter(
            (
                Q(payment_status=False) 
            ) & 
            (
                Q(id__icontains=search) | 
                Q(name__icontains=search) | 
                Q(phone__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bookIn__icontains=search) | 
                Q(bookOut__icontains=search) | 
                Q(roomname__icontains=search)
            )
        )[::-1]
        return render(request,'dash/admin/search_unbookinglist.html',{'search' : search , 'obj' : obj})
    else:
        return render(request,'dash/admin/search_unbookinglist.html',{})

@login_required
def sinvoice1(request):
    user_agent = get_user_agent(request)
    if request.user.is_authenticated == False:
        return redirect('login')
    c=Reservation.objects.filter(payment_status=True)
    count=c.count()
    return render(request, "dash/admin/invoice.html",locals())

