# Generated by Django 4.0.4 on 2022-07-19 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0003_remove_jeopardy_answer_remove_jeopardy_answered_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
    ]
