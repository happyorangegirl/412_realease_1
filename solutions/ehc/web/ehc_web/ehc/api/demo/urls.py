from django.conf.urls import *

from demo import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), {'tpl': 'dinner/index.html'}, name='index'),
    url(r'workflows/$', views.WorkflowView.as_view(), name='workflows'),
]