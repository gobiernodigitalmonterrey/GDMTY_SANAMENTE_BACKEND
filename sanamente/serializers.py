
from rest_framework import serializers
from .models import CategoriaActividadBienestar, CategoriaServicioProfesional, EspecialidadServicioProfesional, \
    CategoriaEntradaBlog

# Create your serializers here.


class CategoriaActividadBienestarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaActividadBienestar
        fields = '__all__'


class CategoriaServicioProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServicioProfesional
        fields = '__all__'


class CategoriaEntradaBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEntradaBlog
        fields = '__all__'


class EspecialidadServicioProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspecialidadServicioProfesional
        fields = '__all__'

