import re

# Step 1: Read the emails.txt file
with open("emails.txt", "r") as file:
    content = file.read()

# Step 2: Split by delimiter '---'
raw_emails = [email.strip() for email in content.split('---') if email.strip()]

# Step 3: Regex patterns
from_pattern = re.compile(r"From:\s*(.+)")
subject_pattern = re.compile(r"Subject:\s*(.+)")
body_pattern = re.compile(r"Body:\s*(.+)")

# Step 4: Spam keywords
spam_keywords = ["win", "free", "prize", "click here"]

emails_data = []

# Step 5: Parse each email
for raw_email in raw_emails:
    sender = from_pattern.search(raw_email).group(1) if from_pattern.search(raw_email) else ""
    subject = subject_pattern.search(raw_email).group(1) if subject_pattern.search(raw_email) else ""
    body = body_pattern.search(raw_email).group(1) if body_pattern.search(raw_email) else ""

    # Spam detection (case-insensitive)
    spam_flag = any(keyword.lower() in (subject + " " + body).lower() for keyword in spam_keywords)

    emails_data.append({
        "from": sender,
        "subject": subject,
        "body": body,
        "is_spam": spam_flag
    })

# Step 6: Stats
total_emails = len(emails_data)
spam_count = sum(email["is_spam"] for email in emails_data)
non_spam_count = total_emails - spam_count

# Step 7: Write email_report.txt
with open("email_report.txt", "w") as report:
    report.write(f"Total Emails: {total_emails}\n")
    report.write(f"Spam Emails: {spam_count}\n")
    report.write(f"Non-Spam Emails: {non_spam_count}\n\n")
    report.write("=== Spam Emails ===\n")
    for email in emails_data:
        if email["is_spam"]:
            report.write(f"From: {email['from']}\nSubject: {email['subject']}\n\n")

# Step 8 (Bonus): Write clean_emails.txt (non-spam)
with open("clean_emails.txt", "w") as clean_file:
    for email in emails_data:
        if not email["is_spam"]:
            clean_file.write(f"From: {email['from']}\n")
            clean_file.write(f"Subject: {email['subject']}\n")
            clean_file.write(f"Body: {email['body']}\n")
            clean_file.write("---\n")

print("Processing complete. Check 'email_report.txt' and 'clean_emails.txt'.")
