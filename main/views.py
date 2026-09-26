from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q

# education
from main.models import Education
from main.forms import EducationForm

# experience
from main.models import Experience
from main.forms import ExperienceForm

# project
from main.models import Project
from main.forms import ProjectForm

def get_educations_json(request):
    search_query = request.GET.get("title", "").strip()
    educations = Education.objects.all().order_by("-started_at")
    if search_query:
        educations = educations.filter(
            Q(institution__icontains=search_query) |
            Q(degree__icontains=search_query)
        )
    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")


def show_education(request):
    json_response = get_educations_json(request)
    educations = serializers.deserialize("json", json_response.content.decode("utf-8"))
    educations = [edu.object for edu in educations]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Elisia Catherine",
        "education_list": educations,
        "title_query": title_query,
    }
    return render(request, "education.html", context)

# tambah edu
def create_education(request):
    form = EducationForm(request.POST or None, request.FILES or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education") 
    context = {
        "form": form,
        "name": "Elisia Catherine",
    }
    return render(request, "education_form.html", context)

# edit education
def edit_education(request, id):
    education = get_object_or_404(Education, pk=id)
    form = EducationForm(request.POST or None, request.FILES or None, instance=education)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "form": form,
        "name": "Elisia Catherine",
        "education": education,
    }
    return render(request, "education_form.html", context)

# hapus education
def delete_education(request, id):
    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
    return redirect("main:show_education")


def show_main(request):
    context = {
        "name": "Elisia Catherine",
        "npm": "2506533570",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "3rd-semester student at Universitas Indonesia, passionate about "
            "web development. Constantly learning, building, and improving my skills."
        ),
    }
    return render(request, "index.html", context)

# API Data Delivery dalam bentuk JSON
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    # ini buat filternya berdasarkan nama organisasi ATAU title/role
    if title_query:
        experiences = experiences.filter(
            Q(organization__icontains=title_query) | Q(title__icontains=title_query)
        )

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

# Menampilkan datanya
def show_experience(request):
    # Mengambil respons JSON dari endpoint
    json_response = get_experiences_json(request)
    
    # Bongkar JSON dan ubah balik jadi objek Python
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    # Ambil data aslinya supaya bisa dibaca di template HTML
    experiences = [exp.object for exp in experiences]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Elisia Catherine",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

# Untuk tambah data pengalaman
def create_experience(request):
    form = ExperienceForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Elisia Catherine",
        "form": form,
    }
    return render(request, "experience_form.html", context)

# Update atau edit experiencenya
def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, request.FILES or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Elisia Catherine",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)

# Menghapus data experience
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")

# Kode untuk project

# API Data Delivery dalam bentuk JSON
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(
            Q(title__icontains=title_query) | Q(description__icontains=title_query)
        )
    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

# menampilkan datanya di halaman project (ini deserialisasi)
def show_projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects = [item.object for item in projects]

    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Elisia Catherine",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

# menambahkan data project
def create_project(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_projects")

    context = {
        "form": form,
        "name": "Elisia Catherine",
        "project": None,
    }
    return render(request, "project_form.html", context)

# mengedit data project yang sudah ada
def edit_project(request, id):
    project = get_object_or_404(Project, pk=id)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_projects")

    context = {
        "form": form,
        "name": "Elisia Catherine",
        "project": project,
    }
    return render(request, "project_form.html", context)

# untuk hapus data project
def delete_project(request, id):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=id)
        project.delete()
    return redirect("main:show_projects")