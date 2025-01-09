from rest_framework import serializers
from .models import Word, UserProfile


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "text", "language", "translations", "sentence_examples"]


class UserProfileSerializer(serializers.ModelSerializer):
    seen_words = WordSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "main_language", "learning_languages", "seen_words"]
        read_only_fields = ["user"]
