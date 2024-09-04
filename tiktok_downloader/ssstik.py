import requests, re, uuid, os
from bs4 import BeautifulSoup as soup



def download(url):
    try:
        with requests.Session() as session:
            cookies = open("data/cookies.txt", "r").read()
            get     = session.get('https://ssstik.io/', cookies={ 'cookie': cookies }).text
            tt_id   = re.search("s_tt = '(.*?)'", get).group(1)

            headers = {
                'authority': 'ssstik.io',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'hx-current-url': 'https://ssstik.io/',
                'hx-request': 'true',
                'hx-target': 'target',
                'hx-trigger': '_gcaptcha_pt',
                'origin': 'https://ssstik.io',
                'pragma': 'no-cache',
                'referer': 'https://ssstik.io/',
                'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }

            params = {
                'url': 'dl',
            }

            data = {
                'id': url,
                'locale': 'en',
                'tt': tt_id,
            }

            response = session.post('https://ssstik.io/abc', params=params, cookies={ 'cookie': cookies }, headers=headers, data=data).text

            body     = soup(response, 'html.parser')
            a        = body.find('a')
            url      = a.get('href')
            text     = a.text

            if text == "Without watermark":
                download = session.get(url)
                name = "download-" + str(uuid.uuid4()).split("-")[0] + ".mp4"

                with open("media/"+name, "wb") as file:
                    file.write(download.content)

                return "Succes download: " + name

            else:
                return "Failled"

    except Exception as e:
        return "Failled"



if __name__ == "__main__":
    try: os.listdir("media")
    except: os.mkdir("media")

    url = input("Input Url: ")
    response = download(url)

    print(response)
