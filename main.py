import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

app = FastAPI(
    title="Ilham Eka Saputra — Portfolio Backend API",
    description="FastAPI Backend for Developer Portfolio integrated with Supabase Database & Cloud Storage.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for all origins (Local Vite React & Vercel Production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Credentials Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://bypxtnuvdldhwsprhvbq.supabase.co")
SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5cHh0bnV2ZGxkaHdzcHJodmJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY1Mzk5ODQsImV4cCI6MjEwMjExNTk4NH0.WphY3WCHLrbAUDe-7JmKTdJmZLX-PiH4VriZ8Bp04vM",
)

supabase_client = None
try:
    from supabase import create_client, Client
    if SUPABASE_URL and "bypxtnuvdldhwsprhvbq" in SUPABASE_URL:
        supabase_client: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as err:
    print(f"[Supabase Init Warning] Could not initialize Supabase Client: {err}")

# Pydantic Schemas
class ProjectItem(BaseModel):
    id: str
    title: str
    description: str
    image: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)
    liveUrl: Optional[str] = ""
    githubUrl: Optional[str] = ""
    featured: Optional[bool] = False
    category: str = "web"

class SkillItem(BaseModel):
    id: str
    name: str
    category: str
    level: int = Field(ge=0, le=100)
    icon: Optional[str] = ""

class ExperienceItem(BaseModel):
    id: str
    company: str
    role: str
    startDate: str
    endDate: str
    description: str

class ProfileItem(BaseModel):
    name: str = "Ilham Eka Saputra"
    tagline: str = "Full-Stack Developer · IoT Engineer · AI Enthusiast"
    bio: str = "Mahasiswa D3 Teknik Informatika UNS Kampus Madiun"
    gpa: str = "3.68"
    phone: str = "085231287023"
    emailPersonal: str = "haamzz93@gmail.com"
    emailAcademic: str = "ilhameka93@student.uns.ac.id"

# Global Portfolio State Fallback (In-Memory & Supabase Synced)
GLOBAL_PORTFOLIO_CONFIG = {
    "cvUrl": "",
    "avatarUrl": "",
    "idPhotoUrl": "",
    "tagline": "Full-Stack Developer · IoT Engineer · AI Enthusiast",
    "bio": "Mahasiswa Semester 5 D3 Teknik Informatika Universitas Sebelas Maret (UNS) Madiun dengan spesialisasi Full-Stack Web & Mobile Development serta integrasi IoT.",
    "projects": [],
    "skills": [],
    "experiences": []
}

# ── Health & Info Endpoints ──
@app.get("/")
def root():
    return {
        "title": "Ilham Eka Saputra — Portfolio Backend API",
        "status": "running",
        "docs": "/docs",
        "supabase_connected": supabase_client is not None,
    }

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "supabase_url": SUPABASE_URL,
        "supabase_active": supabase_client is not None,
    }

# ── Portfolio Consolidated Endpoint ──
@app.get("/api/portfolio")
def get_full_portfolio():
    """Retrieve full portfolio datasets (projects, skills, experiences, profile media)."""
    if supabase_client:
        try:
            projects = supabase_client.table("projects").select("*").execute().data
            skills = supabase_client.table("skills").select("*").execute().data
            experiences = supabase_client.table("experiences").select("*").execute().data
            return {
                "config": GLOBAL_PORTFOLIO_CONFIG,
                "projects": projects if projects else GLOBAL_PORTFOLIO_CONFIG["projects"],
                "skills": skills if skills else GLOBAL_PORTFOLIO_CONFIG["skills"],
                "experiences": experiences if experiences else GLOBAL_PORTFOLIO_CONFIG["experiences"],
            }
        except Exception as e:
            print(f"[Supabase Read Error] {e}")

    return GLOBAL_PORTFOLIO_CONFIG

@app.post("/api/portfolio")
def save_full_portfolio(config: Dict[str, Any]):
    """Save full portfolio config globally across all devices."""
    global GLOBAL_PORTFOLIO_CONFIG
    GLOBAL_PORTFOLIO_CONFIG.update(config)
    return {"status": "success", "config": GLOBAL_PORTFOLIO_CONFIG}

# ── Projects CRUD Endpoints ──
@app.get("/api/projects", response_model=List[ProjectItem])
def get_projects():
    if supabase_client:
        res = supabase_client.table("projects").select("*").execute()
        return res.data
    return []

@app.post("/api/projects", status_code=status.HTTP_201_CREATED)
def create_project(item: ProjectItem):
    if supabase_client:
        res = supabase_client.table("projects").insert(item.dict()).execute()
        return {"status": "success", "data": res.data}
    return {"status": "mock_success", "item": item}

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str):
    if supabase_client:
        res = supabase_client.table("projects").delete().eq("id", project_id).execute()
        return {"status": "success", "deleted_id": project_id}
    return {"status": "mock_success", "deleted_id": project_id}

# ── Skills CRUD Endpoints ──
@app.get("/api/skills", response_model=List[SkillItem])
def get_skills():
    if supabase_client:
        res = supabase_client.table("skills").select("*").execute()
        return res.data
    return []

@app.post("/api/skills", status_code=status.HTTP_201_CREATED)
def create_skill(item: SkillItem):
    if supabase_client:
        res = supabase_client.table("skills").insert(item.dict()).execute()
        return {"status": "success", "data": res.data}
    return {"status": "mock_success", "item": item}

# ── File Upload Endpoints (CV & Images) ──
@app.post("/api/upload/cv")
async def upload_cv_document(file: UploadFile = File(...)):
    allowed = ["application/pdf", "text/plain", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, TXT, DOC, DOCX supported.")
    
    contents = await file.read()
    filename = f"CV_Ilham_Eka_Saputra_{file.filename}"
    
    if supabase_client:
        try:
            supabase_client.storage.from_("cv-files").upload(filename, contents, file_options={"upsert": "true"})
            url = supabase_client.storage.from_("cv-files").get_public_url(filename)
            return {"status": "success", "url": url, "filename": filename}
        except Exception as e:
            print(f"[Supabase CV Storage Error] {e}")

    return {"status": "success", "filename": filename, "bytes": len(contents)}

@app.post("/api/upload/image")
async def upload_image_asset(file: UploadFile = File(...), category: str = Form("avatar")):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")
    
    contents = await file.read()
    filename = f"{category}_{file.filename}"
    
    if supabase_client:
        try:
            supabase_client.storage.from_("portfolio-images").upload(filename, contents, file_options={"upsert": "true"})
            url = supabase_client.storage.from_("portfolio-images").get_public_url(filename)
            return {"status": "success", "url": url, "category": category}
        except Exception as e:
            print(f"[Supabase Image Storage Error] {e}")

    return {"status": "success", "filename": filename, "category": category, "bytes": len(contents)}
