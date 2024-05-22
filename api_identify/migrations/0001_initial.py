# Generated by Django 5.0.6 on 2024-05-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenumber', models.TextField(blank=True, db_index=True, null=True)),
                ('email', models.TextField(blank=True, db_index=True, null=True)),
                ('linkedId', models.IntegerField(blank=True, null=True)),
                ('linkprecedence', models.TextField(choices=[('primary', 'primary'), ('secondary', 'secondary')], default='primary')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
