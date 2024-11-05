from django.contrib import admin  # 管理者URLを追加
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


def redirect_to_map(request):
    return redirect("ramen_map")  # map ページへリダイレクト


urlpatterns = [
    path("admin/", admin.site.urls),  # 管理者URLを追加
    path("accounts/", include("allauth.urls")),
    path("", redirect_to_map),  # ルートにアクセスするとマップにリダイレクト
    path("map/", include("shibuyamenapp.urls")),  # shibuyamenapp のルート
    # パスワードリセットのためのURLパターン
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
