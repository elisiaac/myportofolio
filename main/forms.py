from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, FileInput

from main.models import Experience

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