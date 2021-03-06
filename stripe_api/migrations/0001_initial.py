# Generated by Django 3.1.4 on 2020-12-07 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment_Method",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("card_type", models.CharField(max_length=50)),
                ("card_number", models.BigIntegerField()),
                ("card_exp_month_year", models.DateField()),
                ("card_cvc", models.IntegerField()),
                ("stripe_payment_method_id", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=100)),
                ("stripe_customer_id", models.CharField(max_length=50)),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stripe_api.payment_method",
                    ),
                ),
            ],
        ),
    ]
