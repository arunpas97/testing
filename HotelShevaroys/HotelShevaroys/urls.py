"""HotelShevaroys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from webapp import views as v
from webapp import sadmin as sa
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', v.index, name='index'),
    path('room/', v.room,name='room'),
    path('hall/', v.hall,name='hall'),
    path('service/', v.service,name='service'),
    path('about/', v.about,name='about'),
    path('privacy/', v.privacy,name='privacy'),
    path('gallery/', v.gallery,name='gallery'),
    path('contact/', v.contact,name='contact'),


    # rooms
    path('room/<str:roomname>',v.room_detail,name='room_detail'),
    path('booking/<str:roomname>/<str:price>/',v.bookroom,name='bookroom'),
    path('booking/payment/<str:no>/<str:n>/<str:rn>/<str:am>/<str:p>/<str:e>/',v.payment,name='payment'),
    path('booking_status/<str:o>/<str:n>/',v.success,name='success'),
    path('feedback_form/',v.feedback,name='feedback'),
    path('room_view/<str:roomname>/',v.room_view,name='room_view'),
    
    #user
    path('register', v.register, name='register'),
    path('login', v.Login, name='login'),
    path('logout', v.Logout, name='logout'),
    # path('My_Profile/',v.my_profile,name='my_profile'),
    path('My_Booking/',v.mybooking,name='mybooking'),
    path('Previous_Booking/',v.previous_booking,name='previous_booking'),
    path('Cancel_Booking_list/',v.cancel_booking_list,name='cancel_booking_list'),
    path('cancel_booking_view/<str:id>',v.cancel_booking_view,name='cancel_booking_view'),
    path('cancel_booking/<str:id>/',v.cancel_booking,name='cancel_booking'),
    
    # admin
    path('admin_dashboard/', sa.superadmin, name='superadmin'),
    path('rooms/', sa.srooms, name='srooms'),
    path('add_room/', sa.addroom, name='addroom'),
    path('edit_room/<str:id>/', sa.editroom, name='editroom'),
    path('new_booking/', sa.booking, name='booking'),
    path('conform_booking_list/', sa.bookinglist, name='bookinglist'),
    path('checkin_view/<str:id>/', sa.checkin_view, name='checkin_view'),
    path('checkin_conform/<str:id>/',sa.checkin_conform,name='checkin_conform'),
    path('checkout_view/<str:id>/', sa.checkout_view, name='checkout_view'),
    path('checkout_conform/<str:id>/',sa.checkout_conform,name='checkout_conform'),
    path('previous_conform_booking_list/', sa.prevbooking, name='prevbooking'),
    path('unconform_booking_list/', sa.unbookinglist, name='unbookinglist'),
    path('cancelled_booking_list/', sa.cancellist, name='cancellist'),
    path('update_room_image/', sa.updateimg, name='updateimg'),
    path('invoice/', sa.sinvoice, name='sinvoice'),
    path('search/conform_booking_list/',sa.search_bookinglist,name='search_bookinglist'),
    path('search/unconform_booking_list/',sa.search_unbookinglist,name='search_unbookinglist'),
    path('search/previous_conform_booking_list/',sa.search_prevbooking,name='search_prevbooking'),
    path('search/cancelled_booking_list/',sa.search_cancellist,name='search_cancellist'),
    path('customer_feedback/',sa.customer_feedback,name='customer_feedback'),

    # Reception admin
    path('reception_admin_dashboard/', sa.superadmin1, name='superadmin1'),
    path('reception_rooms/', sa.srooms1, name='srooms1'),
    path('reception_new_booking/', sa.booking1, name='booking1'),
    path('reception_conform_booking_list/', sa.bookinglist1, name='bookinglist1'),
    path('reception_checkin_view/<str:id>/', sa.checkin_view1, name='checkin_view1'),
    path('reception_checkin_conform/<str:id>/',sa.checkin_conform1,name='checkin_conform1'),
    path('reception_checkout_view/<str:id>/', sa.checkout_view1, name='checkout_view1'),
    path('reception_checkout_conform/<str:id>/',sa.checkout_conform1,name='checkout_conform1'),
    path('reception_cancelled_booking_list/', sa.cancellist1, name='cancellist1'),
    path('reception_previous_conform_booking_list/', sa.prevbooking1, name='prevbooking1'),
    path('reception_unconform_booking_list/', sa.unbookinglist1, name='unbookinglist1'),
    path('search/reception_conform_booking_list/',sa.search_bookinglist1,name='search_bookinglist1'),
    path('search/reception_unconform_booking_list/',sa.search_unbookinglist1,name='search_unbookinglist1'),
    path('search/reception_previous_conform_booking_list/',sa.search_prevbooking1,name='search_prevbooking1'),
    path('search/reception_cancelled_booking_list/',sa.search_cancellist1,name='search_cancellist1'),

    # Payment Gateway
    # path('store/',StoreDetails.as_view(),name='checkout'),
    # path('charge/',MyPayment.as_view(),),

    path('stdroom/',v.stdroom,name='stdroom'),
    path('bouvilla/',v.bouvilla,name='bouvilla'),
    path('deluxeroom/',v.deluxeroom,name='deluxeroom'),
    path('dhaliaroom/',v.dhaliaroom,name='dhaliaroom'),
    path('luxuryroom/',v.luxuryroom,name='luxuryroom'),
    path('roseroom/',v.roseroom,name='roseroom'),
    path('orchidroom/',v.orchidroom,name='orchidroom'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
