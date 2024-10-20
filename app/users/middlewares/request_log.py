import socket
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

request_logger = logging.getLogger(settings.AUTH_LOGGER)


class RequestLogMiddleware(MiddlewareMixin):

    def process_request(self, request):

        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }
        request_logger.info(log_data)
