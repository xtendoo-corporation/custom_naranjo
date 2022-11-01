# Copyright 2020 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    licence_car_ids = fields.Many2many(
        comodel_name="licence.car",
        inverse_name='partner_id',
        string="Licence",
        required=False,
    )

class LicenceCarPartner(models.Model):
    _name = 'licence.car.partner'
    _description = 'Licence Car Partner'

    name = fields.Char(
        string="Licence Car Partner",
        required=True,
        index=True,
    )
    partner_id = fields.Many2one(
        comodel_name='partner',
        string='partner',
        required=True,
        ondelete='cascade',
        index=True,
    )
