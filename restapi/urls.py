from django.conf.urls import url
from restapi import views


urlpatterns = [
    url(r'^$', views.view_api_usage),
    url(r'token/(?P<token_serial>[A-Z0-9]+)/balance', views.view_token_balance),
    url(r'token/(?P<token_serial>[A-Z0-9]+)/transaction', views.view_token_transaction)
]
