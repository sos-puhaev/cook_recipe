from django.urls import path
from .views import ViewCookBook

urlpatterns = [
    path('', ViewCookBook.as_view(), name='page_view'),
]
