# Generated manually

from django.db import migrations
from django.utils import timezone

def set_default_timestamps(apps, schema_editor):
    Notice_Board = apps.get_model('cse_app', 'Notice_Board')
    for notice in Notice_Board.objects.filter(created_at__isnull=True):
        notice.created_at = timezone.now()
        notice.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cse_app', '0017_notice_board_created_by_scrollingnotice_created_by'),
    ]

    operations = [
        migrations.RunPython(set_default_timestamps),
    ]