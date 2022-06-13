from odoo import api, fields, models

import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"

    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
    )
