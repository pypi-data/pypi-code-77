from dotenv import load_dotenv
import os
from scrape_youtube import scrape_videos, scrape_comments

def main():
    load_dotenv()
    
    # Authenticate with YouTube API
    KEY = os.environ.get('API_KEY')
    
    query = 'stocks'
    
    driver_path = "C:/WebDriver/bin/chromedriver.exe"
    csv_path = "data/youtube_comments.csv"


    video_list = scrape_videos(query, KEY, driver_path=driver_path)
    print(video_list)
    scrape_comments(video_list, driver_path=driver_path, csv_path=csv_path)
   

if __name__ == "__main__":
    main()