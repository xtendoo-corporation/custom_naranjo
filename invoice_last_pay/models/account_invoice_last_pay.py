# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    last_pay_date = fields.Date(
        string="Last date pay",
        compute="_compute_last_pay_date",
    )

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_last_pay_date(self):
        for record in self:
            last_pay_date = None
            for line in record.line_ids:
                if line.payment_id.is_matched:
                    if not last_pay_date or line.payment_id.payment_date > last_pay_date:
                        last_pay_date = line.payment_id.payment_date
            record.last_pay_date = last_pay_date
