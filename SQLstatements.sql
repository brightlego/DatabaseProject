DROP TABLE IF EXISTS Caregivers;
DROP TABLE IF EXISTS Children;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS ChildSessions;

CREATE TABLE Caregivers
(
    CaregiverID INTEGER PRIMARY KEY NOT NULL,
    PhysicalAddress TEXT NOT NULL,
    ContactNumber VARCHAR(20) NOT NULL,
    EmailAddress  TEXT NOT NULL
);

CREATE TABLE Children
(
    ChildID INTEGER PRIMARY KEY NOT NULL,
    ChildName TEXT NOT NULL,
    CaregiverID INTEGER NOT NULL,
    FOREIGN KEY (CaregiverID) REFERENCES Caregivers(CaregiverID)
);

CREATE TABLE Sessions
(
    SessionID INTEGER PRIMARY KEY NOT NULL,
    SessionType VARCHAR(1) NOT NULL CHECK(SessionType IN ('M', 'A')), --M for morning, A for afternoon
    Date CHAR(10) NOT NULL, --yyyy-mm-dd
    UNIQUE(Date, SessionType)
);

CREATE TABLE ChildSessions
(
    MorningSession INTEGER DEFAULT 0,
    AfternoonSession INTEGER DEFAULT 0,
    ChildID INTEGER NOT NULL,
    BookingType CHAR(1) NOT NULL DEFAULT 'N' CHECK(BookingType IN ('N','M','A','B')), --N for none, M for morning only, A for afternoon only, B for both

    FOREIGN KEY (MorningSession) REFERENCES Sessions(SessionID),
    FOREIGN KEY (AfternoonSession) REFERENCES Sessions(SessionID),
    FOREIGN KEY (ChildID) REFERENCES Children(ChildID),
    PRIMARY KEY (MorningSession, AfternoonSession, ChildID)
);

INSERT INTO Sessions(SessionID, SessionType, Date) VALUES (0, 'M', '0001-01-01');
