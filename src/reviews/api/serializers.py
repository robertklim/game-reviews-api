from rest_framework import serializers

from reviews.models import GameReview

class GameReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameReview
        fields = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
        ]