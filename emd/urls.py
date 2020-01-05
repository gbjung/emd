from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from reporting.views import ReportingView, SuccessView

urlpatterns = [
    path('', ReportingView.as_view()),
    path('success', SuccessView.as_view()),
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
]
