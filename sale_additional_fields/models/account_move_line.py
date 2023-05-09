# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    def _compute_ip_number(self):
        for line in self.filtered("sale_line_ids"):
            for sale_line in line.sale_line_ids.filtered(lambda x: x.ip_number):
                line.ip_number = sale_line.ip_number

    ip_number = fields.Char(
        string='IP number',
        compute='_compute_ip_number',
    )



