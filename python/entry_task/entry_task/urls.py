from django.conf.urls import patterns, url
from entry_task_api.views import product_list

urlpatterns = patterns('',
    url(r'^products/$', product_list),
)