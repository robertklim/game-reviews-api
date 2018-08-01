from django.urls import path
from .views import GameReviewClsAPIView, GameReviewListView, GameReviewCreateView, GameReviewRudView

app_name = 'api-reviews'

urlpatterns = [
    path('', GameReviewClsAPIView.as_view(), name='review-cls'),
    path('list/', GameReviewListView.as_view(), name='review-list'),
    path('create/', GameReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>', GameReviewRudView.as_view(), name='review-rud'),
]