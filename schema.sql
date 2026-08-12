-- ===================================================
-- Supabase Postgres Schema & Storage Setup Script
-- Project: Ilham Eka Saputra — Portfolio Database
-- ===================================================

-- 1. Create Projects Table
CREATE TABLE IF NOT EXISTS public.projects (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  image TEXT DEFAULT '',
  tags TEXT[] DEFAULT '{}',
  "liveUrl" TEXT DEFAULT '',
  "githubUrl" TEXT DEFAULT '',
  featured BOOLEAN DEFAULT false,
  category TEXT DEFAULT 'web',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create Skills Table
CREATE TABLE IF NOT EXISTS public.skills (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  level INT DEFAULT 80 CHECK (level >= 0 AND level <= 100),
  icon TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create Experiences Table
CREATE TABLE IF NOT EXISTS public.experiences (
  id TEXT PRIMARY KEY,
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  "startDate" TEXT NOT NULL,
  "endDate" TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Enable Row Level Security (RLS) & Public Read Policies
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.experiences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow Public Read Projects" ON public.projects FOR SELECT USING (true);
CREATE POLICY "Allow Public Read Skills" ON public.skills FOR SELECT USING (true);
CREATE POLICY "Allow Public Read Experiences" ON public.experiences FOR SELECT USING (true);

-- Allow All Operations for Anon Role (Development Mode)
CREATE POLICY "Allow All Projects Ops" ON public.projects FOR ALL USING (true);
CREATE POLICY "Allow All Skills Ops" ON public.skills FOR ALL USING (true);
CREATE POLICY "Allow All Experiences Ops" ON public.experiences FOR ALL USING (true);

-- 5. Create Storage Buckets for CV Files & Images
INSERT INTO storage.buckets (id, name, public) 
VALUES ('cv-files', 'cv-files', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO storage.buckets (id, name, public) 
VALUES ('portfolio-images', 'portfolio-images', true)
ON CONFLICT (id) DO NOTHING;

-- Storage Public Read Policies
CREATE POLICY "Allow Public Download CV" ON storage.objects FOR SELECT USING (bucket_id = 'cv-files');
CREATE POLICY "Allow Public Upload CV" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'cv-files');
CREATE POLICY "Allow Public Download Images" ON storage.objects FOR SELECT USING (bucket_id = 'portfolio-images');
CREATE POLICY "Allow Public Upload Images" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'portfolio-images');
