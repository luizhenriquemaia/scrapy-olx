from scrapy.cmdline import execute


def init_property_spider(region: str, apartment: bool,  filename: str):
    execute(['scrapy', 'crawl', 'property', '-a', f'region={region}', '-a', f'apartment={apartment}', '-o', filename])