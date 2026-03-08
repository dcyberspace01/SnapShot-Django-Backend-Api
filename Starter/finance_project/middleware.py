class PartitionedCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        for cookie_name in ["sessionid", "csrftoken"]:
            if cookie_name in response.cookies:
                response.cookies[cookie_name]["Partitioned"] = True

        return response
