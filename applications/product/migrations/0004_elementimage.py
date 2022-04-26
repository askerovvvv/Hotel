# Generated by Django 4.0.4 on 2022-04-26 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_options_alter_element_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='imagesfromsite')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='product.element')),
            ],
        ),
    ]
