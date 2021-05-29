# Generated by Django 3.1.7 on 2021-05-29 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checklist',
            options={'ordering': ['-id'], 'verbose_name': 'Чек-лист', 'verbose_name_plural': 'Чек-листы'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-id'], 'verbose_name': 'Пункт', 'verbose_name_plural': 'Пункты'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Секция', 'verbose_name_plural': 'Секции'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['is_complete', '-date', '-id'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AddField(
            model_name='checklist',
            name='is_hide_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='is_hide_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_lists', to='todo.task'),
        ),
        migrations.AlterField(
            model_name='item',
            name='check_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='todo.checklist'),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='section',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='todo.project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='todo.section'),
        ),
    ]
