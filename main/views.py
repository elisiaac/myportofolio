from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Elisia Catherine",
        "npm": "2506533570",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "3rd-semester student at Universitas Indonesia, passionate about web development. Constantly learning, building, and improving my skills."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Elisia Catherine",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)