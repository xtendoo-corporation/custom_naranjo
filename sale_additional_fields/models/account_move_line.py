# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # def _compute_ip_number(self):
    #     self.ip_number = ""
    #     if self.move_id.move_type == "out_invoice":
    #         for line in self.filtered("sale_line_ids"):
    #             for sale_line in line.sale_line_ids:
    #                 if sale_line.ip_number:
    #                     line.ip_number = sale_line.ip_number
    #
    #     elif self.move_id.move_type == "in_invoice":
    #         for line in self.filtered("purchase_order_id"):
    #             line.ip_number = line.purchase_order_id.ip_number

    ip_number = fields.Char(
        string='IP number',
        compute='_compute_ip_number',
    )
    date_approve = fields.Date(
        string="Fecha Servicio",
        compute='_compute_date_approve',
    )

    @api.depends('move_id.move_type', 'sale_line_ids.ip_number', 'purchase_order_id.ip_number')
    def _compute_ip_number(self):
        for record in self:
            record.ip_number = ""
            if record.move_id.move_type in ["out_invoice", "out_refund"]:
                for line in record.filtered("sale_line_ids"):
                    for sale_line in line.sale_line_ids:
                        if sale_line.ip_number:
                            record.ip_number = sale_line.ip_number

            elif record.move_id.move_type in ["in_invoice", "in_refund"]:
                for line in record.filtered("purchase_order_id"):
                    record.ip_number = line.purchase_order_id.ip_number

    @api.depends('move_id.move_type', 'purchase_order_id.date_approve')
    def _compute_date_approve(self):
        for record in self:
            record.date_approve = False
            if record.move_id.move_type in ["in_invoice", "in_refund"]:
                for line in record.filtered("purchase_order_id"):
                    record.date_approve = line.purchase_order_id.date_approve
