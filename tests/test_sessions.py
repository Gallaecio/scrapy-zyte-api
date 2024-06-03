from typing import Any, Dict

import pytest
from pytest_twisted import ensureDeferred
from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import Response

from scrapy_zyte_api.utils import _RAW_CLASS_SETTING_SUPPORT

from . import get_crawler

UNSET = object()


@pytest.mark.parametrize(
    ("setting", "meta", "outcome"),
    (
        (UNSET, UNSET, False),
        (UNSET, True, True),
        (UNSET, False, False),
        (True, UNSET, True),
        (True, True, True),
        (True, False, False),
        (False, UNSET, False),
        (False, True, True),
        (False, False, False),
    ),
)
@ensureDeferred
async def test_enabled(setting, meta, outcome, mockserver):
    settings = {"ZYTE_API_URL": mockserver.urljoin("/")}
    if setting is not UNSET:
        settings["ZYTE_API_SESSION_ENABLED"] = setting
    meta_dict = {}
    if meta is not UNSET:
        meta_dict = {"zyte_api_session_enabled": meta}

    class TestSpider(Spider):
        name = "test"

        def start_requests(self):
            yield Request("https://example.com", meta=meta_dict)

        def parse(self, response):
            pass

    crawler = await get_crawler(settings, spider_cls=TestSpider, setup_engine=False)
    await crawler.crawl()

    session_stats = {
        k: v
        for k, v in crawler.stats.get_stats().items()
        if k.startswith("scrapy-zyte-api/sessions")
    }
    if outcome:
        assert session_stats == {
            "scrapy-zyte-api/sessions/pools/example.com/init/check-passed": 1,
            "scrapy-zyte-api/sessions/pools/example.com/use/check-passed": 1,
        }
    else:
        assert session_stats == {}


