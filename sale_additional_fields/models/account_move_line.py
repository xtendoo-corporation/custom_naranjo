# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ip_number = fields.Char(
        string='IP number',
        related='move_id.ip_number',
        store=True,
    )

