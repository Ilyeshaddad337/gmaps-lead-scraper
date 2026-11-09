from playwright.sync_api import sync_playwright
import re
import pandas as pd
import datetime
import timeit
import sys
OUTPUT_FORMATS = ['csv']


search_result_class = ".Nv2PK.tH5CWc.THOPZb,.Nv2PK.Q2HXcd.THOPZb,.Nv2PK.THOPZb.CpccDe"
profile_class = '.m6QErb.XiKgde'
stop_span = ".HlvSq"

phone_regex =  r'(?:\+?\d{1,3})(?:-*\s*\d){8,12}'
email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
website_link_text = "Accéder au site Web"
cols_to_keep = ['keyword','name','rating', 'phone','website','emails', 'address', 'link']

url = "https://www.google.com/maps/search/"
data = []
if len(sys.argv) < 3:
    print("Usage: python main.py \"<keyword>\" \"dir\"")
    sys.exit(1)

keyword = sys.argv[1]
sub_dir = sys.argv[2]
OUTPUT_FOLDER = 'outputs/' + sub_dir
 
search_query = keyword.replace(" ","+")
print(f"Searching keyword: {keyword}")

run_date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
keyword_dir = keyword.replace(" ", "_")
try:
    import os
    os.makedirs(f"{OUTPUT_FOLDER}/{keyword_dir}", exist_ok=True)
except Exception as e:
    print(f"Error creating output folder: {e}")
out_filename = f"{OUTPUT_FOLDER}/{keyword_dir}/{keyword.replace(" ", "_")}_{run_date}"
print(f"Output will be saved to: {out_filename}")


url += search_query
def save_data(data):
    if not data:
        print("No data to save.")
        return
    df = pd.DataFrame(data)
    if df[df['phone'] != "no phone number"].duplicated(subset=['phone']).any():
        print("No duplicate phone numbers found.")
    else:
        print (df[df['phone'] != "no phone number"].duplicated(subset=['phone']))
    for fmt in OUTPUT_FORMATS:
        
        if fmt == 'json':
            filename = f"{out_filename}.json"
            df.to_json(filename, orient='records', indent=4)
            print(f"Data saved to {filename}")
        elif fmt == 'csv':
            filename = f"{out_filename}.csv"
            df = df[cols_to_keep]
            df.to_csv(filename, index=False)

            filename = f"{out_filename}_phone.csv"
            df = df[df['phone'] != "no phone number"]
            df.to_csv(filename, index=False)            
            print(f"Data saved to {filename}")
    print(f"All data saved successfully to {OUTPUT_FOLDER}/.")

def main():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)

            # Wait for the map to load
            page.wait_for_selector(search_result_class)
            # scroll for more results
            page.query_selector(f"{search_result_class}").hover()
            stop_scrolling = False
            i = 0
            while not stop_scrolling:
                page.mouse.wheel(0, 3000)  # Scroll down
                page.wait_for_timeout(500)
                
                # Check if the stop span is present to indicate no more results
                if page.query_selector(stop_span):
                    print("Reached the end of the results.")
                    stop_scrolling = True
                    print("Stopping the scrolling after ", i, "scrolls.")
                else:
                    i += 1
                    if i>25:
                        print(f"No more results found after {i} scrolls. Stopping.")
                        stop_scrolling = True
                        
                    continue
                
            
            # Extract the restaurant names
            restaurants = page.query_selector_all(f"{search_result_class}")
            print(f"Found {len(restaurants)} results.")
            for restaurant in restaurants:
                resto = {}
                emails = []
                potential_emails = restaurant.query_selector_all("a[href^='mailto:']")
                for email in potential_emails:
                    email_text = email.get_attribute('href')
                    if email_text:
                        email_text = re.sub(r'mailto:', '', email_text)
                        emails.append(email_text)
                resto['keyword'] = keyword
                profile_link = restaurant.query_selector("a")
                if profile_link:
                    profile_url = profile_link.get_attribute("href")
                    resto['name'] = restaurant.inner_text().split('\n')[0]
                    try:
                        resto['rating'] = restaurant.inner_text().split('\n')[1].split(" · ")[0]
                    except Exception:
                        resto['rating'] = "no rating"
                    resto['link'] = profile_url
                    
                    profile_link.click()
                else:
                    print("No profile link found for this restaurant.")
                    continue
                page.wait_for_timeout(1200)  # Wait for the profile to load
                elements = page.query_selector_all(profile_class)
                profile = None
                for element in elements:
                    label = element.get_attribute('aria-label')
                    if not label:
                        continue
                    if "Informations" in label:
                        profile = element
                        
                if profile:
                    # Extract the restaurant name from the profile
                    all_links = profile.query_selector_all("a")
                    potential_emails = profile.query_selector_all("a[href^='mailto:']")
                    for email in potential_emails:
                        email_text = email.get_attribute('href')
                        if email_text:
                            email_text = re.sub(r'mailto:', '', email_text)
                            emails.append(email_text)
                    resto['emails'] = "/".join(emails) if emails else "no emails"
                    website = "no website"
                    for l in all_links:
                        if (l.get_attribute("aria-label") == website_link_text):
                            website = l.get_attribute("href")
                            break
                    resto['website'] = website
                    infos = profile.inner_text()
                    splited = infos.split('\n')
                    if (len(splited) > 1):
                        resto['address'] = splited[1] 
                    resto['phone'] = re.findall(phone_regex, infos)[0] if re.findall(phone_regex, infos) else "no phone number"
                    data.append(resto)
                else:
                    print("Profile not found for the restaurant.")
            browser.close()
            print(f"Found {len(data)} record.")        
            save_data(data)
            
    except Exception as e:
        print(f"An error occurred: {e} at : {keyword}")
start = timeit.default_timer()
print("Starting the scraping process...")
main()
end = timeit.default_timer()
print(f"Scraping completed in {end - start:.2f} seconds.")
