from frapy.commands import FrapyCommand


class Command(FrapyCommand):
    requires_project = True
    default_settings = {"LOG_ENABLED": False}

    def short_desc(self):
        return "List available spiders"

    def run(self, args, opts):
        for s in sorted(self.crawler_process.spider_loader.list()):
            print(s)