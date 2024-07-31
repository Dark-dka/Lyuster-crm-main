# Generated by Django 5.0.7 on 2024-07-29 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_quantity_left_mahsulotlar_received_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mahsulotlar',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='mahsulotlar',
            name='Received',
            field=models.PositiveIntegerField(verbose_name='Получено'),
        ),
        migrations.AlterField(
            model_name='mahsulotlar',
            name='Remainder',
            field=models.PositiveIntegerField(verbose_name='Остаток'),
        ),
    ]
