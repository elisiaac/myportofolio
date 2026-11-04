from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    # Endpoints untuk Project
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.toggle_star_project, name="toggle-star-project"),

    # Endpoints untuk Experience (TI 6)
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", api_views.toggle_star_experience_api, name="toggle-star-experience"),

    # Endpoints untuk Education (TI 6)
    path("educations/", api_views.education_list, name="education-list"),
    path("educations/<uuid:education_id>/", api_views.education_detail, name="education-detail"),
]