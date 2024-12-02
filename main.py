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

def assign_secret_santa(participants: List[Tuple[str, str]]) -> Dict[str, Tuple[str, str]]:
    """
    Assigns Secret Santa pairs randomly, ensuring no one is assigned to themselves.

    Args:
        participants (List[Tuple[str, str]]): List of participants with their names and emails.

    Returns:
        Dict[str, Tuple[str, str]]: A dictionary where the key is the participant's name,
                                    and the value is a tuple with the assigned name and email.
    """
    names = [p[0] for p in participants]
    emails = {p[0]: p[1] for p in participants}
    assigned = names[:]
    random.shuffle(assigned)

    # Ensure no one is assigned to themselves
    while any(n == a for n, a in zip(names, assigned)):
        random.shuffle(assigned)

    return {n: (a, emails[a]) for n, a in zip(names, assigned)}

def send_email(sender: str, recipient: str, subject: str, body: str) -> None:
    """
    Sends an email using SMTP.

    Args:
        sender (str): Sender's email address.
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
            msg['From'] = sender
            msg['To'] = recipient
            server.sendmail(sender, recipient, msg.as_string())
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

    for participant, (santa, santa_email) in assignments.items():
        email_body = f"""
        Hi {participant},

        You are the Secret Santa for: {santa}. Keep it a secret! 🎅

        Happy gifting!
        """
        # send_email(EMAIL, santa_email, "Secret Santa Assignment", email_body)

if __name__ == '__main__':
    main()
