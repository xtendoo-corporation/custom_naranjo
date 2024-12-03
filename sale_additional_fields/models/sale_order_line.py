# Copyright 2023 - Jaime Millan https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ip_number = fields.Char(
        string='IP number',
        compute="_compute_ip_number",
    )
    download_date = fields.Date(
        string='Download Date',
        related='order_id.download_date',
    )
    upload_date = fields.Date(
        string='Upload Date',
        related='order_id.upload_date',
    )

    @api.depends("order_id.ip_number")
    def _compute_ip_number(self):
        for s in self:
            s.ip_number = s.order_id.ip_number
