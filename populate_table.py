import sqlite3
import csv
from datetime import date, timedelta
import random

DB_NAME = "sunnytots.db"

CAREGIVER_CSV = "mock_data/caregivers.csv"
CHILDNAMES_CSV = "mock_data/childnames.csv"

CAREGIVER_INSERT_SQL = """
INSERT INTO Caregivers(
    CaregiverID,
    PhysicalAddress,
    ContactNumber,
    EmailAddress
)
VALUES (?,?,?,?)
"""

CHILD_INSERT_SQL = """
INSERT INTO Children(
    ChildID,
    ChildName,
    CaregiverID
)
VALUES (?,?,?)
"""

SESSION_MORNING_INSERT_SQL = """
INSERT INTO Sessions(
    SessionID,
    SessionType,
    Date
)
VALUES (?,'M',?)
"""

SESSION_AFTERNOON_INSERT_SQL = """
INSERT INTO Sessions(
    SessionID,
    SessionType,
    Date
)
VALUES (?,'A', ?)
"""

CHILD_SESSION_INSERT_SQL = """
INSERT INTO ChildSessions(
    ChildID,
    MorningSession,
    AfternoonSession,
    BookingType
)
VALUES (?,?,?,?)
"""

GET_20_CHILDREN_SQL = "SELECT ChildID FROM Children ORDER BY RANDOM() LIMIT 20"

GET_MORNING_SESSION = "SELECT SessionID FROM Sessions WHERE Date=? AND SessionType='M'"
GET_AFTERNOON_SESSION = (
    "SELECT SessionID FROM Sessions WHERE Date=? AND SessionType='A'"
)


# yyyy-mm-dd
BLACKLIST_DAYS = [
    date(2023, 1, 1),
    date(2023, 12, 25),
    date(2023, 12, 26),
    date(2023, 12, 31),
]
YEAR = 2023


def populate_caregivers(connection):
    print("Populating Caregivers")
    with open(CAREGIVER_CSV, "rt", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        try:
            connection.executemany(CAREGIVER_INSERT_SQL, csvreader)
        except sqlite3.IntegrityError as err:
            print(f"{type(err).__name__}: {str(err)}")


def populate_children(connection):
    print("Populating Children")
    with open(CHILDNAMES_CSV, "rt", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        try:
            connection.executemany(CHILD_INSERT_SQL, csvreader)
        except sqlite3.IntegrityError as err:
            print(f"{type(err).__name__}: {str(err)}")


def days_in_year(year, interval=timedelta(days=1), restrictions=True):
    day = date(year, 1, 1)
    while day.year == year:
        if not (restrictions and (day.weekday() >= 5 or day in BLACKLIST_DAYS)):
            yield day
        day += interval


def populate_sessions(connection):
    print("Populating Sessions")
    errors = {}
    for day in days_in_year(YEAR, restrictions=True):
        daystr = day.isoformat()
        morningid = random.randint(1, 1000000)
        afternoonid = random.randint(1, 1000000)
        try:
            connection.execute(SESSION_MORNING_INSERT_SQL, [morningid, daystr])
            connection.execute(SESSION_AFTERNOON_INSERT_SQL, [afternoonid, daystr])
        except sqlite3.IntegrityError as err:
            errstr = f"{type(err).__name__}: {str(err)}"
            if errstr in errors:
                errors[errstr] += 1
            else:
                errors[errstr] = 1

    for errstr in errors:
        if errors[errstr] == 1:
            print(errstr)
        else:
            print(f"{errstr} x{errors[errstr]}")


def link_child_session(connection):
    errors = {}
    for day in days_in_year(YEAR, restrictions=True):
        morning_children = connection.execute(GET_20_CHILDREN_SQL).fetchall()
        afternoon_children = connection.execute(GET_20_CHILDREN_SQL).fetchall()

        morning_session = connection.execute(
            GET_MORNING_SESSION, [day.isoformat()]
        ).fetchone()
        afternoon_session = connection.execute(
            GET_AFTERNOON_SESSION, [day.isoformat()]
        ).fetchone()

        if morning_session is None or afternoon_session is None:
            continue
        else:
            morning_session = morning_session[0]
            afternoon_session = afternoon_session[0]

        try:
            for (child,) in morning_children:
                if (child,) in afternoon_children:
                    connection.execute(
                        CHILD_SESSION_INSERT_SQL,
                        [
                            child,
                            morning_session,
                            afternoon_session,
                            random.choice("NMAB"),
                        ],
                    )
                else:
                    connection.execute(
                        CHILD_SESSION_INSERT_SQL,
                        [child, morning_session, 0, random.choice("NM")],
                    )

            for (child,) in afternoon_children:
                if (child,) in morning_children:
                    continue
                else:
                    connection.execute(
                        CHILD_SESSION_INSERT_SQL,
                        [child, 0, afternoon_session, random.choice("NA")],
                    )
        except sqlite3.IntegrityError as err:
            errstr = f"{type(err).__name__}: {str(err)}"
            if errstr in errors:
                errors[errstr] += 1
            else:
                errors[errstr] = 1

    for errstr in errors:
        if errors[errstr] == 1:
            print(errstr)
        else:
            print(f"{errstr} x{errors[errstr]}")


connection = sqlite3.connect(DB_NAME)

populate_caregivers(connection)
populate_children(connection)
populate_sessions(connection)
link_child_session(connection)

connection.commit()
connection.close()
