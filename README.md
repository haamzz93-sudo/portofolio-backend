# ⚡ FastAPI Portfolio Backend — Ilham Eka Saputra

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Database_%26_Storage-3FCF8E?style=for-the-badge&logo=supabase)](https://supabase.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Serverless_Function-000000?style=for-the-badge&logo=vercel)](https://vercel.com/)

> Backend Service berbasis **FastAPI** & **Supabase** yang didesain khusus untuk mendukung aplikasi Web Portfolio Ilham Eka Saputra. Kompatibel 100% dengan ekosistem Serverless Vercel Deployment.

---

## ✨ Fitur Utama Backend

- 🚀 **FastAPI Framework**: Performa tinggi dengan dokumentasi otomatis OpenAPI / Swagger UI di `/docs`.
- 🗄️ **Supabase Database & Storage**: Tersambung ke Supabase Postgres Database & Storage Buckets (`cv-files`, `portfolio-images`).
- 📂 **CV & Image Uploader**: Dedicated endpoint `/api/upload/cv` dan `/api/upload/image`.
- 📊 **CRUD Full Dataset**: Managing Projects, Skills, Experiences, dan General Profile.
- ⚡ **Vercel Serverless Compatible**: Struktur `api/index.py` & `vercel.json` siap di-deploy 1-click ke Vercel.

---

## 🛠️ Cara Menjalankan Backend Secara Lokal

1. **Buka folder backend**:
   ```bash
   cd "C:\Users\User\Downloads\Portofolio Backend"
   ```

2. **Buat Virtual Environment (opsional tapi direkomendasikan)**:
   ```bash
   python -m venv venv
   # Mengaktifkan di Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan FastAPI Development Server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Buka dokumentasi Swagger UI di Browser**:
   Akses `http://localhost:8000/docs` atau `http://localhost:8000/redoc`.

---

## 🚀 Cara Hosting Backend ke Vercel

1. Buat repository GitHub baru di akun Anda, misal: `portofolio-backend`.
2. Push seluruh file folder `Portofolio Backend` ini ke repository tersebut:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: FastAPI Backend for Portfolio"
   git branch -M main
   git remote add origin https://github.com/USERNAME/portofolio-backend.git
   git push -u origin main
   ```
3. Buka dashboard [Vercel](https://vercel.com/), pilih **Add New Project**, dan import repository `portofolio-backend`.
4. Masukkan **Environment Variables** di Vercel:
   - `SUPABASE_URL` = `https://bypxtnuvdldhwsprhvbq.supabase.co`
   - `SUPABASE_KEY` = `eyJhbGciOiJIUzI1...`
5. Klik **Deploy**! Backend FastAPI Anda akan aktif secara global di Vercel.

---

## 📜 Lisensi

© 2026 **Ilham Eka Saputra**. All Rights Reserved.
