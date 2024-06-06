import html
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

app = FastAPI()


# Define a Pydantic model for the email data
class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str


# Email sending function
def send_email(email: EmailStr, subject: str, body: str, username, reset_link):
    sender_email = "atifahmad2219@gmail.com"
    sender_password = "******"
    receiver_email = email
    subject = "Password Reset Request"
    html_content = f"""
    <html>
    <body>
        <h2>Hello, {username}</h2>
        <p>You requested to reset your password. Click the link below to reset it:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>If you did not request a password reset, please ignore this email.</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html_content, "html"))
    # Send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to send email
@app.post("/send-email/")
async def send_email_endpoint(email_data: EmailSchema):
    try:
        # Validate email
        validate_email(email_data.email)
        # Send email
        send_email(
            email_data.email,
            email_data.subject,
            email_data.body,
            "Atif Ahmed",
            "https://click-here",
        )
        return {"message": "Email has been sent successfully"}
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
