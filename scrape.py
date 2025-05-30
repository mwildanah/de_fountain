import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#extracting data from tokopedia
def scroll_down_to_bottom(driver):
    SCROLL_PAUSE_TIME = 3.0
    last_height = driver.execute_script("return document.body.scrollHeight")
    i = 400
    while True:
        time.sleep(0.2)
        driver.execute_script(f"window.scrollTo(0, {i});")
        new_height = driver.execute_script("return document.body.scrollHeight") 

        i += 500
        if i > new_height:
            break

def scrape_page(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Wait until the main content is loaded (adjust selector accordingly)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-bk6tzz")))

    # Scroll down until the bottom of the page
    scroll_down_to_bottom(driver)

    # Wait for a few seconds to ensure lazy-loaded content has loaded
    time.sleep(1.0)

    # Get the HTML content after scrolling
    html = driver.page_source
    driver.quit()
    return html

#should updated with better code
def main(page,subcat):
    url = 'https://www.tokopedia.com/p/pertukangan/material-bangunan/{}?page={}'.format(subcat,page)
    html_response = scrape_page(url)

    # Load HTML Response Into BeautifulSoup
    soup = BeautifulSoup(html_response, "html.parser")

    lst = []
    for item in soup.find_all("div", class_="css-bk6tzz"):
        try:
            nama_produk = item.find_all("span", class_="css-20kt3o")[0].text
            harga = item.find_all("span", class_="css-o5uqvq")[0].text.replace('Rp', '').replace('.', '')
            kota = item.find_all("span", class_="css-ywdpwd")[0].text
            toko = item.find_all("span", class_="css-ywdpwd")[1].text

            get_rating_produk = item.find_all("div", class_="css-1riykrk")
            rating_produk = len(get_rating_produk[0].select('.css-177n1u3'))
            rating_text = get_rating_produk[0].find('span').text
            terjual = int(''.join(filter(str.isdigit, rating_text)))
            url_produk = item.find_all("a", class_="css-54k5sq")[0].get('href')

            lst.append({'nama_produk': nama_produk,
                        'harga': harga,
                        'kota': kota,
                        'toko': toko,
                        'rating_produk': rating_produk,
                        'terjual': terjual,
                        'url_produk': url_produk})
        except:
            pass
    print('get {} items'.format(len(lst)))
    return lst

def main1(page,subcat):
    url = 'https://www.tokopedia.com/p/pertukangan/cat-perlengkapan/{}?page={}'.format(subcat,page)
    html_response = scrape_page(url)

    # Load HTML Response Into BeautifulSoup
    soup = BeautifulSoup(html_response, "html.parser")

    lst = []
    for item in soup.find_all("div", class_="css-bk6tzz"):
        try:
            nama_produk = item.find_all("span", class_="css-20kt3o")[0].text
            harga = item.find_all("span", class_="css-o5uqvq")[0].text.replace('Rp', '').replace('.', '')
            kota = item.find_all("span", class_="css-ywdpwd")[0].text
            toko = item.find_all("span", class_="css-ywdpwd")[1].text

            get_rating_produk = item.find_all("div", class_="css-1riykrk")
            rating_produk = len(get_rating_produk[0].select('.css-177n1u3'))
            rating_text = get_rating_produk[0].find('span').text
            terjual = int(''.join(filter(str.isdigit, rating_text)))
            url_produk = item.find_all("a", class_="css-54k5sq")[0].get('href')

            lst.append({'nama_produk': nama_produk,
                        'harga': harga,
                        'kota': kota,
                        'toko': toko,
                        'rating_produk': rating_produk,
                        'terjual': terjual,
                        'url_produk': url_produk})
        except:
            pass
    print('get {} items'.format(len(lst)))
    return lst

if __name__ == "__main__":
    start_time = time.time()
    df = pd.DataFrame()
    df_eval = pd.DataFrame()
    material_bangunan = ['asbes','baja','batako','batu','batu-bata','besi','beton','engsel','gagang-pintu','gembok','genteng','granit','grendel','jendela','kaca','kawat','kayu','keramik-lantai','kusen-pintu','lantai-kayu','paku','pasir','semen','tanah','triplek']
    data_list = []
    for n,subcat in enumerate(material_bangunan):
        print('crawling {}/{} subcategory material bangunan'.format(n+1, len(material_bangunan)))
        for page in range(1,6):            
            print('crawling {} page {} ...'.format(subcat, page))
            result = main(page,subcat)
            df_temp = pd.DataFrame(result)
            df_temp['subcat'] = subcat
            df = pd.concat([df,df_temp])

            ##eval
            data_list.append({'subcat': subcat,
                        'page': page,
                        'item_found': len(result),
                        'get_date': time.strftime('%Y-%m-%d')})
    df_eval = pd.DataFrame(data_list)
    df.to_csv('/data/result_crawl_{}_material_bangunan.csv'.format(time.strftime('%Y_%m_%d_%H_%M_%S')),index=False)
    df_eval.to_csv('/data/evaluation_subcat_{}_material_bangunan.csv'.format(time.strftime('%Y_%m_%d_%H_%M_%S')),index=False)
    print("data material bangunan for {} is done".format(time.strftime('%Y_%m_%d')))
    print("--- %s minutes processing time ---" % (int(time.time() - start_time)/60))

    start_time = time.time()
    df = pd.DataFrame()
    material_bangunan = ['cat-kayu','cat-pelapis','cat-semprot','cat-tembok','kuas-cat','plamir','roller-cat','thinner','wallpaper']
    data_list = []
    for n,subcat in enumerate(material_bangunan):
        print('crawling {}/{} subcategory cat'.format(n+1, len(material_bangunan)))
        for page in range(1,6):
            print('crawling {} page {} ...'.format(subcat, page))
            result = main1(page,subcat)
            df_temp = pd.DataFrame(result)                 
            df_temp['subcat'] = subcat
            df = pd.concat([df,df_temp])

            ##eval
            data_list.append({'subcat': subcat,
                        'page': page,
                        'item_found': len(result),
                        'get_date': time.strftime('%Y-%m-%d')})
    df_eval = pd.DataFrame(data_list)
    df.to_csv('/data/result_crawl_{}_cat.csv'.format(time.strftime('%Y_%m_%d_%H_%M_%S')),index=False)
    df_eval.to_csv('/data/evaluation_subcat_{}_cat.csv'.format(time.strftime('%Y_%m_%d_%H_%M_%S')),index=False)
    print("data cat for {} is done".format(time.strftime('%Y_%m_%d')))
    print("--- %s minutes processing time ---" % (int(time.time() - start_time)/60))
