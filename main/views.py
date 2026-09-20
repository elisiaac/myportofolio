from django.shortcuts import render
from main.models import Experience
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from main.forms import ExperienceForm
from django.db.models import Q


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