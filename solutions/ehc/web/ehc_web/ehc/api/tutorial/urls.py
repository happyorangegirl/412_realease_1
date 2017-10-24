from snippets import views
from django.conf.urls import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'demo', include('demo.urls', namespace='demo')),
    url(r'main', include('main.urls', namespace='main'))
]


