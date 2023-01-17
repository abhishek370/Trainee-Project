from django import views
from django.urls import path
from .views import Home,PD
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('create/',views.index1,name="create"),
    # path('update/',views.index4,name='update'),
    path('',Home.as_view(),name="home"),
    path('pd/',PD.as_view(),name="pd"),
    path('detail/<int:id>',views.Productview,name="detail"),
    path('catdetail/',views.index,name="catdetail"),
    # path('pad/',views.index4,name="pad"),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)