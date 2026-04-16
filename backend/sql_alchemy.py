import enum
from typing import List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Column as Column_, ForeignKey as ForeignKey_, Table as Table_, 
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_, 
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped as Mapped_, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships
participant_meeting = Table_(
    "participant_meeting",
    Base.metadata,
    Column_("participant", ForeignKey_("participant.id"), primary_key=True),
    Column_("meeting", ForeignKey_("meeting.id"), primary_key=True),
)

# Tables definition
class Participant(Base):
    __tablename__ = "participant"
    id: Mapped_[int] = mapped_column(primary_key=True)
    Name: Mapped_[str] = mapped_column(String_(100))

class Event(Base):
    __tablename__ = "event"
    id: Mapped_[int] = mapped_column(primary_key=True)
    /numberEvents: Mapped_[int] = mapped_column(Integer_)
    Name: Mapped_[str] = mapped_column(String_(100))
    Date: Mapped_[dt_date] = mapped_column(Date_)
    Period: Mapped_[timedelta] = mapped_column()
    Place: Mapped_[str] = mapped_column(String_(100))
    calendar_id: Mapped_[int] = mapped_column(ForeignKey_("calendar.id"))
    type_spec: Mapped_[str] = mapped_column(String_(50))
    __mapper_args__ = {
        "polymorphic_identity": "event",
        "polymorphic_on": "type_spec",
    }

class Meeting(Event):
    __tablename__ = "meeting"
    id: Mapped_[int] = mapped_column(ForeignKey_("event.id"), primary_key=True)
    NumberParticipants: Mapped_[str] = mapped_column(String_(100))
    __mapper_args__ = {
        "polymorphic_identity": "meeting",
    }

class Courses(Event):
    __tablename__ = "courses"
    id: Mapped_[int] = mapped_column(ForeignKey_("event.id"), primary_key=True)
    Type: Mapped_[str] = mapped_column(String_(100))
    __mapper_args__ = {
        "polymorphic_identity": "courses",
    }

class Calendar(Base):
    __tablename__ = "calendar"
    id: Mapped_[int] = mapped_column(primary_key=True)
    Name: Mapped_[str] = mapped_column(String_(100))


#--- Relationships of the participant table
Participant.meeting: Mapped_[List_["Meeting"]] = relationship("Meeting", secondary=participant_meeting, back_populates="participant")

#--- Relationships of the event table
Event.calendar: Mapped_["Calendar"] = relationship("Calendar", back_populates="event", foreign_keys=[Event.calendar_id])

#--- Relationships of the meeting table
Meeting.participant: Mapped_[List_["Participant"]] = relationship("Participant", secondary=participant_meeting, back_populates="meeting")

#--- Relationships of the calendar table
Calendar.event: Mapped_[List_["Event"]] = relationship("Event", back_populates="calendar", foreign_keys=[Event.calendar_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)