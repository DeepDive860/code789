from javaspider.spiders.amazon import AmazonSpider
from javaspider.middlewares import BlockResourcesMiddleware
my_spider = AmazonSpider()

# Scrapy settings for javaspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "javaspider"

SPIDER_MODULES = ["javaspider.spiders"]
NEWSPIDER_MODULE = "javaspider.spiders"

# Set Playwright as the download handler for HTTP/HTTPS
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    'javaspider.middlewares.BlockResourcesMiddleware': 543,
}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_PAGE_TIMEOUT = 180000  # 60 seconds
PLAYWRIGHT_PAGE_GOTO_TIMEOUT = 180000  # Set timeout to 60 seconds
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 180000  # 60 seconds
PLAYWRIGHT_ABORT_REQUEST = ""


PLAYWRIGHT_PAGE_CONTEXT = {
    'accept_downloads': False,  # Block downloads
    'java_script': True,  # Allow JavaScript
    'viewport': {'width': 1920, 'height': 1080},  # Set viewport size
    'user_agent': 'your-user-agent',  # Set your user agent
    'ignore_https_errors': True,
    'extra_http_headers': {
        'User-Agent': 'your-user-agent',
    },
    'proxy': None  # Define proxy if needed
}

PLAYWRIGHT_PAGE_REQUESTS = {
    "intercept": True,
    "url": {
        "patterns": ["*.css", "*.jpg", "*.jpeg", "*.png", "*.gif", "*.svg", "*.js"],
        "blocking": True,
    }
}


# Scrapy concurrency settings
CONCURRENT_REQUESTS = 3 # Increase concurrency
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # Limit concurrency per domain
CONCURRENT_REQUESTS_PER_IP = 8  # Limit concurrency per IP
DOWNLOAD_DELAY = 0.5  # Set to 0 for no delay between requests






# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "javaspider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "javaspider.middlewares.JavaspiderSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "javaspider.middlewares.JavaspiderDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "javaspider.pipelines.JavaspiderPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
