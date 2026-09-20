from django.urls import path

from main.views import (
    show_main,
    show_experience,
    create_experience,
    delete_experience,
    edit_experience,
    get_experiences_json,
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)