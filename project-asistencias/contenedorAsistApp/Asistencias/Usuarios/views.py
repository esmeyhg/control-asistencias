import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from Usuarios.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models import Q
from django import forms
from .models import *
from Asistencias import settings
from django.conf import settings
import hashlib
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#METODOS DEL USUARIO, INGRESAR AL SISTEMA, REGISTRARSE, CONSULTAR SU INFO. Y ACTUALIZARLA.

def ingresar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("Usuarios:estudiantes")
        else:
            return render(request, "login.html")

    elif request.method == 'POST':

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)


        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("Usuarios:estudiantes")
        else:
            return render(request, 'login.html', {'mensaje': 'error'})


def registrar(request):
    if request.method == 'GET':
        form = CrearUsuarioForm(use_required_attribute=False)
        return render(request, 'registro.html', {'form': form})
    elif request.method == 'POST':
        form = CrearUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.is_active=True
            instance.save()
            return render(request, 'login.html', {'form': form, 'mensaje':'success'})
        else:
            form = CrearUsuarioForm(request.POST)
            return render(request, 'registro.html', {'form': form})

def abrir_home(request):
    return render(request, "estudiantes/estudiantes.html")

def cuenta_usuario(request):
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("Usuarios:cuenta")
    elif request.method == 'DELETE':
        usuario = User.objects.get(username=request.user.username)
        usuario.is_active = False
        usuario.save()
        logout(request)
        return redirect("Usuarios:login")
    else:
        form = ModificarUsuarioForm(instance=request.user)
        return render(request, "cuenta.html", {"form": form})

def borrar_usuario(request):
    usuario = Usuario.objects.get(username=request.user.username)
    usuario.is_active = False
    usuario.save()
    logout(request)
    return redirect("Usuarios:login")

#METODOS DE LOS ESTUDIANTES, MOSTRAR, REGISTRAR, ELIMINAR Y ACTUALIZAR INFORMACION

def mostrar_estudiantes(request):
    estudiantes_lista = Estudiante.objects.filter(estado = True)
    page = request.GET.get('page', 1)
    paginator = Paginator(estudiantes_lista, 20)
    try:
        estudiantes = paginator.page(page)
    except PageNotAnInteger:
        estudiantes = paginator.page(1)
    except EmptyPage:
        estudiantes = paginator.page(paginator.num_pages)
    return render(request, "estudiantes/estudiantes.html", {'estudiantes':estudiantes})

@transaction.atomic
def crear_estudiante(request):
    if request.method == 'GET':
        estudianteForm = EstudianteForm(request.POST or None)
        return render(request, 'estudiantes/registrar_estudiante.html', {'form': estudianteForm})
    elif request.method == 'POST':
        estudianteForm = EstudianteForm(request.POST, request.FILES)
        if estudianteForm.is_valid():
            estudianteForm.save()
            messages.success(request, 'Estudiante registrado exitosamente.')
            return redirect("Usuarios:estudiantes")
        else:
            estudianteForm = EstudianteForm(request.POST)
            messages.error(request, 'No se pudo registrar el estudiante.')
            return render(request, 'estudiantes/registrar_estudiante.html', {'form': estudianteForm})

def borrar_estudiante (request, idEstudiante):
    estudiante = Estudiante.objects.get(id=idEstudiante)
    estudiante.estado = False
    estudiante.save()
    messages.success(request, 'Estudiante dado de baja exitosamente.')
    return redirect("Usuarios:estudiantes")


def edit(request, idEstudiante):
    estudiante = Estudiante.objects.get(id=idEstudiante)
    return render (request, 'estudiantes/principal_estudiante.html', {'estudiante':estudiante})

def update(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, id=idEstudiante)
    estudianteForm = EstudianteForm(request.POST or None, instance=estudiante)
    if estudianteForm.is_valid():
        estudianteForm.save()
        messages.success(request, 'Estudiante actualizado exitosamente.')
        return redirect("Usuarios:estudiantes")
    return render(request, 'estudiantes/editar_estudiante.html', {'form':estudianteForm, 'estudiante':estudiante})

#METODOS DE LOS PROVEEDORES, MOSTRAR, REGISTRAR, ELIMINAR, ACTUALIZAR
def mostrar_proveedores(request):
    proveedores_lista = Proveedor.objects.filter(estado = True)
    page = request.GET.get('page', 1)
    paginator = Paginator(proveedores_lista, 10)
    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)
    return render(request, "proveedores/proveedores.html", {'proveedores':proveedores})

