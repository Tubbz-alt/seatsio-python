from seatsio.domain import EventReportItem, EventReport


class EventReports:
    def __init__(self, http_client):
        self.http_client = http_client

    def by_status(self, event_key, status=None):
        return self.__fetch_report("byStatus", event_key, status)

    def by_category_label(self, event_key, category_label=None):
        return self.__fetch_report("byCategoryLabel", event_key, category_label)

    def by_category_key(self, event_key, category_key=None):
        return self.__fetch_report("byCategoryKey", event_key, category_key)

    def by_label(self, event_key, label=None):
        return self.__fetch_report("byLabel", event_key, label)

    def by_order_id(self, event_key, order_id=None):
        return self.__fetch_report("byOrderId", event_key, order_id)

    def by_section(self, event_key, section=None):
        return self.__fetch_report("bySection", event_key, section)

    def __fetch_report(self, report_type, event_key, report_filter=None):
        if report_filter:
            url = "/reports/events/{key}/{reportType}/{filter}"
            body = self.http_client.url(url, key=event_key, reportType=report_type, filter=report_filter).get()
            result = []
            for i in body[report_filter]:
                result.append(EventReportItem(i))
            return result
        else:
            url = "/reports/events/{key}/{reportType}"
            body = self.http_client.url(url, key=event_key, reportType=report_type).get()
            return EventReport(body)
