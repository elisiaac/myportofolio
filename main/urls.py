from django.urls import path

from main.views import (
    show_main,
    #experience
    show_experience,
    # create_experience, --> digantikan oleh create_experience_ajax
    edit_experience,
    delete_experience,
    get_experiences_json,
    toggle_star_experience,
    create_experience_ajax,
    # projects
    show_projects,
    create_project,
    edit_project,
    delete_project,
    get_projects_json,
    toggle_star_project,
    # education
    show_education,
    create_education,
    edit_education,
    delete_education,
    get_educations_json,
    # autentikasi
    register,
    login_user,
    logout_user,
    # ajax
    create_project_ajax,
)

from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    # URL Experience
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    # path("experience/add/", create_experience, name="create_experience"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),

    # URL Projects
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:id>/edit/", edit_project, name="edit_project"),
    path("projects/<uuid:id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/star/", toggle_star_project,name="toggle_star_project"),

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

    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)