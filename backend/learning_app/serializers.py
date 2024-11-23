from rest_framework import serializers
from .models import JapaneseCharacter, UserProgress

class JapaneseCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JapaneseCharacter
        fields = ['id', 'character', 'romaji', 'character_type', 'meaning']

class UserProgressSerializer(serializers.ModelSerializer):
    accuracy = serializers.FloatField(read_only=True)
    
    class Meta:
        model = UserProgress
        fields = ['character', 'correct_count', 'incorrect_count', 'last_practiced', 'accuracy']
