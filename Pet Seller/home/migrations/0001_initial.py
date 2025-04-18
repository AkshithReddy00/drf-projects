# Generated by Django 5.1.6 on 2025-03-15 21:31

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalBreed',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('animal_breed', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnimalColor',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('animal_color', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('category_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('animal_views', models.IntegerField(default=0)),
                ('animal_likes', models.IntegerField(default=1)),
                ('animal_name', models.CharField(max_length=100)),
                ('animal_description', models.TextField()),
                ('animal_slug', models.SlugField(max_length=1000, unique=True)),
                ('animal_gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=100)),
                ('animal_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal', to=settings.AUTH_USER_MODEL)),
                ('animal_breed', models.ManyToManyField(blank=True, null=True, to='home.animalbreed')),
                ('animal_colour', models.ManyToManyField(blank=True, null=True, to='home.animalcolor')),
                ('animal_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_category', to='home.category')),
            ],
            options={
                'ordering': ['animal_name'],
            },
        ),
        migrations.CreateModel(
            name='AnimalImages',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('animal_images', models.ImageField(upload_to='animals')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_images', to='home.animal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnimalLocation',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('location', models.CharField(max_length=100)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_location', to='home.animal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
