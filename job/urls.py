from django.urls import re_path
from . import views


app_name = "job"
urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^about$', views.about, name='about'),
    re_path(r'^trend$', views.trend, name='trend'),
    re_path(r'^dept$', views.dept, name='dept'),
    re_path(r'^(?P<job_id>[0-9]+)$', views.item, name='item'),
    re_path(r'^api/message/(?P<job_id>[0-9]+)$', views.message, name='message'),
    re_path(r'^api/dept/$', views.dept_ajax, name='dept_ajax'),
    re_path(r'api/trend/$', views.trend_ajax, name='trend_ajax'),
]
