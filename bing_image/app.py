from bs4 import BeautifulSoup
from urllib.parse import quote as encode_url
import requests, json



class scraper:
	def search(keywords):
		try:
			url = "https://www.bing.com/images/search?q=" + encode_url(keywords + " pinterest post") + "&go=Search&qs=ds&form=QBIR&first=1"
			headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" }
			search = requests.get(url, headers=headers)

			soup = BeautifulSoup(search.text, "html.parser")
			component = soup.select("#mmComponent_images_2 ul li a")

			data_m = json.loads(component[0].get("m"))
			url_image = data_m["murl"]


			return {"status":"succes","url": url_image}

		except Exception as e:
			print(e)
			return {"status":"failled"}


s = scraper.search("brutal.xyz facebook")
print(s)