# Generated by Django 3.2.15 on 2022-09-16 13:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competencias', '0002_profesorcursoprograma_curso_programa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('tipo_calificacion', models.CharField(choices=[('Cuantitativa', 'Cuantitativa'), ('Cualitativa', 'Cualitativa')], default='Cualitativa', max_length=12, verbose_name='El tipo de calificación (Cualitativa o Cuantitativa)')),
                ('nombre', models.CharField(max_length=80, verbose_name='Nombre de la evaluación')),
            ],
            options={
                'ordering': ['profesor_curso_programa', 'tipo_actividad', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='CalificacionCualitativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombre que tiene esta calificación (Excelente, sobresaliente, etc)')),
                ('valor_numerico', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Valor numérico asociado a esta calificación cuantitativa')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CalificacionEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('porcentaje', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Porcentaje del nivel evaluación con respecto al profesor curso programa')),
            ],
            options={
                'ordering': ['nivel_evaluacion', 'profesor_curso_programa', 'porcentaje'],
            },
        ),
        migrations.CreateModel(
            name='RestriccionNivelActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('porcentaje', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Porcentaje del tipo actividad con respecto a profesor curso del programa')),
                ('restriccion_nivel_profesor_curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='restricciones_de_nivel_actividad_asociadas', to='competencias.restriccionnivelprofesorcurso', verbose_name='Restricción de porcentaje para un profesor de un curso de programa y un nivel de evaluación')),
            ],
            options={
                'ordering': ['tipo_actividad', 'restriccion_nivel_profesor_curso', 'porcentaje'],
            },
        ),
        migrations.CreateModel(
            name='TipoActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=80, verbose_name='Nombre de la actividad de evaluación')),
                ('restricciones_nivel_profesor_curso', models.ManyToManyField(related_name='tipos_evaluacion_asociadas', to='evaluaciones.RestriccionNivelActividad', verbose_name='Restricciones de nivel de evaluación para un profesor en un curso de programa')),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='restriccionnivelactividad',
            name='tipo_actividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='restricciones_de_nivel_actividad_asociadas', to='evaluaciones.tipoactividad', verbose_name='Actividad asociadas la evaluación y al profesor curso programa'),
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('numeracion', models.PositiveIntegerField()),
                ('contenido', models.CharField(max_length=255)),
                ('porcentaje', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Porcentaje de la pregunta con respecto a la evaluación')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preguntas_asociadas', to='evaluaciones.actividad', verbose_name='Actividad asociada')),
                ('restriccion_nivel_actividad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preguntas_asociadas', to='evaluaciones.restriccionnivelactividad', verbose_name='Restricción de porcentaje entre un tipo actividad y nivel evaluación para un profesor de un curso de un programa')),
            ],
            options={
                'ordering': ['actividad', 'restriccion_nivel_actividad', 'numeracion', 'contenido'],
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activa', models.BooleanField(default=True)),
                ('resultado', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Resultado cuantitativo de la respuesta')),
                ('calificacion_cualitativa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nota_de_estudiante_asociada', to='evaluaciones.calificacioncualitativa', verbose_name='Calificación cualitativa de la pregunta en la evaluación asociada')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
