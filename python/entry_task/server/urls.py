from django.conf.urls import patterns, url
from entry_task.views import product_views, product_comment_views

v = product_views.ProductViews()
vc = product_comment_views.ProductCommentViews()
urlpatterns = patterns('',
    url(r'^products/$', v.product_list),
    url(r'^products/(?P<id>\d+)/$', v.product_details),
    url(r'^products/(?P<id>\d+)/comments/$', vc.product_comment_list),
)