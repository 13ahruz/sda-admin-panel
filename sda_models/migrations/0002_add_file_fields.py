# Generated migration to add file upload fields without affecting existing data

from django.db import migrations, models
import sda_models.models


class Migration(migrations.Migration):

    dependencies = [
        ('sda_models', '0001_initial'),
    ]

    operations = [
        # Add new file fields to existing models
        migrations.AddField(
            model_name='aboutlogo',
            name='image_file',
            field=models.ImageField(blank=True, help_text='Upload logo image', null=True, upload_to=sda_models.models.upload_to_about_logos),
        ),
        migrations.AddField(
            model_name='project',
            name='cover_photo_file',
            field=models.ImageField(blank=True, help_text='Upload cover photo', null=True, upload_to=sda_models.models.upload_to_project_covers),
        ),
        migrations.AddField(
            model_name='projectphoto',
            name='image_file',
            field=models.ImageField(blank=True, help_text='Upload photo', null=True, upload_to=sda_models.models.upload_to_project_photos),
        ),
        migrations.AddField(
            model_name='news',
            name='photo_file',
            field=models.ImageField(blank=True, help_text='Upload news photo', null=True, upload_to=sda_models.models.upload_to_news_photos),
        ),
        migrations.AddField(
            model_name='newssection',
            name='image_file',
            field=models.ImageField(blank=True, help_text='Upload section image', null=True, upload_to=sda_models.models.upload_to_news_photos),
        ),
        migrations.AddField(
            model_name='teammember',
            name='photo_file',
            field=models.ImageField(blank=True, help_text='Upload member photo', null=True, upload_to=sda_models.models.upload_to_team_photos),
        ),
        migrations.AddField(
            model_name='service',
            name='icon_file',
            field=models.ImageField(blank=True, help_text='Upload service icon', null=True, upload_to=sda_models.models.upload_to_service_icons),
        ),
        migrations.AddField(
            model_name='partnerlogo',
            name='image_file',
            field=models.ImageField(blank=True, help_text='Upload partner logo', null=True, upload_to=sda_models.models.upload_to_partner_logos),
        ),
        migrations.AddField(
            model_name='workprocess',
            name='image_file',
            field=models.ImageField(blank=True, help_text='Upload process image', null=True, upload_to=sda_models.models.upload_to_work_process_images),
        ),
    ]
