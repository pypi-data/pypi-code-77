from google_play_scraper import app

result = app(
    'com.flowy.mobile',
    lang='es', # defaults to 'en'
    country='mx' # defaults to 'us'
)

# url = "https://play.google.com/store/apps/details?id=com.flowy.mobile&hl=en"
def scrape():
  result = app(
    'com.flowy_mobile',
    lang='es', # defaults to 'en'
    country='mx' # defaults to 'us'
  )
  # page = requests.get(url) 
  # soup = BeautifulSoup(page.content, 'html.parser')
  # job_elems = soup.find('div', class_='hAyfc').find('div', class_='BgcNfc').text
  # page = urlopen(url)
  # html_bytes = page.read()
  # html = html_bytes.decode("utf-8")
  # title_index = html.find("<title>")
  
  return result['version']