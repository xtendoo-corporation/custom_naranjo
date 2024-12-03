# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


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
    licence_car_id = fields.Many2one(
        comodel_name='licence.car',
        string='Licence',
        compute='_compute_licence_car_id',
        store=True,
    )

    @api.depends('move_id.move_type', 'sale_line_ids.order_id.licence_car_id', 'purchase_order_id.licence_car_id')
    def _compute_licence_car_id(self):
        for record in self:
            record.licence_car_id = False
            if record.move_id.move_type in ["out_invoice", "out_refund"]:
                for line in record.sale_line_ids:
                    if line.order_id.licence_car_id:
                        record.licence_car_id = line.order_id.licence_car_id
                        break
            elif record.move_id.move_type in ["in_invoice", "in_refund"]:
                if record.purchase_order_id.licence_car_id:
                    record.licence_car_id = record.purchase_order_id.licence_car_id

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

    @api.depends('move_id.move_type', 'move_id.invoice_date', 'purchase_order_id.date_approve', 'move_id.invoice_origin')
    def _compute_date_approve(self):
        print("compute_date_approve------------------------------------")
        for record in self:
            record.date_approve = False
            if record.move_id.move_type in ["in_invoice", "in_refund"]:
                # Para facturas de compra
                if record.purchase_order_id:
                    record.date_approve = record.purchase_order_id.date_approve
            elif record.move_id.move_type in ["out_invoice", "out_refund"]:
                # Para facturas de venta
                if record.sale_line_ids:
                    record.date_approve = record.sale_line_ids[0].order_id.upload_date

                # if record.move_id.invoice_origin:
                #     sale_order = self.env['sale.order'].search(
                #         [('name', '=', record.move_id.invoice_origin)], limit=1
                #     )
                #     if sale_order:
                #         record.date_approve = sale_order.date_order

    @api.depends('move_id.move_type', 'move_id.invoice_date', 'purchase_order_id.download_date', 'move_id.invoice_origin')
    def _compute_date_download(self):
        print("compute_date_download------------------------------------")
        for record in self:
            record.date_download = False
            if record.move_id.move_type in ["in_invoice", "in_refund"]:
                for line in record.filtered("purchase_order_id"):
                    record.date_download = line.purchase_order_id.download_date
            elif record.move_id.move_type in ["out_invoice", "out_refund"]:
                if record.sale_line_ids:
                    record.date_download = record.sale_line_ids[0].order_id.download_date

                # if record.move_id.invoice_origin:
                #     sale_order = self.env['sale.order'].search(
                #         [('name', '=', record.move_id.invoice_origin)], limit=1
                #     )
                #     if sale_order:
                #         record.date_download = sale_order.download_date
