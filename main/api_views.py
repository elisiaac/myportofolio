from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Experience, Education
from main.serializers import ProjectSerializer, ExperienceSerializer, EducationSerializer
from .permissions import IsPortfolioOwnerOrEditorOrReadOnly


# ==========================================
# VIEWS UNTUK PROJECT
# ==========================================
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)
        
    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def toggle_star_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    
    if user in project.starred_by.all():
        project.starred_by.remove(user)
        starred = False
    else:
        project.starred_by.add(user)
        starred = True
        
    return Response(
        {
            "status": "success",
            "starred": starred,
            "star_count": project.starred_by.count(),
        },
        status=status.HTTP_200_OK,
    )


# ==========================================
# VIEWS UNTUK EXPERIENCE
# ==========================================
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by").order_by("-started_at")
        
        title_query = request.query_params.get("title", "").strip()
        if title_query:
            experiences = experiences.filter(
                Q(organization__icontains=title_query) | Q(title__icontains=title_query)
            )
            
        serializer = ExperienceSerializer(experiences, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)
        
    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def toggle_star_experience_api(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    user = request.user
    
    if user in experience.starred_by.all():
        experience.starred_by.remove(user)
        starred = False
    else:
        experience.starred_by.add(user)
        starred = True
        
    return Response(
        {
            "status": "success",
            "starred": starred,
            "star_count": experience.starred_by.count(),
        },
        status=status.HTTP_200_OK,
    )

# ==========================================
# VIEWS UNTUK EDUCATION
# ==========================================
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        educations = Education.objects.order_by("-started_at")
        title_query = request.query_params.get("title", "").strip()
        if title_query:
            educations = educations.filter(
                Q(institution__icontains=title_query) | Q(degree__icontains=title_query)
            )
        serializer = EducationSerializer(educations, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    
    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(education, context={"request": request})
        return Response(serializer.data)
        
    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    serializer = EducationSerializer(
        education, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)