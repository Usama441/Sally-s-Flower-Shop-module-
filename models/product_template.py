from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_flower = fields.Boolean(
        string="Flower",
        default=False,
        help="Identify this product as a flower available in the Flowers menu.",
    )
    scientific_name = fields.Char()
    season_start = fields.Date()
    season_end = fields.Date()
    watering_frequency = fields.Integer(
        string="Watering Frequency (days)",
        help="Number of days between watering.",
    )
    watering_amount = fields.Float(string="Watering Amount (ml)")
