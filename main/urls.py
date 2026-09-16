from django.urls import path

from main.views import (
    show_main,
    show_experience,
    create_experience,
    delete_experience)
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("projects/<uuid:experience_id>/delete/",delete_experience,name="delete_experience")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)