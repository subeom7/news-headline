import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_main_news_titles(soup):
    main_titles = soup.find_all('div', {'class': 'tv_special_tx'})
    return [title.find('p').get_text() for title in main_titles]

def get_news_titles(url):
    res = requests.get(url)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'lxml')
    
    main_titles = get_main_news_titles(soup)
    
    titles = soup.find('div', {'class': 'tv_newslist __persist_content'}).find_all('strong')
    other_titles = [title.get_text() for title in titles]
    
    return main_titles + other_titles

def main():
    sbs_url = "https://media.naver.com/tv/055"
    kbs_url = "https://media.naver.com/tv/056"
    mbc_url = "https://media.naver.com/tv/214"
    
    file_name = datetime.now().strftime('%Y-%m-%d') + '.txt'
    
    all_titles = []
    
    sbs_titles = get_news_titles(sbs_url)
    all_titles.append(("SBS", sbs_titles))
    
    kbs_titles = get_news_titles(kbs_url)
    all_titles.append(("KBS", kbs_titles))

    mbc_titles = get_news_titles(mbc_url)
    all_titles.append(("MBC", mbc_titles))

    with open(file_name, 'w', encoding='utf-8') as f:
        for channel, titles in all_titles:
            f.write(f"● {channel}\n")
            for i, title in enumerate(titles, 1):
                f.write(f"{i}. {title}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
