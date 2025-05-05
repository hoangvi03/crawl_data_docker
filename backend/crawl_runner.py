import os
import sys
import django
from django.conf import settings 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor
print("hello from crawl_runner.py")
print("Python executable: ", sys.executable)

# Cấu hình Django
if not django.conf.settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

from scrapy_crawler.scrapy_crawler.spiders.trangvang import TrangVangSpider
from crawler_app.models import CrawlTask
# Cấu hình twisted reactor để hỗ trợ asyncio
try:
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
except Exception:
    pass

def create_and_run_task(task_id, url_filter):
    task = CrawlTask.objects.get(id=task_id)
    print(f"Running task #{task_id} with filter: {url_filter}")
    try:
        task.status = 'In Progress'
        task.save()

        # Cấu hình và khởi chạy Scrapy crawler
        process = CrawlerProcess(get_project_settings())
        process.crawl(TrangVangSpider, task_id=task.id, url=url_filter)
        process.start()  # Blocking call, chờ đến khi crawl xong

        task.refresh_from_db()
        if task.status != 'Failed':
            task.status = 'Done'
            task.save()
            print(f"Task #{task.id} done.")
    except Exception as e:
        print(f"Crawl failed: {e}")
        task.status = 'Failed'
        task.save()
        
        
if __name__ == "__main__":
    task_id = sys.argv[1]  # Lấy task_id từ tham số dòng lệnh
    url_filter = sys.argv[2]  # Lấy url_filter từ tham số dòng lệnh
    create_and_run_task(task_id, url_filter)