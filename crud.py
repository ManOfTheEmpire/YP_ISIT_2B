from sqlmodel import SQLModel, create_engine, Session, select
from models import User, Team, Participants
from sqlalchemy.orm import joinedload

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

def get_session():
    return Session(engine)

def create_user(user: User):
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_id(user_id: int):
    with get_session() as session:
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

def create_team(team: Team):
    with get_session() as session:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team

def get_teams_by_owner_id(owner_id: int):
    with get_session() as session:
        teams = session.exec(select(Team).where(Team.owner_id == owner_id)).all()
        return teams

def get_teams():
    with get_session() as session:
        statement = select(Team)
        return session.exec(statement).all()

def search_teams_by_title_or_author(query: str):
    with get_session() as session:
        statement = select(Team).where((Team.organ.contains(query)) | (Team.specialization.contains(query)))
        return session.exec(statement).all()

def get_users_with_book(team_id: int):
    with get_session() as session:
        statement = select(User).join(Team, Team.owner_id == User.id).where(Team.id == team_id)
        return session.exec(statement).all()

def get_user_by_email(email: str):
    with get_session() as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

def create_participants(participants: Participants):
    with get_session() as session:
        session.add(participants)
        session.commit()
        session.refresh(participants)
        return participants

def get_participants(user_id: int):
    with get_session() as session:
        statement = select(Participants).where(Participants.requester_id == user_id)
        return session.exec(statement).all()

def get_participants_by_id(exchange_id: int):
    with get_session() as session:
        statement = select(Participants).where(Participants.id == exchange_id)
        return session.exec(statement).first()

def update_participants(participants: Participants):
    with get_session() as session:
        session.add(participants)
        session.commit()
        session.refresh(participants)
        return participants

def get_participants_by_owner_id(owner_id: int):
    with get_session() as session:
        statement = select(Participants).options(joinedload(Participants.team_to_send)).join(Team, Participants.team_to_send_id == Team.id).where(Team.owner_id == owner_id)
        return session.exec(statement).all()
