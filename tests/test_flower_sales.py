from lxml import etree

from odoo.tests import Form, TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestFlowerSales(TransactionCase):
    def test_flowers_action_defaults_and_filters(self):
        action = self.env.ref("flower_shop.action_flower_products")
        context = safe_eval(action.context)
        domain = safe_eval(action.domain)
        flower_model = self.env["product.template"].with_context(**context)

        with Form(flower_model) as form:
            form.name = "Rose"
            form.scientific_name = "Rosa"
            form.list_price = 25.0
        flower = form.record
        ordinary = self.env["product.template"].create({"name": "Flower Vase"})

        self.assertTrue(flower.is_flower)
        self.assertTrue(flower.sale_ok)
        self.assertTrue(flower.product_variant_id.is_flower)
        self.assertFalse(ordinary.is_flower)
        visible = self.env["product.template"].search(domain)
        self.assertIn(flower, visible)
        self.assertNotIn(ordinary, visible)
        self.assertEqual(
            self.env.ref("flower_shop.menu_flower_products").action, action
        )

    def test_sale_selectors_and_catalog_only_offer_sellable_flowers(self):
        templates = self.env["product.template"].create(
            [
                {"name": "Rose", "is_flower": True, "sale_ok": True},
                {"name": "Vase", "is_flower": False, "sale_ok": True},
                {"name": "Nursery Flower", "is_flower": True, "sale_ok": False},
            ]
        )
        flower, ordinary, unavailable = templates
        line_model = self.env["sale.order.line"]
        domains = line_model.fields_get(
            ["product_id", "product_template_id"], attributes=["domain"]
        )
        for field, model in [
            ("product_id", "product.product"),
            ("product_template_id", "product.template"),
        ]:
            domain = domains[field]["domain"]
            if isinstance(domain, str):
                domain = safe_eval(domain, {"company_id": self.env.company.id})
            visible = self.env[model].search(domain)
            candidates = (
                templates
                if model == "product.template"
                else templates.product_variant_id
            )
            self.assertEqual(visible & candidates, candidates[:1])

        partner = self.env["res.partner"].create({"name": "Flower Customer"})
        order = self.env["sale.order"].create({"partner_id": partner.id})
        catalog = self.env["product.product"].search(
            order._get_product_catalog_domain()
        )
        self.assertIn(flower.product_variant_id, catalog)
        self.assertNotIn(ordinary.product_variant_id, catalog)
        self.assertNotIn(unavailable.product_variant_id, catalog)

        with Form(order) as form:
            with form.order_line.new() as line:
                line.product_id = flower.product_variant_id
                line.product_uom_qty = 2
        self.assertEqual(order.order_line.product_id, flower.product_variant_id)

    def test_flower_details_are_available_on_product_form(self):
        view = self.env["product.template"].get_view(
            view_id=self.env.ref("product.product_template_only_form_view").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"])
        self.assertTrue(arch.xpath("//field[@name='is_flower']"))
        page = arch.xpath("//page[@name='flower_details']")[0]
        self.assertEqual(page.get("invisible"), "not is_flower")
        for field in [
            "scientific_name",
            "season_start",
            "season_end",
            "watering_frequency",
            "watering_amount",
        ]:
            self.assertTrue(page.xpath(f".//field[@name='{field}']"))
