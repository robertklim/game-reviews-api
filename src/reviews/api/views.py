from django.db.models import Q
from rest_framework import generics, mixins
from reviews.models import GameReview
from .permissions import IsOwnerOrReadOnly
from .serializers import GameReviewSerializer

class GameReviewClsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    
    def get_queryset(self):
        qs = GameReview.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)
                    ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class GameReviewCreateView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    
    def get_queryset(self):
        return GameReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GameReviewListView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    
    def get_queryset(self):
        return GameReview.objects.all()

class GameReviewRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = GameReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return GameReview.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return GameReview.objects.get(pk=pk)