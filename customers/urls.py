from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('delete-card/<str:card_id>', views.delete_card, name='delete_card'),
    path('login/', views.login, name='login'),
]
