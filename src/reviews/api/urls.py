from django.urls import path
from .views import GameReviewRudView

app_name = 'api-reviews'

urlpatterns = [
    path('<int:pk>', GameReviewRudView.as_view(), name='review-rud'),
]