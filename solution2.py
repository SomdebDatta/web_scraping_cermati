import json

import requests
from bs4 import BeautifulSoup

from utility.constants import Constants
from utility.utils import remove_html_tags


def extract():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    url = Constants.PARENT_URL.value
    r = requests.get(url, headers)
    # return r.status_code
    soup = BeautifulSoup(r.content, "html.parser")

    data = (soup.find_all("script", id="initials"))
    return data

def transform(data):
    clean_data = json.loads(data[0].text)

    job_links = [] 
    for job_link in clean_data['smartRecruiterResult']['all']['content']:
        job_links.append(job_link['ref'])
    
    output_json = {}
    for job in job_links:

        r = requests.get(job)
        sample_job = r.json()
        
        for item in sample_job['customField']:
            if item['fieldLabel'] == 'Department':
                department = item['valueLabel']
            elif item['fieldLabel'] == 'Country':
                country = item['valueLabel']

        output_job = {
            "title": sample_job['name'],
            "location": ','.join([sample_job['location']['city'], country]),
            "description": [remove_html_tags(sample_job['jobAd']['sections']['jobDescription']['text'])],
            "qualification": [remove_html_tags(sample_job['jobAd']['sections']['qualifications']['text'])],
            "posted_by": sample_job['creator']['name']
        }

        if department in output_json.keys():
            output_json[department].append(output_job)
        else:
            output_json[department] = [output_job]
    return output_json

def load(output_json):

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=4)

data = extract()

transformed_data = transform(data)
for item in transformed_data:
    print(len(transformed_data[item]))

result = load(transformed_data)
