# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import fields, models, api


class InvoiceLastPay(models.Model):
    _inherit = 'account.move'

    # payment_id many2one para referencia de pagos
    # payment_date
    last_pay_date = fields.Date(
        string="Last date pay",
        compute="_last_pay_date",
    )

    def _last_pay_date(self):
        # for line in self:
            print("*"*80)
            id_line = self.line_ids.move_id
            print("*" * 80)
            print(id_line)
            for line in id_line:
                print("*" * 80)
                print(line)
                last_pay = line.payment_id.date
                print("*" * 80)
                print(last_pay)
                self.last_pay_date = last_pay

