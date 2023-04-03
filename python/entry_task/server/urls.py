from django.conf.urls import patterns, url
from entry_task.views import product_views, product_comment_views, general_views, auth_views

v = product_views.ProductViews()
vc = product_comment_views.ProductCommentViews()
vg = general_views.GeneralViews()
va = auth_views.AuthViews()
urlpatterns = patterns('',
    url(r'^products/$', v.product_list),
    url(r'^products/(?P<id>\d+)/$', v.product_details),
    url(r'^products/(?P<id>\d+)/comments/?$', vc.product_comment_list),
    url(r'^register/$', va.register),
    url(r'^login/$', va.login),
    url(r'^.*$', vg.endpoint_not_found),
)

handler404 = vg.endpoint_not_found