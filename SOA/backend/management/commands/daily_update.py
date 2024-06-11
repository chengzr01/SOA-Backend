# run the function from crawel.py every day at 6 AM
# python manage.py daily_update

from django.core.management.base import BaseCommand

from backend.crawl import entry


class UpdateDatabase(BaseCommand):
    help = "Update the database with the latest job listings"
    def handle(self, *args, **options):
        entry("https://www.google.com/about/careers/applications/jobs/results/", start_page=1, end_page=2)
        # print
        self.stdout.write(self.style.SUCCESS("Successfully updated the database"))
        
        