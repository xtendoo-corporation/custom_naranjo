# Copyright 2021 - Dario Cruz https://xtendoo.es/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_purchase_order_created = fields.Boolean(
        "Purchase Order Already Created",
    )

    def _action_confirm(self):
        self.is_purchase_order_created = None

        result = super(SaleOrder, self)._action_confirm()

        for order in self.filtered(lambda order: order.supplier_id):

            print("*"*80)
            print("Action confirm", bool(self.env["purchase.order"].search([("origin", "=", order.name,)])))
            print("is_purchase_order_created", order.is_purchase_order_created)
            print("*"*80)

            order.is_purchase_order_created = bool(self.env["purchase.order"].search([("origin", "=", order.name,)]))

            print("is_purchase_order_created 2", order.is_purchase_order_created)


            if not order.is_purchase_order_created:
                order._create_purchase_order(order)

            # purchase_order_id = self.env["purchase.order"].search([("origin", "=", order.name, )])
            # self._is_purchase_order_created(order)
            # if purchase_order_id:
            #     # return {'warning': {
            #     #     'title': ("Pedido anteriormente generado."),
            #     #     'message': "Pedido anteriormente generado."
            #     # }}
            #     # raise ValidationError(_("Pedido anteriormente generado."))
            #     print("*******************************Pedido anteriormente generado.***************************")
            # else:
            #
        return result

    @api.onchange('is_purchase_order_created')
    def onchange_purchase_order_created(self):

        print("*" * 80)
        print("ONCHANGE")
        print("*" * 80)

        if self.is_purchase_order_created:

            print("*"*80)
            print("Cambio de purchase")
            print("*"*80)

            return {'warning': {
                'title': _('Warning'),
                'message': "Pedido anteriormente generado."
            }}

    def _create_purchase_order(self, order):
        PurchaseOrder = self.env["purchase.order"]
        values = order._purchase_prepare_order_values(order)
        purchase_order = PurchaseOrder.create(values)
        purchase_order.button_confirm()

        for line in order.order_line:
            line_values = order._purchase_prepare_line_order_values(purchase_order, line)
            purchase_order.env["purchase.order.line"].create(line_values)
        return purchase_order

    def _is_purchase_order_created(self, order):
        purchase_order_id = self.env["purchase.order"].search([("origin", "=", order.name,)])
        if purchase_order_id:
            return {'warning': {
                'title': ("Pedido anteriormente generado."),
                'message': "Pedido anteriormente generado."
            }}



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
