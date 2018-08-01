from rest_framework import generics
from reviews.models import GameReview
from .serializers import GameReviewSerializer

class GameReviewRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    
    def get_queryset(self):
        return GameReview.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return GameReview.objects.get(pk=pk)