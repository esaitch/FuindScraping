import re


class ScrapingTool:
    @classmethod
    def hash_title(cls, title):
        return str(hash(title))[1:5]