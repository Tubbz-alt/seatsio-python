from seatsio import Channel
from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EventReportsSummaryTest(SeatsioClientTest):

    def test_summaryByStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_status(event.key)

        assert_that(report.get("booked").get("count")).is_equal_to(1)
        assert_that(report.get("booked").get("bySection").get("NO_SECTION")).is_equal_to(1)
        assert_that(report.get("booked").get("byCategoryKey").get("9")).is_equal_to(1)
        assert_that(report.get("booked").get("byCategoryLabel").get("Cat1")).is_equal_to(1)
        assert_that(report.get("booked").get("byChannel").get("NO_CHANNEL")).is_equal_to(1)

        assert_that(report.get("free").get("count")).is_equal_to(231)
        assert_that(report.get("free").get("bySection").get("NO_SECTION")).is_equal_to(231)
        assert_that(report.get("free").get("byCategoryKey").get("9")).is_equal_to(115)
        assert_that(report.get("free").get("byCategoryKey").get("10")).is_equal_to(116)
        assert_that(report.get("free").get("byCategoryLabel").get("Cat1")).is_equal_to(115)
        assert_that(report.get("free").get("byCategoryLabel").get("Cat2")).is_equal_to(116)
        assert_that(report.get("free").get("byChannel").get("NO_CHANNEL")).is_equal_to(231)


    def test_summaryByCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_category_key(event.key)

        assert_that(report.get("9").get("count")).is_equal_to(116)
        assert_that(report.get("9").get("bySection").get("NO_SECTION")).is_equal_to(116)
        assert_that(report.get("9").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("9").get("byStatus").get("free")).is_equal_to(115)
        assert_that(report.get("9").get("byChannel").get("NO_CHANNEL")).is_equal_to(116)

        assert_that(report.get("10").get("count")).is_equal_to(116)
        assert_that(report.get("10").get("bySection").get("NO_SECTION")).is_equal_to(116)
        assert_that(report.get("10").get("byStatus").get("free")).is_equal_to(116)
        assert_that(report.get("10").get("byChannel").get("NO_CHANNEL")).is_equal_to(116)

    def test_summaryByCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_category_label(event.key)

        assert_that(report.get("Cat1").get("count")).is_equal_to(116)
        assert_that(report.get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(116)
        assert_that(report.get("Cat1").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("Cat1").get("byStatus").get("free")).is_equal_to(115)
        assert_that(report.get("Cat1").get("byChannel").get("NO_CHANNEL")).is_equal_to(116)

        assert_that(report.get("Cat2").get("count")).is_equal_to(116)
        assert_that(report.get("Cat2").get("bySection").get("NO_SECTION")).is_equal_to(116)
        assert_that(report.get("Cat2").get("byStatus").get("free")).is_equal_to(116)
        assert_that(report.get("Cat2").get("byChannel").get("NO_CHANNEL")).is_equal_to(116)

    def test_summaryBySection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_section(event.key)

        assert_that(report.get("NO_SECTION").get("count")).is_equal_to(232)
        assert_that(report.get("NO_SECTION").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("NO_SECTION").get("byStatus").get("free")).is_equal_to(231)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("9")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("10")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat1")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat2")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byChannel").get("NO_CHANNEL")).is_equal_to(232)

    def test_summaryBySelectability(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, "A-1")

        report = self.client.events.reports.summary_by_selectability(event.key)

        assert_that(report.get("selectable").get("count")).is_equal_to(231)
        assert_that(report.get("selectable").get("bySection").get("NO_SECTION")).is_equal_to(231)
        assert_that(report.get("selectable").get("byStatus").get("free")).is_equal_to(231)
        assert_that(report.get("selectable").get("byCategoryKey").get("9")).is_equal_to(115)
        assert_that(report.get("selectable").get("byCategoryLabel").get("Cat1")).is_equal_to(115)
        assert_that(report.get("selectable").get("byCategoryKey").get("10")).is_equal_to(116)
        assert_that(report.get("selectable").get("byCategoryLabel").get("Cat2")).is_equal_to(116)
        assert_that(report.get("selectable").get("byChannel").get("NO_CHANNEL")).is_equal_to(231)

        assert_that(report.get("not_selectable").get("count")).is_equal_to(1)
        assert_that(report.get("not_selectable").get("bySection").get("NO_SECTION")).is_equal_to(1)
        assert_that(report.get("not_selectable").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("not_selectable").get("byCategoryKey").get("9")).is_equal_to(1)
        assert_that(report.get("not_selectable").get("byCategoryLabel").get("Cat1")).is_equal_to(1)
        assert_that(report.get("not_selectable").get("byChannel").get("NO_CHANNEL")).is_equal_to(1)

    def test_summaryByChannel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1", "A-2"]
        })

        report = self.client.events.reports.summary_by_channel(event.key)

        assert_that(report.get("NO_CHANNEL").get("count")).is_equal_to(230)
        assert_that(report.get("NO_CHANNEL").get("bySection").get("NO_SECTION")).is_equal_to(230)
        assert_that(report.get("NO_CHANNEL").get("byStatus").get("free")).is_equal_to(230)
        assert_that(report.get("NO_CHANNEL").get("byCategoryKey").get("9")).is_equal_to(114)
        assert_that(report.get("NO_CHANNEL").get("byCategoryLabel").get("Cat1")).is_equal_to(114)
        assert_that(report.get("NO_CHANNEL").get("byCategoryKey").get("10")).is_equal_to(116)
        assert_that(report.get("NO_CHANNEL").get("byCategoryLabel").get("Cat2")).is_equal_to(116)

        assert_that(report.get("channelKey1").get("count")).is_equal_to(2)
        assert_that(report.get("channelKey1").get("bySection").get("NO_SECTION")).is_equal_to(2)
        assert_that(report.get("channelKey1").get("byStatus").get("free")).is_equal_to(2)
        assert_that(report.get("channelKey1").get("byCategoryKey").get("9")).is_equal_to(2)
        assert_that(report.get("channelKey1").get("byCategoryLabel").get("Cat1")).is_equal_to(2)
