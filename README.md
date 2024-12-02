# 🎅 Secret Santa Organizer with Email Notifications

This Python program organizes a **Secret Santa** exchange and sends personalized email notifications to each participant, including the name of their assigned recipient, all while keeping it a secret! 🎁

## Features
- 📋 **Customizable Participants List**: Load participants from a JSON file, including their names, email addresses, and restrictions (e.g., who they cannot be assigned to).
- 🔒 **Respects Exclusions**: Ensures participants are not assigned to themselves or anyone on their exclusion list.
- 📤 **Anonymous Email Notifications**: Sends personalized emails to each participant using an SMTP server.
- ✅ **Randomized Assignments**: Uses a robust algorithm to randomize assignments while adhering to restrictions.

## Requirements
- Python 3.8+
- SMTP credentials for sending emails (e.g., Gmail, Outlook, or custom SMTP server).

## Usage
1. Add your participants to a `participants.json` file:
```json
   [
       {"name": "John", "email": "john@example.com", "exclude": ["Jane"]},
       {"name": "Jane", "email": "jane@example.com", "exclude": ["John", "Alice"]},
       {"name": "Alice", "email": "alice@example.com", "exclude": []}
   ]
```

2. Configure your `.env` file with your SMTP settings:
```
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    EMAIL=your_email@gmail.com
    PASSWORD=your_app_password
```

3. Run the program:
```
   python secret_santa.py
```

4. Each participant will receive an email with the name of their assigned recipient.

## Example Email
```
    Subject: Secret Santa Assignment 🎄

    Hi John,

    Exciting news! This year, your Secret Santa recipient is: **Alice** 🎅.

    Remember to keep it a secret and think of something special to make their day!

    Best wishes,
    Your Secret Santa Organizer
```

## Notes
Ensure your SMTP server allows external applications to send emails. For Gmail, you may need to enable app passwords or less secure apps.

## License
This project is licensed under the MIT License.