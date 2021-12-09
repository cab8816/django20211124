from django.urls import path

from . import views

app_name = 'newhorse'  # 在 URLconf 中添加命名空间。
urlpatterns = [
    # path('index/', views.index)
    path('mytest/', views.mytest),
    path('index/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/detail', views.DetaiView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]
