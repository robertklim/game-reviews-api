from rest_framework import generics
from reviews.models import GameReview
from .serializers import GameReviewSerializer

class GameReviewCreateView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    
    def get_queryset(self):
        return GameReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GameReviewRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    
    def get_queryset(self):
        return GameReview.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return GameReview.objects.get(pk=pk)