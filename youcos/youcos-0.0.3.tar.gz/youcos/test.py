from dotenv import load_dotenv
import os
import time
from scrape_youtube import comments_to_csv, request_videos, request_comments, scrape_comments

def main():
    load_dotenv()
    
    # Authenticate with YouTube API
    KEY = os.environ.get('API_KEY')
    
    query = 'investing'
    
    driver_path = "C:/WebDriver/bin/chromedriver.exe"
    csv_path = "./data/youtube_comments.csv"



    start = time.time()
    comments_to_csv(query,KEY,csv_path=csv_path)
    end = time.time()
    print("time elapsed: ", end - start)

#    video_list = scrape_videos(query, KEY, driver_path=driver_path, maxResults=1)
#    scrape_comments(video_list, driver_path=driver_path, csv_path=csv_path)
   

if __name__ == "__main__":
    main()