@pytest.mark.parametrize(
    ("params_setting", "params_meta", "location_setting", "location_meta", "outcome"),
    (
        (UNSET, UNSET, UNSET, UNSET, False),
        (UNSET, UNSET, UNSET, None, False),
        (UNSET, UNSET, UNSET, False, False),
        (UNSET, UNSET, UNSET, True, True),
        (UNSET, UNSET, False, UNSET, False),
        (UNSET, UNSET, False, None, False),
        (UNSET, UNSET, False, False, False),
        (UNSET, UNSET, False, True, True),
        (UNSET, UNSET, True, UNSET, True),
        (UNSET, UNSET, True, None, False),
        (UNSET, UNSET, True, False, False),
        (UNSET, UNSET, True, True, True),
        (UNSET, False, UNSET, UNSET, False),
        (UNSET, False, UNSET, None, False),
        (UNSET, False, UNSET, False, False),
        (UNSET, False, UNSET, True, True),
        (UNSET, False, False, UNSET, False),
        (UNSET, False, False, None, False),
        (UNSET, False, False, False, False),
        (UNSET, False, False, True, True),
        (UNSET, False, True, UNSET, True),
        (UNSET, False, True, None, False),
        (UNSET, False, True, False, False),
        (UNSET, False, True, True, True),
        (UNSET, True, UNSET, UNSET, True),
        (UNSET, True, UNSET, None, True),
        (UNSET, True, UNSET, False, False),
        (UNSET, True, UNSET, True, True),
        (UNSET, True, False, UNSET, False),
        (UNSET, True, False, None, True),
        (UNSET, True, False, False, False),
        (UNSET, True, False, True, True),
        (UNSET, True, True, UNSET, True),
        (UNSET, True, True, None, True),
        (UNSET, True, True, False, False),
        (UNSET, True, True, True, True),
        (False, UNSET, UNSET, UNSET, False),
        (False, UNSET, UNSET, None, False),
        (False, UNSET, UNSET, False, False),
        (False, UNSET, UNSET, True, True),
        (False, UNSET, False, UNSET, False),
        (False, UNSET, False, None, False),
        (False, UNSET, False, False, False),
        (False, UNSET, False, True, True),
        (False, UNSET, True, UNSET, True),
        (False, UNSET, True, None, False),
        (False, UNSET, True, False, False),
        (False, UNSET, True, True, True),
        (False, False, UNSET, UNSET, False),
        (False, False, UNSET, None, False),
        (False, False, UNSET, False, False),
        (False, False, UNSET, True, True),
        (False, False, False, UNSET, False),
        (False, False, False, None, False),
        (False, False, False, False, False),
        (False, False, False, True, True),
        (False, False, True, UNSET, True),
        (False, False, True, None, False),
        (False, False, True, False, False),
        (False, False, True, True, True),
        (False, True, UNSET, UNSET, True),
        (False, True, UNSET, None, True),
        (False, True, UNSET, False, False),
        (False, True, UNSET, True, True),
        (False, True, False, UNSET, False),
        (False, True, False, None, True),
        (False, True, False, False, False),
        (False, True, False, True, True),
        (False, True, True, UNSET, True),
        (False, True, True, None, True),
        (False, True, True, False, False),
        (False, True, True, True, True),
        (True, UNSET, UNSET, UNSET, True),
        (True, UNSET, UNSET, None, True),
        (True, UNSET, UNSET, False, False),
        (True, UNSET, UNSET, True, True),
        (True, UNSET, False, UNSET, False),
        (True, UNSET, False, None, True),
        (True, UNSET, False, False, False),
        (True, UNSET, False, True, True),
        (True, UNSET, True, UNSET, True),
        (True, UNSET, True, None, True),
        (True, UNSET, True, False, False),
        (True, UNSET, True, True, True),
        (True, False, UNSET, UNSET, False),
        (True, False, UNSET, None, False),
        (True, False, UNSET, False, False),
        (True, False, UNSET, True, True),
        (True, False, False, UNSET, False),
        (True, False, False, None, False),
        (True, False, False, False, False),
        (True, False, False, True, True),
        (True, False, True, UNSET, True),
        (True, False, True, None, False),
        (True, False, True, False, False),
        (True, False, True, True, True),
        (True, True, UNSET, UNSET, True),
        (True, True, UNSET, None, True),
        (True, True, UNSET, False, False),
        (True, True, UNSET, True, True),
        (True, True, False, UNSET, False),
        (True, True, False, None, True),
        (True, True, False, False, False),
        (True, True, False, True, True),
        (True, True, True, UNSET, True),
        (True, True, True, None, True),
        (True, True, True, False, False),
        (True, True, True, True, True),
    ),
)
@ensureDeferred
async def test_param_precedence(
    params_setting, params_meta, location_setting, location_meta, outcome, mockserver
):
    postal_codes = {True: "10001", False: "10002"}
    settings = {
        "ZYTE_API_URL": mockserver.urljoin("/"),
        "ZYTE_API_SESSION_ENABLED": True,
        "ZYTE_API_SESSION_MAX_BAD_INITS": 1,
    }
    meta: Dict[str, Any] = {}

    if params_setting is not UNSET:
        settings["ZYTE_API_SESSION_PARAMS"] = {
            "actions": [
                {
                    "action": "setLocation",
                    "address": {"postalCode": postal_codes[params_setting]},
                }
            ]
        }
    if params_meta is not UNSET:
        meta["zyte_api_session_params"] = {
            "actions": [
                {
                    "action": "setLocation",
                    "address": {"postalCode": postal_codes[params_meta]},
                }
            ]
        }
    if location_setting is not UNSET:
        settings["ZYTE_API_SESSION_LOCATION"] = {
            "postalCode": postal_codes[location_setting]
        }
    if location_meta is None:
        meta["zyte_api_session_location"] = None
    elif location_meta is not UNSET:
        meta["zyte_api_session_location"] = {"postalCode": postal_codes[location_meta]}

    class TestSpider(Spider):
        name = "test"

        def start_requests(self):
            yield Request(
                "https://postal-code-10001.example",
                meta={
                    "zyte_api_automap": {
                        "actions": [
                            {
                                "action": "setLocation",
                                "address": {"postalCode": postal_codes[True]},
                            }
                        ]
                    },
                    **meta,
                },
            )

        def parse(self, response):
            pass

    crawler = await get_crawler(settings, spider_cls=TestSpider, setup_engine=False)
    await crawler.crawl()

    session_stats = {
        k: v
        for k, v in crawler.stats.get_stats().items()
        if k.startswith("scrapy-zyte-api/sessions")
    }
    if outcome:
        assert session_stats == {
            "scrapy-zyte-api/sessions/pools/postal-code-10001.example/init/check-passed": 1,
            "scrapy-zyte-api/sessions/pools/postal-code-10001.example/use/check-passed": 1,
        }
    else:
        assert session_stats == {
            "scrapy-zyte-api/sessions/pools/postal-code-10001.example/init/failed": 1,
        }


