import re
import sys
import bs4
import json
import time
import timeit
import requests
import argparse
import threading
import numpy as np
import pandas as pd
import concurrent.futures
from newspaper import Article
from datetime import date, timedelta, datetime


def datelist_generator(from_date,to_date,format_output="%d/%m/%Y"):
    dates = []
    step = timedelta(days=1)
    while from_date<=to_date:
        dates.append(from_date.strftime(format_output))
        from_date+=step
    return dates

def reformat_date_to_str(tobe_reformat_date,format_output):
    return tobe_reformat_date.strftime(format_output)


def get_soup(link_url):
    htmltext = requests.get(link_url).text
    soup = bs4.BeautifulSoup(htmltext,'html.parser')
    return soup

def get_max_page(soup):
    max_page = 0
    for element_pagination in soup.find_all(name="a",attrs={"class":"pagination__item itp-pagination"}):
        if re.match(r"\d+",element_pagination.string):
            if max_page<int(element_pagination.string):
                max_page = int(element_pagination.string)
    print(f"max_page: {max_page}")
    return max_page

def get_n_news_perpage(soup):
    return len(soup.find_all("article"))

def collect_urls_perpage(soup,n_news_perpage):
    urls = []
    for l in range(n_news_perpage):
        li_url = soup.find_all("article")[l].find('a').get("href")
        urls.append(li_url)
    return urls

def get_urls_task(page_i,keyword,from_date,to_date):
    template_i = f"https://www.detik.com/search/searchnews?query={keyword}&page={page_i}&result_type=relevansi&siteid=3&fromdatex={from_date}&todatex={to_date}"    
    soup_i = get_soup(template_i)
    n_news_perpage = get_n_news_perpage(soup_i)
    urls = collect_urls_perpage(soup_i,n_news_perpage)
    urls = list(set(urls))
    return urls

def detik_page_url_generator(from_date:str,to_date:str,keyword:str):
    """
    - one keyword
    - format from_data and to_date in string 'dd/mm/yyyy'
    """
    page=1
    template = f"https://www.detik.com/search/searchnews?query={keyword}&page={page}&result_type=relevansi&siteid=3&fromdatex={from_date}&todatex={to_date}"
    soup = get_soup(template)
    max_page = get_max_page(soup)
    
    # asynchronous
    start_time = timeit.default_timer()
    semaphore = threading.BoundedSemaphore(4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_task = [executor.submit(get_urls_task, page_i=page_i,keyword=keyword,from_date=from_date,to_date=to_date) for page_i in range(1,max_page+1)] 
        result_task = [future.result() for future in concurrent.futures.as_completed(future_task)]
    end_time = timeit.default_timer()
    urls_all = []
    for urls_perpage in result_task:
        urls_all.extend(urls_perpage)
    urls_all = list(set(np.array(urls_all)))
    print(f"Finished collect all url, total : {len(urls_all)}, {end_time - start_time:.2f}s")
    return urls_all

def get_news(url):
    article = Article(f'{url}','id')
    article.download()
    article.parse()
    authors = ", ".join(article.authors)
    title = article.title
    publish_date = article.publish_date.strftime("%Y-%m-%d %H:%M")
    meta_site_name = article.meta_site_name
    meta_description = article.meta_description
    meta_keywords = ", ".join(article.meta_keywords)
    text = title+'\n'+article.text
    news_dict = {
            "authors" : authors,
            "title" : title,
            "publish_date" : publish_date,
            "meta_site_name" : meta_site_name,
            "meta_description" : meta_description,
            "meta_keywords" : meta_keywords,
            "text" : text,
        }
    return news_dict

def get_all_news(urls):
    start_time = timeit.default_timer()
    semaphore = threading.BoundedSemaphore(4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_task = [executor.submit(get_news, url=url) for url in urls] 
        result_task = [future.result() for future in concurrent.futures.as_completed(future_task)]
    end_time = timeit.default_timer()
    news_all = []
    for news in result_task:
        news_all.extend([news])
    print(f"Finished collect all news, total : {len(news_all)}, {end_time - start_time:.2f}s")
    return news_all

def list_of_strings(arg):
    return arg.split(',')

if __name__ == "__main__":
    st = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--from_date", required=True, type=str)
    parser.add_argument("--to_date", required=True, type=str)
    parser.add_argument('--keyword', required=True, type=list_of_strings)
    args = parser.parse_args()

    from_date = args.from_date
    to_date = args.to_date
    keywords = args.keyword

    all_keywords_urls_list = []
    for keyword in keywords:
        print(f"/============/{keyword}/============/")
        urls_keyword = detik_page_url_generator(from_date=from_date,to_date=to_date,keyword=keyword)
        all_keywords_urls_list.extend(urls_keyword)

    print(f"Total URL: {len(all_keywords_urls_list)}")

    uniq_urls = list(set(all_keywords_urls_list))
    print(f"Unique url collected: {len(uniq_urls)}")

    list_of_dict = get_all_news(uniq_urls)
    df_news = pd.DataFrame(list_of_dict)
    df_news = df_news.drop_duplicates().reset_index(drop=True)
    df_news.to_parquet('detiknews.parquet',engine='fastparquet')
    print(f"/============/ Finished scraping news, rt:{time.time()-st}s /============/")

