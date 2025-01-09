from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    text = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    sentence_examples = models.JSONField(
        null=True, blank=True
    )  # {'example1': '...', 'example2': '...'}
    translations = models.ManyToManyField(
        "self", symmetrical=False, related_name="translated_from"
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_language = models.CharField(max_length=50)
    learning_languages = models.JSONField()  # ['french', 'spanish']
    seen_words = models.ManyToManyField(Word, related_name="seen_by_users")
