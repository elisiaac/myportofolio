Nama : Elisia Catherine
NPM  : 2506533570
Kelas: PBP A

Semoga PBP aku index A! AMIN.

## Deskripsi Project:
Website portofolio ini merupakan salah satu tugas mata kuliah PBP 2026/2027. Isinya membahas mengenai siapa saya, pendidikan yang saya tempuh saat ini, pengalaman-pengalaman yang saya miliki, project yang pernah saya lakukan, dan sedikit tentang hobi saya. Web portofolio pribadi yang dibangun menggunakan framework **Django**.

Walau ini merupakan tugas mata kuliah, tapi saya tertarik untuk mengembangkan website ini sepenuh hati❤️ Sampai jumpa di next week for next update, yippie!

## Setup Proyek
Untuk menjalankan proyek ini secara lokal, ikuti instruksi berikut:
1. Clone repositori ini ke komputer lokal:
   ```bash
   git clone https://github.com/elisiaac/myportofolio.git
   cd myportofolio
   ```

2. Buat dan juga aktifkan virtual environment:
    - **Windows:**
    ```
    python -m venv env
    env\Scripts\activate
    ```

    - **macOS / Linux**
    ```
    python3 -m venv env
    source env/bin/activate
    ```

3. Install dependensi proyek:
    ```
    pip install -r requirements.txt
    ```

4. Lakukan migrasi skema database:
    ```
    python manage.py migrate
    ```

5. Jalankan development server:
    ```
    python manage.py runserver
    ```
    Lalu akses website di browser pada tautan http://localhost:8000/


## Progress Mingguan:
### Week 1
Membuat project & setup django, melakukan integrasi ke PWS
### Week 2
Membuat section baru "education" yang diisi dengan 5 konten foto selama menempuh pendidikan di Fasilkom & keterangan kuliah saat ini
### Week 3
Membuat page experience yang diisi dengan 4 pengalaman
### Week 4
Saya mengimplementasikan  CRUD dan penyajian data JSON pada modul Experience dengan merefaktor template agar mewarisi base.html. Halaman create dan update data menggunakan satu berkas template yang sama (experience_form.html), di mana judul halaman dan tombol besifat dinamis dengan adanya logika percabangan {% if experience %}.

## Pertanyaan Reflektif
### Tugas 1
1. Untuk semantik HTML5 yang sudah saya gunakan sejauh ini adalah section yang saat ini digunakan pada dua bagian. Ada bagian hero section yang memuat "About Me" dan section education. Menurut saya elemen tersebut membantu saya dengan memisahkan dengan jelas content yang ada dengan membungkus masing-masing bagian. Selain itu section yang saya gunakan ini sangat berguna saat navigasi dari navbar (dengan <section id="ini nama section">). Dan yang paling mudah saya rasakan adalah kemudahan pengaturan margin tiap sectionnya.

Untuk elemen semantik seperti article dan aside belum saya gunakan sejauh ini.


2. Ada beberapa tantangan yang saya alami selama mengerjakan ini. Pertama, saya mengganti navigation bar yang ada di contoh tutorial 1 menjadi navbar glassmorph yang melayang. Kesulitannya muncul saat saya menambahkan efek hover pada tiap link dinavbar, di mana tampilan dari navbarnya jadi ikut melebar. Selain itu pada section education saya menambahkan gallery photos yang menunjukkan beberapa kegiatan saya selama berkuliah di Fasilkom, saat saya deploy saya menyadari adanya hal yang kurang oke secara experience di mobile, di mana posisi dari gallerynya sangat panjang sehingga agak "tidak memuaskan" untuk harus scroll berkali-kali. Sehingga saya mengevaluasinya dengan menyesuaikan ukuran untuk setiap photo sehingga experiencenya scroll tidak membuat bosan/jenuh. 

3. Batasan utama yang saya rasakan sejauh ini adalah pengelolaan isi/content yang semuanya dilakukan serba manual. Kalau mau menambahkan sesuatu atau banhkan revisi minor, saya harus membuka html mengeditnya, lalu push lagi semua. Sejauh ini terasa cukup memakan waktu. Untuk fungsi yang ingin saya tambahkan berikutnya adalah fitur dark mode (saya cukup lama menyiapkan color palette untuk ini hehe) dan sudah merancangnya juga melalui Figma. Dan belajar dari website portofolio yang sudah pernah saya buat sebelumnya (untuk tugas PMB) saya mau menambahkan fitur email yang dapat diisi langsung melalui website saya, dan benar-benar bisa terkirim kepada saya (yang diweb PMB saya tidak terintegrasi).

