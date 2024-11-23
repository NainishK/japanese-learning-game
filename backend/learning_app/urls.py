from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'characters', views.JapaneseCharacterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('random/', views.get_random_character, name='random-character'),
    path('check/', views.check_answer, name='check-answer'),
    path('list/', views.list_characters, name='list-characters'),
    path('progress/', views.get_progress, name='get-progress'),
]
