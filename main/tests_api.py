from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import Project


class ProjectAPITests(APITestCase):

  def setUp(self):
    # Membuat user biasa dan user superuser untuk pengujian hak akses
    self.user = User.objects.create_user(
        username="testuser", password="testpassword123"
    )
    self.superuser = User.objects.create_superuser(
        username="adminuser", password="adminpassword123"
    )

    # Membuat contoh data proyek awal
    self.project = Project.objects.create(
        title="Proyek Test 1",
        description="Deskripsi proyek uji coba",
        category="Web Development",
        project_url="https://example.com",
    )

    # URL endpoints berdasarkan namespace api
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
            "category": "Web Development",
            "project_url": "https://new-example.com",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

  def test_toggle_star_authenticated(self):
    """User yang terautentikasi dapat melakukan star/unstar pada proyek"""
    self.client.force_authenticate(user=self.user)

    # Pertama kali dipanggil: memberikan star
    response = self.client.post(self.star_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data["starred"])
    self.assertEqual(response.data["star_count"], 1)

    # Dipanggil ulang: membatalkan star (unstar)
    response_unstar = self.client.post(self.star_url)
    self.assertEqual(response_unstar.status_code, status.HTTP_200_OK)
    self.assertFalse(response_unstar.data["starred"])
    self.assertEqual(response_unstar.data["star_count"], 0)

  def test_toggle_star_unauthenticated(self):
    """User yang belum login ditolak saat mencoba memberi star (401/403)"""
    # Tanpa force_authenticate
    response = self.client.post(self.star_url)
    self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
    )

    def test_editor_permissions_on_project(self):
        """Editor boleh melakukan PATCH pada project, tapi ditolak saat POST (create) atau DELETE"""
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_user = User.objects.create_user(username="projecteditor", password="password123")
        editor_user.groups.add(editor_group)

        # 1. Editor mencoba POST (create) -> Harus ditolak (403 Forbidden)
        self.client.force_authenticate(user=editor_user)
        response_post = self.client.post(self.list_url, {
            "title": "Proyek Editor",
            "description": "Test",
            "category": "Web Development"
        }, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)

        # 2. Editor mencoba PATCH (update) -> Harus diizinkan (200 OK)
        response_patch = self.client.patch(self.detail_url, {
            "title": "Updated Project by Editor"
        }, format="json")
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

        # 3. Editor mencoba DELETE -> Harus ditolak (403 Forbidden)
        response_delete = self.client.delete(self.detail_url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)