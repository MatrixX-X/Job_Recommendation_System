import requests
import json
import csv
import time
import html2text
import re
import os
import random



url = "https://www.naukri.com/jobapi/v3/search"
# params = {
#     "noOfResults": 20,
#     "urlType": "search_by_keyword",
#     "searchType": "adv",
#     "keyword": "data engineer",
#     "pageNo": 1,
#     "k": "data engineer",
#     "seoKey": "data-engineer-jobs",
#     "src": "jobsearchDesk",
#     "latLong": ""
# }

HEADERS_SEARCH = {
    "appid": "109",
    "accept":"application/json",                # This might be required (based on Naukri’s site)
    "accept-language":"en-US,en;q=0.9",
    "clientid":"d3skt0p",
    "content-type":"application/json",
    "gid":"LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
    "nkparam":"plzUjb4e3MtcOg7niUtLT4T9N+7dakrxw+/Fl/noUSve7ZboozSCwpNJJdCZN3tk5iAfHZvC2aA06Mx4RT+6yw==",
    "priority":"u=1, i",
    "referer":"https://www.naukri.com/data-engineer-jobs?k=data%20engineer",
    "sec-ch-ua":"'Chromium';v='136', 'Google Chrome';v='136', 'Not.A/Brand';v='99'",
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"'Windows'",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "systemid": "Naukri",             # Often required
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Cookie":"test=naukri.com; _t_us=68382344; _t_s=direct; _t_r=1030%2F%2F; persona=default; _t_ds=2662f7521748509508-362662f752-02662f752; J=0; _ga=GA1.1.1045481938.1748509509; ak_bmsc=1BEA87FE1F0AC768A495623C5B8B1C80~000000000000000000000000000000~YAAQHtksMTh1IceWAQAAushJGxtVfXW5Y2TGl6nKoOp4ArLpIbqVDbKVpXijonJ9rHmeFuRpE0U8h0AI+uWZL5IirPCnsCu2fY7hOyVBbu4U3e61FO2/PAKZuUZZshuf1ShEmY7NsInzefhFX3nUY152pSnb5vJQOV1DSKMHDHrjQB0iWeA+7aUL5yWcb+YViH2FpzeQMMYhJx0LyROcLRQsR4ljqD0okKSJXo9y+JCbHaw/JohHvHMCAniL6vSUgd3hRb3BbBJpJFlbXUutvebftKUrZJNJ2HwFJpAlQEFPeivOij7sRPFQPTnXbohdbi+45rwuJUYePh+t8MOxut6dsmnNKc6YTlLi37qIUOMMslRhnyL79nLYZcvSlsCm0miPKjDR2ZXRaw6PlrTwX1YqgaYW24HXhlhyh0XbrdQlSmMvKYvvKgSzlVhrb/cjw6LZ5E5ZiKgzkP/JE6HgNOBfvHPQPT5embR67yRqZTXsut2awc8=; _gcl_au=1.1.390230163.1748509510; _ga_T749QGK6MQ=GS2.1.s1748509509^$o1^$g1^$t1748509522^$j47^$l0^$h0; __gads=ID=0f0a2d9475746f09:T=1748509524:RT=1748509524:S=ALNI_MbKJM1bWKFlS9aE67am7HcWXeXxzA; __gpi=UID=00001105bddd8d9c:T=1748509524:RT=1748509524:S=ALNI_MbpfCE8MJSEGU5gqeOKm660Jgnbug; __eoi=ID=9ba87395436b8de6:T=1748509524:RT=1748509524:S=AA-AfjY3skrbCxfNqpCzgGq20XQZ; jd=290525915784; bm_sv=F0B6F453931E225F02F2FC29B8ED1521~YAAQ9PY3F2wxzcKWAQAAMcRVGxumno72PRBefpNDT981QtiUf1MNxzXocPVHZzgeYzVcti+3MduHgoWqGigNvmo/I3AW+BjFtR499IZsePXZNGPvbJNqiOxu/jVjyXQgo5JuTFX7YQtr5Gs9pSD3P79cT/YqYoROMIqzEIhekjDerCFGWLGHlRDhtNb4OhXHUgP3rhXfC1+3d3ioWkvqv/1G4/gnGkBKdpFPErxppz+sY62DnukeT9tu74W/1eXPIA==~1; HOWTORT=ul=1748510294874&r=https%3A%2F%2Fwww.naukri.com%2Fdata-engineer-jobs%3Fk%3Ddata%2520engineer&hd=1748510295091; _ga_K2YBNZVRLL=GS2.1.s1748509509^$o1^$g1^$t1748510295^$j60^$l0^$h0"
}

html_to_text = html2text.HTML2Text()
html_to_text.ignore_links = True
html_to_text.ignore_images = True
html_to_text.body_width = 0

file_path = "naukri_skills_jobs_safe.csv"

def clean_jd_text(raw):
    raw = raw.strip()
    raw = re.sub(r'\n{2,}', '\n', raw)
    return "".join(line.strip() for line in raw.splitlines())

def get_placeholder(placeholders, key):
    for item in placeholders:
        if item.get("type") == key:
            return item.get("label", "N/A")
    return "N/A"

