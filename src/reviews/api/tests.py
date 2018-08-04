from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from reviews.models import GameReview

User = get_user_model()

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

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

    def test_post_item(self):
        data = {'title': 'Post test title', 'content': 'Post test content'}
        url = api_reverse('api-reviews:review-cls')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
                         status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        game_review = GameReview.objects.first()
        url = game_review.get_api_url()
        data = {'title': 'Updated test title',
                'content': 'Updated test content'}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_post_item_with_user(self):
        data = {'title': 'Post test title', 'content': 'Post test content'}
        url = api_reverse('api-reviews:review-cls')
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_ownership(self):
        owner = User(username='testuser2', email='test2@test.com')
        owner.set_password('secret')
        owner.save()
        game_review = GameReview.objects.create(
            user=owner,
            title='testuser2 title',
            content='Some testuser2 content'
        )
        
        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        url = game_review.get_api_url()
        data = {'title': 'Updated test title',
                'content': 'Updated test content'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'testuser',
            'password': 'secret',
        }
        url = api_reverse('api-login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            game_review = GameReview.objects.first()
            url = game_review.get_api_url()
            data = {'title': 'Second updated test title',
                    'content': 'Second updated test content'}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code,
                            status.HTTP_200_OK)
