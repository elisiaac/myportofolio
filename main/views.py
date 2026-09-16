from django.shortcuts import render
from main.models import Experience
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from main.forms import ExperienceForm


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


def show_experience(request):
    context = {
        "name": "Elisia Catherine",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


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

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")