# --- Persistent job ID cache ---
def load_scraped_ids(filepath="scraped_job_ids.txt"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_scraped_id(job_id, filepath="scraped_job_ids.txt"):
    with open(filepath, "a") as f:
        f.write(job_id + "\n")

# scraped_job_ids = set()




# == Software & Engineering
# Software Engineer, Backend Developer, Full Stack Developer, Frontend Developer,  DevOps Engineer, Site Reliability Engineer (SRE), Embedded Systems Engineer, Mobile App Developer

# == Data & AI
# Data Scientist, Data Analyst, Data Engineer, Machine Learning Engineer, NLP Engineer, Business Intelligence (BI) Developer, AI Researcher

# == Cloud & Infrastructure
# Cloud Engineer, AWS Solution Architect, Azure Cloud Engineer, Cloud Security Engineer, System Administrator

# == Testing & QA
# QA Engineer, Automation Test Engineer, Performance Test Engineer

# == Product & Management
# Product Manager, Project Manager, Scrum Master

# == Cybersecurity & Networking
# Cybersecurity Analyst, Network Engineer

# == Analytics & Business
# Business Analyst, Financial Analyst

# --- Skills (limit to 5–10 for safety per run) ---
# skills = [
#     "Data Engineer", "Java Developer"         //DONE
# ]

# skills = [
#     "Full Stack Developer", "Software Engineer", "Backend Developer", "Frontend Developer", "DevOps Engineer", "Site Reliability Engineer", "Embedded Systems Engineer", "Mobile App Developer"        # DONE
#       "Data Scientist", "Data Analyst", "Machine Learning Engineer", "NLP Engineer",  "Business Intelligence (BI) Developer", "AI Researcher",
#       "Cloud Engineer", "AWS Solution Architect", "Azure Cloud Engineer", "Cloud Security Engineer", "System Administrator", "QA Engineer", "Automation Test Engineer", "Performance Test Engineer"
#       
# ]

skills = ["Product Manager", "Project Manager", "Scrum Master"]     # to be executed

def safe_scrape():
    scraped_job_ids = load_scraped_ids()
    write_header = not os.path.exists(file_path)  # Write header only if file doesn't exist
    with open("naukri_skills_jobs_safe.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Skill", "Title", "Company", "Experience", "Salary", "Location", "JD URL", "Full JD", "Job ID", "Required Skills"])

        for skill in skills:
            wrd = skill.lower().replace(" ", "-")
            referer=f"https://www.naukri.com/{wrd}-jobs?k={skill}"

            HEADERS_SEARCH["referer"]=referer

            print(f"\n🔍 Scraping for skill: {skill}")
            for page in range(1, 51):  # 2 pages per skill
                print(f"  📄 Page {page}...")
                params = {
                    "noOfResults": 20,
                    "keyword": skill,
                    "pageNo": page,
                    "urlType": "search_by_keyword",
                    "searchType": "adv",
                    "k": skill,
                    "seoKey": skill.lower().replace(" ", "-") + "-jobs",
                    "src": "jobsearchDesk",
                    "latLong": ""
                }

                try:
                    res = requests.get("https://www.naukri.com/jobapi/v3/search", headers=HEADERS_SEARCH, params=params)
                    if res.status_code != 200:
                        print(f"    ❌ Search API error: {res.status_code}")
                        time.sleep(60)
                        continue
                    jobs = res.json().get("jobDetails", [])
                    
                    if not jobs or not isinstance(jobs, list) or len(jobs) == 0:
                        print(f"    ⛔ No more jobs found on page {page}. Stopping skill.")
                        break  # exit page loop

                    for job in jobs:
                        job_id = job.get("jobId", "")
                        if job_id in scraped_job_ids:
                            continue  # skip duplicate

                        scraped_job_ids.add(job_id)
                        save_scraped_id(job_id)
                        title = job.get("title", "")
                        company = job.get("companyName", "")

                        placeholders = job.get("placeholders", [])

                        experience = get_placeholder(placeholders, "experience")
                        salary = get_placeholder(placeholders, "salary")
                        location = get_placeholder(placeholders, "location")

                        jd_url = job.get("jdURL", "")

                        raw_desc = job.get('jobDescription') or job.get('description') or ""
                        desc = html_to_text.handle(raw_desc)
                        cjd = clean_jd_text(desc)

                        req_skills = job.get('tagsAndSkills')
                        print(f"    ✅ {title} at {company}")

                        writer.writerow([skill, title, company, experience, salary, location, jd_url, cjd, job_id, req_skills])

                        time.sleep(random.uniform(1.5, 2.5))
                except Exception as e:
                    print(f"    ❌ Error: {e}")
                    time.sleep(60)
                time.sleep(random.uniform(5, 10))  # Cooldown after page   

                if page % 10 == 0:
                    print("Long cooldown after 10 pages...")
                    time.sleep(random.uniform(30, 60)) 

            print("  ⏸️ Cooldown before next skill...")
            time.sleep(random.uniform(15, 25))

        print("\n✅ Scraping completed safely! Data saved to 'naukri_skills_jobs_safe.csv'")


# --- Run ---
if __name__ == "__main__":
    safe_scrape()