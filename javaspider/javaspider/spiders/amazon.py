import scrapy
import random
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin, urlparse, parse_qs

def abort_request(request):
        
    exempted_format = [
        ".css",
        ".jpg",
        ".webp",
        ".png",
        "google",
        "crazyegg",
        "adrum",
        "ttf",
        "youtube",
    ]
    return request.resource_type == "image" or any(
        i in request.url for i in exempted_format
    )

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://amazon.com"]

    USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko',
    # Add more user agents as needed
]
    custom_settings = {
        "PLAYWRIGHT_ABORT_REQUEST": abort_request
    }

    def start_requests(self):
        
        target_urls = {
            "https://www.amazon.com/s?k=PC&rh=p_n_deal_type%3A23566065011&_encoding=UTF8&content-id=amzn1.sym.b85c8aef-9e73-4ff5-846f-0679727cb218&pd_rd_r=36cba143-a778-4880-b8d7-5b3d342c5b72&pd_rd_w=pKtM8&pd_rd_wg=zErgd&pf_rd_p=b85c8aef-9e73-4ff5-846f-0679727cb218&pf_rd_r=G36MCJCCF8QC2CJTVYQQ&ref=pd_hp_d_atf_unk": {
                "callback": self.parse_1,
                "wait_for_selector": "div.sg-col-inner"
            },
            # "https://www.amazon.com/s?k=handbags&_encoding=UTF8&content-id=amzn1.sym.41b63905-8227-4707-958b-3928e735686a&pd_rd_r=00fc60d5-945c-4797-a9c6-c33775d855fc&pd_rd_w=gS2BQ&pd_rd_wg=sJBcm&pf_rd_p=41b63905-8227-4707-958b-3928e735686a&pf_rd_r=G36MCJCCF8QC2CJTVYQQ&ref=pd_hp_d_btf_unk": {
            #     "callback": self.parse_2,
            #     "wait_for_selector": "div.sg-col-inner"
            # }
        
        }

        for url, meta_data in target_urls.items():

            yield scrapy.Request(
            url=url,
            headers={'User-Agent': random.choice(self.USER_AGENT_LIST)},  
            callback=meta_data["callback"],
            meta= {
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                
                    PageMethod("wait_for_selector", meta_data["wait_for_selector"], state="visible", timeout= 300000)
                ],
            },
        )

    def parse(self, response):
        print("HEHE")
        pass

    async def parse_1(self, response):

        items = response.css("div.sg-col-inner")

        for item in items:
            link = item.css("a.a-link-normal.s-no-outline::attr(href)").get()
            full_link = response.urljoin(link)

            if link: 
                full_link = response.urljoin(link)

            yield scrapy.Request(
                url=full_link,
                callback=self.parse_1_item,
                meta= {
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div.centerColAlign", state="attached", timeout= 180000)
                    ],
                },
            )

        next_page = response.css("li.a-last a::attr(href)").get()
        
        if next_page:
            full_next_page = response.urljoin(next_page)

            self.writefile(full_next_page)
            

            yield scrapy.Request(
                url=full_next_page,
                callback= self.parse_1,
                meta= {
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div.sg-col-inner", state="attached", timeout=180000)
                    ],
                },
            )
    
    
    # async def parse_2(self, response):

    #     items = response.css("div.sg-col-inner")

    #     for item in items:
    #         link = item.css("a.a-link-normal.s-no-outline::attr(href)").get()
    #         full_link = response.urljoin(link)

    #         if link:
    #             full_link = response.urljoin(link)

    #         yield response.follow(
    #             url=full_link,
    #             callback=self.parse_2_item,
    #             meta={
    #                 "playwright": True,
    #                 "playwright_include_pages": [
    #                     PageMethod("wait_for_selector", "div.sg-col-inner", timeout=60000)
    #                 ]
    #             },
    #         )

    async def parse_1_item(self, response):
        items = response.css("div#ppd")

        for item in items:

            product_name = item.css("span#productTitle::text").get()
            price = item.css("span.a-price-whole::text").get()
            brand = item.css("tr.po-brand span.a-size-base::text").get()
            operating_system = item.css("tr.po-operating_system span.po-break-word::text").get()
            product_description = item.css("span.a-list-item::text").get()

            yield {
                "product_name": product_name,
                "price": price,
                "brand": brand,
                "operating_system": operating_system,
                "product_description": product_description,
            }

    async def parse_2_item(self, response):
        items = response.css("div.a-row")

        for item in items:

            product_name = item.css("span#productTitle::text").get()
            price = item.css("span.a-price-whole::text").get()
            fabric_type = item.css("span.a-color-base::text").get()
            details = item.css("div.a-fixed-left-grid-col.a-col-right span.a-color-base::text").getall()
            details = [detail.strip() for detail in details if detail.strip()]


            yield {
                "product_name": product_name,
                "price": price,
                "fabric_type": fabric_type,
                "details": details
            } 

    async def block_resources(route, request):
        if request.resource_type in ["image", "stylesheet", "font", "media"]:
            await route.abort()
        else:
            await route.continue_()

    
    async def setup_page(self, page):
        # Register route to block certain resources
        await page.route("**/*", self.block_resources)

    def writefile(self, link):

        with open("link.txt", "a") as file:
            file.write(link + "\n")
















        



        
    




        



       