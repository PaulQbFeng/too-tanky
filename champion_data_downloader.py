import os
import requests
from bs4 import BeautifulSoup


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)
    r = requests.get(url, timeout=1)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(r.text)
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


base_url ='https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/'

r=requests.get(base_url, timeout=1)
urls=[]
soup = BeautifulSoup(r.text, 'html.parser')
for link in soup.find_all('a'):
    urls.append(link.get('href'))

#urls = ['/', 'https://www.communitydragon.org', 'https://cdn.communitydragon.org', 'https://raw.communitydragon.org', 'https://github.com/communitydragon/docs/blob/master/assets.md', None, None, 'https://discord.gg/rZQwuek', 'https://www.patreon.com/communitydragon', '?C=N&O=A', '?C=N&O=D', '?C=S&O=A', '?C=S&O=D', '?C=M&O=A', '?C=M&O=D', '../', '-1.json', '1.json', '10.json', '101.json', '102.json', '103.json', '104.json', '105.json', '106.json', '107.json', '11.json', '110.json', '111.json', '112.json', '113.json', '114.json', '115.json', '117.json', '119.json', '12.json', '120.json', '121.json', '122.json', '126.json', '127.json', '13.json', '131.json', '133.json', '134.json', '136.json', '14.json', '141.json', '142.json', '143.json', '145.json', '147.json', '15.json', '150.json', '154.json', '157.json', '16.json', '161.json', '163.json', '164.json', '166.json', '17.json', '18.json', '19.json', '2.json', '20.json', '200.json', '201.json', '202.json', '203.json', '21.json', '22.json', '221.json', '222.json', '223.json', '23.json', '234.json', '235.json', '236.json', '238.json', '24.json', '240.json', '245.json', '246.json', '25.json', '254.json', '26.json', '266.json', '267.json', '268.json', '27.json', '28.json', '29.json', '3.json', '30.json', '31.json', '32.json', '33.json', '34.json', '35.json', '350.json', '36.json', '360.json', '37.json', '38.json', '39.json', '4.json', '40.json', '41.json', '412.json', '42.json', '420.json', '421.json', '427.json', '429.json', '43.json', '432.json', '44.json', '45.json', '48.json', '497.json', '498.json', '5.json', '50.json', '51.json', '516.json', '517.json', '518.json', '523.json', '526.json', '53.json', '54.json', '55.json', '555.json', '56.json', '57.json', '58.json', '59.json', '6.json', '60.json', '61.json', '62.json', '63.json', '64.json', '67.json', '68.json', '69.json', '7.json', '711.json', '72.json', '74.json', '75.json', '76.json', '77.json', '777.json', '78.json', '79.json', '8.json', '80.json', '81.json', '82.json', '83.json', '84.json', '85.json', '86.json', '875.json', '876.json', '887.json', '888.json', '89.json', '895.json', '897.json', '9.json', '90.json', '91.json', '92.json', '96.json', '98.json', '99.json', 'https://discord.gg/rZQwuek', 'https://www.patreon.com/communitydragon', 'https://github.com/communitydragon/cdtb', 'https://hextechdocs.dev', 'https://github.com/communitydragon/awesome-league', 'https://www.communitydragon.org', 'https://github.com/communitydragon', 'https://github.com/communitydragon/docs/blob/master/assets.md', 'https://github.com/communitydragon', 'https://discord.gg/rZQwuek', 'https://www.patreon.com/communitydragon', 'https://www.riotgames.com/en/legal']

curated_urls=[]

for x in urls:
    if type(x) == str:
        if x.endswith('.json'):
            curated_urls.append(x)

for i in range(len(curated_urls)):
    curated_urls[i] = base_url + curated_urls[i]
    download(curated_urls[i], "data/raw-community-dragon/champions")
