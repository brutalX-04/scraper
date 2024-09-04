import requests, re, uuid, os
from bs4 import BeautifulSoup as soup


def download(url):
    try:
        cookies = open("data/cookies_tiktok.txt", "r").read()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }

        get  = requests.get(url, cookies={"cookie": cookies}, headers=headers)
        url  = re.search('"playAddr":"(.*?)"', get.text).group(1).replace("\\u002F", "/")

        download = requests.get(url, cookies={"cookie": cookies})
        name = "download-" + str(uuid.uuid4()).split("-")[0] + ".mp4"

        with open("media/"+name, "wb") as file:
            file.write(download.content)
        
        return "Succes download: " + name

    except Exception as e:
        return "Failled"



if __name__ == "__main__":
    try: os.listdir("media")
    except: os.mkdir("media")

    url = input("Input Url: ")
    response = download(url)

    print(response)