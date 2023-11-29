# Generated by Django 4.2.7 on 2023-11-28 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='feedback',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_set', to='feedback.trip'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='driver_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.driver'),
        ),
    ]
