from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import JapaneseCharacter, UserProgress
from .serializers import JapaneseCharacterSerializer
from django.db.models import Q
import random
import json

class JapaneseCharacterViewSet(viewsets.ModelViewSet):
    queryset = JapaneseCharacter.objects.all()
    serializer_class = JapaneseCharacterSerializer

@api_view(['GET'])
def get_random_character(request):
    try:
        # 40% chance to get a review character if any exist
        review_chars = list(UserProgress.objects.filter(needs_review=True).select_related('character'))
        if review_chars and random.random() < 0.4:
            progress = random.choice(review_chars)
            random_char = progress.character
        else:
            # Get all characters
            all_chars = list(JapaneseCharacter.objects.all())
            if not all_chars:
                return JsonResponse({'error': 'No characters found'}, status=404)

            # Get specific type if requested
            character_type = request.query_params.get('type')
            if character_type:
                all_chars = [c for c in all_chars if c.character_type == character_type]
                if not all_chars:
                    return JsonResponse({'error': f'No {character_type} characters found'}, status=404)
            
            # Choose random character
            random_char = random.choice(all_chars)
            
            # Get or create progress
            progress, created = UserProgress.objects.get_or_create(character=random_char)
        
        if not progress.has_seen:
            progress.has_seen = True
            progress.save()
        
        data = {
            'id': random_char.id,
            'character': random_char.character,
            'romaji': random_char.romaji,
            'character_type': random_char.character_type,
            'needs_review': progress.needs_review
        }
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def check_answer(request):
    try:
        character_id = request.data.get('character_id')
        user_answer = request.data.get('answer', '').lower()
        was_revealed = request.data.get('was_revealed', False)
        
        if not character_id:
            return JsonResponse({'error': 'character_id is required'}, status=400)
        
        character = JapaneseCharacter.objects.get(id=character_id)
        is_correct = character.romaji.lower() == user_answer

        # Update progress
        progress, created = UserProgress.objects.get_or_create(character=character)
        
        if was_revealed:
            progress.revealed_count += 1
            progress.consecutive_correct = 0
            progress.mark_for_review()
        else:
            if is_correct:
                progress.correct_count += 1
                progress.consecutive_correct += 1
                progress.check_if_learned()
            else:
                progress.incorrect_count += 1
                if progress.incorrect_count >= 3:  # Mark for review if struggled 3 or more times
                    progress.mark_for_review()
                progress.consecutive_correct = 0
        
        progress.last_attempt_revealed = was_revealed
        progress.save()
        
        return JsonResponse({
            'correct': is_correct,
            'correct_answer': character.romaji,
            'accuracy': progress.accuracy(),
            'needs_review': progress.needs_review
        }, json_dumps_params={'ensure_ascii': False})
    except JapaneseCharacter.DoesNotExist:
        return JsonResponse({'error': 'Character not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def list_characters(request):
    try:
        characters = JapaneseCharacter.objects.all()
        data = [{'id': c.id, 'character': c.character, 'romaji': c.romaji, 'type': c.character_type} 
                for c in characters]
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_progress(request):
    try:
        # Get total numbers
        total_hiragana = JapaneseCharacter.objects.filter(character_type='hiragana').count()
        total_katakana = JapaneseCharacter.objects.filter(character_type='katakana').count()
        
        # Get seen characters using has_seen field
        seen_hiragana = UserProgress.objects.filter(
            character__character_type='hiragana',
            has_seen=True
        ).count()
        
        seen_katakana = UserProgress.objects.filter(
            character__character_type='katakana',
            has_seen=True
        ).count()
        
        # Get review counts
        review_hiragana = UserProgress.objects.filter(
            character__character_type='hiragana',
            needs_review=True
        ).count()
        
        review_katakana = UserProgress.objects.filter(
            character__character_type='katakana',
            needs_review=True
        ).count()
        
        return JsonResponse({
            'hiragana_progress': {
                'seen': seen_hiragana,
                'total': total_hiragana,
                'percentage': round((seen_hiragana / total_hiragana) * 100 if total_hiragana > 0 else 0, 1),
                'needs_review': review_hiragana
            },
            'katakana_progress': {
                'seen': seen_katakana,
                'total': total_katakana,
                'percentage': round((seen_katakana / total_katakana) * 100 if total_katakana > 0 else 0, 1),
                'needs_review': review_katakana
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
