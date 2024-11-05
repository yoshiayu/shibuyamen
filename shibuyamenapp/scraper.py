import requests
from bs4 import BeautifulSoup
from .models import RamenShop
import logging
import csv
import os

# ロギング設定
logger = logging.getLogger(__name__)


def scrape_ramen_shops():
    url = (
        "https://ramendb.supleks.jp/search?state=tokyo&city=%E6%B8%8B%E8%B0%B7%E5%8C%BA"
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    shops = []

    for shop_element in soup.find_all("div", class_="name"):
        try:
            shop_name = shop_element.find("h4").text.strip()
            shop_link = "https://ramendb.supleks.jp" + shop_element.find("a")["href"]
            area_element = shop_element.find_next("div", class_="area")
            shop_address = (
                area_element.get_text(separator=" ").strip()
                if area_element
                else "住所不明"
            )

            # Geocoding APIを使って住所から緯度・経度を取得
            latitude, longitude = geocode_address(shop_address)

            # 緯度・経度が取得できた場合のみ店舗情報を保存
            if latitude is not None and longitude is not None:
                ramen_shop, created = RamenShop.objects.get_or_create(
                    name=shop_name,
                    address=shop_address,
                    defaults={
                        "link": shop_link,
                        "location_latitude": latitude,
                        "location_longitude": longitude,
                    },
                )
                shops.append(ramen_shop)
            else:
                logger.error(f"Skipping shop {shop_name} due to missing coordinates.")
        except Exception as e:
            logger.error(f"Error scraping shop: {str(e)}")
            continue

    return shops


# スクレイピングでラーメン店データを取得してCSVに保存する
def scrape_and_save_to_csv():
    # 保存先のパスを指定
    save_dir = "/Users/yoshiayu/shibuyamenmap/shibuyamenpro/data"
    os.makedirs(save_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成
    csv_path = os.path.join(save_dir, "ramen_shops.csv")

    print(f"CSVファイルの保存先: {csv_path}")

    url = (
        "https://ramendb.supleks.jp/search?state=tokyo&city=%E6%B8%8B%E8%B0%B7%E5%8C%BA"
    )
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "lxml")

    shop_list = []

    for shop_element in soup.find_all("div", class_="name"):
        try:
            shop_info = {}
            shop_name = shop_element.find("h4").text.strip()
            shop_link = "https://ramendb.supleks.jp" + shop_element.find("a")["href"]
            area_element = shop_element.find_next("div", class_="area")
            shop_address = (
                area_element.get_text(separator=" ").strip()
                if area_element
                else "住所不明"
            )

            shop_info["name"] = shop_name
            shop_info["url"] = shop_link
            shop_info["address"] = shop_address
            shop_info["latitude"], shop_info["longitude"] = geocode_address(
                shop_address
            )

            if shop_info["latitude"] and shop_info["longitude"]:
                shop_list.append(shop_info)
        except Exception as e:
            logger.error(f"Error scraping shop: {str(e)}")
            continue

    try:
        with open(csv_path, "w", newline="") as csvfile:
            fieldnames = ["name", "url", "address", "latitude", "longitude"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(shop_list)
        print(f"CSVファイルが保存されました: {csv_path}")
    except IOError as e:
        print(f"ファイル保存中にエラーが発生しました: {e}")


def geocode_address(address):
    api_key = "AIzaSyBuGe50Xgx_kKsNoTfzG02EWHFkSXWT8Vo"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        location_data = response.json()

        if location_data["status"] == "OK":
            latitude = location_data["results"][0]["geometry"]["location"]["lat"]
            longitude = location_data["results"][0]["geometry"]["location"]["lng"]
            print(f"Address: {address}, Lat: {latitude}, Lng: {longitude}")
            return latitude, longitude
        else:
            logger.error(
                f"Geocoding failed for address {address}: {location_data['status']}"
            )
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for address {address}: {str(e)}")
        return None, None
