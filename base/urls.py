from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('home/',home,name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('completedrides/', completedrides, name='completedrides'),
    path('my_bookings/',my_bookings,name='my_bookings'),
    path('bookings/<int:id>',bookings,name='bookings'),
    path('cancelbooking/<int:id>',cancelbooking,name='cancelbooking'),
    path('completebooking/<int:id>',completebooking,name='completebooking'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)