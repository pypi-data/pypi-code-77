# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['top_github_scraper']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'pandas>=1.2.2,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.12.0,<10.0.0']

setup_kwargs = {
    'name': 'top-github-scraper',
    'version': '0.1.0.5',
    'description': 'Scrape top GitHub repositories and users based on keyword',
    'long_description': '# Top Github Users Scraper\n\nScrape top Github repositories and users based on keywords. \n\nI used this tool to analyze the top 1k machine learning users in [this article](https://towardsdatascience.com/i-scraped-more-than-1k-top-machine-learning-github-profiles-and-this-is-what-i-found-1ab4fb0c0474?sk=68156d6b1c05614d356645728fe02584).\n\n![demo](https://github.com/khuyentran1401/top-github-scraper/blob/master/figures/demo.gif?raw=True)\n\n## Setup\n\n**Installation**\n```bash\npip install top-github-scraper\n```\n**Add Credentials**\n\nTo make sure you can scrape many repositories and users, add your GitHub\'s credentials to `.env` file.\n```bash\ntouch .env\n```\nAdd your username and [token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) to `.env` file:\n```bash\nGITHUB_USERNAME=yourusername\nGITHUB_TOKEN=yourtoken\n```\n## Usage\n**Get Top Github Repositories\' URLs**\n```python\nfrom top_github_scraper import get_top_urls\n\nget_top_repos(keyword="machine learning", stop_page=20)\n```\nAfter running the script above, a file named \n* `top_repo_urls_<keyword>_<start_page>_<end_page>.json` \n\nwill be saved to your current directory.\n\n**Get Top Github Repositories\' Information**\n```python\nfrom top_github_scraper import get_top_urls\n\nget_top_urls("machine learning", stop_page=20)\n```\nAfter running the script above, 2 files named \n* `top_repo_urls_<keyword>_<start_page>_<end_page>.json` \n* `top_repo_info_<keyword>_<start_page>_<end_page>.json` \n\nwill be saved to your current directory.\n\n**Get Top Github Users\' Profiles**\n```python\nfrom top_github_scraper import get_top_users\n\nget_top_users("machine learning", stop_page=20)\n```\nAfter running the script above, 3 files named \n* `top_repo_urls_<keyword>_<start_page>_<end_page>.json` \n* `top_repo_info_<keyword>_<start_page>_<end_page>.json`\n* `top_user_info_<keyword>_<start_page>_<end_page>.csv` \n\nwill be saved to your current directory.\n\n### Parameters\n* **get_top_urls**\n    * `keyword` : str\n        Keyword to search for (.i.e, machine learning)\n    * `save_path` : str, optional\n        where to save the output file, by default `"top_repo_urls"`\n    * `start_page` : int, optional\n        page number to start scraping from, by default `0`\n    * `stop_page` : int, optional\n        page number of the last page to scrape, by default `50`\n* **get_top_repos**\n    * `keyword` : str\n        Keyword to search for (.i.e, machine learning)\n    * `max_n_top_contributors`: int\n        number of top contributors in each repository to scrape from, by default `10`\n    * `start_page` : int, optional\n        page number to start scraping from, by default `0`\n    * `stop_page` : int, optional\n        page number of the last page to scrape, by default `50`\n    * `url_save_path` : str, optional\n        where to save the output file of URLs, by default `"top_repo_urls"`\n    * `repo_save_path` : str, optional\n        where to save the output file of repositories\' information, by default `"top_repo_info"`\n* **get_top_users**\n    * `keyword` : str\n        Keyword to search for (.i.e, machine learning)\n    * `max_n_top_contributors`: int\n        number of top contributors in each repository to scrape from, by default `10`\n    * `start_page` : int, optional\n        page number to start scraping from, by default `0`\n    * `stop_page` : int, optional\n        page number of the last page to scrape, by default `50`\n    * `url_save_path` : str, optional\n        where to save the output file of URLs, by default `"top_repo_urls"`\n    * `repo_save_path` : str, optional\n        where to save the output file of repositories\' information, by default `"top_repo_info"`\n    * `user_save_path` : str, optional\n        where to save the output file of users\' profiles, by default `"top_user_info"`\n## How the Data is Scraped\n\n`top-github-scraper` scrapes the owners as well as the contributors of the top repositories that pop up in the search when searching for a specific keyword on GitHub.\n\n![image](https://github.com/khuyentran1401/top-github-scraper/blob/master/figures/machine_learning_results.png?raw=True)\n\nFor each user, `top-github-scraper` scrapes 16 data points:\n* `login`: username\n* `url`: URL of the user\n* `contributions`: Number of contributions to the repository that the user is scraped from\n* `stargazers_count`: Number of stars of the repository that the user is scraped from\n* `forks_count`: Number of forks of the repository that the user is scraped from\n* `type`: Whether this account is a user or an organization\n* `name`: Name of the user\n* `company`: User\'s company\n* `location`: User\'s location\n* `email`: User\'s email\n* `hireable`: Whether the user is hireable\n* `bio`: Short description of the user\n* `public_repos`: Number of public repositories the user has (including forked repositories)\n* `public_gists`: Number of public repositories the user has (including forked gists)\n* `followers`: Number of followers the user has\n* `following`: Number of people the user is following\n\n',
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/top-github-scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
