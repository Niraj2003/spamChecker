from django.urls import path
from .views import UserLogin, UserCreate, mark_spam, search

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('spam/', mark_spam, name='mark-spam'),
    path('search/', search, name='search'),
]
