# Generated by Django 3.1.7 on 2021-03-15 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210315_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Product name',
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=1, max_length=120, unique=True, verbose_name='Product name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, verbose_name='Nick-name'),
        ),
    ]
