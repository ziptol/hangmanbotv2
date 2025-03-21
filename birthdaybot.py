import csv
from datetime import datetime
import os

def ensure_csv_has_header(file_path):
    """Ensure the CSV file has a header row."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['username', 'birthday'])

def check_birthdays(file_path):
    ensure_csv_has_header(file_path)

    today = datetime.now().strftime("%m-%d")
    birthday_people = []

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['birthday'] == today:
                    birthday_people.append(row['username'])
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading birthday file: {e}")

    return birthday_people

def birthday_exists(file_path, username):
    ensure_csv_has_header(file_path)

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'].lower() == username.lower():
                    return True
    except FileNotFoundError:
        # No file means no birthdays yet
        return False
    except Exception as e:
        print(f"Error checking birthday file: {e}")
    return False

def add_birthday(file_path, username, birthday):
    ensure_csv_has_header(file_path)

    # Validate date
    try:
        datetime.strptime(birthday, "%m-%d")
    except ValueError:
        raise ValueError("Invalid date format! Please use MM-DD (e.g., 03-20).")

    # Check for existing username
    if birthday_exists(file_path, username):
        raise ValueError(f"{username} already has a birthday recorded.")

    # Append to CSV
    try:
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, birthday])
    except Exception as e:
        print(f"Error writing to birthday file: {e}")
        raise e
    
def remove_birthday(file_path, username):
    ensure_csv_has_header(file_path)
    found = False
    updated_rows = []

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'].lower() != username.lower():
                    updated_rows.append(row)
                else:
                    found = True

        if not found:
            return False  # Username not found

        # Rewrite file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['username', 'birthday'])
            writer.writeheader()
            writer.writerows(updated_rows)

        return True  # Successfully removed
    except Exception as e:
        print(f"Error removing birthday: {e}")
        raise e

def list_birthdays(file_path):
    ensure_csv_has_header(file_path)

    birthday_list = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                birthday_list.append(f"{row['username']} - {row['birthday']}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading birthday file: {e}")
    return birthday_list