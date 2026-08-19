"""
初期データを投入するマネジメントコマンド
実行: python manage.py seed_data
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '週間チャレンジ・就労マナークイズの初期データを投入します'

    def handle(self, *args, **options):
        from gamification.seed_data import run
        run()
        self.stdout.write(self.style.SUCCESS('✅ 初期データの投入が完了しました'))
