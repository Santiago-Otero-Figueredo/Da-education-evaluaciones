from pprint import pprint
from django.db.models import Q, QuerySet

from apps.core.models import ModeloBase

from typing import List, Optional

from django.contrib.auth.models import AbstractUser
from django.db import models




class Usuario(AbstractUser, ModeloBase):
    codigo = models.CharField(max_length=30, verbose_name="código del usuario", null=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['first_name', 'last_name']
        permissions = (
            ("gestionar_usuarios", "Usuarios - Gestionar"),
            ("cargar_estudiantes", "Usuarios - Cargar estudiantes"),
            ("cargar_personal", "Usuarios - Cargar usuarios"),
            ("matricular_estudiantes", "Usuarios - Matricular estudiantes"),
            ("gestionar_configuracion_formularios", "Configuración formularios"),
            ("gestionar_estados_estudiantes", "Usuarios - Gestionar estados estudiantes"),
        )

    def obtener_rol(self):
        return self.groups.first()

    @staticmethod
    def obtener_estudiantes():
        return Usuario.objects.filter(groups__name="Estudiante", is_active=True)

    @staticmethod
    def obtener_profesores():
        return Usuario.objects.filter(
            Q(groups__name="Profesor"),
            is_active=True,
        ).distinct()

    @staticmethod
    def obtener_todos_los_estudiantes():
        return Usuario.objects.filter(
            Q(groups__name="Estudiante"),
            is_active=True
        ).distinct()

    @staticmethod
    def obtener_estudiante_por_codigo(codigo: str) -> Optional['Usuario']:
        try:
            return Usuario.objects.get(codigo=codigo)
        except Usuario.DoesNotExist:
            return None


    @staticmethod
    def crear(usuario, rol):
        from django.contrib.auth.models import Group

        # usuario: es una Serie (pandas) o diccionario con los datos básicos del usuario
        # password será primera letra del nombre mayuscula, codigo y primera letra del apellido mayuscula

        # TODO: Cambiar el tema del codigo a una clase aparte, porque se sale del estandar

        codigo = usuario["codigo"]
        nombre = usuario["nombre"].upper().strip()
        apellido = usuario["apellido"].upper().strip()

        password = "{}{}{}".format(nombre[0], usuario["email"].strip().split("@")[0], apellido[0])
        usuario = Usuario.objects.create_user(
            username=usuario["email"].strip(),
            first_name=nombre,
            last_name=apellido,
            email=usuario["email"].strip(),
            password=password,
            codigo=codigo
        )

        rol = Group.objects.get(name=rol)
        rol.user_set.add(usuario)

        return usuario

    def obtener_informacion_notas_estudiante(self, id_profesor_curso_programa:int, campos: List[str], agrupacion: List[str], agrupacion_suma: List[str]) -> dict:
        import pandas as pd

        consulta_respuestas = self.nota_de_estudiante_asociada.filter(
            pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__profesor_curso_programa__pk=id_profesor_curso_programa
        ).values(*campos).order_by(*agrupacion)

        df_respuestas = pd.DataFrame(consulta_respuestas)

        df_respuestas = df_respuestas.fillna(0)
        df_respuestas['calificaciones'] = df_respuestas['calificacion_cualitativa__valor_maximo'] + df_respuestas['resultado']
        df_respuestas = df_respuestas.drop(columns=['calificacion_cualitativa__valor_maximo', 'resultado'])
        df_respuestas['resultado_por_porcentaje'] = df_respuestas['calificaciones'] * df_respuestas['pregunta__porcentaje']

        df_total_porcentaje = df_respuestas.groupby(
            agrupacion_suma
        )['pregunta__porcentaje', 'resultado_por_porcentaje'].sum()

        df_total_porcentaje['df_resultado_ponderado'] = df_total_porcentaje['resultado_por_porcentaje'] / df_total_porcentaje['pregunta__porcentaje']
        diccionario_calificaciones = df_total_porcentaje['df_resultado_ponderado'].to_dict()

        return diccionario_calificaciones

    def obtener_respuestas_estudiante(self, id_profesor_curso_programa: int):
        from apps.competencias.models import RestriccionNivelProfesorCurso

        diccionario_calificaciones = self.obtener_informacion_notas_estudiante(
            id_profesor_curso_programa=id_profesor_curso_programa,
            campos=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk',
                    'calificacion_cualitativa__valor_maximo', 'resultado',
                    'pregunta__porcentaje', 'pregunta__actividad'],
            agrupacion=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk'],
            agrupacion_suma=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk']
        )


        diccionario_resumen = {}
        for calificacion, resultado in diccionario_calificaciones.items():
            diccionario_resumen[RestriccionNivelProfesorCurso.obtener_por_id(calificacion)] = round(resultado, 2)

        pprint(diccionario_calificaciones)
        return diccionario_resumen


    def obtener_respuestas_estudiante_por_evaluacion(self, id_profesor_curso_programa: int):
        from apps.competencias.models import RestriccionNivelProfesorCurso
        from apps.evaluaciones.models import Actividad

        diccionario_calificaciones = self.obtener_informacion_notas_estudiante(
            id_profesor_curso_programa=id_profesor_curso_programa,
            campos=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk',
                    'calificacion_cualitativa__valor_maximo', 'resultado',
                    'pregunta__porcentaje', 'pregunta__actividad'],
            agrupacion=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk'],
            agrupacion_suma=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk',
            'pregunta__actividad']
        )



        diccionario_resumen = {}
        for calificacion, resultado in diccionario_calificaciones.items():
            calificacion_nivel = RestriccionNivelProfesorCurso.obtener_por_id(calificacion[0])
            if calificacion_nivel not in diccionario_resumen.keys():
                diccionario_resumen[calificacion_nivel] = []

            diccionario_resumen[calificacion_nivel].append(
                    {Actividad.obtener_por_id(calificacion[1]):round(resultado, 2)}
                )

        pprint(diccionario_resumen)
        return diccionario_resumen


    def obtener_respuestas_estudiante_por_pregunta(self, id_profesor_curso_programa: int):
        from apps.competencias.models import RestriccionNivelProfesorCurso
        from apps.evaluaciones.models import Actividad, Pregunta

        diccionario_resultados = self.obtener_informacion_notas_estudiante(
            id_profesor_curso_programa=id_profesor_curso_programa,
            campos=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk',
                    'calificacion_cualitativa__valor_maximo', 'resultado',
                    'pregunta__porcentaje', 'pregunta__actividad', 'pregunta'],
            agrupacion=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk'],
            agrupacion_suma=['pregunta__restriccion_nivel_actividad__restriccion_nivel_profesor_curso__pk',
            'pregunta__actividad', 'pregunta']
        )



        diccionario_resumen = {}
        for calificacion, resultado in diccionario_resultados.items():
            restriccion_nivel = RestriccionNivelProfesorCurso.obtener_por_id(calificacion[0])
            if restriccion_nivel not in diccionario_resumen.keys():
                diccionario_resumen[restriccion_nivel] = []

            diccionario_calificaciones = {}
            actividad = Actividad.obtener_por_id(calificacion[1])
            if actividad not in diccionario_calificaciones.keys():
                diccionario_calificaciones[actividad] = []

            pregunta = Pregunta.obtener_por_id(calificacion[2])
            diccionario_calificaciones[actividad].append(
                {pregunta:round(resultado, 2)}
            )

            diccionario_resumen[restriccion_nivel].append(
                diccionario_calificaciones
            )


        pprint(diccionario_resumen)

        return diccionario_resultados


    def obtener_profesores_por_curso_del_programa(id_curso_del_programa: int) -> QuerySet['Usuario']:

        return Usuario.obtener_profesores().filter(
            profesor_curso_programa_asociados__curso_programa__pk=id_curso_del_programa
        )
