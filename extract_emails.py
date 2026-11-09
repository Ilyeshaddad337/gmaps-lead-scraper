import pandas as pd
import re
from datetime import datetime


def extract_emails_from_text(text, domain=r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"):
    """
    Extracts email addresses from a given text.
    
    Args:
        text (str): The input text from which to extract email addresses.
        
    Returns:
        list: A list of unique email addresses found in the text.
    """
    # Regular expression pattern for matching email addresses
    domain = domain.replace("www.", "")  # Remove 'www.' if present
    domain = domain.lower().strip()
    email_pattern = r'[a-zA-Z0-9._%+-]+@'+domain
    
    # Find all matches in the text
    emails = re.findall(email_pattern, text)
    l = list(set(emails))
    if len(l) == 0:
        return 'info@'+domain  # Default email if none found
    
    # Clean up email addresses by removing any surrounding whitespace
    cleaned_emails = [email.strip() for email in l if email.strip()]
    # Return unique email addresses
    return cleaned_emails[0]

def extract_emails_from_website(website):
    """
    Extracts email addresses from a given website URL.
    
    Args:
        website (str): The URL of the website to scrape for email addresses.
        
    Returns:
        list: A list of unique email addresses found on the website.
    """
    try:
        # Importing requests and BeautifulSoup inside the function to avoid unnecessary imports if not used
        import requests
        from bs4 import BeautifulSoup
        cleaned_website = website.strip().lower().split("?")[0]
        
        domain  = cleaned_website.split("//")[-1].split("/")[0]
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        headers = {'User-Agent': user_agent}
        print(f"Extracting emails from {cleaned_website} ", end=" ")
        response = requests.get(cleaned_website, headers=headers)
        print(f"Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        
        # Extract emails from the text
        emails = extract_emails_from_text(text, domain=domain)
        
        return emails
    except Exception as e:
        print(f"Error extracting emails from {website}: {e}")
        return "info@"+website.split("//")[-1].split("/")[0].replace("www.","")  # Return default email if error occurs


def main ():
    inp_file = input("input the file with the companies website: ")
    df = pd.read_csv(inp_file)  # Load the CSV file
    df['emails']  = df['website'].apply(extract_emails_from_website)  # Extract emails from each website
    df.to_csv(f'leads-w-emails/{inp_file.split("/")[-1]}', index=False)


if __name__ == "__main__":
    start = datetime.now()
    main()
    end = datetime.now()
    print(f"Execution time: {end - start}")
    print("Emails extraction completed.")
