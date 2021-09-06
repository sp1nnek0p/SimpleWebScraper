from bs4 import BeautifulSoup
import pandas as pd
import requests

url = 'https://realpython.github.io/fake-jobs/'
rq = requests.get(url)
soup = BeautifulSoup(rq.content, 'html.parser')

results = soup.find(id='ResultsContainer')

elements = results.find_all('div', class_='card-content')

# Find only the Python Jobs listed.
python_jobs = results.find_all('h2', string=lambda text: 'python' in text.lower())

print(f"There are {len(python_jobs)} jobs available")
jobs_list = list()
for pj in python_jobs:
    jobs_list.append(pj.text.strip())

python_job_elements = [
    h2.parent.parent.parent for h2 in python_jobs
]

links_list = list()
for job_element in python_job_elements:
    links = job_element('a')
    for link in links:
        link_url = job_element.find_all('a')[1]['href']
        # print(f'Apply: {link_url}\n')
        if not link_url in links_list:
            links_list.append(link_url)

python_company_elements = [
    h3.parent.parent.parent for h3 in python_jobs
]

company_list = list()

for company in python_company_elements:
    comp = company.find('h3', class_='company')
    # print(comp.text.strip())
    company_list.append(comp.text.strip())

python_location_elements = [
    p.parent.parent.parent for p in python_jobs
]

location_list = list()
for location in python_location_elements:
    loc = location.find('p', class_='location')
    # print(loc.text.strip())
    location_list.append(loc.text.strip())

ti_list = list()
co_list = list()
lo_list = list()

for e in elements:
    title = e.find('h2', class_='title')
    company = e.find('h3', class_='company')
    location = e.find('p', class_='location')
    ti_list.append(title.text.strip())
    co_list.append(company.text.strip())
    lo_list.append(location.text.strip())

# Export to Excel Workbook
data = pd.DataFrame({
    "Job title" : jobs_list,
    "Company" : company_list,
    "location" : location_list,
    "Job Link" : links_list
})

all_data = pd.DataFrame({
    "title" : ti_list,
    "company" : co_list,
    "location" : lo_list
})

writer = pd.ExcelWriter('output.xlsx')
data.to_excel(writer, 'Python Jobs')
all_data.to_excel(writer, 'All Jobs')
writer.save()





