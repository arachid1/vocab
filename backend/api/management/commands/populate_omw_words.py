import nltk
import os

nltk.data.path.append("/root/nltk_data/corpora")
print("Files in /root/nltk_data/corpora:", os.listdir("/root/nltk_data/corpora"))

from django.core.management.base import BaseCommand
from api.models import Word
from nltk.corpus import wordnet as wn

nltk.download("wordnet")
nltk.download("omw-1.4")
print(wn.synsets("house", lang="fra"))

print("Available languages:", wn.langs())
print(nltk.data.path)


class Command(BaseCommand):
    help = "Populate database with words and translations from Open Multilingual WordNet (OMW)"

    def handle(self, *args, **kwargs):
        # Download WordNet and OMW data (only the first time)

        total_words_added = 0
        # Define the languages you're interested in
        target_languages = [
            "eng",
            "fr",
            "es",
            "arb",
        ]  # 'arb' = Arabic (Classical Arabic)

        # Limit the number of words for each language for now
        max_words_per_language = 50  # Adjust this based on capacity
        added_words = {}

        for lang in target_languages:
            if lang not in wn.langs():
                print(f"Language {lang} not available in WordNet.")
                continue
            # Fetch synsets (word groups) for the target language
            synsets = list(wn.all_synsets(lang=lang))[:max_words_per_language]
            print(f"Synsets for language {lang}: {len(synsets)}")

            for synset in synsets:
                # Extract the word(s) in the current language
                words = synset.lemma_names(lang=lang)

                # Fetch examples (limit to 2 examples for now)
                examples = synset.examples()[:2]

                for word_text in words:
                    # Create or get the base word
                    word, created = Word.objects.get_or_create(
                        text=word_text,
                        language=lang,
                        sentence_examples={"examples": examples},
                    )

                    if created:
                        total_words_added += 1
                    # Track words to add translations later
                    added_words.setdefault(synset, []).append(word)

        # Add translations for each synset
        for synset, word_objects in added_words.items():
            for word in word_objects:
                # Link translations (words in the same synset)
                translations = [w for w in word_objects if w != word]
                word.translations.add(*translations)

        self.stdout.write(
            self.style.SUCCESS(
                f"OMW words and translations populated successfully! Total words added: {total_words_added}"
            )
        )
