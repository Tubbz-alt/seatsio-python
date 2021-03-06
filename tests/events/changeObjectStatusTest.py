from seatsio import Channel, SocialDistancingRuleset
from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeObjectStatusTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        res = self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo")

        assert_that(self.client.events.retrieve_object_status(event.key, "A-1").status).is_equal_to("status_foo")
        assert_that(self.client.events.retrieve_object_status(event.key, "A-2").status).is_equal_to("status_foo")
        assert_that(self.client.events.retrieve_object_status(event.key, "A-3").status).is_equal_to("free")

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")
        object = res.objects["A-1"]
        assert_that(object.status).is_equal_to("status_foo")
        assert_that(object.label).is_equal_to("A-1")
        assert_that(object.labels).is_equal_to({"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}})
        assert_that(object.category_label).is_equal_to("Cat1")
        assert_that(object.category_key).is_equal_to("9")
        assert_that(object.ticket_type).is_none()
        assert_that(object.order_id).is_none()
        assert_that(object.object_type).is_equal_to("seat")
        assert_that(object.for_sale).is_true()
        assert_that(object.section).is_none()
        assert_that(object.entrance).is_none()
        assert_that(object.num_booked).is_none()
        assert_that(object.capacity).is_none()
        assert_that(object.left_neighbour).is_none()
        assert_that(object.right_neighbour).is_equal_to("A-2")

    def test_hold_token(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo", hold_token.hold_token)

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.hold_token).is_none()

        status1 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.hold_token).is_none()

    def test_order_id(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo", order_id="myOrder")

        assert_that(self.client.events.retrieve_object_status(event.key, "A-1").order_id).is_equal_to("myOrder")
        assert_that(self.client.events.retrieve_object_status(event.key, "A-2").order_id).is_equal_to("myOrder")

    def test_tickettype(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("A-1", ticket_type="Ticket Type 1")
        props2 = ObjectProperties("A-2", ticket_type="Ticket Type 2")

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.ticket_type).is_equal_to("Ticket Type 1")

        status2 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status2.status).is_equal_to("status_foo")
        assert_that(status2.ticket_type).is_equal_to("Ticket Type 2")

    def test_quantity(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("GA1", quantity=5)
        props2 = ObjectProperties("GA2", quantity=10)

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        assert_that(self.client.events.retrieve_object_status(event.key, "GA1").quantity).is_equal_to(5)
        assert_that(self.client.events.retrieve_object_status(event.key, "GA2").quantity).is_equal_to(10)

    def test_extra_data(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("A-1", extra_data={"foo": "bar"})
        props2 = ObjectProperties("A-2", extra_data={"foo": "baz"})

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        assert_that(self.client.events.retrieve_object_status(event.key, "A-1").extra_data).is_equal_to({"foo": "bar"})
        assert_that(self.client.events.retrieve_object_status(event.key, "A-2").extra_data).is_equal_to({"foo": "baz"})

    def test_keepExtraDataTrue(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", keep_extra_data=True)

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.extra_data).is_equal_to(extra_data)

    def test_keepExtraDataFalse(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", keep_extra_data=False)

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.extra_data).is_none()

    def test_noKeepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus")

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.extra_data).is_none()

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1", "A-2"]
        })

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", channel_keys=["channelKey1"])

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.status).is_equal_to("someStatus")

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1", "A-2"]
        })

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", ignore_channels=True)

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.status).is_equal_to("someStatus")

    def test_ignoreSocialDistancing(self):
        chart_key = self.create_test_chart()
        rulesets = {
            'ruleset': SocialDistancingRuleset.fixed(
                name='My first ruleset',
                disabled_seats=["A-1"]
            )
        }
        self.client.charts.save_social_distancing_rulesets(chart_key, rulesets)
        event = self.client.events.create(chart_key, social_distancing_ruleset_key='ruleset')

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", ignore_social_distancing=True)

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.status).is_equal_to("someStatus")