@pytest.mark.parametrize(
    ("params", "close_reason", "stats"),
    (
        (
            {"browserHtml": True},
            "bad_session_inits",
            {
                "scrapy-zyte-api/sessions/pools/forbidden.example/init/failed": 1,
            },
        ),
        (
            {"browserHtml": True, "url": "https://example.com"},
            "failed_forbidden_domain",
            {
                "scrapy-zyte-api/sessions/pools/forbidden.example/init/check-passed": 1,
                "scrapy-zyte-api/sessions/pools/forbidden.example/use/failed": 1,
            },
        ),
    ),
)
@ensureDeferred
async def test_url_override(params, close_reason, stats, mockserver):
    """If session params define a URL, that URL is used for session
    initialization. Otherwise, the URL from the request getting the session
    assigned first is used for session initialization."""
    settings = {
        "RETRY_TIMES": 0,
        "ZYTE_API_URL": mockserver.urljoin("/"),
        "ZYTE_API_SESSION_ENABLED": True,
        "ZYTE_API_SESSION_PARAMS": params,
        "ZYTE_API_SESSION_MAX_BAD_INITS": 1,
    }

    class TestSpider(Spider):
        name = "test"
        start_urls = ["https://forbidden.example"]

        def parse(self, response):
            pass

        def closed(self, reason):
            self.close_reason = reason

    crawler = await get_crawler(settings, spider_cls=TestSpider, setup_engine=False)
    await crawler.crawl()

    session_stats = {
        k: v
        for k, v in crawler.stats.get_stats().items()
        if k.startswith("scrapy-zyte-api/sessions")
    }
    assert crawler.spider.close_reason == close_reason
    assert session_stats == stats


class ConstantChecker:

    def __init__(self, result):
        self._result = result

    def check(self, request: Request, response: Response) -> bool:
        if self._result in (True, False):
            return self._result
        raise self._result


class TrueChecker(ConstantChecker):
    def __init__(self):
        super().__init__(True)


class FalseChecker(ConstantChecker):
    def __init__(self):
        super().__init__(False)


class CloseSpiderChecker(ConstantChecker):
    def __init__(self):
        super().__init__(CloseSpider("checker_failed"))


class TrueCrawlerChecker(ConstantChecker):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super().__init__(crawler.settings["ZYTE_API_SESSION_ENABLED"])


class FalseCrawlerChecker(ConstantChecker):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super().__init__(not crawler.settings["ZYTE_API_SESSION_ENABLED"])


