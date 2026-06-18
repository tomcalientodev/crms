
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . import api
from .api import EmployeeViewSet, CustomerViewSet
from .password_reset import RequestPasswordResetView, VerifyResetCodeView, ResetPasswordView
from .permissions import OrganizationOwnerPermission
from django.contrib.auth import views as auth_views




urlpatterns = [
    
    # path('', views.welcome, name='welcome'),
    # path('base', views.base, name='base'),

    # path('loginpage', views.loginPage, name='login'),
    # path('logout', views.logoutUser, name='logout'),
    # path('register_page', views.register, name='register-page'),
    
    path('user_info/', api.user_info),

    path('owner_permissions/', OrganizationOwnerPermission.as_view()),

    path('employees', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'}),),
    path('employees/<pk>/', EmployeeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),),

    path('customers', CustomerViewSet.as_view({ 'post': 'create'})),
    path('customers/<pk>/', CustomerViewSet.as_view({'get': 'retrieve', 'put': 'update'})),

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), #logs user in.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('create_organization_and_owner', api.create_organization_and_owner),

    
    # path('product_page', views.product_page, name='product-page'),
    # path('payment_successful', views.payment_successful, name='payment-successful'),
    # path('payment_cancelled', views.payment_cancelled, name='payment-cancelled'),
    # path('stripe_webhook', views.stripe_webhook, name= 'stripe-webhook' ),

]






