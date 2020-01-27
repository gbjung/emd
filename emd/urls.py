from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from reporting.views import ReportingView, SuccessView
from usaspending.views import USASpendingView


urlpatterns = [
    path('', ReportingView.as_view(), name='reporting'),
    path('usaspending', USASpendingView.as_view(), name='usaspending'),
    path('success', SuccessView.as_view()),
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
]
