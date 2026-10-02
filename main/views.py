from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
# tutorial 4
import datetime 
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied

# education
from main.models import Education
from main.forms import EducationForm

# experience
from main.models import Experience
from main.forms import ExperienceForm

# project
from main.models import Project
from main.forms import ProjectForm

# Tutorial 4 (menambahkan yang belum aja)
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Tutorial 5
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# TUGAS 4
# Helper untuk memeriksa apakah user bisa mengedit (Superuser atau Group Editor)
def is_editor_or_superuser(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name="Editor").exists())

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Elisia Catherine",
        "npm": "2506533570",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "3rd-semester student at Universitas Indonesia, passionate about "
            "web development. Constantly learning, building, and improving my skills."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

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
        "is_editor": is_editor_or_superuser(request.user),
    }
    return render(request, "education.html", context)

# tambah edu
@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
@login_required(login_url="/login/")
def edit_education(request, id):
    if not is_editor_or_superuser(request.user):
        raise PermissionDenied
    
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
@login_required(login_url="/login/")
def delete_education(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
    return redirect("main:show_education")

# tugas 5: endpoint JSON disusun manual dengan JsonResponse (termasuk info star)
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    filter_type = request.GET.get("filter", "")
    experiences = Experience.objects.prefetch_related("starred_by").order_by("-started_at")

    # filter berdasarkan nama organisasi ATAU title/role
    if title_query:
        experiences = experiences.filter(
            Q(organization__icontains=title_query) | Q(title__icontains=title_query)
        )
    if filter_type == "starred":
        if request.user.is_authenticated:
            experiences = experiences.filter(starred_by=request.user)
        else:
            experiences = experiences.none()

    data = []
    for exp in experiences:
        starred_users = list(exp.starred_by.all())
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "organization": exp.organization,
                "description": exp.description,
                "category_display": exp.get_category_display(),
                "thumbnail": exp.thumbnail.url if exp.thumbnail else "",
                "started_at": exp.started_at.strftime("%B %Y"),
                "ended_at": exp.ended_at.strftime("%B %Y") if exp.ended_at else "",
                "is_ongoing": exp.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            },
        })
    return JsonResponse(data, safe=False)

# Halaman hanya merender kerangka; data diambil lewat fetch() di JavaScript
def show_experience(request):
    context = {
        "name": "Elisia Catherine",
        "title_query": request.GET.get("title", "").strip(),
        "filter_type": request.GET.get("filter", ""),
        "is_editor": is_editor_or_superuser(request.user),
        "form": ExperienceForm() if request.user.is_superuser else None,
    }
    return render(request, "experience.html", context)

# tugas 5: tambah experience lewat AJAX (dipanggil dari modal)
@require_POST
def create_experience_ajax(request):
    # Cek hak akses di server (belum login -> is_superuser False -> 403)
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST, request.FILES)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# untuk tambah data pengalaman
# Ini harusnya ga dipakai lagi
# @login_required(login_url="/login/")
# def create_experience(request):
#     if not request.user.is_superuser:
#         raise PermissionDenied
#     form = ExperienceForm(request.POST or None, request.FILES or None)

#     if request.method == "POST" and form.is_valid():
#         form.save()
#         messages.success(request, "Pengalaman baru berhasil ditambahkan!")
#         return redirect("main:show_experience")

#     context = {
#         "name": "Elisia Catherine",
#         "form": form,
#     }
#     return render(request, "experience_form.html", context)

# update atau edit experiencenya
@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    if not is_editor_or_superuser(request.user):
        raise PermissionDenied
    
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

# menghapus data experience
@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")

# untuk star di experience (mendukung AJAX -> JSON, fallback redirect)
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            users = list(experience.starred_by.all())
            return JsonResponse({
                "is_starred": request.user in users,
                "star_count": len(users),
                "starred_by_names": ", ".join(u.username for u in users),
            })
    return redirect("main:show_experience")

# Kode untuk project
# API Data Delivery dalam bentuk JSON
# Diperbarui sesuai dengan tutorial 5
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    filter_type = request.GET.get("filter", "")
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(
            Q(title__icontains=title_query) | Q(description__icontains=title_query)
        )
    if filter_type == "starred" and request.user.is_authenticated:
        projects = projects.filter(starred_by=request.user)

    data = []
    for project in projects:
        starred_users = list(project.starred_by.all())
        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "category_display": project.get_category_display(),
                "project_url": project.project_url or "",
                "thumbnail": project.thumbnail.url if project.thumbnail else "",
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            }
        })
    return JsonResponse(data, safe=False)

# menampilkan datanya di halaman project (ini deserialisasi)
def show_projects(request):
    context = {
        "name": "Elisia Catherine",
        "title_query": request.GET.get("title", "").strip(),
        "filter_type": request.GET.get("filter", ""),
        "is_editor": is_editor_or_superuser(request.user),
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)

# menambahkan data project
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
@login_required(login_url="/login/")
def edit_project(request, id):
    if not is_editor_or_superuser(request.user):
        raise PermissionDenied
    
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
@login_required(login_url="/login/")
def delete_project(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        project = get_object_or_404(Project, pk=id)
        project.delete()
    return redirect("main:show_projects")

# Tutorial 4 : star for project
# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

# Fungsi register (Tutorial 4)
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Elisia Catherine",
        "form": form,
    }
    return render(request, "register.html", context)

# fungsi login
def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Elisia Catherine",
        "form": form,
    }
    return render(request, "login.html", context)

# fungsi logout
def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tutorial 5 --> Langkah 1: Membuat View create_project_ajax
@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST, request.FILES)

    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

