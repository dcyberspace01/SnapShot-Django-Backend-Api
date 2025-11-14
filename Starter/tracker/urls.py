from django.urls import path
from tracker import views
from .views import login_view, transactions_api_view, user_api_view, logout_view



urlpatterns = [
    path("", views.index, name='index'),
    path(
      "transactions/", 
      views.transactions_list,
      name='transactions-list'
    ),
    path("api/login/", login_view, name='login'),
    path("api/transactions/", transactions_api_view),
    path("api/user/", user_api_view),
    path("api/logout/", logout_view),
]

