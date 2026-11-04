from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main.models import Project, Experience
from datetime import date
from django.utils import timezone

class ProjectAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.superuser = User.objects.create_superuser(
            username="adminuser", password="adminpassword123"
        )

        self.project = Project.objects.create(
            title="Proyek Test 1",
            description="Deskripsi proyek uji coba",
            category="Web Development",
            project_url="https://example.com",
        )

        self.list_url = reverse("api:project-list")
        self.detail_url = reverse(
            "api:project-detail", kwargs={"project_id": self.project.id}
        )
        self.star_url = reverse(
            "api:toggle-star-project", kwargs={"project_id": self.project.id}
        )

    def test_get_project_list(self):
        """Memastikan endpoint list proyek dapat diakses dan mengembalikan status 200"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.project.title)

    def test_create_project_authorized(self):
        """Superuser dapat membuat proyek baru melalui API (POST)"""
        self.client.force_authenticate(user=self.superuser)
        payload = {
            "title": "Proyek Baru",
            "description": "Deskripsi proyek baru",
            "category": "web",
            "project_url": "https://new-example.com",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_create_project_invalid_input(self):
        """Validasi 400 Bad Request jika input tidak sesuai/kosong"""
        self.client.force_authenticate(user=self.superuser)
        payload = {"title": "   ", "description": "Deskripsi tanpa judul valid"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Pastikan database tidak bertambah
        self.assertEqual(Project.objects.count(), 1)

    def test_toggle_star_authenticated(self):
        """User yang terautentikasi dapat melakukan star/unstar pada proyek"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["starred"])
        self.assertEqual(response.data["star_count"], 1)

        response_unstar = self.client.post(self.star_url)
        self.assertEqual(response_unstar.status_code, status.HTTP_200_OK)
        self.assertFalse(response_unstar.data["starred"])
        self.assertEqual(response_unstar.data["star_count"], 0)

    def test_toggle_star_unauthenticated(self):
        """User yang belum login ditolak saat mencoba memberi star (401/403)"""
        response = self.client.post(self.star_url)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_editor_permissions_on_project(self):
        """Editor boleh PATCH, tapi ditolak saat POST (create) atau DELETE"""
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_user = User.objects.create_user(
            username="projecteditor", password="password123"
        )
        editor_user.groups.add(editor_group)
        self.client.force_authenticate(user=editor_user)

        # 1. Editor mencoba POST -> Ditolak (403) dan database tidak berubah
        response_post = self.client.post(
            self.list_url,
            {"title": "Proyek Editor", "description": "Test"},
            format="json",
        )
        self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

        # 2. Editor mencoba PATCH -> Diizinkan (200)
        response_patch = self.client.patch(
            self.detail_url, {"title": "Updated by Editor"}, format="json"
        )
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated by Editor")

        # 3. Editor mencoba DELETE -> Ditolak (403) dan database tidak terhapus
        response_delete = self.client.delete(self.detail_url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_csrf_enforced(self):
        """Membuktikan permintaan modifikasi (tanpa force_authenticate) butuh token CSRF"""
        csrf_client = APIClient(enforce_csrf_checks=True)
        # Login normal dengan cookie session, bukan token/force
        csrf_client.login(username="adminuser", password="adminpassword123")
        
        response = csrf_client.post(
            self.list_url, {"title": "No CSRF Token"}, format="json"
        )
        # Harus ditolak karena klien tidak menyertakan CSRF header
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ExperienceAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="expuser", password="password123"
        )
        self.superuser = User.objects.create_superuser(
            username="expadmin", password="password123"
        )
        
        self.experience = Experience.objects.create(
            title="Teaching Assistant",
            organization="Fasilkom UI",
            description="Membantu kelas PBP",
            category="Work",
            started_at=date(2026, 9, 1)
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", kwargs={"experience_id": self.experience.id}
        )

    def test_get_experience_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_editor_permissions_on_experience(self):
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_user = User.objects.create_user(
            username="expeditor", password="password123"
        )
        editor_user.groups.add(editor_group)
        
        self.client.force_authenticate(user=editor_user)
        
        # PATCH berhasil
        response_patch = self.client.patch(
            self.detail_url, {"title": "Senior TA"}, format="json"
        )
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # DELETE gagal, isi database dicek
        response_delete = self.client.delete(self.detail_url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)