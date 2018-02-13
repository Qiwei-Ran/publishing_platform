class PaginationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """

    def process_request(self, request):
        try:
            request.page = int(request.REQUEST['page'])
            # (KeyError, ValueError, TypeError)
        except Exception as e:
            request.page = 1
