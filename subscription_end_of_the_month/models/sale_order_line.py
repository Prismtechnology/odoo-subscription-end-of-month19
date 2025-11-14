# -*- coding: utf-8 -*-

import calendar
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.tools.misc import format_date


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        """Override to adjust invoice line description for current month invoicing and prevent deferred revenue."""
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)
        
        # Note: start_date and end_date removal is handled in account.move.line model
        
        # Only modify descriptions for current_month invoices
        if (self.order_id.invoice_timing == 'current_month' and 
            self.order_id.plan_id and 
            (self.recurring_invoice or self.order_id.subscription_state == '7_upsell')):
            
            # Calculate the billing period based on the plan
            billing_period_value = self.order_id.plan_id.billing_period_value or 1
            billing_period_unit = self.order_id.plan_id.billing_period_unit or 'month'
            next_invoice_date = self.order_id.next_invoice_date or fields.Date.today()
            
            # Calculate period_end (last day of current billing month)
            period_end_month = next_invoice_date
            last_day = calendar.monthrange(period_end_month.year, period_end_month.month)[1]
            period_end = period_end_month.replace(day=last_day)
            
            # Calculate period_start based on billing period
            if billing_period_unit == 'day':
                period_start = period_end - timedelta(days=billing_period_value - 1)
            elif billing_period_unit == 'week':
                period_start = period_end - timedelta(weeks=billing_period_value)
                period_start = period_start.replace(day=1)  # Start at 1st of month
            elif billing_period_unit == 'month':
                # Go back X months from period_end and start at 1st of that month
                temp_start = period_end - relativedelta(months=billing_period_value - 1)
                period_start = temp_start.replace(day=1)
            elif billing_period_unit == 'year':
                temp_start = period_end - relativedelta(years=billing_period_value)
                period_start = temp_start.replace(day=1)
            else:
                # Fallback: 1 month
                period_start = period_end.replace(day=1)
            
            # Get the original description without the period part
            description = res.get('name') or self.name
            
            # Extract base product name (remove existing period information)
            if '\n' in description:
                base_description = description.split('\n')[0]
            else:
                base_description = description
            
            # Format the period for billing
            lang_code = self.order_id.partner_id.lang
            duration = self.order_id.plan_id.billing_period_display
            format_start = format_date(self.env, period_start, lang_code=lang_code)
            format_end = format_date(self.env, period_end, lang_code=lang_code)
            start_to_end = _("%(start)s to %(end)s", start=format_start, end=format_end)
            
            # Update the description with the calculated period
            res['name'] = f"{base_description}\n{duration} ({start_to_end})"
        
        return res
