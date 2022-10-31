# Copyright 2022 - Dario Cruz https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime

from odoo import api, fields, models

class Licence(models.Model):
    _name = "licence"
    _description = "Licence"

    name = fields.Char(
        string="Licence",
        required=True,
        index=True,
        tracking=True,
    )

    date_expiration = fields.Date(
        string='expiration date',
        required=True,
    )
