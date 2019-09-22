from django.conf.urls import url
from App import views
urlpatterns=[
    url(r'^admins/$',views.index,name='index'),#主页
    url(r'^login/$',views.login,name='login'),#登录
    url(r'^product_list/$',views.product_list,name='product_list'),#商品列表
    url(r"^product_list/(?P<page>\d+)/$", views.product_list, name='product_list'),
    url(r'^product_detail/(\d+)/$',views.product_detail,name='product_detail'),#商品详情
    url(r'^add_product$',views.add_product,name='add_product'),#添加商品
    url(r'^delete_product/(\d+)/$',views.delete_product,name='delete_product'),#商品删除
    url(r'^order_list$',views.order_list,name='order_list'),#订单列表
    url(r'^order_detail/(\d+)/$',views.order_detail,name='order_detail'),#订单详情
    url(r'^user_list$',views.user_list,name='user_list'),#用户列表
    url(r'^user_detail/(\d+)/$',views.user_detail,name='user_detail'),#用户详情
    url(r'^user_rank$',views.user_rank,name='user_rank'),#用户等级
    url(r'^web_site$',views.web_site,name='web_site'),#站点设计
    url(r'^order_back$',views.order_back,name='order_back'),#退货订单
    url(r'^delproduct_list$',views.delproduct_list,name='delproduct_list'),#已删除商品列表
    url(r'^delproduct_list/(?P<page>\d+)/$',views.delproduct_list,name='delproduct_list'),#
    url(r'^recover_product/(\d+)/$',views.recover_product,name='recover_product'),#恢复商品
    url(r'^orderback_detail/(\d+)/$',views.orderback_detail,name='orderback_detail'),#订单退货详情
    url(r'^logout/$',views.logout,name='logout')



]