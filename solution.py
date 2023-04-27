"""Central module."""
import concurrent.futures
import json

import requests
from bs4 import BeautifulSoup

from utility.constants import Constants
from utility.utils import remove_html_tags


def main() -> None:
    """This is the main orchestrator function."""
    job_links = []
    all_jobs = {}

    def extract() -> None:
        """
        Extraction function.
        This function explores the home link dynamically to go to the Jobs page.
        Then it appends all the jobs' links to a list.
        """
        url = Constants.PARENT_URL.value
        r = requests.get(url, Constants.HEADERS.value)
        soup = BeautifulSoup(r.content, Constants.HTML_PARSER.value)

        data = soup.find_all(Constants.SCRIPT.value, id=Constants.ID_INITIALS.value)

        clean_data = json.loads(data[0].text)

        for job_link in clean_data["smartRecruiterResult"]["all"]["content"]:
            job_links.append(job_link["ref"])

    def transform(job) -> None:
        """
        Transform function.
        This function parses one job link at a time and curates the data in the required
        format.
        """
        r = requests.get(job)
        sample_job = r.json()

        for item in sample_job["customField"]:
            if item["fieldLabel"] == "Department":
                department = item["valueLabel"]
            elif item["fieldLabel"] == "Country":
                country = item["valueLabel"]

        job_output = {
            "title": sample_job["name"],
            "location": ",".join([sample_job["location"]["city"], country]),
            "description": [
                remove_html_tags(
                    sample_job["jobAd"]["sections"]["jobDescription"]["text"]
                )
            ],
            "qualification": [
                remove_html_tags(
                    sample_job["jobAd"]["sections"]["qualifications"]["text"]
                )
            ],
            "posted_by": sample_job["creator"]["name"],
        }

        if department in all_jobs.keys():
            all_jobs[department].append(job_output)
        else:
            all_jobs[department] = [job_output]

    def load(output_json) -> None:
        """
        Load Function.
        This function writes the scraped data into a json file and saves it.
        """
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4)

    extract()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(transform, job_links)

    load(all_jobs)


if __name__ == "__main__":
    main()