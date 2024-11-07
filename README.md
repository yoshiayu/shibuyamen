# 渋谷ラーメンマップアプリ

## アプリ紹介
このアプリケーションは、渋谷エリアで利用できるラーメン店情報を提供するために開発されました。ユーザーは地図上でラーメン店の位置を確認し、お気に入りやレビューを通じてラーメン店を評価し、渋谷エリアでの一人や女性向けのラーメン体験を向上させることを目指しています。

### プロジェクトテーマ
渋谷エリア内のラーメン店に特化した情報を提供し、訪問の際に便利な機能を実装しました。Google Mapsとの連携を通じて、ユーザーが近くのラーメン店を視覚的に確認できるようになっています。

## 機能
- ラーメン店の位置をGoogle Mapsで表示
- キーワード、レビュー数、評価ポイントによるラーメン店検索
- お気に入り登録機能とレビュー投稿機能
- 緯度経度情報をもとにした位置情報の表示
- スクレイピング機能による最新のラーメン店情報の自動更新

## アプリケーションのアーキテクチャとフロー
バックエンドにはDjangoを採用し、データベースにPostgreSQLを使用しています。ユーザーはログイン後、ラーメン店を検索したり、レビューを投稿することでアプリの機能を活用できます。

### 画面遷移のリレーション図
以下はアプリケーションの画面遷移フローです：

```mermaid
graph TD;
    A[ホーム画面] -->|ラーメン店を地図で確認| B[ラーメンマップ画面]
    A -->|検索| C[ラーメン店検索画面]
    C -->|検索結果クリック| D[ラーメン店詳細画面]
    D -->|レビュー投稿| E[レビュー投稿画面]
    D -->|お気に入り登録| F[お気に入り登録]
    E -->|レビュー送信後| D
```

## バージョン管理
- **Python**: 3.8以上
- **Django**: 4.2.16
- **PostgreSQL**: 13以上
- **HTML5**: 最新仕様
- **CSS3**: 最新仕様

## 制作工程管理

### 1. 初期設定と計画
- アプリケーション要件定義、Djangoプロジェクトのセットアップ。
- Google Maps APIの連携設定と地図表示準備。
- データベースにはPostgreSQLを採用し、必要なテーブルとER図の設計を実施。

### 2. データベースおよびバックエンド実装
- ラーメン店、レビュー、ユーザー、お気に入り情報を管理するデータベース設計。
- Djangoを用いたラーメン店情報の管理、レビュー機能、お気に入り登録機能の実装。

### 3. フロントエンド開発
- Google Maps APIとの連携を活用し、地図上にラーメン店の位置をピン表示。
- JavaScriptとCSSを用いて、レスポンシブで見やすいUIを実装。

### 4. テストとバグ修正
- 各コンポーネントのテストとデバッグ。
- UI確認とデザイン最適化を行い、ユーザーがスムーズに情報を検索・利用できるよう調整。

### 5. デプロイメント
- ローカルサーバーでのデプロイとパフォーマンスの確認。
- GitHubでのバージョン管理とリモートチームによるコラボレーション。

## 使用ツール
- **プロジェクト管理**: GitHubでのイシュー管理。
- **開発環境**: Visual Studio Code。
- **データベース**: PostgreSQLを使用。
- **テスト**: Djangoのテスト機能によるユニットテスト。

## インストールと使用方法

### 1. リポジトリをクローンします：
```bash
git clone https://github.com/your-username/shibuya-ramen-map-app.git

