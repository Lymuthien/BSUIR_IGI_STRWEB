import pytz
import requests
import logging

logger = logging.getLogger(__name__)

class TimezoneService:
    @staticmethod
    def get_timezone_from_ip(ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            tz = response.json().get('timezone')
            return pytz.timezone(tz) if tz else pytz.timezone('UTC')
        except:
            return pytz.timezone('UTC')

    @staticmethod
    def get_timezone(request):
        ip = request.META.get('REMOTE_ADDR')
        logger.info(f"ip:{ip}")

        return TimezoneService.get_timezone_from_ip(ip)