from django.conf.urls import *

import dashboard_view

urlpatterns = [
    url(r'^$', dashboard_view.IndexView.as_view(), name='index'),
    url(r'autoclear/$', dashboard_view.AutoclearView.as_view(), name='autoclear'),
    url(r'clearlog/$', dashboard_view.ClearlogView.as_view(), name='clearlog'),
]