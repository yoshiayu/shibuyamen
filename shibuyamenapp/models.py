from django.db import models
from django.contrib.auth.models import User


# ラーメン店舗モデル
class RamenShop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=100)  # 新しいフィールド
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    scraped_data = models.TextField(blank=True, null=True)
    location_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    location_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)  # ここを修正

    def __str__(self):
        return self.name


# レビューモデル
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ramen_shop = models.ForeignKey(
        RamenShop, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # 1〜5の評価
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.ramen_shop.name}"


# いいね（中間テーブル）
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ramen_shop = models.ForeignKey(RamenShop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.ramen_shop.name}"
