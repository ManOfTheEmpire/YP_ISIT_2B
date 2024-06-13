from sqlmodel import Field, SQLModel, create_engine, Session, Relationship
from typing import Optional, List

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organ: str
    specialization: str
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: "User" = Relationship(back_populates="teams")
    participants: List["Participants"] = Relationship(back_populates="team_to_send")

class Participants(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_to_send_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team_to_send: "Team" = Relationship(back_populates="participants")
    requester_id: Optional[int] = Field(default=None, foreign_key="user.id")
    requester: "User" = Relationship(back_populates="participants")
    status: str = Field(default="pending")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    password: str
    teams: List["Team"] = Relationship(back_populates="owner")
    participants: List["Participants"] = Relationship(back_populates="requester") 





DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
