from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(ActividadBienestar)
admin.site.register(ActividadBienestarFavorito)
admin.site.register(ActividadBienestarValoracion)
admin.site.register(CategoriaActividadBienestar)
admin.site.register(CategoriaServicioProfesional)
admin.site.register(EspecialidadServicioProfesional)
admin.site.register(ModalidadServicioProfesional)
admin.site.register(NumeroTelefonicoEmergencia)
admin.site.register(ServicioProfesional)
admin.site.register(ServicioProfesionalFavorito)
admin.site.register(ServicioProfesionalValoracion)
