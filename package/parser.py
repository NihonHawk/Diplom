from bs4 import BeautifulSoup
import requests
import json


class parser():

    def get_codes():
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/86.0.4240.198 Safari/537.36 "
        }
        primo_codes_list = []
        x = 0
        
        request = requests.get("https://protogamer.ru/genshin-impact/promocodes", headers=headers)

        if request.status_code != 200: print("Error"), exit
            
        soup = BeautifulSoup(request.content, "html.parser")
        primo = soup.find("div", class_="container").find_all("div", class_="row")
        
        for items in primo:
            if "Окончен" in items.get_text():
                break
            else:
                div = items.find_all("div")
                if div[0].get_text() not in primo_codes_list:
                    primo_codes_list.append({"Code" : div[0].get_text()})
                for item in div:
                    if item.get('title') != None:
                        if "Reward" not in primo_codes_list[x].keys():
                            primo_codes_list[x].update({
                            "Reward" : [item.get('title'), item.span.get_text()]})
                        else:
                            primo_codes_list[x]["Reward"].extend([item.get('title'), item.span.get_text()])
                x += 1  

        return primo_codes_list

    def get_news():
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/86.0.4240.198 Safari/537.36 "
        }
        page = 1
        url = f"https://genshin.mihoyo.com/content/yuanshen/getContentList?pageSize=10&pageNum={page}&channelId=245"
        response = requests.get(url, headers=headers)
        news = json.loads(response.text)

        post_list = []

        for items in range(len(news["data"]["list"])):
            post_url = 'https://genshin.mihoyo.com/ru/news/detail/' + str(news["data"]["list"][items]["contentId"])
            post_src = news["data"]["list"][items]["ext"][1]["value"][0]["url"]
            post_title = news["data"]["list"][items]["title"].replace("Genshin Impact |", "").replace("| Genshin Impact","").replace(" | ", "")
            post_title_description = news["data"]["list"][items]["intro"]
            post_meta = news["data"]["list"][items]["start_time"]

            post_list.append(
                {
                    "Тема": post_title,
                    "Описание": post_title_description,
                    "Изображение": post_src,
                    "Ссылка": post_url,
                    "Дата": post_meta,
                }
            )
    
        return post_list