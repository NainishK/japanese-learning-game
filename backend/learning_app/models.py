from django.db import models

class JapaneseCharacter(models.Model):
    character = models.CharField(max_length=10)
    romaji = models.CharField(max_length=10)
    character_type = models.CharField(max_length=20, choices=[
        ('hiragana', 'Hiragana'),
        ('katakana', 'Katakana'),
        ('kanji', 'Kanji'),
    ])
    meaning = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.character} ({self.romaji})"

class UserProgress(models.Model):
    character = models.ForeignKey(JapaneseCharacter, on_delete=models.CASCADE)
    correct_count = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)
    last_practiced = models.DateTimeField(auto_now=True)
    has_seen = models.BooleanField(default=False)
    needs_review = models.BooleanField(default=False)
    revealed_count = models.IntegerField(default=0)
    consecutive_correct = models.IntegerField(default=0)
    last_attempt_revealed = models.BooleanField(default=False)
    
    def mark_for_review(self):
        self.needs_review = True
        self.consecutive_correct = 0
        self.save()
    
    def check_if_learned(self):
        # Character is considered learned if it has been correctly answered 3 times in a row
        if self.consecutive_correct >= 3:
            self.needs_review = False
            self.save()
            return True
        return False
    
    def accuracy(self):
        total = self.correct_count + self.incorrect_count
        return (self.correct_count / total * 100) if total > 0 else 0
    
    def __str__(self):
        return f"Progress for {self.character}"
