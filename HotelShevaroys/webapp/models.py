from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse_lazy
from datetime import date

ROOM_STATUS = ( 
    ("Available", "Available"), 
    ("Not Available", "Not Available"),    
    ) 

ROOM_CHOICES = (
   
   ('Standard Room','Standard Room'),
   ('Bougainvilla Room','Bougainvilla Room'),
   ('Rose Room','Rose Room'),
   ('Dahlia Room','Dahlia Room'),
   ('Orchid Room','Orchid Room'),
   ('King Orchid','King Orchid'),
   ('Deluxe Villa','Deluxe Villa'),
   ('Luxury Villa','Luxury Villa'),
   
   
	)
ROOM_TYPE = (

   ('Room','Room'),
   ('Villa','Villa'),
   
  	
  	)
PAYMENT = (

   ('Cash','Cash'),
   ('Online','Online'),
       
    )
# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(db_column="Name", max_length=50,default='')
  mobile = models.CharField(db_column="Mobile", max_length=10, default='')
  email = models.CharField(db_column="Email", max_length=100, default='')
  pass1 = models.CharField(db_column="Password", max_length=100, default='')
  admin_status = models.BooleanField(default=False)
  radmin_status = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.name}'



class Room(models.Model):
    
    #type,no_of_rooms,capacity,prices,Hotel
    roomname= models.CharField(max_length=50,choices = ROOM_CHOICES)
    roomtype = models.CharField(max_length=50,choices = ROOM_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    # price2 = models.IntegerField(null=True)
    price2 = models.CharField(max_length=10, blank=True, default="None")
    size = models.IntegerField()
    img = models.ImageField(upload_to=f'rooms/',null=True, blank=True)
    img2 = models.ImageField(upload_to=f'rooms/',null=True, blank=True)
    img3 = models.ImageField(upload_to=f'rooms/',null=True, blank=True)
    img4 = models.ImageField(upload_to=f'rooms/',null=True, blank=True)
    dis=models.CharField(db_column="Room Description", max_length=1000, null=True, default="")
    status = models.CharField(choices =ROOM_STATUS,max_length = 15)
    date_disable = models.CharField(max_length=50, blank=True, default="")
    date_disable1 = models.CharField(max_length=50, blank=True, default="")
    date_disable2 = models.CharField(max_length=50, blank=True, default="")
    max_price_date1 = models.CharField(max_length=50, blank=True, default="")
    max_price_date2 = models.CharField(max_length=50, blank=True, default="")
    # roomnumber = models.IntegerField()
    def __str__(self):
        return self.roomname



class Roomimg(models.Model):
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  updateimg = models.ImageField(upload_to=f'rooms/',null=True)
  

class Reservation(models.Model):
  # room = models.ForeignKey(Room, on_delete = models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length = 120, default="")
  phone = models.CharField(max_length = 10, default="")
  email = models.EmailField(max_length = 50, default="")
  bookIn = models.CharField(max_length = 50,blank=True, default="")
  bookOut = models.CharField(max_length = 50,blank=True, default="")
  roomname = models.CharField(db_column="Room Name", choices=ROOM_CHOICES, max_length=100,default="")
  roomamt = models.CharField(max_length = 50,blank=True, default="")
  noofroom = models.CharField(max_length=15,blank=True, default="")
  adult = models.CharField(max_length=15,blank=True, default="")
  exper = models.CharField(max_length=15,blank=True, default="")
  kids = models.CharField(max_length=15,blank=True, default="")
  # pay = models.CharField(db_column="Payment", choices=PAYMENT, max_length=15,blank=True, default="")
  amount = models.CharField(max_length=10, blank=True, default="")
  # amount2 = models.CharField(max_length=10, blank=True, default="")
  t = models.CharField(max_length=10,blank=True, default="")
  tamount = models.CharField(max_length=10,blank=True, default="")
  date = models.CharField(max_length = 50,blank=True, default="")
  razorpayid = models.CharField(max_length=255,default="")
  razorpay_payment_id = models.CharField(max_length=255,default="None")
  payment_status = models.BooleanField(default=False)
  cancel = models.BooleanField(default=False)
  checkin = models.BooleanField(default=False)
  checkin_time = models.CharField(max_length = 50,blank=True,default="")
  checkout = models.BooleanField(default=False)
  checkout_time = models.CharField(max_length = 50,blank=True,default="")
  pre_bookIn = models.CharField(max_length = 50,blank=True, default="")
 
  # kidage = models.CharField(max_length=15, blank=True, default="")
  

  def __str__(self):
    return 'Guest Name: %s Guest Phone: %s Type of Room: %s Book in: %s Book out: %s'%(self.name, self.phone, self.roomname, self.bookIn, self.bookOut)

  # def is_past_due(self):
  #   return date.today() > self.bookIn

  # def price(self):
  #     delta = self.bookOut - self.bookIn
  #     if delta.days == 0:
  #         payment = int(self.Room.roomname.price) * int((1 + delta.days)) * int(self.noofroom)
  #     else:
  #         payment = int(self.Room.roomname.price) * int((delta.days)) * int(self.noofroom)
  #     return payment

# class PaymentDetails(Base):
#   uuid = models.UUIDField(default=uuid.uuid4, editable=False)
#   user = models.CharField(max_length=20 , default="")
#   name = models.CharField(max_length=50)
#   amount = models.CharField(max_length=50)
#   email = models.EmailField(max_length=80)
#   mobile = models.CharField(max_length=10 , default="")
#   roomname = models.CharField(max_length=50 , default="")

#   def __str__(self):
#     return self.name+ ' ' +self.roomname

PAYMENT_STATUS = (('Success','Success'),('Pending','Pending'),('Failed','Failed'))
# class RazorpayResponsew(Base):
  
#   response = models.TextField()
#   status = models.CharField(max_length=8,choices=PAYMENT_STATUS)
#   razorpayid = models.CharField(max_length=255,default="")
#   user = models.CharField(max_length=20 , default="")
#   mobile = models.CharField(max_length=10 , default="")
#   roomname = models.CharField(max_length=50 , default="")
#   tamount= models.CharField(max_length=10 , default="")
  

#   def __str__(self):
#     return self.user+ ' ' +self.roomname + ' '+self.tamount + ' '+self.status 


class confom(models.Model):
  user = models.CharField(max_length = 120, default="")
  resvno = models.CharField(max_length = 120, default="")
  name = models.CharField(max_length = 120, default="")
  phone = models.CharField(max_length = 10, default="")
  email = models.EmailField(max_length = 50, default="")
  date = models.CharField(max_length = 50,blank=True, default="")
  bookIn = models.CharField(max_length = 50,blank=True, default="")
  bookOut = models.CharField(max_length = 50,blank=True, default="")
  roomname = models.CharField(db_column="Room Name", choices=ROOM_CHOICES, max_length=100,default="")
  roomamt = models.CharField(max_length = 50,blank=True, default="")
  noofroom = models.CharField(max_length=15,blank=True, default="")
  adult = models.CharField(max_length=15,blank=True, default="")
  exper = models.CharField(max_length=15,blank=True, default="")
  kids = models.CharField(max_length=15,blank=True, default="")
  # pay = models.CharField(db_column="Payment", choices=PAYMENT, max_length=15,blank=True, default="")
  amount = models.CharField(max_length=10,blank=True, default="")
  t = models.CharField(max_length=10,blank=True, default="")
  tamount = models.CharField(max_length=10,blank=True, default="")
  razorpayid = models.CharField(max_length=255,default="")
  razorpay_payment_id = models.CharField(max_length=255,default="None")
  payment_status = models.BooleanField(default=True)
  cancel = models.BooleanField(default=False)

  def __str__(self):
    return self.name+ ' ' +self.roomname + ' '+self.tamount + ' '+' True'


class Feedback(models.Model):
  # user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length = 120, default="")
  email = models.EmailField(max_length = 50, default="")
  phone = models.CharField(max_length = 10, default="")
  feedback = models.CharField(max_length = 500000,blank=True,default="")

  def __str__(self):
    return 'Guest Name: %s Guest Email: %s'%(self.name, self.email)