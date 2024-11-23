from django.core.management.base import BaseCommand
from learning_app.models import JapaneseCharacter

class Command(BaseCommand):
    help = 'Populates the database with Japanese characters (Hiragana and Katakana)'

    def handle(self, *args, **kwargs):
        # First, clear existing characters
        JapaneseCharacter.objects.all().delete()
        self.stdout.write('Cleared existing characters')

        # Basic Hiragana
        hiragana = {
            # Vowels
            'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
            # K-row
            'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
            # S-row
            'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
            # T-row
            'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
            # N-row
            'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
            # H-row
            'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
            # M-row
            'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
            # Y-row
            'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
            # R-row
            'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
            # W-row
            'わ': 'wa', 'を': 'wo',
            # N
            'ん': 'n',
            # Dakuten variants (K -> G)
            'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
            # Dakuten variants (S -> Z)
            'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
            # Dakuten variants (T -> D)
            'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
            # Dakuten variants (H -> B)
            'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
            # Handakuten variants (H -> P)
            'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
            # Contracted sounds
            'きょ': 'kyo', 'しょ': 'sho', 'ちょ': 'cho', 'にょ': 'nyo', 'ひょ': 'hyo',
            'みょ': 'myo', 'りょ': 'ryo', 'ぎょ': 'gyo', 'じょ': 'jo', 'びょ': 'byo',
            'ぴょ': 'pyo'
        }

        # Basic Katakana
        katakana = {
            # Vowels
            'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
            # K-row
            'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
            # S-row
            'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
            # T-row
            'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
            # N-row
            'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
            # H-row
            'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
            # M-row
            'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
            # Y-row
            'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
            # R-row
            'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
            # W-row
            'ワ': 'wa', 'ヲ': 'wo',
            # N
            'ン': 'n',
            # Dakuten variants (K -> G)
            'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
            # Dakuten variants (S -> Z)
            'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
            # Dakuten variants (T -> D)
            'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
            # Dakuten variants (H -> B)
            'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
            # Handakuten variants (H -> P)
            'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
            # Contracted sounds
            'キョ': 'kyo', 'ショ': 'sho', 'チョ': 'cho', 'ニョ': 'nyo', 'ヒョ': 'hyo',
            'ミョ': 'myo', 'リョ': 'ryo', 'ギョ': 'gyo', 'ジョ': 'jo', 'ビョ': 'byo',
            'ピョ': 'pyo'
        }

        count = 0
        # Add Hiragana
        for char, romaji in hiragana.items():
            try:
                JapaneseCharacter.objects.create(
                    character=char,
                    romaji=romaji,
                    character_type='hiragana'
                )
                count += 1
                self.stdout.write(f'Added hiragana: {romaji}')
            except Exception as e:
                self.stdout.write(f'Error adding hiragana {romaji}: {str(e)}')

        # Add Katakana
        for char, romaji in katakana.items():
            try:
                JapaneseCharacter.objects.create(
                    character=char,
                    romaji=romaji,
                    character_type='katakana'
                )
                count += 1
                self.stdout.write(f'Added katakana: {romaji}')
            except Exception as e:
                self.stdout.write(f'Error adding katakana {romaji}: {str(e)}')

        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} characters'))
