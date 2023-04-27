import json

import requests
from bs4 import BeautifulSoup

from utility.constants import Constants
from utility.utils import remove_html_tags

def main():

    def extract():
        
        url = Constants.PARENT_URL.value
        r = requests.get(url, Constants.HEADERS.value)
        soup = BeautifulSoup(r.content, Constants.HTML_PARSER.value)

        data = (soup.find_all(Constants.SCRIPT.value, id=Constants.ID_INITIALS.value))
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

    load(transformed_data)

if __name__ == "__main__":
    main()
