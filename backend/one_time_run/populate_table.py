import sqlite3
import csv
from datetime import date, timedelta
import random
import os

DIR = os.path.split(os.path.realpath(__file__))[0]

DB_NAME = os.path.join(DIR, "..", "sunnytots.db")

CAREGIVER_CSV = os.path.join(DIR, "mock_data", "caregivers.csv")
CHILDNAMES_CSV = os.path.join(DIR, "mock_data", "childnames.csv")

CAREGIVER_INSERT_SQL = """
INSERT INTO Caregivers(
    CaregiverID,
    PhysicalAddress,
    ContactNumber,
    EmailAddress,
    Name
)
VALUES (?,?,?,?,?)
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
    SessionType,
    Date
)
VALUES ('M',?)
"""

SESSION_AFTERNOON_INSERT_SQL = """
INSERT INTO Sessions(
    SessionType,
    Date
)
VALUES ('A', ?)
"""

CHILD_SESSION_INSERT_SQL = """
INSERT INTO ChildSessions(
    ChildID,
    Date,
    MorningSession,
    AfternoonSession,
    MorningBooked,
    AfternoonBooked
)
VALUES (?,?,?,?,?,?)
"""

GET_N_CHILDREN_SQL = "SELECT ChildID FROM Children ORDER BY RANDOM() LIMIT ?"

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
        try:
            connection.execute(SESSION_MORNING_INSERT_SQL, [daystr])
            connection.execute(SESSION_AFTERNOON_INSERT_SQL, [daystr])
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
    print("")
    errors = {}
    for day in days_in_year(YEAR, restrictions=True):
        morning_children = connection.execute(
            GET_N_CHILDREN_SQL, [random.randint(1, 20)]
        ).fetchall()
        afternoon_children = connection.execute(
            GET_N_CHILDREN_SQL, [random.randint(1, 20)]
        ).fetchall()

        datestr = day.isoformat()

        try:
            for (child,) in morning_children:
                if (child,) in afternoon_children:
                    connection.execute(
                        CHILD_SESSION_INSERT_SQL,
                        [
                            child,
                            datestr,
                            True,
                            True,
                            random.choice([True, False]),
                            random.choice([True, False]),
                        ],
                    )
                else:
                    print(datestr)
                    print(
                        connection.execute(
                            "SELECT * FROM Sessions WHERE Date=?", [datestr]
                        ).fetchall()
                    )
                    connection.execute(
                        CHILD_SESSION_INSERT_SQL,
                        [
                            child,
                            datestr,
                            True,
                            False,
                            random.choice([True, False]),
                            False,
                        ],
                    )

            for (child,) in afternoon_children:
                if (child,) in morning_children:
                    continue
                else:
                    connection.execute(
                        CHILD_SESSION_INSERT_SQL,
                        [
                            child,
                            datestr,
                            False,
                            True,
                            False,
                            random.choice([True, False]),
                        ],
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


def main():
    connection = sqlite3.connect(DB_NAME)

    # connection.execute("PRAGMA foreign_keys = ON")

    populate_caregivers(connection)
    populate_children(connection)
    populate_sessions(connection)
    link_child_session(connection)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
