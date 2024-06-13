# Copyright 2022 - Dario Cruz https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class LicenceCar(models.Model):
    _name = "licence.car"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Licence Car"

    name = fields.Char(
        string="Licence car",
        required=True,
        index=True,
        tracking=True,
    )
    date_expiration = fields.Date(
        string='Expiration date',
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
    )
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        print("*" * 50)
        record = super(LicenceCar, self).create(vals)
        print("*" * 80)
        print(vals)
        if 'partner_id' in vals:
            print("*"*50)
            print(vals)
            partner = self.env['res.partner'].browse(vals['partner_id'])
            partner.licence_car_ids = [(4, record.id)]
        return record





