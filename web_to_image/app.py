import requests, json, shutil, time, os



def req_server(url):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'authorization': 'Bearer null',
        'content-type': 'application/json',
        'origin': 'https://www.freeconvert.com',
        'priority': 'u=1, i',
        'referer': 'https://www.freeconvert.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    json_data = {
        'tasks': {
            'import': {
                'operation': 'import/webpage',
                'url': url,
                'filename': url,
            },
            'convert': {
                'operation': 'convert',
                'input': 'import',
                'input_format': 'webpage',
                'output_format': 'jpg',
                'options': {
                    'page_size': 'letter',
                    'page_orientation': 'portrait',
                    'margin': '0',
                    'initial_delay': '3',
                    'hide_cookie': True,
                    'use_print_stylesheet': True,
                },
                'type': 'webpage',
            },
            'export-url': {
                'operation': 'export/url',
                'input': 'convert',
            },
        },
    }

    response = requests.post('https://api.freeconvert.com/v1/process/jobs', headers=headers, json=json_data).json()

    status = response["status"]

    if status == "processing":
        url_self = response["links"]["self"]
        print(url_self)
        time.sleep(5)
        return url_self

    else:
        return "failled"


def get_url_image(url):
    get_status = requests.get(url).json()
    status = get_status["status"]

    if status == "completed":
        url_image = get_status["tasks"][1]["result"]["url"]
        return url_image

    else:
        time.sleep(3)
        retries = 0
        while retries < 10:
            check = requests.get(url).json()
            status = check["status"]
            if status == "completed":
                url_image = check["tasks"][1]["result"]["url"]
                return url_image

            retries+=1
            time.sleep(3)

        return "failled"



def download(url):
    req = req_server(url)
    if req != "failled":
        url_image = get_url_image(req)
        if url_image != "failled":
            filename = url_image.split("/")[-1]
            file_type = filename.split(".")[-1]
            file_path = "data/media/" + filename

            get_image = requests.get(url_image)

            with open(file_path, "wb") as file:
                file.write(get_image.content)

            if file_type == "zip":
                path_unpack = "data/media/unpack"
                shutil.unpack_archive(file_path, path_unpack)
                file = os.listdir("data/media/unpack")[0]
                os.remove(file_path)
                file_path = "data/media/unpack/" + file


            print("succes: " + file_path)

            if file_type == "zip":
                shutil.rmtree(path_unpack)

            else:
                os.remove(file_path)


    else:
        print("Failled")


download("https://github.com/brutalX-04")