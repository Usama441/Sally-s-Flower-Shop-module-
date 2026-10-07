from odoo import fields, models


class Flower(models.Model):
    _name = "flower.shop.flower"
    _description = "Flower"
    _rec_name = "common_name"
    _order = "common_name, id"

    common_name = fields.Char(required=True)
    scientific_name = fields.Char()
    season_start = fields.Date()
    season_end = fields.Date()
    watering_frequency = fields.Integer(
        string="Watering Frequency (days)",
        help="Number of days between watering.",
    )
    watering_amount = fields.Float(string="Watering Amount (ml)")
