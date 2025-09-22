# Generated manually

from django.db import migrations
from django.utils import timezone

def update_empty_timestamps(apps, schema_editor):
    Notice_Board = apps.get_model('cse_app', 'Notice_Board')
    for notice in Notice_Board.objects.filter(created_at__isnull=True):
        notice.created_at = timezone.now()
        notice.updated_at = timezone.now()
        notice.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cse_app', '0019_update_notice_board_timestamps'),
    ]

    operations = [
        migrations.RunPython(update_empty_timestamps),
    ]