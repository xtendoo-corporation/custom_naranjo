# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.auto.addons.account_move_exception.init_hook import store_exception_fields
from odoo.custom.src.odoo.odoo.service.server import start


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ip_number = fields.Char(
        string='IP number',
        compute='_compute_ip_number',
    )
    date_approve = fields.Date(
        string="Fecha Servicio",
        compute='_compute_date_approve',
        store=True,
    )
    date_download = fields.Date(
        string="Fecha Descarga",
        compute='_compute_date_download',
        store=True,
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

    @api.depends('move_id.move_type', 'purchase_order_id.date_approve', 'move_id.invoice_origin')
    def _compute_date_approve(self):
        for record in self:
            record.date_approve = False
            if record.move_id.move_type in ["in_invoice", "in_refund"]:
                # Para facturas de compra
                if record.purchase_order_id:
                    record.date_approve = record.purchase_order_id.date_approve
            elif record.move_id.move_type in ["out_invoice", "out_refund"]:
                # Para facturas de venta
                if record.move_id.invoice_origin:
                    # Buscar la orden de venta basada en invoice_origin
                    sale_order = self.env['sale.order'].search(
                        [('name', '=', record.move_id.invoice_origin)], limit=1
                    )
                    if sale_order:
                        record.date_approve = sale_order.date_order

    @api.depends('move_id.move_type', 'purchase_order_id.download_date', 'move_id.invoice_origin')
    def _compute_date_download(self):
        for record in self:
            record.date_download = False
            if record.move_id.move_type in ["in_invoice", "in_refund"]:
                for line in record.filtered("purchase_order_id"):
                    record.date_download = line.purchase_order_id.download_date
            elif record.move_id.move_type in ["out_invoice", "out_refund"]:
                if record.move_id.invoice_origin:
                    sale_order = self.env['sale.order'].search(
                        [('name', '=', record.move_id.invoice_origin)], limit=1
                    )
                    if sale_order:
                        record.date_download = sale_order.download_date
