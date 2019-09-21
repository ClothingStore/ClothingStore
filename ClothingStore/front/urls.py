from django.conf.urls import url

from front import views

urlpatterns = [
    # 注册
    url(r'register/',views.register,name='register'),
    # 登录
    url(r'userlogin/',views.userlogin,name='userlogin'),
    # 主页
    url(r'^$',views.index,name='index'),
    # 服装板块
    url(r'section/(\d+)',views.section,name='section'),
    # 个人信息修改
    url(r'^udaisetting/$',views.udaisetting,name='udaisetting'),
    # 退出
    url(r'logout/', views.logoutuser, name='logout'),
    # 收货地址
    url(r'address/',views.address,name='address'),
    # 修改收货地址
    url(r'edit/(\d+)/',views.edit,name='edit'),
    # 个人中心欢迎界面
    url(r'welcome/',views.welcome,name='welcome'),
    # 个人订单
    url(r'userorder/',views.order,name='userorder'),
    # 订单详情
    url(r'orderdetail/(\d+)/',views.orderdetail,name='orderdetail'),
    # 付款
    url(r'parment/(\d+)/',views.parment,name='parment'),
    # 收货
    url(r'shou/(\d+)/',views.shouhuo,name='shouhuo'),
    # 退款
    url(r'ordertui/(\d+)/$',views.ordertui,name='ordertui'),
    url(r'ordertui/$',views.ordertui,name='ordertui'),
    url(r'yesorder/(\d+)/$',views.yesorder,name='yesorder'),
    # 服装列表展示
    url(r'clothlist/$',views.clothlist,name='clothlist'),
    # 购物车
    url(r'shopcat/$', views.shopcat, name='shopcat'),
    # 添加购物车
    # url(r'^addshop/(?P<action>\w+)/$',views.AddShop.as_view(),name='addshop'),
    # 服装详情
    url(r'clodetail/(\d+)/$', views.clodetail, name='clodetail'),





]