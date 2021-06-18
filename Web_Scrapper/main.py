from bs4 import BeautifulSoup
import requests


def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    url = f'https://in.indeed.com/jobs?q=python+fresher&l=Mumbai%2C+Maharashtra&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup, job_list):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_='company').text.strip()
        try:
            salary_txt = item.find('span', class_='salaryText').text.strip()
        except:
            salary_txt = ''
        summary = item.find('div', class_='summary').text.strip().replace('\n', '')
        link_txt = 'https://in.indeed.com' + item.find('a').get('href')
        job = {'title':title, 'company':company, 'salary':salary_txt, 'summary':summary, 'link':link_txt}
        job_list.append(job)

    print(job_list)


job_list = []
c = extract(0)
transform(c, job_list)










