from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_song_song_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='lyrics',
            field=models.TextField(blank=True, null=True),
        ),
    ]
