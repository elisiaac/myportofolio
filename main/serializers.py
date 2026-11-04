from django.utils.html import strip_tags
from rest_framework import serializers
from main.models import Project, Experience, Education

class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        # Disesuaikan dengan field di model Project saya
        fields = [
            "id", "title", "description", "category",
            "project_url", "thumbnail",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    # validate_tech_stack dihapus karena saya pakainya 'category' dengan CATEGORY_CHOICES.
    # DRF akan memvalidasi input 'category' secara otomatis berdasarkan pilihan yang ada.

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "organization", "description", "category",
            "started_at", "ended_at", "is_ongoing", "thumbnail",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title (Peran) cannot be empty.")
        return value

    def validate_organization(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Organization cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate(self, data):
        # Validasi tanggal selesai tidak boleh sebelum tanggal mulai
        if data.get('ended_at') and data.get('started_at'):
            if data['ended_at'] < data['started_at']:
                raise serializers.ValidationError("Tanggal selesai tidak boleh sebelum tanggal mulai.")
        return data

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
    

class EducationSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Education
        fields = [
            "id", "institution", "degree",
            "started_at", "ended_at", "is_ongoing", "logo",
        ]
        read_only_fields = ["id"]

    def validate_institution(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Institution cannot be empty.")
        return value

    def validate_degree(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Degree cannot be empty.")
        return value

    def validate(self, data):
        if data.get('ended_at') and data.get('started_at'):
            if data['ended_at'] < data['started_at']:
                raise serializers.ValidationError("Tanggal selesai tidak boleh sebelum tanggal mulai.")
        return data