from django.contrib import admin
from django.urls import path
from vehicleassist.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    # =======================  Admin  ========================================
    path('dashboard/', dashboard, name='dashboard'),
    path('addDriver', addDriver, name='addDriver'),
    path('manageDriver', manageDriver, name='manageDriver'),
    path('editDriver/<int:pid>', editDriver, name='editDriver'),
    path('deleteDriver/<int:pid>', deleteDriver, name='deleteDriver'),
    path('newRequest', newRequest, name='newRequest'),
    path('approvedRequest', approvedRequest, name='approvedRequest'),
    path('cancelRequest', cancelRequest, name='cancelRequest'),
    path('allRequest/', allRequest, name='allRequest'),
    path('viewRequestDetails/<int:pid>', viewRequestDetails, name='viewRequestDetails'),
    path('deleteRequest/<int:pid>', deleteRequest, name='deleteRequest'),
    path('onethewayDriver', onethewayDriver, name='onethewayDriver'),
    path('taskComplete', taskComplete, name='taskComplete'),
    path('betweendateReport', betweendateReport, name='betweendateReport'),
    path('search', search, name='search'),
    path('changePassword', changePassword, name='changePassword'),

    # ====================  Driver   ========================================
    path('driverlogin', driverlogin, name='driverlogin'),
    path('profile', profile, name='profile'),
    path('ddashboard', ddashboard, name='ddashboard'),
    path('newsRequest', newsRequest, name='newsRequest'),
    path('onthewayRequest', onthewayRequest, name='onthewayRequest'),
    path('completedRequest', completedRequest, name='completedRequest'),
    path('totalRequest', totalRequest, name='totalRequest'),
    path('dviewRequestDetails/<int:pid>', dviewRequestDetails, name='dviewRequestDetails'),
    path('dsearch', dsearch, name='dsearch'),
    path('dbetweendateReport', dbetweendateReport, name='dbetweendateReport'),
    path('dchangePassword', dchangePassword, name='dchangePassword'),

    path('logout/', Logout, name='logout'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
