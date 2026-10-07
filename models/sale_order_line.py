from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _domain_product_id(self):
        return super()._domain_product_id() + [("is_flower", "=", True)]
