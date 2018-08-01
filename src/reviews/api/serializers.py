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
        read_only_fields = ['user']

    def validate_title(self, value):
        qs = GameReview.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This title has already been used')
        return value