from django.shortcuts import render, get_object_or_404, redirect
from .models import Likes, RamenShop
from .forms import ReviewForm, ShopSearchForm
from .scraper import scrape_ramen_shops, scrape_and_save_to_csv
import logging
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
import json

logger = logging.getLogger(__name__)


def generate_csv(request):
    scrape_and_save_to_csv()
    return HttpResponse("CSVファイルが保存されました。")


def ramen_map(request):
    # スクレイピングして最新の店舗情報を取得
    shops = scrape_ramen_shops()

    # 緯度経度が取得できた店舗のみをGoogle Mapsに表示
    ramen_shops = RamenShop.objects.filter(
        location_latitude__isnull=False, location_longitude__isnull=False
    )

    # 各ラーメン店の緯度・経度が正しくテンプレートに渡るように修正
    shops_with_coordinates = [
        {
            "name": shop.name,
            "latitude": float(shop.location_latitude),  # Decimalをfloatに変換
            "longitude": float(shop.location_longitude),  # Decimalをfloatに変換
            "address": shop.address,
            "rating": (
                float(shop.rating) if shop.rating else None
            ),  # Decimalをfloatに変換
        }
        for shop in ramen_shops
    ]

    context = {
        "ramen_shops_json": json.dumps(
            shops_with_coordinates, ensure_ascii=False
        ),  # JSON形式でテンプレートに渡す
    }

    return render(request, "shibuyamenapp/map.html", context)


# レビュー追加のビュー
def add_review(request, shop_id):
    try:
        shop = get_object_or_404(RamenShop, id=shop_id)
    except Exception as e:
        # エラーテンプレートにデータを渡す
        return render(
            request,
            "shibuyamenapp/error.html",
            {"message": "該当するラーメン店舗が見つかりません。"},
        )

    # 通常処理
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ramen_shop = shop
            review.save()
            return redirect("shop_detail", shop_id=shop_id)
    else:
        form = ReviewForm()

    return render(
        request, "shibuyamenapp/add_review.html", {"form": form, "shop": shop}
    )


# いいね機能のビュー
def like_shop(request, shop_id):
    shop = get_object_or_404(RamenShop, id=shop_id)
    like, created = Likes.objects.get_or_create(user=request.user, ramen_shop=shop)
    if not created:
        like.delete()  # 既にいいねしている場合は取り消し
    return redirect("ramen_map")


# 店舗詳細ページのビュー
def shop_detail(request, shop_id):
    shop = get_object_or_404(RamenShop, id=shop_id)
    reviews = shop.reviews.all()  # 店舗に関連する全レビューを取得
    return render(
        request, "shibuyamenapp/shop_detail.html", {"shop": shop, "reviews": reviews}
    )


# 店舗検索機能のビュー
def search_shops(request):
    form = ShopSearchForm(request.GET or None)
    query = request.GET.get("query", "")
    sort_by = request.GET.get("sort", "name")

    # 名前によるフィルタリング
    if query:
        results = RamenShop.objects.filter(name__icontains=query)
    else:
        results = RamenShop.objects.all()

    # ソートオプションに応じたソート
    if sort_by == "point":
        results = results.order_by("-scraped_data__point_val")
    elif sort_by == "review":
        results = results.order_by("-scraped_data__review_val")
    elif sort_by == "like":
        results = results.order_by("-scraped_data__like_val")
    else:
        results = results.order_by("name")

    # 全店舗を表示するためのデータ
    ramen_shops = RamenShop.objects.all()

    context = {
        "form": form,
        "results": results,
        "ramen_shops": ramen_shops,  # 全店舗を追加
    }
    return render(request, "shibuyamenapp/search_results.html", context)


def all_shops_view(request):
    # すべてのラーメン店舗を取得
    ramen_shops = RamenShop.objects.all()

    context = {
        "ramen_shops": ramen_shops,
    }
    return render(request, "shibuyamenapp/all_shops.html", context)
