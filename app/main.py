from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine
from app import models
from app.routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/programmes/tourism")
def prog_tourism(request: Request):
    return templates.TemplateResponse("prog_tourism.html", {"request": request})

@app.get("/programmes/corporate")
def prog_corporate(request: Request):
    return templates.TemplateResponse("prog_corporate.html", {"request": request})

@app.get("/programmes/parks")
def prog_parks(request: Request):
    return templates.TemplateResponse("prog_parks.html", {"request": request})

@app.get("/programmes/schools")
def prog_schools(request: Request):
    return templates.TemplateResponse("prog_schools.html", {"request": request})

@app.get("/programmes/awareness")
def prog_awareness(request: Request):
    return templates.TemplateResponse("prog_awareness.html", {"request": request})

@app.get("/partners")
def partners(request: Request):
    return templates.TemplateResponse("partners.html", {"request": request})

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})