@transaction.atomic
def crear_proveedor(request):
    if request.method == 'GET':
        proveedorForm = ProveedorForm(request.POST or None)
        return render(request, 'proveedores/registrar_proveedor.html', {'form': proveedorForm})
    elif request.method == 'POST':
        proveedorForm = ProveedorForm(request.POST, request.FILES)
        if proveedorForm.is_valid():
            proveedorForm.save()
            messages.success(request, 'Proveedor registrado exitosamente.')
            return redirect("Usuarios:proveedores")
        else:
            proveedorForm = ProveedorForm(request.POST)
            messages.error(request, 'No se pudo registrar el proveedor.')
            return render(request, 'proveedores/registrar_proveedor.html', {'form': proveedorForm})

def borrar_proveedor(request, idProveedor):
    proveedor = Proveedor.objects.get(id=idProveedor)
    proveedor.estado = False
    proveedor.save()
    messages.success(request, 'Proveedor dado de baja exitosamente.')
    return redirect("Usuarios:proveedores")

def update_proveedor(request, idProveedor):
    proveedor = get_object_or_404(Proveedor, id=idProveedor)
    proveedorForm = ProveedorForm(request.POST or None, instance=proveedor)
    if proveedorForm.is_valid():
        proveedorForm.save()
        messages.success(request, 'Proveedor actualizado exitosamente.')
        return redirect("Usuarios:proveedores")
    return render(request, 'proveedores/editar_proveedor.html', {'form':proveedorForm, 'proveedor':proveedor})

#METODOS DE LOS FACILITADORES, MOSTRAR, REGISTRAR, ELIMINAR, ACTUALIZAR
def mostrar_facilitadores(request):
    facilitadores_lista = Facilitador.objects.filter(estado = True)

    page = request.GET.get('page', 1)
    paginator = Paginator(facilitadores_lista, 10)
    try:
        facilitadores = paginator.page(page)
    except PageNotAnInteger:
        facilitadores = paginator.page(1)
    except EmptyPage:
        facilitadores = paginator.page(paginator.num_pages)

    return render(request, 'facilitadores/facilitadores.html', {'facilitadores':facilitadores})

def borrar_facilitador(request, idFacilitador):
    facilitador = Facilitador.objects.get(id=idFacilitador)
    facilitador.estado = False
    facilitador.save()
    messages.success(request, 'Ponente dado de baja exitosamente.')
    return redirect("Usuarios:facilitadores")

@transaction.atomic
def crear_facilitador(request):
    if request.method == 'GET':
        facilitadorForm = FacilitadorForm(request.POST or None)
        return render(request, 'facilitadores/registro_facilitador.html', {'form': facilitadorForm})
    elif request.method == 'POST':
        facilitadorForm = FacilitadorForm(request.POST, request.FILES)
        if facilitadorForm.is_valid():
            facilitadorForm.save()
            messages.success(request, 'Ponente registrado exitosamente.')
            return redirect("Usuarios:facilitadores")
        else:
            facilitadorForm = FacilitadorForm(request.POST)
            messages.error(request, 'No se pudo registrar el ponente.')
            return render(request, 'facilitadores/registro_facilitador.html', {'form': facilitadorForm})


def update_facilitador(request, idFacilitador):
    facilitador = get_object_or_404(Facilitador, id=idFacilitador)
    facilitadorForm = FacilitadorForm(request.POST or None, instance=facilitador)
    if facilitadorForm.is_valid():
        facilitadorForm.save()
        messages.success(request, 'Ponente actualizado exitosamente.')
        return redirect("Usuarios:facilitadores")
    return render(request, 'facilitadores/editar_facilitador.html', {'form':facilitadorForm, 'facilitador':facilitador})


#METODOS DE LAS PLÁTICAS, MOSTRAR, REGISTRAR, ELIMINAR, ACTUALIZAR
def mostrar_platicas(request):
    platicas_lista = Platica.objects.filter(estado = True)
    page = request.GET.get('page', 1)
    paginator = Paginator(platicas_lista, 10)
    try:
        platicas = paginator.page(page)
    except PageNotAnInteger:
        platicas = paginator.page(1)
    except EmptyPage:
        platicas = paginator.page(paginator.num_pages)
    return render(request, 'platicas/platicas.html', {'platicas':platicas})

