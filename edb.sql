-- Create database
CREATE DATABASE EducationDB;
USE EducationDB;

-- Person table (generalized superclass)
CREATE TABLE Person (
    PersonID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL, -- Store hashed passwords at application level
    RoleType ENUM('Student', 'Instructor', 'Administrator') NOT NULL,
    CHECK (RoleType IN ('Student', 'Instructor', 'Administrator'))
);

-- Student table (specialized subclass)
CREATE TABLE Student (
    PersonID INT PRIMARY KEY,
    DateOfBirth DATE,
    EnrollmentDate DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Instructor table (specialized subclass)
CREATE TABLE Instructor (
    PersonID INT PRIMARY KEY,
    HireDate DATE,
    Department VARCHAR(100),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Administrator table (specialized subclass)
CREATE TABLE Administrator (
    PersonID INT PRIMARY KEY,
    PrivilegeLevel VARCHAR(50),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Course table
CREATE TABLE Course (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Description TEXT,
    InstructorID INT,
    FOREIGN KEY (InstructorID) REFERENCES Instructor(PersonID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Enrollment table - many-to-many between Student and Course
CREATE TABLE Enrollment (
    EnrollmentID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    EnrollmentDate DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (StudentID) REFERENCES Student(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE (StudentID, CourseID) -- Unique enrollment per course per student
);

-- Exam table
CREATE TABLE Exam (
    ExamID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    ExamDate DATE NOT NULL,
    Duration INT NOT NULL, -- Duration in minutes
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Result table
CREATE TABLE Result (
    ResultID INT AUTO_INCREMENT PRIMARY KEY,
    ExamID INT,
    StudentID INT,
    Score DECIMAL(5,2) NOT NULL CHECK (Score >= 0 AND Score <= 100),
    Grade CHAR(2),
    FOREIGN KEY (ExamID) REFERENCES Exam(ExamID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (StudentID) REFERENCES Student(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE (ExamID, StudentID)
);

-- Function to calculate Grade based on Score
DELIMITER //
CREATE FUNCTION CalculateGrade(score DECIMAL(5,2)) RETURNS CHAR(2)
DETERMINISTIC
BEGIN
    DECLARE grade CHAR(2);
    IF score >= 85 THEN
        SET grade = 'A';
    ELSEIF score >= 70 THEN
        SET grade = 'B';
    ELSEIF score >= 55 THEN
        SET grade = 'C';
    ELSEIF score >= 40 THEN
        SET grade = 'D';
    ELSE
        SET grade = 'F';
    END IF;
    RETURN grade;
END;
//
DELIMITER ;

-- Triggers to automatically calculate Grade on Result insert and update
DELIMITER //
CREATE TRIGGER trg_BeforeResultInsert
BEFORE INSERT ON Result
FOR EACH ROW
BEGIN
    SET NEW.Grade = CalculateGrade(NEW.Score);
END;
//
CREATE TRIGGER trg_BeforeResultUpdate
BEFORE UPDATE ON Result
FOR EACH ROW
BEGIN
    SET NEW.Grade = CalculateGrade(NEW.Score);
END;
//
DELIMITER ;

-- Trigger to auto-insert Result records with score 0 for all enrolled students when a new exam is inserted
DELIMITER //
CREATE TRIGGER trg_AfterExamInsert
AFTER INSERT ON Exam
FOR EACH ROW
BEGIN
    INSERT INTO Result (ExamID, StudentID, Score, Grade)
    SELECT NEW.ExamID, StudentID, 0, 'F' FROM Enrollment WHERE CourseID = NEW.CourseID;
END;
//
DELIMITER ;

-- Audit log table for tracking critical changes
CREATE TABLE AuditLog (
    AuditID INT AUTO_INCREMENT PRIMARY KEY,
    TableName VARCHAR(50),
    OperationType VARCHAR(10),
    ChangedBy VARCHAR(100),
    ChangeTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Details TEXT
);

-- Example trigger for logging inserts into Result
DELIMITER //
CREATE TRIGGER trg_LogResultInsert
AFTER INSERT ON Result
FOR EACH ROW
BEGIN
    INSERT INTO AuditLog(TableName, OperationType, ChangedBy, Details)
    VALUES ('Result', 'INSERT', USER(), CONCAT('Inserted ResultID:', NEW.ResultID, ' Score:', NEW.Score));
END;
//
DELIMITER ;

-- View to allow students to see only their own results
CREATE VIEW StudentResultsView AS
SELECT r.ResultID, r.ExamID, r.Score, r.Grade, s.PersonID AS StudentID
FROM Result r
JOIN Student s ON r.StudentID = s.PersonID;

-- User privileges setup (example usage, must be run with admin rights)
-- CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'password';
-- GRANT ALL PRIVILEGES ON EducationDB.* TO 'admin_user'@'localhost';
-- CREATE USER 'instructor_user'@'localhost' IDENTIFIED BY 'password';
-- GRANT SELECT, INSERT, UPDATE ON EducationDB.* TO 'instructor_user'@'localhost';
-- CREATE USER 'student_user'@'localhost' IDENTIFIED BY 'password';
-- GRANT SELECT ON StudentResultsView TO 'student_user'@'localhost';

-- Sample stored procedure to safely enroll a student in a course
DELIMITER //
CREATE PROCEDURE EnrollStudent(IN p_studentID INT, IN p_courseID INT)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Enrollment WHERE StudentID = p_studentID AND CourseID = p_courseID) THEN
        INSERT INTO Enrollment(StudentID, CourseID) VALUES (p_studentID, p_courseID);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in this course';
    END IF;
END;
//
DELIMITER ;


-- sample data

INSERT INTO Person (FullName, Email, Password, RoleType) VALUES
('Alice Johnson', 'alice@example.com', 'hashed_password_1', 'Student'),
('Bob Smith', 'bob@example.com', 'hashed_password_2', 'Student'),
('Carol White', 'carol@example.com', 'hashed_password_3', 'Student'),
('David Brown', 'david@example.com', 'hashed_password_4', 'Instructor'),
('Eva Green', 'eva@example.com', 'hashed_password_5', 'Administrator');
INSERT INTO Person (FullName, Email, Password, RoleType)
VALUES ('Frank Black', 'blk@example.com', 'hashed_password_6', 'Administrator');
INSERT INTO Person (PersonID, FullName, Email, Password, RoleType)
VALUES (7, 'Jax Briggs', 'jax@example.com', 'hashed_password_7', 'instructor');


UPDATE Person
SET PersonID = 1
WHERE FullName = 'Alice Johnson';
UPDATE Person
SET PersonID = 2
WHERE FullName = 'Bob Smith';
UPDATE Person
SET PersonID = 3
WHERE FullName = 'Carol White';
UPDATE Person
SET PersonID = 4
WHERE FullName = 'David Brown';
UPDATE Person
SET PersonID = 5
WHERE FullName = 'Eva Green';
UPDATE Person
SET PersonID = 6
WHERE FullName = 'Frank Black';

SELECT * FROM Person;

INSERT INTO Student (PersonID, DateOfBirth) VALUES
(1, '2000-01-15'),
(2, '2001-03-22'),
(3, '2002-05-10');

DELETE FROM Student
WHERE DateOfBirth = '2003-07-18';

DELETE FROM Student
WHERE DateOfBirth = '2004-09-25';

SELECT * FROM Student;

INSERT INTO Instructor (PersonID, HireDate, Department) VALUES
(4, '2020-06-01', 'Computer Science');
INSERT INTO Instructor (PersonID, HireDate, Department) VALUES
(7, '2018-10-01', 'Cybernetics');


SELECT * FROM Instructor;

INSERT INTO Administrator (PersonID, PrivilegeLevel) VALUES
(5, 'Full Access'),
(6, 'Limited Access');

INSERT INTO Course (CourseName, Description, InstructorID) VALUES
('Computer Science 101', 'Introduction to Programming', 4);
INSERT INTO Course (CourseName, Description, InstructorID) VALUES
('Cybernetics', 'Understanding Man & Machine as One', 7);
INSERT INTO Course (CourseID, CourseName, Description, InstructorID) VALUES
(245, 'Cybernetics', 'Understanding Man & Machine as One', 7);



UPDATE Course
SET CourseID = 101
WHERE `InstructorID` = 4;
UPDATE Course
SET CourseID = 242
WHERE InstructorID = 7;

SELECT * FROM Course


INSERT INTO Enrollment (StudentID, CourseID) VALUES
(1, 101),
(2, 101),
(3, 242);
 UPDATE `Enrollment`
 SET `CourseID` = 245
 WHERE `StudentID` = 2;
SELECT * FROM Enrollment;


INSERT INTO Exam (CourseID, ExamDate, Duration) VALUES
(101, '2025-12-01', 120),
(242, '2025-12-02', 120);

INSERT INTO Exam (`ExamID`, CourseID, ExamDate, Duration) VALUES
(11, 245, '2025-12-04', 120);


UPDATE Exam
SET ExamID =20
WHERE `ExamDate` = '2025-12-01';
UPDATE Exam
SET ExamID =12
WHERE `ExamDate` = '2025-12-02'

SELECT * FROM Exam;


INSERT INTO Result (ExamID, StudentID, Score) VALUES
(21, 1, 85.5),
(11, 2, 78.0),
(12, 3, 92.0);

UPDATE `Result`
SET `ExamID` = 11
WHERE `Score` = 78.0;

UPDATE `Result`
SET `ExamID` = 20
WHERE `Score` = 78.0;

DELETE FROM Result
where StudentID = 3;

UPDATE `Result`
SET `ResultID` = 1
WHERE `Score` = 92.0;
UPDATE `Result`
SET `ResultID` = 3
WHERE `Score` = 78.0;
UPDATE `Result`
SET `ResultID` = 2
WHERE `Score` = 85.5;
INSERT INTO Result (ResultID, ExamID, StudentID, Score) VALUES
(1, 20, 2, 78.0);
INSERT INTO Result (ResultID, ExamID, StudentID, Score) VALUES
(2, 11, 1, 85.0);

INSERT INTO Result (ResultID, ExamID, StudentID, Score) VALUES
(1, 12, 3, 92.0);


SELECT * FROM `Result`;


INSERT INTO AuditLog (TableName, OperationType, ChangedBy, Details) VALUES
('Result', 'INSERT', 'admin_user', 'Inserted ResultID:1 Score:85.5'),
('Result', 'INSERT', 'admin_user', 'Inserted ResultID:2 Score:78.0'),
('Result', 'INSERT', 'admin_user', 'Inserted ResultID:3 Score:92.0'),
('Result', 'INSERT', 'admin_user', 'Inserted ResultID:4 Score:88.5'),
('Result', 'INSERT', 'admin_user', 'Inserted ResultID:5 Score:76.0');

SELECT * FROM Course;

SELECT * FROM Student;

SELECT * FROM Person;
