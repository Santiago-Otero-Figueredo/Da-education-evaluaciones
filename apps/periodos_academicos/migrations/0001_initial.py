# Generated by Django 3.2.15 on 2022-09-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodoAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('ano', models.PositiveIntegerField(verbose_name='año del periodo académico')),
                ('periodo', models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III')], max_length=3, verbose_name='periodo académico')),
                ('fecha_inicio', models.DateField(verbose_name='fecha de inicio del periodo académico')),
                ('fecha_fin', models.DateField(verbose_name='fecha de finalización del periodo académico')),
            ],
            options={
                'ordering': ['-ano', '-periodo'],
                'permissions': (('gestionar_periodos_academicos', 'Periodos académicos - Gestionar'),),
                'unique_together': {('ano', 'periodo')},
            },
        ),
    ]
