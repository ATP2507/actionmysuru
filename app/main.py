from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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