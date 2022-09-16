# Generated by Django 3.2.15 on 2022-09-16 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competencias', '0003_initial'),
        ('evaluaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nota',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nota_de_estudiante_asociada', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante que respondió pregunta'),
        ),
        migrations.AddField(
            model_name='nota',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nota_de_estudiante_asociada', to='evaluaciones.pregunta', verbose_name='Pregunta de la evaluación asociada'),
        ),
        migrations.AddField(
            model_name='calificacionevaluacion',
            name='nivel_evaluacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='calificaciones_evaluacion_asociadas', to='competencias.nivelevaluacion', verbose_name='Nivel de evaluación asociado al profesor curso programa'),
        ),
        migrations.AddField(
            model_name='calificacionevaluacion',
            name='profesor_curso_programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='calificaciones_evaluacion_asociadas', to='competencias.restriccionnivelprofesorcurso', verbose_name='Profesor curso programa asociado al nivel de evaluación'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='profesor_curso_programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='actividades_asociadas', to='competencias.profesorcursoprograma', verbose_name='Profesor curso programa asociado'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='tipo_actividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='actividades_asociadas', to='evaluaciones.tipoactividad', verbose_name='Tipo actividad asociadas'),
        ),
    ]
