DROP TABLE IF EXISTS Caregivers;
DROP TABLE IF EXISTS Children;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS ChildSessions;

CREATE TABLE Caregivers
(
    CaregiverID INTEGER PRIMARY KEY AUTOINCREMENT,
    PhysicalAddress TEXT NOT NULL,
    ContactNumber VARCHAR(20) NOT NULL,
    EmailAddress  TEXT NOT NULL,
    Name TEXT NOT NULL
);

CREATE TABLE Children
(
    ChildID INTEGER PRIMARY KEY AUTOINCREMENT,
    ChildName TEXT NOT NULL,
    CaregiverID INTEGER NOT NULL,
    FOREIGN KEY (CaregiverID) REFERENCES Caregivers(CaregiverID)
);

CREATE TABLE Sessions
(
    SessionType CHAR(1) NOT NULL CHECK(SessionType IN ('M', 'A')), --M for morning, A for afternoon
    Date CHAR(10) NOT NULL, --yyyy-mm-dd
    PRIMARY KEY(Date, SessionType)
);

CREATE TABLE ChildSessions
(
    MorningSession BOOLEAN DEFAULT FALSE,
    AfternoonSession BOOLEAN DEFAULT FALSE,
    MorningBooked BOOLEAN DEFAULT FALSE,
    AfternoonBooked BOOLEAN DEFAULT FALSE,

    ChildID INTEGER NOT NULL,
    Date CHAR(10) NOT NULL, --yyyy-mm-dd

    FOREIGN KEY (ChildID) REFERENCES Children(ChildID),
    FOREIGN KEY (Date) REFERENCES Sessions(Date),
    PRIMARY KEY (Date, ChildID)
);
