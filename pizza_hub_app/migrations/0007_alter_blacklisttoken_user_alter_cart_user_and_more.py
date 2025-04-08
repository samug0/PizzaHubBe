# Generated by Django 5.1.7 on 2025-04-07 23:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_hub_app', '0006_alter_blacklisttoken_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklisttoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.user'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.user'),
        ),
        migrations.AlterField(
            model_name='cartproductextra',
            name='additional_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.additionalproduct'),
        ),
        migrations.AlterField(
            model_name='cartproductextra',
            name='cart_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.cartproduct'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.user'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.order'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.product'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.order'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.user'),
        ),
        migrations.AlterField(
            model_name='productpayment',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.payments'),
        ),
        migrations.AlterField(
            model_name='productpayment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza_hub_app.product'),
        ),
    ]
