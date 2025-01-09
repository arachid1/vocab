from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Word, UserProfile
from .serializers import WordSerializer, UserProfileSerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    @action(detail=False, methods=["get"])
    def new_words(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        seen_words = user_profile.seen_words.all()
        new_words = Word.objects.exclude(id__in=seen_words)
        serializer = self.get_serializer(new_words, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def mark_as_seen(self, request, pk=None):
        user_profile = UserProfile.objects.get(user=request.user)
        word = self.get_object()
        user_profile.seen_words.add(word)
        return Response({"status": "word marked as seen"})


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
