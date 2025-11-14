# -*- coding: utf-8 -*-

import calendar
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    invoice_timing = fields.Selection([
        ('regular', 'Regular'),
        ('current_month', 'Current Month')
    ], string='Invoice Timing', default='current_month',
       help='Choose when and how to generate subscription invoices:\n\n'
            '• Regular: Standard Odoo behavior - invoices are generated at the beginning '
            'of each billing period for upcoming services\n\n'
            '• Current Month: The invoice is created on the scheduled invoice date, '
            'but the billing period covers the current month (from 1st to last day of the month '
            'containing the invoice date)\n\n'
            'Example with invoice date June 30th:\n'
            '- Regular: Invoice on June 1st for June 1-30 services\n'
            '- Current Month: Invoice on June 30th for June 1-30 services (current month period)')

    @api.depends('plan_id')
    def _compute_invoice_timing_visible(self):
        """Show invoice timing field only for subscription orders."""
        for order in self:
            order.invoice_timing_visible = bool(order.plan_id)

    invoice_timing_visible = fields.Boolean(
        string='Invoice Timing Visible',
        compute='_compute_invoice_timing_visible',
        help='Technical field to show/hide invoice timing based on subscription plan'
    )

    #####################################################
    #                     Fields                       #
    #####################################################

    #####################################################
    #                      Model                       #
    #####################################################
     
    #####################################################
    #                     Constrains                    #
    #####################################################
     
    #####################################################
    #                     OnChange                      #
    #####################################################
    
    #####################################################
    #                     Compute                       #
    #####################################################
            
    #####################################################
    #                    Functions                      #
    #####################################################

    def _prepare_next_invoice_date(self, subscription_plan, period_start):
        """Override to calculate next invoice date based on billing period from plan."""
        # Apply custom logic ONLY for current_month timing mode
        if self.plan_id and subscription_plan and self.invoice_timing == 'current_month':
            
            # Get billing period from the plan
            billing_period_value = subscription_plan.billing_period_value or 1
            billing_period_unit = subscription_plan.billing_period_unit or 'month'
            
            # Use current next_invoice_date as base, or today if not set
            base_date = self.next_invoice_date or fields.Date.today()
            
            # Calculate next invoice date based on billing period
            if billing_period_unit == 'day':
                next_date = base_date + timedelta(days=billing_period_value)
            elif billing_period_unit == 'week':
                next_date = base_date + timedelta(weeks=billing_period_value)
            elif billing_period_unit == 'month':
                next_date = base_date + relativedelta(months=billing_period_value)
                # For monthly billing, set to last day of the target month
                last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                next_date = next_date.replace(day=last_day)
            elif billing_period_unit == 'year':
                next_date = base_date + relativedelta(years=billing_period_value)
                # For yearly billing, set to last day of the target month
                last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                next_date = next_date.replace(day=last_day)
            else:
                # Fallback to monthly if unit is unknown
                next_date = base_date + relativedelta(months=billing_period_value)
                last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                next_date = next_date.replace(day=last_day)
                
            return next_date
        else:
            # Fall back to standard behavior for non-subscription orders
            return super()._prepare_next_invoice_date(subscription_plan, period_start)

    def _update_next_invoice_date(self):
        """Override to calculate next invoice date based on billing period from plan."""
        # Process subscription orders with custom logic ONLY for current_month timing
        for order in self.filtered(lambda o: o.plan_id and o.invoice_timing == 'current_month'):
            val = order.plan_id.billing_period_value or 1
            unit = (order.plan_id.billing_period_unit or 'month').lower()
            base = order.next_invoice_date or fields.Date.today()

            if unit == 'day':
                next_date = base + timedelta(days=val)
            elif unit == 'week':
                next_date = base + timedelta(weeks=val)
            elif unit == 'month':
                next_date = base + relativedelta(months=val)
                # option: dernier jour du mois cible
                last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                next_date = next_date.replace(day=last_day)
            elif unit == 'year':
                next_date = base + relativedelta(years=val)
                last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                next_date = next_date.replace(day=last_day)
            else:
                # fallback: mensuel
                next_date = base + relativedelta(months=val)
                last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                next_date = next_date.replace(day=last_day)

            order.next_invoice_date = next_date
            order.last_reminder_date = False
                
        # Process orders with standard logic (non-subscription OR regular timing)
        standard_orders = self.filtered(lambda o: not o.plan_id or o.invoice_timing != 'current_month')
        if standard_orders:
            super(SaleOrderInherit, standard_orders)._update_next_invoice_date()
    
    #####################################################
    #                     Actions                       #
    #####################################################