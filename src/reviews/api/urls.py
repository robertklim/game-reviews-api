from django.urls import path
from .views import GameReviewRudView, GameReviewCreateView

app_name = 'api-reviews'

urlpatterns = [
    path('create', GameReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>', GameReviewRudView.as_view(), name='review-rud'),
]