def borrar_platica(request, idPlatica):
    platica = Platica.objects.get(id=idPlatica)
    platica.estado = False
    platica.save()
    messages.success(request, 'Plática dada de baja exitosamente.')
    return redirect("Usuarios:platicas")

@transaction.atomic
def crear_platica(request):
    if request.method == 'GET':
        platicaForm = PlaticaForm(request.POST or None)
        return render(request, 'platicas/registrar_platica.html', {'form': platicaForm})
    elif request.method == 'POST':
        platicaForm = PlaticaForm(request.POST, request.FILES)
        if platicaForm.is_valid():
            platicaForm.save()
            messages.success(request, 'Plática registrada exitosamente.')
            asistenciasForm = AsistenciaForm(request.POST or None)
            return redirect("Usuarios:registrarAsistencias", {'form': asistenciasForm})
        else:
            platicaForm = PlaticaForm(request.POST)
            messages.error(request, 'No se pudo registrar la plática.')
            return render(request, 'platicas/registrar_platica.html', {'form': platicaForm})


def update_platica(request, idPlatica):
    platica = get_object_or_404(Platica, id=idPlatica)
    platicaForm = PlaticaForm(request.POST or None, instance=platica)
    if platicaForm.is_valid():
        platicaForm.save()
        messages.success(request, 'Plática actualizada exitosamente.')
        return redirect("Usuarios:platicas")
    return render(request, 'platicas/editar_platica.html', {'form':platicaForm, 'platica':platica})


#METODOS DE LAS ASISTENCIAS, MOSTRAR, REGISTRAR, ELIMINAR Y ACTUALIZAR INFORMACION

def mostrar_asistencias(request):
    asistencias_lista = Asistencia.objects.all().order_by('idPlatica')
    page = request.GET.get('page', 1)
    paginator = Paginator(asistencias_lista, 3)
    try:
        asistencias = paginator.page(page)
    except PageNotAnInteger:
        asistencias = paginator.page(1)
    except EmptyPage:
        asistencias = paginator.page(paginator.num_pages)
    return render(request, 'asistencias/asistencias.html', {'asistencias':asistencias})

def mostrar_asistencias_platica(request, idPlatica):
    asistencias_lista = Asistencia.objects.filter(idPlatica=idPlatica, asistencia=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(asistencias_lista, 3)
    try:
        asistencias = paginator.page(page)
    except PageNotAnInteger:
        asistencias = paginator.page(1)
    except EmptyPage:
        asistencias = paginator.page(paginator.num_pages)
    return render(request, 'asistencias/asistencias.html', {'asistencias':asistencias})


@transaction.atomic
def crear_asistencias(request):
    if request.method == 'GET':
        asistenciasForm = AsistenciaForm(request.POST or None)
        return render(request, 'asistencias/crear_asistencias.html', {'form': asistenciasForm})
    elif request.method == 'POST':
        asistenciasForm = AsistenciaForm(request.POST, request.FILES)
        if asistenciasForm.is_valid():
            asistenciasForm.save()
            messages.success(request, 'Asistencias registradas exitosamente.')
            return redirect("Usuarios:asistencias")
        else:
            asistenciasForm = AsistenciaForm(request.POST)
            messages.error(request, 'No se pudieron registrar las asistencias.')
            return render(request, 'asistencias/crear_asistencias.html', {'form': asistenciasForm})

def borrar_asistencias (request, idAsistencia):
    asistencias = Asistencia.objects.get(id=idAsistencia)
    asistencias.estado = False
    asistencias.save()
    messages.success(request, 'Asistencias eliminadas exitosamente.')
    return redirect("Usuarios:asistencias")

def update_asistencias(request, idAsistencia):
    asistencias = Asistencia.objects.get(id=idAsistencia)
    asistenciasForm = AsistenciaForm(request.POST or None, instance=asistencias)
    if asistenciasForm.is_valid():
        asistenciasForm.save()
        messages.success(request, 'Asistencias actualizadas exitosamente.')
        return redirect("Usuarios:asistencias")
    return render(request, 'asistencias/editar_asistencias.html', {'form':asistenciasForm, 'asistencias':asistencias})


def salir(request):
    logout(request)
    return redirect("Usuarios:login")