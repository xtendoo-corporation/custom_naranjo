# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    def _compute_ip_number(self):
        self.ip_number = ""
        for line in self.filtered("sale_line_ids"):
            print("*"*80)
            print("line", line)
            print("*"*80)
            for sale_line in line.sale_line_ids:
                print("*" * 80)
                print("sale_line", sale_line)
                print("*" * 80)
                if sale_line.ip_number:
                    print("*" * 80)
                    print("sale_line.ip_number", sale_line.ip_number)
                    print("*" * 80)
                    line.ip_number = sale_line.ip_number

    ip_number = fields.Char(
        string='IP number',
        compute='_compute_ip_number',
    )



