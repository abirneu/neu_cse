# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cse_app', '0018_update_notice_timestamps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice_board',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notice_board',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]