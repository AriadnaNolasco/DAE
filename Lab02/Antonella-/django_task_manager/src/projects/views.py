from django.shortcuts import render, get_object_or_404, redirect
from .models import Project

# 📌 Listar proyectos
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

# 📌 Crear un nuevo proyecto
def project_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        Project.objects.create(name=name, description=description)
        return redirect('project_list')
    return render(request, 'projects/project_form.html')

# 📌 Editar un proyecto existente
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.save()
        return redirect('project_list')
    return render(request, 'projects/project_form.html', {'project': project})

# 📌 Eliminar un proyecto
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
