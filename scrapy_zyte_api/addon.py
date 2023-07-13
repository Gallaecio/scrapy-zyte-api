from scrapy.settings import BaseSettings

from scrapy_zyte_api import ScrapyZyteAPIDownloaderMiddleware


class Addon:
    def update_settings(self, settings: BaseSettings) -> None:
        # read the current values of the settings and store them separately
        settings.set(
            "_ZYTE_API_FALLBACK_HTTP_HANDLER",
            settings.getwithbase("DOWNLOAD_HANDLERS")["http"],
            "addon",
        )
        settings.set(
            "_ZYTE_API_FALLBACK_HTTPS_HANDLER",
            settings.getwithbase("DOWNLOAD_HANDLERS")["https"],
            "addon",
        )
        if not settings.get("ZYTE_API_FALLBACK_REQUEST_FINGERPRINTER_CLASS"):
            # This is a special case as this fallback setting can be set by the
            # user. In that case we just keep it.
            settings.set(
                "ZYTE_API_FALLBACK_REQUEST_FINGERPRINTER_CLASS",
                settings.get("REQUEST_FINGERPRINTER_CLASS"),
                "addon",
            )

        settings["DOWNLOAD_HANDLERS"][
            "http"
        ] = "scrapy_zyte_api.handler.ScrapyZyteAPIHTTPDownloadHandler"
        settings["DOWNLOAD_HANDLERS"][
            "https"
        ] = "scrapy_zyte_api.handler.ScrapyZyteAPIHTTPSDownloadHandler"
        settings["DOWNLOADER_MIDDLEWARES"][ScrapyZyteAPIDownloaderMiddleware] = 1000
        settings.set(
            "REQUEST_FINGERPRINTER_CLASS",
            "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
            "addon",
        )
        settings.set(
            "TWISTED_REACTOR",
            "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "addon",
        )
        settings.set("ZYTE_API_TRANSPARENT_MODE", True, "addon")
