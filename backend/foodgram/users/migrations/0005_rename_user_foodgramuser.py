# Generated by Django 4.2 on 2023-04-24 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('authtoken', '0003_tokenproxy'),
        ('recipes', '0002_rename_title_recipe_name_and_more'),
        ('users', '0004_user_delete_foodgramuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='FoodgramUser',
        ),
    ]
