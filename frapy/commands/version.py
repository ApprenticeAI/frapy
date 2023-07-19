import frapy
from frapy.commands import FrapyCommand
from frapy.utils.versions import frapy_components_versions


class Command(FrapyCommand):
    default_settings = {"LOG_ENABLED": False, "SPIDER_LOADER_WARN_ONLY": True}

    def syntax(self):
        return "[-v]"

    def short_desc(self):
        return "Print Frapy version"

    def add_options(self, parser):
        FrapyCommand.add_options(self, parser)
        parser.add_argument(
            "--verbose",
            "-v",
            dest="verbose",
            action="store_true",
            help="also display twisted/python/platform info (useful for bug reports)",
        )

    def run(self, args, opts):
        if opts.verbose:
            versions = frapy_components_versions()
            width = max(len(n) for (n, _) in versions)
            for name, version in versions:
                print(f"{name:<{width}} : {version}")
        else:
            print(f"Frapy {frapy.__version__}")
