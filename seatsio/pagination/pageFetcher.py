from seatsio.pagination.page import Page


class PageFetcher:
    def __init__(self, cls, http_client, url, **kwargs):
        self.cls = cls
        self.url = url
        self.httpClient = http_client
        self.page_size = None
        self.query_params = {}
        self.kwargs = kwargs

    def fetch_after(self, after_id=None):
        if after_id:
            self.set_query_param("start_after_id", after_id)
        return self.__fetch()

    def fetch_before(self, before_id=None):
        if before_id:
            self.set_query_param("end_before_id", before_id)
        return self.__fetch()

    def __fetch(self):
        if self.page_size:
            self.set_query_param("limit", self.page_size)
        response = self.httpClient.url(self.url, self.query_params, **self.kwargs).get()
        return Page.from_response(response, self.cls)

    def set_page_size(self, page_size):
        self.page_size = page_size

    def set_query_param(self, key, value):
        self.query_params[key] = value
