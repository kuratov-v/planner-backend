# Generated by Django 3.1.7 on 2021-04-30 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purpose', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purposeresult',
            name='purpose',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='results', to='purpose.purpose'),
        ),
        migrations.AlterField(
            model_name='purposestatus',
            name='purpose',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='purpose.purpose'),
        ),
    ]
