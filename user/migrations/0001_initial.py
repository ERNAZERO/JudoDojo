# Generated by Django 4.2.5 on 2023-09-17 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("password", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_Coach", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Coach",
            fields=[
                (
                    "myuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("second_name", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("name_of_academy", models.CharField(max_length=255)),
                ("dan", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
            bases=("user.myuser",),
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "myuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("second_name", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=255)),
                ("parent_name", models.CharField(max_length=255)),
                ("parent_surname", models.CharField(max_length=255)),
                ("parent_phone_number", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                (
                    "rating_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=3),
                ),
                ("belt_status", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=("user.myuser",),
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("group_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "coach_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.coach"
                    ),
                ),
                (
                    "student_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.student"
                    ),
                ),
            ],
        ),
    ]