from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, FileInput, URLInput

from main.models import Education # revisi
from main.models import Experience
# Mau nambah page project untuk Tugas 3
from main.models import Project 

# Tutorial 5
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

# untuk Education
class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "started_at",
            "ended_at",
            "logo",
        ]
        labels = {
            "institution": "Nama Institusi / Sekolah / Universitas",
            "degree": "Gelar / Jurusan / Tingkat Pendidikan",
            "started_at": "Waktu Mulai",
            "ended_at": "Waktu Selesai (Kosongkan kalau masih berlangsung)",
            "logo": "Logo Institusi",
        }
        widgets = {
            "institution": TextInput(attrs={
                "placeholder": "Contoh: Universitas Indonesia",
            }),
            "degree": TextInput(attrs={
                "placeholder": "Contoh: S1 Sistem Informasi",
            }),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
            "logo": FileInput(),
        }

    # Tugas 5: sanitasi input di sisi server (perlindungan XSS)
    def clean_institution(self):
        institution = strip_tags(self.cleaned_data["institution"]).strip()
        if not institution:
            raise ValidationError("Institusi tidak boleh kosong atau hanya berisi tag HTML.")
        return institution

    def clean_degree(self):
        degree = strip_tags(self.cleaned_data["degree"]).strip()
        if not degree:
            raise ValidationError("Gelar/jurusan tidak boleh kosong atau hanya berisi tag HTML.")
        return degree

    def clean(self):
        cleaned = super().clean()
        started, ended = cleaned.get("started_at"), cleaned.get("ended_at")
        if started and ended and ended < started:
            self.add_error("ended_at", "Waktu selesai tidak boleh lebih awal dari waktu mulai.")
        return cleaned

# Untuk experience
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "organization",
            "category",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]
        labels = {
            "title": "Role/Posisi",
            "organization": "Organisasi/Perusahaan",
            "category": "Kategori Pengalaman",
            "description": "Deskripsi Pekerjaan/Kegiatan",
            "thumbnail": "Foto Thumbnail",
            "started_at": "Waktu Mulai",
            "ended_at": "Waktu Selesai (Kosongin kalau masih berlangsung)",
        }
        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Contoh: Ketua Suku", "maxlength": 255}
            ),
            "organization": TextInput(
                attrs={"placeholder": "Contoh: Ristek", "maxlength": 255}
            ),
            "category": Select(attrs={"class": "form-select"}),
            "description": Textarea(
                attrs={"placeholder": "Ceritakan pengalaman/kegiatannya", "rows": 3}
            ),

            # kalo mau pake jam pakenya DateTimeInput
            "thumbnail": FileInput(),
            "started_at": DateInput(
                attrs={"type": "date"}
            ),
            "ended_at": DateInput(attrs={'type': 'date'})
        }

    # Tugas 5: sanitasi input di sisi server (perlindungan XSS)
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Role/posisi tidak boleh kosong atau hanya berisi tag HTML.")
        return title

    def clean_organization(self):
        organization = strip_tags(self.cleaned_data["organization"]).strip()
        if not organization:
            raise ValidationError("Organisasi tidak boleh kosong atau hanya berisi tag HTML.")
        return organization

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi tidak boleh kosong atau hanya berisi tag HTML.")
        return description

    def clean(self):
        cleaned = super().clean()
        started, ended = cleaned.get("started_at"), cleaned.get("ended_at")
        if started and ended and ended < started:
            self.add_error("ended_at", "Waktu selesai tidak boleh lebih awal dari waktu mulai.")
        return cleaned

# untuk project
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "project_url",
        ]
        labels = {
            "title": "Project Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail Image",
            "project_url": "Project URL",
        }
        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Contoh: Portofolio Web App",
            }),
            "description": Textarea(attrs={
                "placeholder": "Contoh: Aplikasi portofolio pribadi berbasis Django...",
                "rows": 4,
            }),
            "category": Select(attrs={"class": "form-select"}),
            "thumbnail": FileInput(),
            "project_url": URLInput(attrs={
                "placeholder": "Opsional, contoh: https://github.com/username/proyek",
            }),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi tidak boleh kosong atau hanya berisi tag HTML.")
        return description