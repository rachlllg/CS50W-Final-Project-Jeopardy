# Generated by Django 4.0.4 on 2022-07-19 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0002_jeopardy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jeopardy',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='answered',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='category',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='choiceone',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='choicethree',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='choicetwo',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='clue',
        ),
        migrations.RemoveField(
            model_name='jeopardy',
            name='cluevalue',
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=2000)),
                ('clue', models.CharField(max_length=2000)),
                ('cluevalue', models.IntegerField(choices=[(100, 'One'), (200, 'Two'), (300, 'Three'), (400, 'Four'), (500, 'Five')])),
                ('answer', models.CharField(max_length=2000)),
                ('choiceone', models.CharField(max_length=2000)),
                ('choicetwo', models.CharField(max_length=2000)),
                ('choicethree', models.CharField(max_length=2000)),
                ('answered', models.BooleanField(default=False)),
                ('jeopardy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jeopardy.jeopardy')),
            ],
        ),
    ]