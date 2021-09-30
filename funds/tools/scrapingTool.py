import re


class ScrapingTool:
    @classmethod
    def hash_title(cls, title):
        return str(hash(title))[1:5]

    @classmethod
    def create_project_id(cls, pid, id):
        return str(pid) + str(id).zfill(3)