from requests import get
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List
from dotenv import load_dotenv

import re
import pprint
import os
import time
import random


load_dotenv()


class ScrapArticle:
    journal_list: list = os.getenv("SCRAP_LIST").split(",")
    no_image: str = ("https://user-images.githubusercontent.com/"
                     "81741466/263754639-170bee96-6728-40c6-b60d-9d45d0db4e99.jpeg")
    days: int = int(os.getenv("DAYS"))

    def scrap_articles(self) -> List[dict]:
        scrap_data = []
        for journal_url in self.journal_list:
            base_url: str = (
                f"https://media.naver.com/press/{journal_url}/ranking?type=popular&date="
            )
            today: str = "".join(
                str(datetime.date(datetime.today() - timedelta(days=self.days))).split("-")
            )
            url: str = f"{base_url}{today}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
            response = get(url, headers=headers)
            time.sleep(random.uniform(10, 13))
            num = re.compile("\\d+")
            if response.status_code != 200:
                print("scrapping failed")
                pprint.pprint(response.raise_for_status)
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                journal = soup.find("a", class_="press_hd_name_link").text.strip()
                rank_lists = soup.find_all("ul", class_="press_ranking_list")
                journal_articles = []
                for rank_list in rank_lists:
                    articles = rank_list.find_all("a", class_="_es_pc_link")
                    for article in articles:
                        view_data = article.find("span", class_="list_view")
                        if not view_data:
                            continue
                        else:
                            data: dict = {"title": "", "image": "", "journal": journal, "url": "", "view": 0,
                                          "publish_date": today}
                            image = article.find("div", class_="list_img")
                            if not image:
                                data["image"] = self.no_image
                            else:
                                data["image"] = image.find("img")["src"]
                            data["url"] = article["href"]
                            data["title"] = article.find("strong", class_="list_title").text
                            view_data = "".join(num.findall(view_data.text))
                            data["view"] = view_data
                            journal_articles.append(data)
                scrap_data.append({f"{journal}": journal_articles})
        return scrap_data
