from django.core.management.base import BaseCommand
from shibuyamenapp.scraper import scrape_and_save_to_csv


class Command(BaseCommand):
    help = "Scrapes ramen shop data and saves it to CSV."

    def handle(self, *args, **options):
        scrape_and_save_to_csv()
        self.stdout.write(self.style.SUCCESS("CSVファイルが正常に保存されました。"))
