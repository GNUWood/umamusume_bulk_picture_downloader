import requests, re, json, os, threading

header = {
    "x-microcms-api-key":"xCZfLPNnbazeFHih87prlh1pomFsB1LFq6qZ"
}

charadata  = requests.get("https://6azuq3sitt-aw4monxblm4y4x0oos66.microcms.io/api/v1/character?limit=150",headers=header)
characters = charadata.json()

character_info = []
num = 0


def download_task(url, num):
    image_data = requests.get(url=url)
    image_name = f"{num}.png"
    if re.search(r"01\.png$", url):
        image_path = "制服"
    if re.search(r"02\.png$", url):
        image_path = "勝負服"
    if re.search(r"03\.png$", url):
        image_path = "原案"
    if re.search(r"04\.png$", url):
        image_path = "starting future"
    image_dir = image_path + "/" + image_name
    with open(image_dir, "wb") as f:
        f.write(image_data.content)



for i in characters["contents"]:
    images = []

    for image in i["visual"]:
        images.append(image["image"]["url"])

    character_info.append({
        "name":i["name"],
        "images": images
    })

    num = num + 1

data = {} #List to Dict
data["character"] = character_info

with open("info.json","w",encoding="utf-8") as f:
    f = json.dumps(data, ensure_ascii=False, indent=4)

print(f"{num}人分のデータを取得しました。画像のリクエストを開始します。")

#ディレクトリチェック

chara_number_list = ""

dir_name = ["制服","勝負服","原案","starting future"]
for i in dir_name:
    if os.path.isdir(i):
        pass
    else:
        os.makedirs(i)
num = 0 #カウントリセット

for i in data["character"]:
    for url in i["images"]:
        thread = threading.Thread(target=download_task, args=[url,num],)
        thread.start()

    thread.join()
    chara_number_list += f"{num}: {i['name']}\n"
    num = num + 1
    print(f"完了: {i['name']}")
with open("character_id.txt","w", encoding="utf-8") as f:
    f.write(chara_number_list)

print("全てのキャラクターの画像取得が完了しました。")