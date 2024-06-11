
class ExemptCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path matches any URL under "accounts/"
        if request.path.startswith("/accounts/"):
            # Exempt CSRF protection
            setattr(request, '_dont_enforce_csrf_checks', True)

        response = self.get_response(request)
        return response