import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Participant", "description": "Operations for Participant entities"},
        {"name": "Participant Relationships", "description": "Manage Participant relationships"},
        {"name": "Event", "description": "Operations for Event entities"},
        {"name": "Event Relationships", "description": "Manage Event relationships"},
        {"name": "Meeting", "description": "Operations for Meeting entities"},
        {"name": "Meeting Relationships", "description": "Manage Meeting relationships"},
        {"name": "Courses", "description": "Operations for Courses entities"},
        {"name": "Calendar", "description": "Operations for Calendar entities"},
        {"name": "Calendar Relationships", "description": "Manage Calendar relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["participant_count"] = database.query(Participant).count()
    stats["event_count"] = database.query(Event).count()
    stats["meeting_count"] = database.query(Meeting).count()
    stats["courses_count"] = database.query(Courses).count()
    stats["calendar_count"] = database.query(Calendar).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Participant functions
#
############################################

@app.get("/participant/", response_model=None, tags=["Participant"])
def get_all_participant(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Participant)
        participant_list = query.all()

        # Serialize with relationships included
        result = []
        for participant_item in participant_list:
            item_dict = participant_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            meeting_list = database.query(Meeting).join(participant_meeting, Meeting.id == participant_meeting.c.meeting).filter(participant_meeting.c.participant == participant_item.id).all()
            item_dict['meeting'] = []
            for meeting_obj in meeting_list:
                meeting_dict = meeting_obj.__dict__.copy()
                meeting_dict.pop('_sa_instance_state', None)
                item_dict['meeting'].append(meeting_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Participant).all()


@app.get("/participant/count/", response_model=None, tags=["Participant"])
def get_count_participant(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Participant entities"""
    count = database.query(Participant).count()
    return {"count": count}


@app.get("/participant/paginated/", response_model=None, tags=["Participant"])
def get_paginated_participant(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Participant entities"""
    total = database.query(Participant).count()
    participant_list = database.query(Participant).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": participant_list
        }

    result = []
    for participant_item in participant_list:
        meeting_ids = database.query(participant_meeting.c.meeting).filter(participant_meeting.c.participant == participant_item.id).all()
        item_data = {
            "participant": participant_item,
            "meeting_ids": [x[0] for x in meeting_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/participant/search/", response_model=None, tags=["Participant"])
def search_participant(
    database: Session = Depends(get_db)
) -> list:
    """Search Participant entities by attributes"""
    query = database.query(Participant)


    results = query.all()
    return results


@app.get("/participant/{participant_id}/", response_model=None, tags=["Participant"])
async def get_participant(participant_id: int, database: Session = Depends(get_db)) -> Participant:
    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    meeting_ids = database.query(participant_meeting.c.meeting).filter(participant_meeting.c.participant == db_participant.id).all()
    response_data = {
        "participant": db_participant,
        "meeting_ids": [x[0] for x in meeting_ids],
}
    return response_data



@app.post("/participant/", response_model=None, tags=["Participant"])
async def create_participant(participant_data: ParticipantCreate, database: Session = Depends(get_db)) -> Participant:

    if participant_data.meeting:
        for id in participant_data.meeting:
            # Entity already validated before creation
            db_meeting = database.query(Meeting).filter(Meeting.id == id).first()
            if not db_meeting:
                raise HTTPException(status_code=404, detail=f"Meeting with ID {id} not found")

    db_participant = Participant(
        Name=participant_data.Name        )

    database.add(db_participant)
    database.commit()
    database.refresh(db_participant)


    if participant_data.meeting:
        for id in participant_data.meeting:
            # Entity already validated before creation
            db_meeting = database.query(Meeting).filter(Meeting.id == id).first()
            # Create the association
            association = participant_meeting.insert().values(participant=db_participant.id, meeting=db_meeting.id)
            database.execute(association)
            database.commit()


    meeting_ids = database.query(participant_meeting.c.meeting).filter(participant_meeting.c.participant == db_participant.id).all()
    response_data = {
        "participant": db_participant,
        "meeting_ids": [x[0] for x in meeting_ids],
    }
    return response_data


@app.post("/participant/bulk/", response_model=None, tags=["Participant"])
async def bulk_create_participant(items: list[ParticipantCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Participant entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_participant = Participant(
                Name=item_data.Name            )
            database.add(db_participant)
            database.flush()  # Get ID without committing
            created_items.append(db_participant.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Participant entities"
    }


@app.delete("/participant/bulk/", response_model=None, tags=["Participant"])
async def bulk_delete_participant(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Participant entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_participant = database.query(Participant).filter(Participant.id == item_id).first()
        if db_participant:
            database.delete(db_participant)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Participant entities"
    }

@app.put("/participant/{participant_id}/", response_model=None, tags=["Participant"])
async def update_participant(participant_id: int, participant_data: ParticipantCreate, database: Session = Depends(get_db)) -> Participant:
    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    setattr(db_participant, 'Name', participant_data.Name)
    existing_meeting_ids = [assoc.meeting for assoc in database.execute(
        participant_meeting.select().where(participant_meeting.c.participant == db_participant.id))]

    meetings_to_remove = set(existing_meeting_ids) - set(participant_data.meeting)
    for meeting_id in meetings_to_remove:
        association = participant_meeting.delete().where(
            (participant_meeting.c.participant == db_participant.id) & (participant_meeting.c.meeting == meeting_id))
        database.execute(association)

    new_meeting_ids = set(participant_data.meeting) - set(existing_meeting_ids)
    for meeting_id in new_meeting_ids:
        db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
        if db_meeting is None:
            raise HTTPException(status_code=404, detail=f"Meeting with ID {meeting_id} not found")
        association = participant_meeting.insert().values(meeting=db_meeting.id, participant=db_participant.id)
        database.execute(association)
    database.commit()
    database.refresh(db_participant)

    meeting_ids = database.query(participant_meeting.c.meeting).filter(participant_meeting.c.participant == db_participant.id).all()
    response_data = {
        "participant": db_participant,
        "meeting_ids": [x[0] for x in meeting_ids],
    }
    return response_data


@app.delete("/participant/{participant_id}/", response_model=None, tags=["Participant"])
async def delete_participant(participant_id: int, database: Session = Depends(get_db)):
    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    database.delete(db_participant)
    database.commit()
    return db_participant

@app.post("/participant/{participant_id}/meeting/{meeting_id}/", response_model=None, tags=["Participant Relationships"])
async def add_meeting_to_participant(participant_id: int, meeting_id: int, database: Session = Depends(get_db)):
    """Add a Meeting to this Participant's meeting relationship"""
    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Check if relationship already exists
    existing = database.query(participant_meeting).filter(
        (participant_meeting.c.participant == participant_id) &
        (participant_meeting.c.meeting == meeting_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = participant_meeting.insert().values(participant=participant_id, meeting=meeting_id)
    database.execute(association)
    database.commit()

    return {"message": "Meeting added to meeting successfully"}


@app.delete("/participant/{participant_id}/meeting/{meeting_id}/", response_model=None, tags=["Participant Relationships"])
async def remove_meeting_from_participant(participant_id: int, meeting_id: int, database: Session = Depends(get_db)):
    """Remove a Meeting from this Participant's meeting relationship"""
    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    # Check if relationship exists
    existing = database.query(participant_meeting).filter(
        (participant_meeting.c.participant == participant_id) &
        (participant_meeting.c.meeting == meeting_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = participant_meeting.delete().where(
        (participant_meeting.c.participant == participant_id) &
        (participant_meeting.c.meeting == meeting_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Meeting removed from meeting successfully"}


@app.get("/participant/{participant_id}/meeting/", response_model=None, tags=["Participant Relationships"])
async def get_meeting_of_participant(participant_id: int, database: Session = Depends(get_db)):
    """Get all Meeting entities related to this Participant through meeting"""
    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    meeting_ids = database.query(participant_meeting.c.meeting).filter(participant_meeting.c.participant == participant_id).all()
    meeting_list = database.query(Meeting).filter(Meeting.id.in_([id[0] for id in meeting_ids])).all()

    return {
        "participant_id": participant_id,
        "meeting_count": len(meeting_list),
        "meeting": meeting_list
    }





############################################
#
#   Event functions
#
############################################

@app.get("/event/", response_model=None, tags=["Event"])
def get_all_event(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Event)
        query = query.options(joinedload(Event.calendar))
        event_list = query.all()

        # Serialize with relationships included
        result = []
        for event_item in event_list:
            item_dict = event_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if event_item.calendar:
                related_obj = event_item.calendar
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['calendar'] = related_dict
            else:
                item_dict['calendar'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Event).all()


@app.get("/event/count/", response_model=None, tags=["Event"])
def get_count_event(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Event entities"""
    count = database.query(Event).count()
    return {"count": count}


@app.get("/event/paginated/", response_model=None, tags=["Event"])
def get_paginated_event(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Event entities"""
    total = database.query(Event).count()
    event_list = database.query(Event).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": event_list
    }


@app.get("/event/search/", response_model=None, tags=["Event"])
def search_event(
    database: Session = Depends(get_db)
) -> list:
    """Search Event entities by attributes"""
    query = database.query(Event)


    results = query.all()
    return results


@app.get("/event/{event_id}/", response_model=None, tags=["Event"])
async def get_event(event_id: int, database: Session = Depends(get_db)) -> Event:
    db_event = database.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    response_data = {
        "event": db_event,
}
    return response_data



@app.post("/event/", response_model=None, tags=["Event"])
async def create_event(event_data: EventCreate, database: Session = Depends(get_db)) -> Event:

    if event_data.calendar is not None:
        db_calendar = database.query(Calendar).filter(Calendar.id == event_data.calendar).first()
        if not db_calendar:
            raise HTTPException(status_code=400, detail="Calendar not found")
    else:
        raise HTTPException(status_code=400, detail="Calendar ID is required")

    db_event = Event(
        Place=event_data.Place,        Period=event_data.Period,        Date=event_data.Date,        /numberEvents=event_data./numberEvents,        Name=event_data.Name,        calendar_id=event_data.calendar        )

    database.add(db_event)
    database.commit()
    database.refresh(db_event)




    return db_event


@app.post("/event/bulk/", response_model=None, tags=["Event"])
async def bulk_create_event(items: list[EventCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Event entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.calendar:
                raise ValueError("Calendar ID is required")

            db_event = Event(
                Place=item_data.Place,                Period=item_data.Period,                Date=item_data.Date,                /numberEvents=item_data./numberEvents,                Name=item_data.Name,                calendar_id=item_data.calendar            )
            database.add(db_event)
            database.flush()  # Get ID without committing
            created_items.append(db_event.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Event entities"
    }


@app.delete("/event/bulk/", response_model=None, tags=["Event"])
async def bulk_delete_event(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Event entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_event = database.query(Event).filter(Event.id == item_id).first()
        if db_event:
            database.delete(db_event)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Event entities"
    }

@app.put("/event/{event_id}/", response_model=None, tags=["Event"])
async def update_event(event_id: int, event_data: EventCreate, database: Session = Depends(get_db)) -> Event:
    db_event = database.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    setattr(db_event, 'Place', event_data.Place)
    setattr(db_event, 'Period', event_data.Period)
    setattr(db_event, 'Date', event_data.Date)
    setattr(db_event, '/numberEvents', event_data./numberEvents)
    setattr(db_event, 'Name', event_data.Name)
    if event_data.calendar is not None:
        db_calendar = database.query(Calendar).filter(Calendar.id == event_data.calendar).first()
        if not db_calendar:
            raise HTTPException(status_code=400, detail="Calendar not found")
        setattr(db_event, 'calendar_id', event_data.calendar)
    database.commit()
    database.refresh(db_event)

    return db_event


@app.delete("/event/{event_id}/", response_model=None, tags=["Event"])
async def delete_event(event_id: int, database: Session = Depends(get_db)):
    db_event = database.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    database.delete(db_event)
    database.commit()
    return db_event





############################################
#
#   Meeting functions
#
############################################

@app.get("/meeting/", response_model=None, tags=["Meeting"])
def get_all_meeting(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Meeting)
        query = query.options(joinedload(Meeting.calendar))
        meeting_list = query.all()

        # Serialize with relationships included
        result = []
        for meeting_item in meeting_list:
            item_dict = meeting_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if meeting_item.calendar:
                related_obj = meeting_item.calendar
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['calendar'] = related_dict
            else:
                item_dict['calendar'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            participant_list = database.query(Participant).join(participant_meeting, Participant.id == participant_meeting.c.participant).filter(participant_meeting.c.meeting == meeting_item.id).all()
            item_dict['participant'] = []
            for participant_obj in participant_list:
                participant_dict = participant_obj.__dict__.copy()
                participant_dict.pop('_sa_instance_state', None)
                item_dict['participant'].append(participant_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Meeting).all()


@app.get("/meeting/count/", response_model=None, tags=["Meeting"])
def get_count_meeting(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Meeting entities"""
    count = database.query(Meeting).count()
    return {"count": count}


@app.get("/meeting/paginated/", response_model=None, tags=["Meeting"])
def get_paginated_meeting(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Meeting entities"""
    total = database.query(Meeting).count()
    meeting_list = database.query(Meeting).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": meeting_list
        }

    result = []
    for meeting_item in meeting_list:
        participant_ids = database.query(participant_meeting.c.participant).filter(participant_meeting.c.meeting == meeting_item.id).all()
        item_data = {
            "meeting": meeting_item,
            "participant_ids": [x[0] for x in participant_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/meeting/search/", response_model=None, tags=["Meeting"])
def search_meeting(
    database: Session = Depends(get_db)
) -> list:
    """Search Meeting entities by attributes"""
    query = database.query(Meeting)


    results = query.all()
    return results


@app.get("/meeting/{meeting_id}/", response_model=None, tags=["Meeting"])
async def get_meeting(meeting_id: int, database: Session = Depends(get_db)) -> Meeting:
    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    participant_ids = database.query(participant_meeting.c.participant).filter(participant_meeting.c.meeting == db_meeting.id).all()
    response_data = {
        "meeting": db_meeting,
        "participant_ids": [x[0] for x in participant_ids],
}
    return response_data



@app.post("/meeting/", response_model=None, tags=["Meeting"])
async def create_meeting(meeting_data: MeetingCreate, database: Session = Depends(get_db)) -> Meeting:

    if meeting_data.calendar is not None:
        db_calendar = database.query(Calendar).filter(Calendar.id == meeting_data.calendar).first()
        if not db_calendar:
            raise HTTPException(status_code=400, detail="Calendar not found")
    else:
        raise HTTPException(status_code=400, detail="Calendar ID is required")
    if meeting_data.participant:
        for id in meeting_data.participant:
            # Entity already validated before creation
            db_participant = database.query(Participant).filter(Participant.id == id).first()
            if not db_participant:
                raise HTTPException(status_code=404, detail=f"Participant with ID {id} not found")

    db_meeting = Meeting(
        Place=meeting_data.Place,        Period=meeting_data.Period,        Date=meeting_data.Date,        /numberEvents=meeting_data./numberEvents,        Name=meeting_data.Name,        NumberParticipants=meeting_data.NumberParticipants,        calendar_id=meeting_data.calendar        )

    database.add(db_meeting)
    database.commit()
    database.refresh(db_meeting)


    if meeting_data.participant:
        for id in meeting_data.participant:
            # Entity already validated before creation
            db_participant = database.query(Participant).filter(Participant.id == id).first()
            # Create the association
            association = participant_meeting.insert().values(meeting=db_meeting.id, participant=db_participant.id)
            database.execute(association)
            database.commit()


    participant_ids = database.query(participant_meeting.c.participant).filter(participant_meeting.c.meeting == db_meeting.id).all()
    response_data = {
        "meeting": db_meeting,
        "participant_ids": [x[0] for x in participant_ids],
    }
    return response_data


@app.post("/meeting/bulk/", response_model=None, tags=["Meeting"])
async def bulk_create_meeting(items: list[MeetingCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Meeting entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.calendar:
                raise ValueError("Calendar ID is required")

            db_meeting = Meeting(
                Place=item_data.Place,                Period=item_data.Period,                Date=item_data.Date,                /numberEvents=item_data./numberEvents,                Name=item_data.Name,                NumberParticipants=item_data.NumberParticipants,                calendar_id=item_data.calendar            )
            database.add(db_meeting)
            database.flush()  # Get ID without committing
            created_items.append(db_meeting.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Meeting entities"
    }


@app.delete("/meeting/bulk/", response_model=None, tags=["Meeting"])
async def bulk_delete_meeting(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Meeting entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_meeting = database.query(Meeting).filter(Meeting.id == item_id).first()
        if db_meeting:
            database.delete(db_meeting)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Meeting entities"
    }

@app.put("/meeting/{meeting_id}/", response_model=None, tags=["Meeting"])
async def update_meeting(meeting_id: int, meeting_data: MeetingCreate, database: Session = Depends(get_db)) -> Meeting:
    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    setattr(db_meeting, 'NumberParticipants', meeting_data.NumberParticipants)
    existing_participant_ids = [assoc.participant for assoc in database.execute(
        participant_meeting.select().where(participant_meeting.c.meeting == db_meeting.id))]

    participants_to_remove = set(existing_participant_ids) - set(meeting_data.participant)
    for participant_id in participants_to_remove:
        association = participant_meeting.delete().where(
            (participant_meeting.c.meeting == db_meeting.id) & (participant_meeting.c.participant == participant_id))
        database.execute(association)

    new_participant_ids = set(meeting_data.participant) - set(existing_participant_ids)
    for participant_id in new_participant_ids:
        db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
        if db_participant is None:
            raise HTTPException(status_code=404, detail=f"Participant with ID {participant_id} not found")
        association = participant_meeting.insert().values(participant=db_participant.id, meeting=db_meeting.id)
        database.execute(association)
    database.commit()
    database.refresh(db_meeting)

    participant_ids = database.query(participant_meeting.c.participant).filter(participant_meeting.c.meeting == db_meeting.id).all()
    response_data = {
        "meeting": db_meeting,
        "participant_ids": [x[0] for x in participant_ids],
    }
    return response_data


@app.delete("/meeting/{meeting_id}/", response_model=None, tags=["Meeting"])
async def delete_meeting(meeting_id: int, database: Session = Depends(get_db)):
    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    database.delete(db_meeting)
    database.commit()
    return db_meeting

@app.post("/meeting/{meeting_id}/participant/{participant_id}/", response_model=None, tags=["Meeting Relationships"])
async def add_participant_to_meeting(meeting_id: int, participant_id: int, database: Session = Depends(get_db)):
    """Add a Participant to this Meeting's participant relationship"""
    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    db_participant = database.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    # Check if relationship already exists
    existing = database.query(participant_meeting).filter(
        (participant_meeting.c.meeting == meeting_id) &
        (participant_meeting.c.participant == participant_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = participant_meeting.insert().values(meeting=meeting_id, participant=participant_id)
    database.execute(association)
    database.commit()

    return {"message": "Participant added to participant successfully"}


@app.delete("/meeting/{meeting_id}/participant/{participant_id}/", response_model=None, tags=["Meeting Relationships"])
async def remove_participant_from_meeting(meeting_id: int, participant_id: int, database: Session = Depends(get_db)):
    """Remove a Participant from this Meeting's participant relationship"""
    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Check if relationship exists
    existing = database.query(participant_meeting).filter(
        (participant_meeting.c.meeting == meeting_id) &
        (participant_meeting.c.participant == participant_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = participant_meeting.delete().where(
        (participant_meeting.c.meeting == meeting_id) &
        (participant_meeting.c.participant == participant_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Participant removed from participant successfully"}


@app.get("/meeting/{meeting_id}/participant/", response_model=None, tags=["Meeting Relationships"])
async def get_participant_of_meeting(meeting_id: int, database: Session = Depends(get_db)):
    """Get all Participant entities related to this Meeting through participant"""
    db_meeting = database.query(Meeting).filter(Meeting.id == meeting_id).first()
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    participant_ids = database.query(participant_meeting.c.participant).filter(participant_meeting.c.meeting == meeting_id).all()
    participant_list = database.query(Participant).filter(Participant.id.in_([id[0] for id in participant_ids])).all()

    return {
        "meeting_id": meeting_id,
        "participant_count": len(participant_list),
        "participant": participant_list
    }





############################################
#
#   Courses functions
#
############################################

@app.get("/courses/", response_model=None, tags=["Courses"])
def get_all_courses(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Courses)
        query = query.options(joinedload(Courses.calendar))
        courses_list = query.all()

        # Serialize with relationships included
        result = []
        for courses_item in courses_list:
            item_dict = courses_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if courses_item.calendar:
                related_obj = courses_item.calendar
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['calendar'] = related_dict
            else:
                item_dict['calendar'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Courses).all()


@app.get("/courses/count/", response_model=None, tags=["Courses"])
def get_count_courses(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Courses entities"""
    count = database.query(Courses).count()
    return {"count": count}


@app.get("/courses/paginated/", response_model=None, tags=["Courses"])
def get_paginated_courses(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Courses entities"""
    total = database.query(Courses).count()
    courses_list = database.query(Courses).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": courses_list
    }


@app.get("/courses/search/", response_model=None, tags=["Courses"])
def search_courses(
    database: Session = Depends(get_db)
) -> list:
    """Search Courses entities by attributes"""
    query = database.query(Courses)


    results = query.all()
    return results


@app.get("/courses/{courses_id}/", response_model=None, tags=["Courses"])
async def get_courses(courses_id: int, database: Session = Depends(get_db)) -> Courses:
    db_courses = database.query(Courses).filter(Courses.id == courses_id).first()
    if db_courses is None:
        raise HTTPException(status_code=404, detail="Courses not found")

    response_data = {
        "courses": db_courses,
}
    return response_data



@app.post("/courses/", response_model=None, tags=["Courses"])
async def create_courses(courses_data: CoursesCreate, database: Session = Depends(get_db)) -> Courses:

    if courses_data.calendar is not None:
        db_calendar = database.query(Calendar).filter(Calendar.id == courses_data.calendar).first()
        if not db_calendar:
            raise HTTPException(status_code=400, detail="Calendar not found")
    else:
        raise HTTPException(status_code=400, detail="Calendar ID is required")

    db_courses = Courses(
        Place=courses_data.Place,        Period=courses_data.Period,        Date=courses_data.Date,        /numberEvents=courses_data./numberEvents,        Name=courses_data.Name,        Type=courses_data.Type,        calendar_id=courses_data.calendar        )

    database.add(db_courses)
    database.commit()
    database.refresh(db_courses)




    return db_courses


@app.post("/courses/bulk/", response_model=None, tags=["Courses"])
async def bulk_create_courses(items: list[CoursesCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Courses entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.calendar:
                raise ValueError("Calendar ID is required")

            db_courses = Courses(
                Place=item_data.Place,                Period=item_data.Period,                Date=item_data.Date,                /numberEvents=item_data./numberEvents,                Name=item_data.Name,                Type=item_data.Type,                calendar_id=item_data.calendar            )
            database.add(db_courses)
            database.flush()  # Get ID without committing
            created_items.append(db_courses.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Courses entities"
    }


@app.delete("/courses/bulk/", response_model=None, tags=["Courses"])
async def bulk_delete_courses(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Courses entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_courses = database.query(Courses).filter(Courses.id == item_id).first()
        if db_courses:
            database.delete(db_courses)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Courses entities"
    }

@app.put("/courses/{courses_id}/", response_model=None, tags=["Courses"])
async def update_courses(courses_id: int, courses_data: CoursesCreate, database: Session = Depends(get_db)) -> Courses:
    db_courses = database.query(Courses).filter(Courses.id == courses_id).first()
    if db_courses is None:
        raise HTTPException(status_code=404, detail="Courses not found")

    setattr(db_courses, 'Type', courses_data.Type)
    database.commit()
    database.refresh(db_courses)

    return db_courses


@app.delete("/courses/{courses_id}/", response_model=None, tags=["Courses"])
async def delete_courses(courses_id: int, database: Session = Depends(get_db)):
    db_courses = database.query(Courses).filter(Courses.id == courses_id).first()
    if db_courses is None:
        raise HTTPException(status_code=404, detail="Courses not found")
    database.delete(db_courses)
    database.commit()
    return db_courses





############################################
#
#   Calendar functions
#
############################################

@app.get("/calendar/", response_model=None, tags=["Calendar"])
def get_all_calendar(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Calendar)
        calendar_list = query.all()

        # Serialize with relationships included
        result = []
        for calendar_item in calendar_list:
            item_dict = calendar_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            event_list = database.query(Event).filter(Event.calendar_id == calendar_item.id).all()
            item_dict['event'] = []
            for event_obj in event_list:
                event_dict = event_obj.__dict__.copy()
                event_dict.pop('_sa_instance_state', None)
                item_dict['event'].append(event_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Calendar).all()


@app.get("/calendar/count/", response_model=None, tags=["Calendar"])
def get_count_calendar(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Calendar entities"""
    count = database.query(Calendar).count()
    return {"count": count}


@app.get("/calendar/paginated/", response_model=None, tags=["Calendar"])
def get_paginated_calendar(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Calendar entities"""
    total = database.query(Calendar).count()
    calendar_list = database.query(Calendar).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": calendar_list
        }

    result = []
    for calendar_item in calendar_list:
        event_ids = database.query(Event.id).filter(Event.calendar_id == calendar_item.id).all()
        item_data = {
            "calendar": calendar_item,
            "event_ids": [x[0] for x in event_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/calendar/search/", response_model=None, tags=["Calendar"])
def search_calendar(
    database: Session = Depends(get_db)
) -> list:
    """Search Calendar entities by attributes"""
    query = database.query(Calendar)


    results = query.all()
    return results


@app.get("/calendar/{calendar_id}/", response_model=None, tags=["Calendar"])
async def get_calendar(calendar_id: int, database: Session = Depends(get_db)) -> Calendar:
    db_calendar = database.query(Calendar).filter(Calendar.id == calendar_id).first()
    if db_calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")

    event_ids = database.query(Event.id).filter(Event.calendar_id == db_calendar.id).all()
    response_data = {
        "calendar": db_calendar,
        "event_ids": [x[0] for x in event_ids]}
    return response_data



@app.post("/calendar/", response_model=None, tags=["Calendar"])
async def create_calendar(calendar_data: CalendarCreate, database: Session = Depends(get_db)) -> Calendar:


    db_calendar = Calendar(
        Name=calendar_data.Name        )

    database.add(db_calendar)
    database.commit()
    database.refresh(db_calendar)

    if calendar_data.event:
        # Validate that all Event IDs exist
        for event_id in calendar_data.event:
            db_event = database.query(Event).filter(Event.id == event_id).first()
            if not db_event:
                raise HTTPException(status_code=400, detail=f"Event with id {event_id} not found")

        # Update the related entities with the new foreign key
        database.query(Event).filter(Event.id.in_(calendar_data.event)).update(
            {Event.calendar_id: db_calendar.id}, synchronize_session=False
        )
        database.commit()



    event_ids = database.query(Event.id).filter(Event.calendar_id == db_calendar.id).all()
    response_data = {
        "calendar": db_calendar,
        "event_ids": [x[0] for x in event_ids]    }
    return response_data


@app.post("/calendar/bulk/", response_model=None, tags=["Calendar"])
async def bulk_create_calendar(items: list[CalendarCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Calendar entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_calendar = Calendar(
                Name=item_data.Name            )
            database.add(db_calendar)
            database.flush()  # Get ID without committing
            created_items.append(db_calendar.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Calendar entities"
    }


@app.delete("/calendar/bulk/", response_model=None, tags=["Calendar"])
async def bulk_delete_calendar(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Calendar entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_calendar = database.query(Calendar).filter(Calendar.id == item_id).first()
        if db_calendar:
            database.delete(db_calendar)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Calendar entities"
    }

@app.put("/calendar/{calendar_id}/", response_model=None, tags=["Calendar"])
async def update_calendar(calendar_id: int, calendar_data: CalendarCreate, database: Session = Depends(get_db)) -> Calendar:
    db_calendar = database.query(Calendar).filter(Calendar.id == calendar_id).first()
    if db_calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")

    setattr(db_calendar, 'Name', calendar_data.Name)
    if calendar_data.event is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Event).filter(Event.calendar_id == db_calendar.id).update(
            {Event.calendar_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if calendar_data.event:
            # Validate that all IDs exist
            for event_id in calendar_data.event:
                db_event = database.query(Event).filter(Event.id == event_id).first()
                if not db_event:
                    raise HTTPException(status_code=400, detail=f"Event with id {event_id} not found")

            # Update the related entities with the new foreign key
            database.query(Event).filter(Event.id.in_(calendar_data.event)).update(
                {Event.calendar_id: db_calendar.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_calendar)

    event_ids = database.query(Event.id).filter(Event.calendar_id == db_calendar.id).all()
    response_data = {
        "calendar": db_calendar,
        "event_ids": [x[0] for x in event_ids]    }
    return response_data


@app.delete("/calendar/{calendar_id}/", response_model=None, tags=["Calendar"])
async def delete_calendar(calendar_id: int, database: Session = Depends(get_db)):
    db_calendar = database.query(Calendar).filter(Calendar.id == calendar_id).first()
    if db_calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    database.delete(db_calendar)
    database.commit()
    return db_calendar







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



