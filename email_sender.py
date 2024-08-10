import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import ssl
from markdown2 import Markdown

logger = logging.getLogger(__name__)

def markdown_to_html(markdown_text):
    markdowner = Markdown()
    return markdowner.convert(markdown_text)

def create_html_email(subject, markdown_body):
    html_body = markdown_to_html(markdown_body)
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
            }}
            ol {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>{subject}</h1>
        {html_body}
    </body>
    </html>
    """
    return html_template

def send_email(smtp_settings, subject, body):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{smtp_settings['SMTP_FROM_NAME']} <{smtp_settings['SMTP_FROM']}>"
        msg['To'] = smtp_settings['SMTP_FROM']
        msg['Subject'] = subject

        # Attach both plain text and HTML versions
        text_part = MIMEText(body, 'plain')
        html_part = MIMEText(create_html_email(subject, body), 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)

        context = ssl.create_default_context()

        if smtp_settings['SMTP_PORT'] == 465:
            # Use SMTP_SSL for port 465
            logger.info(f"Connecting to {smtp_settings['SMTP_HOST']}:{smtp_settings['SMTP_PORT']} using SSL")
            with smtplib.SMTP_SSL(smtp_settings['SMTP_HOST'], smtp_settings['SMTP_PORT'], context=context) as server:
                server.set_debuglevel(1)  # Enable debug output
                logger.info(f"Attempting to login with username: {smtp_settings['SMTP_USERNAME']}")
                server.login(smtp_settings['SMTP_USERNAME'], smtp_settings['SMTP_PASSWORD'])
                logger.info("Login successful")
                
                logger.info("Sending email")
                server.send_message(msg)
                logger.info("Email sent successfully")
        else:
            # Use SMTP with STARTTLS for other ports (usually 587)
            logger.info(f"Connecting to {smtp_settings['SMTP_HOST']}:{smtp_settings['SMTP_PORT']}")
            with smtplib.SMTP(smtp_settings['SMTP_HOST'], smtp_settings['SMTP_PORT']) as server:
                server.set_debuglevel(1)  # Enable debug output
                
                if smtp_settings['SMTP_SECURITY'] == 'starttls':
                    logger.info("Initiating STARTTLS")
                    server.starttls(context=context)
                
                logger.info(f"Attempting to login with username: {smtp_settings['SMTP_USERNAME']}")
                server.login(smtp_settings['SMTP_USERNAME'], smtp_settings['SMTP_PASSWORD'])
                logger.info("Login successful")
                
                logger.info("Sending email")
                server.send_message(msg)
                logger.info("Email sent successfully")

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication Error: {str(e)}")
    except smtplib.SMTPConnectError as e:
        logger.error(f"SMTP Connection Error: {str(e)}")
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"SMTP Server Disconnected: {str(e)}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP Error: {str(e)}")
    except ssl.SSLError as e:
        logger.error(f"SSL Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}")
