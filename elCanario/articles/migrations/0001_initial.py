# Generated by Django 4.1.3 on 2023-04-20 23:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Precio de compra')),
                ('increase', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Incremento')),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Precio de venta')),
            ],
            options={
                'verbose_name': 'Artículo',
                'verbose_name_plural': 'Artículos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ArticleOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
            ],
        ),
        migrations.CreateModel(
            name='ArticlePromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('total_purchased', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, max_length=128, null=True, verbose_name='Descripcion')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Cantidad')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Gasto',
                'verbose_name_plural': 'Gastos',
                'ordering': ['total_cost'],
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.category')),
            ],
            options={
                'verbose_name': 'Valor',
                'verbose_name_plural': 'Valores',
                'ordering': ['name'],
                'unique_together': {('name', 'category_id')},
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveSmallIntegerField(default=0, verbose_name='Existencias')),
                ('article_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='articles.article', verbose_name='Artículo')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
                'ordering': ['article_id', 'stock'],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Descuento')),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='$ VENTA')),
                ('remainder', models.SmallIntegerField(blank=True, null=True, verbose_name='Cantidad restante')),
                ('article_id', models.ManyToManyField(through='articles.ArticlePromotion', to='articles.article', verbose_name='Artículos')),
            ],
            options={
                'verbose_name': 'Promoción',
                'verbose_name_plural': 'Promociones',
                'ordering': ['sell_price'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_quantity', models.PositiveSmallIntegerField(blank=True, editable=False, null=True, verbose_name='Cantidad de Artículos')),
                ('total_pay', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='Total a pagar')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Detalles')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de ultima modificación')),
                ('delivery_status', models.BooleanField(default=False, verbose_name='Estado de la entrega')),
                ('article_id', models.ManyToManyField(through='articles.ArticleOrder', to='articles.article', verbose_name='Artículos')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['customer_id'],
            },
        ),
        migrations.CreateModel(
            name='ArticleValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.category')),
                ('value_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.value')),
            ],
            options={
                'verbose_name': 'Valores y Categorías de Artículo',
                'verbose_name_plural': 'Valores y Categorías de Artículos',
                'unique_together': {('article_id', 'category_id')},
            },
        ),
        migrations.AddField(
            model_name='articlepromotion',
            name='promotion_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.promotion'),
        ),
        migrations.AddField(
            model_name='articleorder',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.order'),
        ),
        migrations.AddField(
            model_name='article',
            name='characteristics_id',
            field=models.ManyToManyField(blank=True, related_name='characteristics_id', through='articles.ArticleValue', to='articles.value'),
        ),
    ]
