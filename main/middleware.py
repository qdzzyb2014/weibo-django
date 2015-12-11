from django.utils import timezone


class RefreshLastseenMiddleware(object):

    def process_response(self, request, response):
        try:
            if request.user.is_authenticated():
                request.user.last_seen = timezone.now()
        finally:
            return response
