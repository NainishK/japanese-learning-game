from django.contrib import admin
from .models import JapaneseCharacter, UserProgress

@admin.register(JapaneseCharacter)
class JapaneseCharacterAdmin(admin.ModelAdmin):
    list_display = ('character', 'romaji', 'character_type')
    list_filter = ('character_type',)
    search_fields = ('character', 'romaji')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('character', 'correct_count', 'incorrect_count', 'last_practiced')
    list_filter = ('last_practiced',)
