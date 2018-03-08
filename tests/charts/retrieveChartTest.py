from seatsio import Chart
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveChartTest(SeatsioClientTest):
    
    def test(self):
        chart = self.client.charts.create()
        self.client.charts.add_tag(chart.key, "tag1")
        self.client.charts.add_tag(chart.key, "tag2")
        
        retrieved_chart = self.client.charts.retrieve(chart.key)

        assert_that(retrieved_chart).is_instance(Chart)
        assert_that(retrieved_chart.id).is_not_zero()
        assert_that(retrieved_chart.key).is_not_blank()
        assert_that(retrieved_chart.status).is_equal_to("NOT_USED")
        assert_that(retrieved_chart.name).is_equal_to("Untitled chart")
        assert_that(retrieved_chart.publishedVersionThumbnailUrl).is_not_blank()
        assert_that(retrieved_chart.draftVersionThumbnailUrl).is_none()
        assert_that(retrieved_chart.events).is_none()
        assert_that(retrieved_chart.tags).contains_exactly_in_any_order("tag1", "tag2")
        assert_that(retrieved_chart.archived).is_false()