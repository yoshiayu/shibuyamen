from django import forms
from .models import Review


# レビューフォーム
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]


# 店舗検索フォーム
class ShopSearchForm(forms.Form):
    query = forms.CharField(label="店舗名で検索", max_length=100, required=False)
