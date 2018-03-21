from seatsio.domain import Event
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListChartsTest(SeatsioClientTest):

    def test_all(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        charts = self.client.charts.list().all()

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart2.key, chart1.key)

    def test_filter(self):
        chart1 = self.client.charts.create(name="some stadium")
        chart2 = self.client.charts.create(name="a theatre")
        chart3 = self.client.charts.create(name="some other stadium")

        charts = self.client.charts.list().set_filter("stadium").all()

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart1.key)

    def test_tag(self):
        chart1 = self.__chart_with_tag(tag="tag1")
        chart2 = self.client.charts.create()
        chart3 = self.__chart_with_tag(tag="tag1")

        charts = self.client.charts.list().set_tag("tag1").all()

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart1.key)

    def test_tag_and_filter(self):
        chart1 = self.__chart_with_tag(name="some stadium", tag="tag1")
        chart2 = self.__chart_with_tag(tag="tag1")
        chart3 = self.__chart_with_tag(name="some other stadium")
        chart4 = self.client.charts.create()

        charts = self.client.charts.list().set_filter("stadium").set_tag("tag1").all()

        assert_that(charts).extracting("key").contains_exactly(chart1.key)

    def test_expand(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)

        retrieved_charts = self.client.charts.list().set_expand_events().all()

        # assert_that(retrieved_charts[0].events[0]).is_instance(Event) # TODO fix
        assert_that(retrieved_charts[0].events).extracting("id").contains_exactly(event2.id, event1.id)

    def __chart_with_tag(self, name=None, tag=None):
        chart = self.client.charts.create(name)
        self.client.charts.add_tag(chart.key, tag)
        return chart
