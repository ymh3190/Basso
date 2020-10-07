import requests
from bs4 import BeautifulSoup

URL = "http://www.saramin.co.kr/zf_user/search/recruit?searchword=python&recruitPageCount=100&recruitPage="

# 총 페이지 수를 반환합니다.
def get_last_page():
    result = requests.get(f"{URL}1")
    soup = BeautifulSoup(result.text, "html.parser")
    links = soup.find("div", {"class": "pagination"}).find_all("a")

    if links[-1]["title"] == "다음":
        result = requests.get(f"{URL}11")
        soup = BeautifulSoup(result.text, "html.parser")
        pages = soup.find("div", {"class": "pagination"}).find_all("span")
        last_page = int(pages[-1].string)
    else:
        result = requests.get(f"{URL}1")
        soup = BeautifulSoup(result.text, "html.parser")
        pages = soup.find("div", {"class": "pagination"}).find_all("span")
        last_page = int(pages[-1].string)
    return last_page

def extract_job(html):
    title = html.find("h2").find('a')["title"]
    company = html.find("strong").find('a')["title"]
    job_conditions = html.find("div", {"class": "job_condition"}).find("span").find_all('a')
    location = None
    if len(job_conditions) == 1:
        location = job_conditions[0].string
    elif len(job_conditions) == 2:
        location = f"{job_conditions[0].string} {job_conditions[1].string}"
    else:
        location = "None"
    rec_idx = html.find("div", {"class": "toolTipWrap wrap_scrap"}).find('a')["rec_idx"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={rec_idx}"
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}{page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
