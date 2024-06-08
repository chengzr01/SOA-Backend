import json

import requests
from bs4 import BeautifulSoup

from backend.models import Job

'''
this function will be called by the main function
it will take the url as an argument
'''
def entry(url, start_page = 1, end_page = None):
    # if url is metacareers.com/jobs/
    if url == 'metacareers.com/jobs/':
        pass
    elif url.startswith('https://www.google.com/about/careers/applications/jobs/results/'):
        return googlecareers(url)


def googlecareers(url, save = True, start_page = 1, end_page = None):
    # URL of the website to scrape
    base_url = "https://www.google.com/about/careers/applications/jobs/results/"
    has_next_page = True
    page_number = start_page
    num_records_inserted = 0
    while has_next_page:
        if (end_page is not None) and (page_number > end_page):
            break
        print("-" * 20, "Scraping page ", page_number, "-" * 20)
        url = base_url + f"?page={page_number}"
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        assert response.status_code == 200


        # print(soup.prettify())
        # Find and extract job listings
        job_listings = soup.find_all("div", class_ = "sMn82b")

        for job in job_listings:
            try:
                location = job.find("span", class_="r0wTof").text.strip()
            except AttributeError:
                location = "Not specified"
            try:
                level = job.find("span", class_ = "wVSTAb").text.strip()
            except AttributeError:
                try:
                    level = job.find("span", class_ = "RP7SMd").find("span").text.strip()
                except:
                    level = "Not specified"
            try:
                corporate = job.find("span", class_ = "RP7SMd").find("span").text.strip()
            except:
                corporate = "Not specified"
            try:
                uls = job.find("ul")
                requirements = [li.get_text() for li in uls.find_all('li')]
            except:
                requirements = "Not specified"
            job_title = job.find("h3").text.strip()
            if save:
                    # Create a new JobListing object and save it to the database
                job_listing = Job(
                    location=location,
                    job_title=job_title,
                    level=level,
                    corporate = corporate,
                    requirements = json.dumps(requirements)
                )
                job_listing.save()
                # Insert the job listing into the database
                # cursor.execute('''INSERT INTO job_listings (location, job_title, level, corporate, requirements)
                #         VALUES (?, ?, ?, ?, ?)''', (location, job_title, level, corporate, json.dumps(requirements)))
                num_records_inserted += 1
            # print("Location:", location)
            # print("Job Title:", job_title)
            # print("Level:", level)
            # print("Corperate:", corperate)
            # print("Requirements:", requirements)
        
            # print("-" * 50)
        # if save:
            # print("Number of records inserted:", num_records_inserted)
            # conn.commit()
            # num_records_inserted = 0
            
        
        next_button = soup.find_all("a", class_="WpHeLc VfPpkd-mRLv6")[-1]
        has_next_page = next_button is not None
        # If there is a next page, update the URL to scrape the next page
        if has_next_page:
            page_number += 1
            url = base_url + next_button['href'].split("/")[-1]
            print(url)
            print("going to next page")
            print("-" * 50)
    # if save:
    #     # Close the connection to the database after crawling
    #     conn.close()
        
# entry("https://www.google.com/about/careers/applications/jobs/results/")
# test case
# job = Job(location="Mountain View, CA, USA", job_title="Software Engineer", level="Entry level", corporate="Google", requirements=json.dumps(["BS in Computer Science or equivalent", "Experience in software development", "Experience with Python, Java, or C++"]))
# job.save()
