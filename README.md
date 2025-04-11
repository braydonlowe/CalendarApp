# LearningSuite & Canvas Calendar Integration
BYU Unified Calendar is a tool designed to consolidate class schedules from Learning Suite and Canvas into a single calendar view. By leveraging web scraping and an ICS file URL, the app fetches and syncs course schedules for a single BYU student, ensuring all classes appear in one place for easy access.

## Features
- **Web Scraping Integration** – Extracts class schedule data from **Learning Suite**.  
- **Canvas ICS Sync** – Imports course calendar data from Canvas via an **ICS file URL**.  
- **Unified Calendar View** – Displays all classes in a single interface for better organization.

## **Usage**  
1. Provide your **Canvas ICS file URL**.  
2. The app scrapes **Learning Suite** for additional class data.  
3. View your **complete schedule** in one place.


## **Technologies Used**  
- **Python** (for web scraping and processing)  
- **Selenium** (for Learning Suite scraping)  
- **Requests** (for handling ICS file fetching)  
- **SQLite** for storing calendar data locally.


## ERD Diagram
![Screenshot](Assets/ERD_4-10-25.png)


## **Setup & Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/byu-unified-calendar.git
   cd byu-unified-calendar
   ```
2. Install dependencies:  
   ```bash
   ./install.sh
   ```
3. Run the app:  
   ```bash
   ./calendarApp.sh
   ```

4. Provide your credentials
When running the application, you'll be prompted to enter your Canvas ICS file URL and Learning Suite login credentials (username and password).


## **Usage**
Once the program is running, you'll be prompted to choose an action:
```sh
[1] See Classes
[2] View Assignments Due This Week
[3] Quit
```

1. See Classes – Displays a list of all your classes fetched from Learning Suite and Canvas.

2. View Assignments Due This Week – Displays assignments that are due within the current week.

3. Quit – Exits the program.



## Security Considerations

### 1. **Password Hashing with bcrypt**
   - **Hashing Passwords**: Instead of storing raw passwords in the database, this application hashes user passwords using the **bcrypt** algorithm. bcrypt is a strong cryptographic hash function that includes a **salt** to defend against rainbow table attacks and uses **adaptive hashing** to make brute-force attacks more difficult over time.
   - **Salt Generation**: Each password is salted before hashing, ensuring that even if two users have the same password, their hashed values will be different.
   - **Storing Hashed Passwords**: The application stores the resulting bcrypt hash in the database, **not the raw password**, making it harder for attackers to recover the original passwords even if they gain access to the database.
   
   #### Example of Password Hashing:
   ```python
   import bcrypt

   # Hashing a password
   password = 'user_password_here'
   hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

   # Storing the hashed password in the database
   # (save 'hashed_password' to your database)
   ```

### 2. **User Authentication via bcrypt**
   - **Authentication Process**: When a user attempts to log in, the application compares the provided password with the stored hash in the database using bcrypt’s `checkpw` function. bcrypt takes care of verifying the hash and salt, ensuring that the password is correct without storing the original password.
   
   #### Example of Password Verification:
   ```python
   # Verifying a password
   entered_password = 'user_entered_password'
   stored_hash = 'stored_hash_from_db'  # Fetch this from your database

   if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8')):
       print("Password is correct")
   else:
       print("Invalid password")
   ```

### 3. **CLI User Input and Authentication**
   - **Multiple Users**: The application allows authentication of multiple users from the CLI by accepting **username** and **password** pairs. Each user’s password is hashed individually before storage.
   
   #### Example of the Secure CLI Password Input:
   ```sh
   read -p "Enter your username: " username
   read -s -p "Enter your password: " password
   ```
   The -s and -p allow the user to put in their password without it being shown on the CLI. This allows a smooth transition from the password input to user validation inside of the program.

### 4. **Storing Passwords in the Database**
   - **Database Design**: Passwords are **never** stored in plain text. Instead, the **bcrypt hash** of the password is stored.
   
   #### Example Database Schema:
   ```sql
   CREATE TABLE User (
       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL -- Stored the bcrypt hash here
   );
   ```
   


## **Troubleshooting**
Authentication Failures: If you're unable to log in, double-check your credentials and make sure you're entering the correct Canvas ICS URL.

Data Fetching Issues: If scraping from Learning Suite fails, ensure that the necessary permissions are granted and that the Learning Suite interface has not changed.

## **Contributing**
If you have suggestions, improvements, or find any bugs, feel free to open an issue or submit a pull request. Contributions are welcome!

