from django.urls import path

from main.views import (
    show_main,
    #experience
    show_experience,
    create_experience,
    edit_experience,
    delete_experience,
    get_experiences_json,
    # projects
    show_projects,
    create_project,
    edit_project,
    delete_project,
    get_projects_json,
    toggle_star,
    # education
    show_education,
    create_education,
    edit_education,
    delete_education,
    get_educations_json,
    # autentikasi
    register,
    login_user,
    logout_user  
)

from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),

    # URL Projects
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:id>/edit/", edit_project, name="edit_project"),
    path("projects/<uuid:id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/star/", toggle_star,name="toggle_star"),

    # URL Education
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/<uuid:id>/edit/", edit_education, name="edit_education"),
    path("education/<uuid:id>/delete/", delete_education, name="delete_education"),
    path("api/educations/", get_educations_json, name="get_educations_json"),

    # URL Autentikasi
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)