Untuk penggunaan AI saya gunakan dengan menanyakan:
Mana yang lebih baik digunakan untuk membuat website, pengukuran dengan px atau rem. https://share.gemini.google/2Fnmf9zvQ3z0
(sejauh ini hanya itu).

Karena pemecahan masalah yang saya lakukan juga lebih banyak dilakukan dengan trial dan error, kalau sudah buntu saya mencoba cari informasi dari youtube, di sana ada banyak sekali penjelasan mengenai alur pembuatan website dan juga bagaimana styling menggunakan css. Selain itu karena keterbatasan ingatan saya juga dengan hal-hal ini, saya menggunakan referensi website lama saya sebagai acuan kode dan styling css untuk belajar. Misalnya ada tombol a --> saya cek file css untuk melihat bagaimana dulu saya menstyling button tersebut, kenapa outputnya bisa begitu? --> lalu saya coba aplikasikan "styling" lain dengan trial pada code proto saya yang sekarang dan jadilah seperti yang ada saat ini YIPPIE!



### Tugas 2
1. Alur pemrosesannya dimulai saat pengguna mengetikkan alamat URL halaman portofolionya di browser yang mengirimkan sebuah HTTP GET Request ke server web Django (di sini soalnya pake django). Berkas urls.py proyek berperilaku sebagai gerbang utama yang memeriksa pola awalan URL yang diketik, lalu meneruskan rutenya ke urls.py aplikasi menggunakan fungsi include(). Lalu berkas routing masuk ke jalur URL yang lebih spesifik ke fungsi pemroses tertentu di dalam view. View merespons dengan memanggil model untuk mengambil data portofolio dari database menggunakan Django. Model memproses data dan mengembalikan data dalam bentuk objek Python ke view. Selanjutnya, view 'memasukkan' data tersebut ke dalam berkas template HTML, lalu di render. Hasil akhir berupa dokumen HTML lengkap yang sudah ada informasi dan designnya.

2. Menurut saya, ketika data-data portofolio di tuliskan secara hardcoded dalam template akan menyulitkan pemeliharaan dan pengembangan. Di mana dari keterbatasan yang dirasakan pada tugas 1, untuk memperbarui data, menambahkan atau menghapus data menjadi sulit karena perlu membuka file dan mengubahnya satu persatu. Selain itu setelah selesai diganti, admin masih perlu deploy ulang. Dengan menyimpan data pada model, manipulasi data menjadi lebih mudah. Selain itu yang saya rasakan saat mencoba di Tugas 2 ini, pengelolaannya lebih mudah dan terstruktur. Sekali menambahkan data langsung muncul dan rapih.

3. Yang saya pahami, makemigration dan migrate itu saling melengkapi dalam mensinkronkan kode ke database. Untuk yang makemigration digunakan untuk memeriksa perubahan-perubahan yang terjadi pada modelnya dan akan disimpan sebagai suatu berkas migrasi (contoh di saya : 0001_initial.py) yang ada di folder migrations. Perubahan databasenya akan terjadi saat menjalankan code migrate. Contohnya pada kasus model Experience saya, saya wajib menjalankan kedua perintah tersebut secara berurutan: pertama makemigrations untuk membuat instruksi pembuatan tabel pengalaman beserta field pendukungnya, kemudian migrate agar tabel tersebut benar-benar terbentuk di dalam database sehingga fitur CRUD siap menyimpan dan mengelola data pengalaman pengguna.

Untuk penggunaan AI saya gunakan dengan menanyakan:
Apa saja opsi-opsi yang tersedia untuk memasukkan data dengan tipe image ke database. Dan AI gemini memberikan saya beberapa saran. Saya juga lanjur bertanya untuk project ini lebih baik image diletakkan pada folder static atau di internet/cloud. Saya sendiri sudah mencoba beberapa cara, tapi dari yang disarankan ada beberapa kendala, misalnya website untuk cloudnya tidak dapat merespon request pembuatan akun saya, dan beberapa kendala lainnya.
https://share.gemini.google/ml0DZlQPIKzK

Untuk hal-hal terkait css dan html lagi lagi saya pelajari dari youtube dan searching di google, beberapa diantaranya:
https://youtu.be/dGPzLsKPafE?si=dOFPIyuEFXA2iNWK
https://www.w3schools.com/django/django_admin.php
https://youtu.be/OV8MVmtgmoY?si=uumihd-xd3fKKF6y


Ada beberapa hal yang saya masih kurang paham juga saat mengerjakan ini sehingga saya bertanya kepada teman-teman saya. Terima kasiiii:3