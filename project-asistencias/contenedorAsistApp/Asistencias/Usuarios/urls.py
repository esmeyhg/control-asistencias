from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.conf import settings
from Asistencias import settings
from django.conf.urls import url,include    
app_name="Usuarios"

urlpatterns = [
    path('%slogin/' % settings.PATH_PREFIX, ingresar, name='login'),
    path('%sregistro/' % settings.PATH_PREFIX, registrar, name='registro'),
    path('%slogout/' % settings.PATH_PREFIX, salir, name='logout'),
    path('%sdelete/' % settings.PATH_PREFIX, login_required(borrar_usuario), name='delete'),
    path('%scuenta/' % settings.PATH_PREFIX, login_required(cuenta_usuario), name='cuenta'),
    path('%sestudiantes/' % settings.PATH_PREFIX, login_required(mostrar_estudiantes), name='estudiantes'),
    path('%sregistrarEstudiante/' % settings.PATH_PREFIX, login_required(crear_estudiante), name='registrarEstudiante'),
    path('%sdeleteEstudiante/<int:idEstudiante>' % settings.PATH_PREFIX, login_required(borrar_estudiante), name='deleteEstudiante'),
    path('%sdetalleEstudiante/<int:idEstudiante>' % settings.PATH_PREFIX, login_required(edit), name='detalleEstudiante'),
    path('%supdateEstudiante/<int:idEstudiante>' % settings.PATH_PREFIX, login_required(update), name='updateEstudiante'),
    path('%sfacilitadores/' % settings.PATH_PREFIX, login_required(mostrar_facilitadores), name='facilitadores'),
    path('%sregistrarFacilitador/' % settings.PATH_PREFIX, login_required(crear_facilitador), name='registrarFacilitador'),
    path('%sdeleteFacilitador/<int:idFacilitador>' % settings.PATH_PREFIX, login_required(borrar_facilitador), name='deleteFacilitador'),
    path('%supdateFacilitador/<int:idFacilitador>' % settings.PATH_PREFIX, login_required(update_facilitador), name='updateFacilitador'),
    path('%sproveedores/' % settings.PATH_PREFIX, login_required(mostrar_proveedores), name='proveedores'),
    path('%sregistrarProveedor/' % settings.PATH_PREFIX, login_required(crear_proveedor), name='registrarProveedor'),
    path('%sdeleteProveedor/<int:idProveedor>' % settings.PATH_PREFIX, login_required(borrar_proveedor), name='deleteProveedor'),
    path('%supdateProveedor/<int:idProveedor>' % settings.PATH_PREFIX, login_required(update_proveedor), name='updateProveedor'),
    path('%splaticas/' % settings.PATH_PREFIX, login_required(mostrar_platicas), name='platicas'),
    path('%sregistrarPlatica/' % settings.PATH_PREFIX, login_required(crear_platica), name='registrarPlatica'),
    path('%sdeletePlatica/<int:idPlatica>' % settings.PATH_PREFIX, login_required(borrar_platica), name='deletePlatica'),
    path('%supdatePlatica/<int:idPlatica>' % settings.PATH_PREFIX, login_required(update_platica), name='updatePlatica'),
    path('%sasistencias/<int:idPlatica>' % settings.PATH_PREFIX, login_required(mostrar_asistencias_platica), name='asistenciasPlatica'),
    path('%sasistencias/' % settings.PATH_PREFIX, login_required(mostrar_asistencias), name='asistencias'),
    path('%sregistrarAsistencias/' % settings.PATH_PREFIX, login_required(crear_asistencias), name='registrarAsistencias'),
    path('%sdeleteAsistencias/<int:idAsistencia>' % settings.PATH_PREFIX, login_required(borrar_asistencias), name='deleteAsistencias'),
    path('%supdateAsistencias/<int:idAsistencia>' % settings.PATH_PREFIX, login_required(update_asistencias), name='updateAsistencias'),
]