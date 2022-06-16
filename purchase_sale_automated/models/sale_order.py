# Copyright 2021 - Dario Cruz https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime

from odoo import _, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()

        for order in self.filtered(lambda order: order.supplier_id):
            purchase_order_id = self.env["purchase.order"].search([("origin", "=", order.name, )])
            if purchase_order_id:
                # raise ValidationError(_("Pedido anteriormente generado."))
                print("Pedido anteriormente generado.")
            else:
                order._create_purchase_order(order)
        return result

    def _create_purchase_order(self, order):
        PurchaseOrder = self.env["purchase.order"]
        values = order._purchase_prepare_order_values(order)
        purchase_order = PurchaseOrder.create(values)
        purchase_order.button_confirm()

        for line in order.order_line:
            line_values = order._purchase_prepare_line_order_values(purchase_order, line)
            purchase_order.env["purchase.order.line"].create(line_values)
        return purchase_order

    def _purchase_prepare_order_values(self, order):
        self.ensure_one()
        date_order = datetime.datetime.now()
        return {
            "partner_id": order.supplier_id.id,
            "company_id": self.company_id.id,
            # "currency_id": order.supplier_id.property_purchase_currency_id.id
            "origin": order.name,
            "payment_term_id": order.payment_term_id.id,
            "date_order": date_order,
        }

    def _purchase_prepare_line_order_values(self, purchase_order, line):
        self.ensure_one()
        # compute quantity from SO line UoM
        product_quantity = line.product_uom_qty
        purchase_qty_uom = line.product_uom._compute_quantity(
            product_quantity, line.product_id.uom_po_id
        )
        price_unit = 0.0
        date_planned = datetime.datetime.now()
        return {
            "name": "[%s] %s" % (line.product_id.default_code, line.name)
            if line.product_id.default_code
            else line.name,
            "product_qty": purchase_qty_uom,
            "product_id": line.product_id.id,
            "product_uom": line.product_id.uom_po_id.id,
            "price_unit": price_unit,
            "date_planned": date_planned,
            "taxes_id": None,
            "order_id": purchase_order.id,
            "sale_line_id": line.id,
        }





# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#
#     def write(self, values):
#         increased_lines = None
#         decreased_lines = None
#         increased_values = {}
#         decreased_values = {}
#         if "product_uom_qty" in values:
#             precision = self.env["decimal.precision"].precision_get(
#                 "Product Unit of Measure"
#             )
#             increased_lines = self.sudo().filtered(
#                 lambda r: r.product_id.is_product_sample
#                 and r.purchase_line_count
#                 and float_compare(
#                     r.product_uom_qty,
#                     values["product_uom_qty"],
#                     precision_digits=precision,
#                 )
#                 == -1
#             )
#             decreased_lines = self.sudo().filtered(
#                 lambda r: r.product_id.is_product_sample
#                 and r.purchase_line_count
#                 and float_compare(
#                     r.product_uom_qty,
#                     values["product_uom_qty"],
#                     precision_digits=precision,
#                 )
#                 == 1
#             )
#             increased_values = {
#                 line.id: line.product_uom_qty for line in increased_lines
#             }
#             decreased_values = {
#                 line.id: line.product_uom_qty for line in decreased_lines
#             }
#
#         result = super(SaleOrderLine, self).write(values)
#
#         if increased_lines:
#             increased_lines._purchase_increase_ordered_qty(
#                 values["product_uom_qty"], increased_values
#             )
#         if decreased_lines:
#             decreased_lines._purchase_decrease_ordered_qty(
#                 values["product_uom_qty"], decreased_values
#             )
#         return result
#
#     def _purchase_sample_create(self):
#         sale_line_purchase_map = {}
#         supplier_po_map = {}
#         for line in self:
#             line = line.with_company(line.company_id)
#             # determine vendor of the order (take the first matching company and product)
#             purchase_order = self._get_purchase_order(line)
#             # add a PO line to the PO
#             values = line._purchase_sample_prepare_line_values(purchase_order)
#             line.env["purchase.order.line"].create(values)
#             origins = []
#             if purchase_order.origin:
#                 origins = purchase_order.origin.split(", ") + origins
#             if line.order_id.name not in origins:
#                 origins += [line.order_id.name]
#                 purchase_order.write({"origin": ", ".join(origins)})
#             supplier_po_map[line.order_id.partner_id.id] = purchase_order
#             return sale_line_purchase_map
#
#     def _get_purchase_order(self, line):
#         PurchaseOrder = self.env["purchase.order"]
#         purchase_order = PurchaseOrder.search(
#             [
#                 ("partner_id", "=", line.order_id.partner_id.id),
#                 ("state", "=", "draft"),
#                 ("company_id", "=", line.company_id.id),
#             ],
#             limit=1,
#         )
#         if purchase_order:
#             return purchase_order
#         return self._create_purchase_order(line)
#
#     def _create_supplier_line(self, line):
#         self.ensure_one()
#         vals = [
#             ("name", "=", line.order_id.partner_id.id),
#             ("product_tmpl_id", "=", line.product_id.product_tmpl_id.id),
#         ]
#         have_supplier = self.env["product.supplierinfo"].search(vals)
#         if len(have_supplier) < 1:
#             self.env["product.supplierinfo"].sudo().create(
#                 {
#                     "name": line.order_id.partner_id.id,
#                     "product_tmpl_id": line.product_id.product_tmpl_id.id,
#                 }
#             )
#
#     def _create_purchase_order(self, line):
#         self._create_supplier_line(line)
#         PurchaseOrder = self.env["purchase.order"]
#         values = line._purchase_sample_prepare_order_values(line.order_id.partner_id)
#         purchase_order = PurchaseOrder.create(values)
#         purchase_order.button_confirm()
#         return purchase_order
#
#     def _purchase_sample_generation(self):
#         """Create a Purchase for the first time
#         from the sale line.
#          If the SO line already created a PO, it
#         will not create a second one.
#         """
#         sale_line_purchase_map = {}
#         for line in self:
#             # Do not regenerate PO line if the SO line has already
#             # created one in the past (SO cancel/reconfirmation case)
#             if line.product_id.is_product_sample:
#                 if not line.purchase_line_count:
#                     result = line._purchase_sample_create()
#                     sale_line_purchase_map.update(result)
#         return sale_line_purchase_map
#
#     def _purchase_sample_prepare_order_values(self, supplierinfo):
#         self.ensure_one()
#         date_order = datetime.datetime.now()
#         return {
#             "partner_id": supplierinfo.id,
#             "partner_ref": supplierinfo.ref,
#             "company_id": self.company_id.id,
#             "currency_id": supplierinfo.property_purchase_currency_id.id
#             or self.env.company.currency_id.id,
#             "dest_address_id": False,  # False since only supported in stock
#             "origin": self.order_id.name,
#             "payment_term_id": supplierinfo.property_supplier_payment_term_id.id,
#             "date_order": date_order,
#         }
#
#     def _purchase_sample_prepare_line_values(self, purchase_order, quantity=False):
#         self.ensure_one()
#         # compute quantity from SO line UoM
#         product_quantity = self.product_uom_qty
#         purchase_qty_uom = self.product_uom._compute_quantity(
#             product_quantity, self.product_id.uom_po_id
#         )
#         price_unit = 0.0
#         date_planned = datetime.datetime.now()
#         return {
#             "name": "[%s] %s" % (self.product_id.default_code, self.name)
#             if self.product_id.default_code
#             else self.name,
#             "product_qty": purchase_qty_uom,
#             "product_id": self.product_id.id,
#             "product_uom": self.product_id.uom_po_id.id,
#             "price_unit": price_unit,
#             "date_planned": date_planned,
#             "taxes_id": None,
#             "order_id": purchase_order.id,
#             "sale_line_id": self.id,
#         }
#
#     def _purchase_decrease_ordered_qty(self, new_qty, origin_values):
#         """Decrease the quantity from SO line will add a next
#         acitivities on the related purchase order
#         :param new_qty: new quantity (lower than the current
#         one on SO line), expressed
#             in UoM of SO line.
#         :param origin_values: map from sale line id to old
#         value for the ordered quantity (dict)
#         """
#         purchase_to_notify_map = {}  # map PO -> set(SOL)
#         last_purchase_lines = self.env["purchase.order.line"].search(
#             [("sale_line_id", "in", self.ids)]
#         )
#         for purchase_line in last_purchase_lines:
#             purchase_to_notify_map.setdefault(
#                 purchase_line.order_id, self.env["sale.order.line"]
#             )
#             purchase_to_notify_map[purchase_line.order_id] |= purchase_line.sale_line_id
#
#         # create next activity
#         for purchase_order, sale_lines in purchase_to_notify_map.items():
#             render_context = {
#                 "sale_lines": sale_lines,
#                 "sale_orders": sale_lines.mapped("order_id"),
#                 "origin_values": origin_values,
#             }
#             purchase_order._activity_schedule_with_view(
#                 "mail.mail_activity_data_warning",
#                 user_id=purchase_order.user_id.id or self.env.uid,
#                 views_or_xmlid="sale_purchase.exception_purchase_on_sale_quantity_decreased",
#                 render_context=render_context,
#             )
#
#     def _purchase_increase_ordered_qty(self, new_qty, origin_values):
#         """Increase the quantity on the related purchase lines
#         :param new_qty: new quantity (higher than the current one on SO line), expressed
#             in UoM of SO line.
#         :param origin_values: map from sale line id to old value for the ordered quantity (dict)
#         """
#         for line in self:
#             last_purchase_line = self.env["purchase.order.line"].search(
#                 [("sale_line_id", "=", line.id)], order="create_date DESC", limit=1
#             )
#             if last_purchase_line.state in [
#                 "draft",
#                 "sent",
#                 "to approve",
#             ]:  # update qty for draft PO lines
#                 quantity = line.product_uom._compute_quantity(
#                     new_qty, last_purchase_line.product_uom
#                 )
#                 last_purchase_line.write({"product_qty": quantity})
#             elif last_purchase_line.state in [
#                 "purchase",
#                 "done",
#                 "cancel",
#             ]:  # create new PO, by forcing the quantity as the difference from SO line
#                 quantity = line.product_uom._compute_quantity(
#                     new_qty - origin_values.get(line.id, 0.0),
#                     last_purchase_line.product_uom,
#                 )
#                 line._purchase_service_create(quantity=quantity)
