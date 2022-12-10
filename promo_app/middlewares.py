import json
import traceback

from django.http import HttpRequest, HttpResponse
from loguru import logger

from promo_project.settings import DJANGO_LOGURU_CONFIG

logger.remove(0)
logger.configure(**DJANGO_LOGURU_CONFIG['loguru'])


class LoguruMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ignore_urls: list = DJANGO_LOGURU_CONFIG.get('ignore', [])

    def __call__(self, request: HttpRequest):
        if not self.__is_contains_ignore_url(request.get_raw_uri()):
            self.__log_request(request)
            response: HttpResponse = self.get_response(request)
            self.__log_response(response)
            self.__log_user(request)
            return response
        return self.get_response(request)

    def __is_contains_ignore_url(self, url):
        """Содержит ли данный url игнорируемый url"""
        return any(item in url for item in self.ignore_urls)

    def __log_request(self, request: HttpRequest):
        """ Логирование HttpRequest """
        url = request.get_raw_uri()
        logger.info(f"URL: {url}")
        logger.info(f"Method: {request.method}")
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            logger.info(f"Data: {{{''}}}")
        else:
            logger.info(f"Data: {body}")

    def __log_response(self, response: HttpResponse):
        """ Логирование HttpResponse """
        try:
            content = json.loads(response.content)
        except json.JSONDecodeError:
            logger.info(f"Response: {{{''}}}")
        else:
            logger.info(f"Response: {content}")
        logger.info(f"Status Code: {response.status_code}")

    def process_exception(self, request: HttpRequest, exception: Exception):
        """ Логирование Exception """
        logger.error(str(traceback.format_exc()))

    def __log_user(self, request: HttpRequest):
        """ Логирование данных пользователя """
        logger.info(f"User_id: {request.user.id}")
        logger.info(f"----------------------")
