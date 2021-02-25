# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _default_order_type(self):
        return self.env['purchase.order.type'].search([], limit=1)

    order_type = fields.Many2one(comodel_name='purchase.order.type',
                                 readonly=False,
                                 states=Purchase.READONLY_STATES,
                                 string='Type',
                                 ondelete='restrict',
                                 default=_default_order_type)

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super().onchange_partner_id()
        purchase_type = (self.partner_id.purchase_type or
                         self.partner_id.commercial_partner_id.purchase_type)
        if purchase_type:
            self.order_type = purchase_type

    @api.multi
    @api.onchange('order_type')
    def onchange_order_type(self):
        for order in self:
            if order.order_type.payment_term_id:
                order.payment_term_id = order.order_type.payment_term_id.id
            if order.order_type.incoterm_id:
                order.incoterm_id = order.order_type.incoterm_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/' and vals.get('order_type'):
            purchase_type = self.env['purchase.order.type'].browse(
                vals['order_type'])
            if purchase_type.sequence_id:
                vals['name'] = purchase_type.sequence_id.next_by_id()
        return super().create(vals)
