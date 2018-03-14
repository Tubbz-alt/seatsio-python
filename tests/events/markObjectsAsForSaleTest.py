from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class MarkObjectsAsForSaleTest(SeatsioClientTest):

    def test_objects_and_categories(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_for_sale(event.key, ["o1", "o2"], ["cat1", "cat2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.forSaleConfig.forSale).is_true()
        assert_that(retrieved_event.forSaleConfig.objects).contains_exactly("o1", "o2")
        assert_that(retrieved_event.forSaleConfig.categories).contains_exactly("cat1", "cat2")

    def test_objects(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_for_sale(event.key, objects=["o1", "o2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.forSaleConfig.forSale).is_true()
        assert_that(retrieved_event.forSaleConfig.objects).contains_exactly("o1", "o2")
        assert_that(retrieved_event.forSaleConfig.categories).is_empty()

    def test_categories(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_for_sale(event.key, categories=["cat1", "cat2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.forSaleConfig.forSale).is_true()
        assert_that(retrieved_event.forSaleConfig.objects).is_empty()
        assert_that(retrieved_event.forSaleConfig.categories).contains_exactly("cat1", "cat2")