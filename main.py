import smtplib
import random
from email.mime.text import MIMEText
from typing import List, Tuple, Dict
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# SMTP configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')


def load_participants(file_path: str) -> List[Dict[str, str]]:
    """
    Loads participants from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        List[Dict[str, str]]: List of participants with name and email.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def assign_secret_santa(participants: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """
    Assigns Secret Santa pairs randomly while respecting exclusions,
    ensuring no one is assigned to themselves or to a restricted name.

    Args:
        participants (List[Dict[str, str]]): List of participants, each represented as a dictionary
                                             with 'name', 'email', and 'exclude' keys.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where the key is the participant's name,
                                   and the value is another dictionary with the assigned
                                   'name' and 'email'.
    """
    # Extract names and emails
    names = [p['name'] for p in participants]
    emails = {p['name']: p['email'] for p in participants}
    restrictions = {p['name']: set(p['exclude']) for p in participants}
    assigned = names[:]
    
    # Shuffle until valid assignments are found
    max_attempts = 1000
    for attempt in range(max_attempts):
        random.shuffle(assigned)
        # Check if all assignments are valid
        if all(assigned[i] not in restrictions[names[i]] and assigned[i] != names[i]
               for i in range(len(names))):
            break
    else:
        raise ValueError("Unable to find a valid assignment with the given restrictions.")
    
    # Build the result dictionary
    return {names[i]: {'name': assigned[i], 'email': emails[assigned[i]]} for i in range(len(names))}

def send_email(recipient: str, subject: str, body: str) -> None:
    """
    Sends an email using SMTP.

    Args:
        recipient (str): Recipient's email address.
        subject (str): Email subject line.
        body (str): Email body content.

    Raises:
        Exception: If there is an issue sending the email.
    """
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL
            msg['To'] = recipient
            server.sendmail(EMAIL, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")

def main() -> None:
    """
    Main function to assign Secret Santa pairs and send anonymous emails.
    """

    # Get participants
    participants = load_participants('participants.json')
    if not participants:
        print("No participants found. Please check the .env file.")
        return

    assignments = assign_secret_santa(participants)
    for participant, person_to_send in assignments.items():
        email_subject= "Tu amigo invisible este año 2024 es ..."
        email_body = f"""
        Hola mi vida,

        ¡Qué emoción! Estoy aquí para contarte que este año tu amigo invisible es: {participant} 🎅.

        Recuerda mantenerlo en secreto hasta el día del intercambio, y piensa en algo especial que le saque una sonrisa.

        Buena semanita, mi niño, y coge una rebequita por si refresca,
        Tu organizador del Amigo Invisible 🎄
        """
        santa_email = person_to_send['email']

        send_email(
            recipient = santa_email,
            subject = email_subject,
            body = email_body
        )
        

if __name__ == '__main__':
    main()
