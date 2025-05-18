import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os

def read_existing_data(csv_filename):
    existing_links = set()
    existing_texts = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_links.add(row['link'])
                existing_texts.add(row['text'])
    return existing_links, existing_texts

csv_filename = 'dawn_editorials.csv'

existing_links, existing_texts = read_existing_data(csv_filename)

cookies = {
    'scribe': 'true',
    '_ga': 'GA1.1.1907201366.1747025023',
    '__gads': 'ID=8193cd20350546c0:T=1747024929:RT=1747030567:S=ALNI_MZyDE_fRNePC-V5sCy5dTYTqaHBug',
    '__gpi': 'UID=000010a9f0ab5eb2:T=1747024929:RT=1747030567:S=ALNI_MZaW1gQKpV_vcx866eAHVljS1tbmg',
    '__eoi': 'ID=8ad4ba78019cac91:T=1747024929:RT=1747030567:S=AA-AfjaK941aa8UTJ2oKY9fyw8QZ',
    'consent_visits': '22',
    'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CQRTEQAQRTEQAEsACBENBqFoAP_gAEPgAB5QJ1JD7C7FbSFCyD5zaLsAcAhHRsAAYoQAAASBAmABQAKQIAQCgkAYFASgBAACAAAAICRBIQMECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmAgAAIIACAAAgAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAABAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBOpIPYXYraQoWQcKbBdgBgEK6NgADFCAAACQIEwAKABSBACAUkgCAIgUAAAAAAAABASIJAAhAAEAAAgAKAAAAAAAgAAAAAABBAAAEAAgAAAAAAAAQBAAAgABAAAAAgAAESEAABBAAQAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAA%22%2C%222~55.70.89.93.108.122.149.184.196.236.259.311.313.314.323.358.415.442.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%22BD5AF29E-8C02-474C-9BDC-721CB9E55FCC%22%5D%5D',
    'FCNEC': '%5B%5B%22AKsRol_5ApDZrSuQA-22eDCLNop0IxRaXuVxN2KtReQ3Nb2wM1Sc9gnh4NX_etmDHS9e5IROH6HiiIJc2CVaoKhPMJ7YjPyTBCxF1MnP7nqWUNhMLj-SZlu5ZylobTpzYT_JIVk0GfPvPBN51M8P4oeaUdgX1e6lCg%3D%3D%22%5D%5D',
    '_ga_C521GRS8DF': 'GS2.1.s1747025022$o1$g1$t1747030716$j46$l0$h10443523',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.dawn.com/newspaper/editorial',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'scribe=true; _ga=GA1.1.1907201366.1747025023; __gads=ID=8193cd20350546c0:T=1747024929:RT=1747030567:S=ALNI_MZyDE_fRNePC-V5sCy5dTYTqaHBug; __gpi=UID=000010a9f0ab5eb2:T=1747024929:RT=1747030567:S=ALNI_MZaW1gQKpV_vcx866eAHVljS1tbmg; __eoi=ID=8ad4ba78019cac91:T=1747024929:RT=1747030567:S=AA-AfjaK941aa8UTJ2oKY9fyw8QZ; consent_visits=22; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CQRTEQAQRTEQAEsACBENBqFoAP_gAEPgAB5QJ1JD7C7FbSFCyD5zaLsAcAhHRsAAYoQAAASBAmABQAKQIAQCgkAYFASgBAACAAAAICRBIQMECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmAgAAIIACAAAgAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAABAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBOpIPYXYraQoWQcKbBdgBgEK6NgADFCAAACQIEwAKABSBACAUkgCAIgUAAAAAAAABASIJAAhAAEAAAgAKAAAAAAAgAAAAAABBAAAEAAgAAAAAAAAQBAAAgABAAAAAgAAESEAABBAAQAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAA%22%2C%222~55.70.89.93.108.122.149.184.196.236.259.311.313.314.323.358.415.442.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%22BD5AF29E-8C02-474C-9BDC-721CB9E55FCC%22%5D%5D; FCNEC=%5B%5B%22AKsRol_5ApDZrSuQA-22eDCLNop0IxRaXuVxN2KtReQ3Nb2wM1Sc9gnh4NX_etmDHS9e5IROH6HiiIJc2CVaoKhPMJ7YjPyTBCxF1MnP7nqWUNhMLj-SZlu5ZylobTpzYT_JIVk0GfPvPBN51M8P4oeaUdgX1e6lCg%3D%3D%22%5D%5D; _ga_C521GRS8DF=GS2.1.s1747025022$o1$g1$t1747030716$j46$l0$h10443523',
}


base_url = 'https://www.dawn.com/newspaper/editorial'
response = requests.get(base_url, cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

articles = soup.find_all('article')

data_list = []

for article in articles:
    title_tag = article.find("a", class_="story__link")
    if not title_tag:
        continue

    link = title_tag['href']
    title = title_tag.text.strip()

    if link in existing_links:
        print(f"Duplicate found, skipping: {title}")
        continue

    data = {
        'country': 'Pakistan',
        'source': 'Dawn',
        'type': 'Editorial',
        'title': title,
        'link': link,
        'published_date': '',
        'published_by': 'Dawn',
        'description': '',
        'text': ''
    }

    desc_tag = article.find("div", class_="story__excerpt")
    if desc_tag:
        data['description'] = desc_tag.text.strip()

    try:
        page_response = requests.get(link, cookies=cookies, headers=headers)
        page_soup = BeautifulSoup(page_response.text, 'html.parser')

        time_tag = page_soup.find('span', class_="timestamp--published")
        if not time_tag:
            continue

        raw_date = time_tag.text.strip().replace('Published', '').strip()
        data['published_date'] = raw_date

        try:
            pub_date = datetime.strptime(raw_date, "%B %d, %Y")
            if pub_date < datetime.today() - timedelta(days=5):
                print(f"Skipping old article: {title} ({raw_date})")
                continue
        except Exception as e:
            print(f"Date parse error for {title}: {e}")
            continue

        text_tags = page_soup.find_all('p')
        if len(text_tags) > 4:
            content = [p.text.strip() for p in text_tags[1:-4]]
        else:
            content = [p.text.strip() for p in text_tags]

        article_text = ' '.join(content)
        if article_text in existing_texts:
            print(f"Duplicate text found, skipping: {title}")
            continue

        data['text'] = ' '.join(content)

        data_list.append(data)
        existing_links.add(link)

    except Exception as e:
        print(f"Error fetching {link}: {e}")
        continue

if data_list:
    fieldnames = data_list[0].keys()
    with open(csv_filename, 'a', newline='', encoding='utf-8') as f:  # Use 'a' to append
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:  # Write header only if file is empty
            writer.writeheader()
        writer.writerows(data_list)
    print(f"\nSaved {len(data_list)} new articles to '{csv_filename}'")
else:
    print("No new articles to save.")