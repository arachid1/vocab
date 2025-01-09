from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    text = models.CharField(max_length=100)  # The word itself
    language = models.CharField(max_length=50)  # Language of the word
    sentence_examples = models.JSONField(
        null=True, blank=True
    )  # JSON field for sentence examples, such as {'example1': '...', 'example2': '...'}
    translations = models.ManyToManyField(
        "self", symmetrical=True, related_name="translated_from"
    )  # Symmetrical=True since translations are mutual

    def __str__(self):
        return f"{self.text} ({self.language})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Links to Django's User model
    main_language = models.CharField(max_length=50)  # User's main language
    learning_languages = (
        models.JSONField()
    )  # A list of learning languages ['french', 'spanish']
    seen_words = models.ManyToManyField(
        Word, related_name="seen_by_users"
    )  # Tracks words seen by the user
