from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, timedelta, datetime
import json

app = FastAPI(
    title="Birthday Calendar API",
    description="Manage and view birthdays."
)

class Birthday(BaseModel):
    name: str
    birthday: date
    message: Optional[str] = None

birthday_db: List[dict] = []

# Load data
try:
    with open("birthdays.json", "r") as f:
        raw_data = json.load(f)
        birthday_db = [
            {
                "name": entry["name"],
                "birthday": datetime.strptime(entry["birthday"], "%Y-%m-%d").date(),
                "message": entry.get("message")
            }
            for entry in raw_data
        ]
except FileNotFoundError:
    print("Empty list.")


# Root route
@app.get("/")
def root():
    return {"message": "🎉 Birthday API is up and running!"}


# Add a new birthday and save it
@app.post("/birthdays/", response_model=Birthday)
def add_birthday(entry: Birthday):
    birthday_db.append(entry.dict())

    # Save to file
    with open("birthdays.json", "w") as f:
        json.dump(
            [dict(e) for e in birthday_db],
            f,
            indent=2,
            default=str
        )
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

        # If birthday already passed this year, move to next year
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

        if day and b_date.day != day:
            continue
        if month and b_date.month != month:
            continue
        if year and b_date.year != year:
            continue

        results.append(entry)

    return results
