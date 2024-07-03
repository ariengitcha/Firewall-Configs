import os
import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Environment variables for GitHub and email credentials
GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_TOKEN = os.getenv('GIT_TOKEN')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = 'arien.seghetti@gmail.com'

# Define search queries for different vendors
search_queries = {
    'Fortinet': '"firewall" "FortiOS" extension:conf extension:cfg extension:json',
    'Palo Alto': '"firewall" "PAN-OS" extension:xml extension:cfg extension:json',
    'Check Point': '"firewall" "Check Point" extension:cfg extension:json extension:txt extension:csv',
    'Cisco ASA': '"firewall" "ASA" extension:cfg extension:conf extension:txt',
    'Cisco Firepower': '"firewall" "Firepower" extension:cfg extension:conf extension:json extension:xml',
    'Juniper': '"firewall" "JunOS" extension:conf extension:set extension:xml extension:txt'
}

SEARCH_URL = 'https://api.github.com/search/code'
RESULTS_PER_PAGE = 30  # Maximum allowed by GitHub API

def search_github(query, per_page=RESULTS_PER_PAGE):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'q': query,
        'per_page': per_page,
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params, auth=HTTPBasicAuth(GIT_USERNAME, GIT_TOKEN))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")

def send_email(subject, body, to_email, from_email, from_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    try:
        urls = []
        for vendor, query in search_queries.items():
            results = search_github(query)
            print(f"Total results for {vendor}: {results['total_count']}")
            for item in results['items']:
                repo_url = item['repository']['html_url']
                file_path = item['path']
                file_url = f"{repo_url}/blob/main/{file_path}"
                urls.append(file_url)
                print(f"Vendor: {vendor}, Repository: {repo_url}, File: {file_path}, URL: {file_url}")

        email_body = "\n".join(urls)
        send_email(
            subject="Firewall Config URLs",
            body=email_body,
            to_email=RECIPIENT_EMAIL,
            from_email=EMAIL_ADDRESS,
            from_password=EMAIL_PASSWORD
        )
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
