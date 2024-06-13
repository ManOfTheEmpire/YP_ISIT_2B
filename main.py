from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import *
from crud import *
from typing import List




app = FastAPI()
templates = Jinja2Templates(directory="templates")
create_db_and_tables()
@app.get("/about-us", response_class=HTMLResponse)
async def support(request: Request):
    return templates.TemplateResponse("about_us.html", {"request": request})


@app.get("/support", response_class=HTMLResponse)
async def support(request: Request):
    return templates.TemplateResponse("support.html", {"request": request})

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})


@app.post("/register")
async def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    created_user = create_user(user)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_email(email)
    if user and user.password == password:
        response = RedirectResponse(url=f"/profile/{user.id}", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_id", value=str(user.id))  # сохраняем user_id в cookie
        return response
    return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid credentials"})

    
@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def view_profile(request: Request, user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    teams = get_teams_by_owner_id(user_id)
    participants = get_participants_by_owner_id(user_id)

    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "books": teams, "participants": participants})
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/profile/{user_id}/add_team")
async def add_team(
    user_id: int,
    organ: str = Form(...),
    specialization: str = Form(...),
):
    team = Team(organ=organ, specialization=specialization, owner_id=user_id)
    created_team = create_team(team)
    return RedirectResponse(url=f"/profile/{user_id}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/profile/{user_id}/search_teams")
async def search_teams(request: Request, user_id: int, query: str = Form(...)):
    teams = search_teams_by_title_or_author(query)
    users_with_teams = []
    for team in teams:
        users_with_teams.extend(get_users_with_book(team.id))
    return templates.TemplateResponse("search_results.html", {"request": request, "books": teams, "users_with_books": users_with_teams})

@app.post("/request_team")
async def request_book(request: Request, team_id: int = Form(...), user_id: int = Form(...)):
    participants = Participants(team_to_send_id=team_id, requester_id=user_id)
    create_participants(participants)
    return RedirectResponse(url=f"/profile/{user_id}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/accept_participants")
async def accept_participants(request: Request, participants_id: int = Form(...)):
    participants = get_participants_by_id(participants_id)
    if participants:
        participants.status ="member"
        update_participants(participants)
        return RedirectResponse(url=f"/profile/{participants.requester_id}", status_code=status.HTTP_303_SEE_OTHER)
    return HTTPException(status_code=404, detail="Exchange not found")
@app.post("/decline_participants")
async def decline_participants(request: Request, participants_id: int = Form(...)):
    participants = get_participants_by_id(participants_id)
    if participants:
        participants.requester_id = None
        update_participants(participants)
        return RedirectResponse(url=f"/profile/{participants.requester_id}", status_code=status.HTTP_303_SEE_OTHER)
    return HTTPException(status_code=404, detail="Exchange not found")



