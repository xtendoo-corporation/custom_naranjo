# Copyright 2022 - Dario Cruz https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    ip_number = fields.Char(
        string="Nº IP",
        required=False,
        allow_none=False,
    )
    upload_date = fields.Date(
        string="Fecha de carga",
        required=False,
        allow_none=False,
    )
    download_date = fields.Date(
        string="Fecha de descarga",
        required=False,
        allow_none=False,
    )
    licence_id = fields.Many2one(
        comodel_name="licence",
        string="Licence",
        required=False,
    )

