from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, FileInput, URLInput

from main.models import Education # revisi
from main.models import Experience
# Mau nambah page project untuk Tugas 3
from main.models import Project 

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

# untuk project
class ProjectForm(ModelForm): # fungsinya buat memetakan field-field dari main/models.py
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
            "project_url": URLInput(attrs={
                "placeholder": "wajib dengan format https://",
            }),
        }