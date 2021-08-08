from bs4 import BeautifulSoup
import requests
import time

print('What are the skills you\'re not familiar with?')
print('When you\'re done, press ENTER:')
unfamiliar_skills = []
skill = input('>>')
while(skill != ''):
    unfamiliar_skills.append(skill)
    skill = input('>>')

print(f'Filtering out {unfamiliar_skills} from job search')


def find_jobs(f, version):
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")
    for job in jobs:
        published_date = job.find('span', class_="sim-posted").span.text.strip()
        if 'few' in published_date:
            company_name = job.find('h3', class_="joblist-comp-name").text.replace(' ', '').strip()
            skills_needed = job.find('span', class_="srp-skills").text.replace(' ', '').strip()

            skills = skills_needed.split(',')
            if(len(set(skills) & set(unfamiliar_skills)) == 0):

                # the link to the full-description of the job is under header-->h2-->a tag
                # with the link being under the "href"
                more_info = job.header.h2.a['href']

                # put the job information every 30 min in a .txt file
                # formatted as jobs_version{version}.txt
                f.write(f"Company Name: {company_name} \n")
                f.write(f"Required Skills: {skills_needed} \n")
                f.write(f"More Information: {more_info} \n")
                f.write('\n')

    print(f'File Saved: jobs_version{version}.txt')


if __name__ == "__main__":
    version = 1
    while True:
        with open(f'jobs_pool/jobs_version{version}.txt', 'w') as f:
            find_jobs(f, version)
        # run every 30 minutes
        sleep_time = 30
        print(f"Waiting for {sleep_time} minutes ...")
        time.sleep(sleep_time * 60)
        version += 1