# Generated by Django 3.1.7 on 2021-04-13 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('end_value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('mode', models.CharField(choices=[('sum', 'Сумма'), ('avg', 'Среднее значение'), ('max', 'Максимальное значение')], max_length=3)),
                ('invert_value', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurposeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True)),
                ('purpose', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='purpose.purpose')),
            ],
        ),
        migrations.CreateModel(
            name='PurposeResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('purpose', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purpose.purpose')),
            ],
        ),
    ]
