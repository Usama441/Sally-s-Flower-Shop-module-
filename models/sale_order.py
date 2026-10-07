from odoo import models
from odoo.fields import Domain


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_product_catalog_domain(self):
        return super()._get_product_catalog_domain() & Domain("is_flower", "=", True)