@pytest.mark.parametrize(
    ("checker", "close_reason", "stats"),
    (
        *(
            pytest.param(
                checker,
                close_reason,
                stats,
                marks=pytest.mark.skipif(
                    not _RAW_CLASS_SETTING_SUPPORT,
                    reason=(
                        "Configuring component classes instead of their import "
                        "paths requires Scrapy 2.4+."
                    ),
                ),
            )
            for checker, close_reason, stats in (
                (
                    TrueChecker,
                    "finished",
                    {
                        "scrapy-zyte-api/sessions/pools/example.com/init/check-passed": 1,
                        "scrapy-zyte-api/sessions/pools/example.com/use/check-passed": 1,
                    },
                ),
                (
                    FalseChecker,
                    "bad_session_inits",
                    {"scrapy-zyte-api/sessions/pools/example.com/init/check-failed": 1},
                ),
                (CloseSpiderChecker, "checker_failed", {}),
                (
                    TrueCrawlerChecker,
                    "finished",
                    {
                        "scrapy-zyte-api/sessions/pools/example.com/init/check-passed": 1,
                        "scrapy-zyte-api/sessions/pools/example.com/use/check-passed": 1,
                    },
                ),
                (
                    FalseCrawlerChecker,
                    "bad_session_inits",
                    {"scrapy-zyte-api/sessions/pools/example.com/init/check-failed": 1},
                ),
            )
        ),
        (
            "tests.test_sessions.TrueChecker",
            "finished",
            {
                "scrapy-zyte-api/sessions/pools/example.com/init/check-passed": 1,
                "scrapy-zyte-api/sessions/pools/example.com/use/check-passed": 1,
            },
        ),
        (
            "tests.test_sessions.FalseChecker",
            "bad_session_inits",
            {"scrapy-zyte-api/sessions/pools/example.com/init/check-failed": 1},
        ),
        ("tests.test_sessions.CloseSpiderChecker", "checker_failed", {}),
        (
            "tests.test_sessions.TrueCrawlerChecker",
            "finished",
            {
                "scrapy-zyte-api/sessions/pools/example.com/init/check-passed": 1,
                "scrapy-zyte-api/sessions/pools/example.com/use/check-passed": 1,
            },
        ),
        (
            "tests.test_sessions.FalseCrawlerChecker",
            "bad_session_inits",
            {"scrapy-zyte-api/sessions/pools/example.com/init/check-failed": 1},
        ),
    ),
)
@ensureDeferred
async def test_checker(checker, close_reason, stats, mockserver):
    settings = {
        "ZYTE_API_URL": mockserver.urljoin("/"),
        "ZYTE_API_SESSION_CHECKER": checker,
        "ZYTE_API_SESSION_ENABLED": True,
        "ZYTE_API_SESSION_MAX_BAD_INITS": 1,
    }

    class TestSpider(Spider):
        name = "test"
        start_urls = ["https://example.com"]

        def parse(self, response):
            pass

        def closed(self, reason):
            self.close_reason = reason

    crawler = await get_crawler(settings, spider_cls=TestSpider, setup_engine=False)
    await crawler.crawl()

    session_stats = {
        k: v
        for k, v in crawler.stats.get_stats().items()
        if k.startswith("scrapy-zyte-api/sessions")
    }
    assert crawler.spider.close_reason == close_reason
    assert session_stats == stats


@pytest.mark.parametrize(
    ("postal_code", "url", "close_reason", "stats"),
    (
        (
            None,
            "https://example.com",
            "finished",
            {
                "scrapy-zyte-api/sessions/pools/example.com/init/check-passed": 1,
                "scrapy-zyte-api/sessions/pools/example.com/use/check-passed": 1,
            },
        ),
        (
            "10001",
            "https://postal-code-10001.example",
            "finished",
            {
                "scrapy-zyte-api/sessions/pools/postal-code-10001.example/init/check-passed": 1,
                "scrapy-zyte-api/sessions/pools/postal-code-10001.example/use/check-passed": 1,
            },
        ),
        (
            "10002",
            "https://postal-code-10001.example",
            "bad_session_inits",
            {"scrapy-zyte-api/sessions/pools/postal-code-10001.example/init/failed": 1},
        ),
        (
            "10001",
            "https://no-location-support.example",
            "unsupported_set_location",
            {},
        ),
    ),
)
@ensureDeferred
async def test_checker_location(postal_code, url, close_reason, stats, mockserver):
    """The default checker looks into the outcome of the ``setLocation`` action
    if a location meta/setting was used."""
    settings = {
        "ZYTE_API_URL": mockserver.urljoin("/"),
        "ZYTE_API_SESSION_ENABLED": True,
        "ZYTE_API_SESSION_MAX_BAD_INITS": 1,
    }
    if postal_code is not None:
        settings["ZYTE_API_SESSION_LOCATION"] = {"postalCode": postal_code}

    class TestSpider(Spider):
        name = "test"

        def start_requests(self):
            yield Request(
                url,
                meta={
                    "zyte_api_automap": {
                        "actions": [
                            {
                                "action": "setLocation",
                                "address": {"postalCode": postal_code},
                            }
                        ]
                    },
                },
            )

        def parse(self, response):
            pass

        def closed(self, reason):
            self.close_reason = reason

    crawler = await get_crawler(settings, spider_cls=TestSpider, setup_engine=False)
    await crawler.crawl()

    session_stats = {
        k: v
        for k, v in crawler.stats.get_stats().items()
        if k.startswith("scrapy-zyte-api/sessions")
    }
    assert crawler.spider.close_reason == close_reason
    assert session_stats == stats