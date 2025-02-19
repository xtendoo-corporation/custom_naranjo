# Copyright 2020 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    licence_car_ids = fields.Many2many(
        comodel_name="licence.car",
        inverse_name='partner_id',
        string="Licence",
        required=False,
        domain="[('partner_id', '=', id)]",
    )
