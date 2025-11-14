# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleSubscriptionPlanInherit(models.Model):
    _inherit = 'sale.subscription.plan'

    invoice_timing = fields.Selection([
        ('regular', 'Regular'),
        ('current_month', 'Current Month')
    ], string='Invoice Timing', default='current_month')
    
    def _prepare_order_values(self, order):
        """Inherit to add invoice_timing preference to new subscription orders."""
        res = super()._prepare_order_values(order)
        res.update({
            'invoice_timing': self.invoice_timing
        })
        return res
