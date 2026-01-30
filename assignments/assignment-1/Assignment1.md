# Homework 1: Entity-Relationship Modeling for Cloud Storage (Dropbox Lite)

**Objective:** Design an Entity-Relationship (ER) Diagram that captures the core metadata structure of a file storage system.

## Scenario
You are tasked with designing the database schema for "Dropbox Lite." This system tracks who owns what, where files live, and who has access to them.

## Requirements & Constraints
1.  **Users:** Every request to the system includes a `user_id`. You do not need to model authentication, but you must track users to establish ownership and sharing.
2.  **Files & Directories:** * The system must support both files and directories (folders).
    * Files and directories exist in a hierarchy (a directory can contain multiple files and other directories).
    * Files themselves are stored in an external cloud blob store. Your database should only store a `file_id` (a reference to that external system), the filename, and the file size.
3.  **Ownership:** * Every file and directory has exactly **one** owner (a user).
4.  **Sharing:**
    * Users can share individual files with other users.
    * A file can be shared with many users, and a user can have many files shared with them.
    * For this assignment, do not worry about sharing entire directories or "organizational" accounts—focus on user-to-user file sharing.

## Deliverables
1.  **ER Diagram:** Create a diagram showing Entities, Attributes, and Relationships. You may use tools like Google Drawings, Lucidchart, or a clear hand-drawn photo.
2.  **Create Table Statements** Ensure you clearly mark Primary Keys (PK) and Foreign Keys (FK).