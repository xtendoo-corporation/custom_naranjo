from odoo import api, fields, models

import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"

    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
    )
    matricula = fields.Char(string="Matrícula", required=False, allow_none=False)
    ip_number = fields.Char(string="Nº IP", required=False, allow_none=False)
