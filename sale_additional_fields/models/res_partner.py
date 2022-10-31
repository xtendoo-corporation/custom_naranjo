# Copyright 2020 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    licence_car_id = fields.Many2one(
        comodel_name="licence.car",
        string="Licence",
        required=False,
    )
