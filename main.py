from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, timedelta, datetime

app = FastAPI(title="Birthday Calendar API", description="Manage and view birthdays.")

# In-memory database
birthday_db: List[dict] = []

# Pydantic model
class Birthday(BaseModel):
    name: str
    birthday: date
    message: Optional[str] = None

# Add a birthday
@app.post("/birthdays/", response_model=Birthday)
def add_birthday(entry: Birthday):
    birthday_db.append(entry.dict())
    return entry

# Get all birthdays
@app.get("/birthdays/", response_model=List[Birthday])
def get_all_birthdays():
    return birthday_db

# Get upcoming birthdays (within X days)
@app.get("/birthdays/upcoming", response_model=List[Birthday])
def get_upcoming_birthdays(days: int = Query(7, ge=1, le=365)):
    today = date.today()
    upcoming = today + timedelta(days=days)
    upcoming_birthdays = []

    for entry in birthday_db:
        b_date = entry["birthday"]
        b_this_year = b_date.replace(year=today.year)

        # Handle birthdays already passed this year
        if b_this_year < today:
            b_this_year = b_this_year.replace(year=today.year + 1)

        if today <= b_this_year <= upcoming:
            upcoming_birthdays.append(entry)

    return upcoming_birthdays

# Search birthdays by day, month, or year
@app.get("/birthdays/search", response_model=List[Birthday])
def search_birthdays(
    day: Optional[int] = Query(None, ge=1, le=31),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=1900, le=2100),
):
    results = []

    for entry in birthday_db:
        b_date = entry["birthday"]

        # Check each filter condition
        if day and b_date.day != day:
            continue
        if month and b_date.month != month:
            continue
        if year and b_date.year != year:
            continue

        results.append(entry)

    return results
