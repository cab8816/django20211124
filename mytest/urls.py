from django.contrib.auth import login, logout
from django.urls import path
from mytest import views
from mytest.views import PublisherCreateView, \
    PublisherUpdateView, PublisherDeleteView

urlpatterns = [
    path('hello/', views.hello),
    path('current_date/', views.current_datetime),
    path('displaymeta/', views.display_meta),
    path('search/', views.search),
    path('contact/', views.contact),
    path('searchxie/', views.searchxie),
    path('hellopdf/', views.hellopdf),
    path('setcolor/<str:favorite_color>/', views.set_color),
    path('showcolor/', views.show_color),
    path('login/', views.login),
    path('logout/', logout),
    path('publisher/add/', PublisherCreateView.as_view(), name='publisher-add'),
    path('publisher/', views.publisherListView(), name='publisher-list'),
    path('publisher/<int:pk>/', PublisherUpdateView.as_view(), name='publisher-update'),
    path('publisher/<int:pk>/delete/', PublisherDeleteView.as_view(), name='publisher-delete'),
]
