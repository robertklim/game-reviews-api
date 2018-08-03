from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from reviews.models import GameReview

User = get_user_model()

class GameReviewAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testuser', email='test@test.com')
        user_obj.set_password('secret')
        user_obj.save()
        game_review = GameReview.objects.create(
            user = user_obj,
            title = 'Test title',
            content = 'Some test content'
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
    
    def test_single_review(self):
        review_count = GameReview.objects.count()
        self.assertEqual(review_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse('api-reviews:review-cls')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list(self):
        data = {'title': 'Post test title', 'content': 'Post test content'}
        url = api_reverse('api-reviews:review-cls')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_item(self):
        game_review = GameReview.objects.first()
        data = {}
        url = game_review.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        game_review = GameReview.objects.first()
        url = game_review.get_api_url()
        data = {'title': 'Updated test title', 'content': 'Updated test content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 
                         status.HTTP_403_FORBIDDEN)

