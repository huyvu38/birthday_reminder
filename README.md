# Birthday_reminder
This is a RESTful API built with FastAPI that allows user to manage and view birthdays, including upcoming birthdays and searching birthdays for a specific date.

### Feature
Add Birthday: Add a new birthday to the calendar 

Delete Birthday: Remove a birthday from the calendar

Get Upcoming Birthdays: Retrieve the next upcoming birthdays in chronological order.

Get Birthdays by Date: Retrieve all birthdays for a specific date.

### Technologies
Python
FastAPI

### Setup


1.  **Clone the repository:**

    ```bash
    git clone [https://your-repo-url.git](https://your-repo-url.git)
    cd birthday_reminder
    ```

2.  **Install dependencies:**

    ```bash
    pip install fastapi uvicorn
    ```

### Running the API

1.  Navigate to the project directory in your terminal.

2.  Run the Uvicorn server:

    ```bash
    uvicorn main:app --reload
    ```

3.  Open the interactive API documentation in your browser:

    ```
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    ```
