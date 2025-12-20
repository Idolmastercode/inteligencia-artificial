import scrapy
import json

class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    allowed_domains = ["reddit.com"]
    # Usamos la API JSON de Reddit
    start_urls = ["https://www.reddit.com/r/python/.json"]

    def parse(self, response):
        data = json.loads(response.text)
        posts = data["data"]["children"]

        for post in posts:
            data_post = post["data"]
            
            titulo = data_post.get("title")
            autor = data_post.get("author")
            score = data_post.get("score")

            yield {
                "titulo": titulo, # Pasa por el pipeline
                "autor": autor,
                "score": score,
            }