# Copyright 2022 - Dario Cruz https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # partner_id_vat = fields.Char(related='partner_id.vat', string='VAT No')

    partner_zip = fields.Char(
        comodel_name='res.partner',
        string='zip',
        related='partner_id.zip',
        readonly=True,
    )
