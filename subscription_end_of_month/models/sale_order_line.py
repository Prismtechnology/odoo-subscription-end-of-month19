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
            
            # Use next_invoice_date to determine which month to bill
            next_invoice_date = self.order_id.next_invoice_date
            if next_invoice_date:
                # For current_month, we bill for the month of the next_invoice_date
                # Example: if next_invoice_date is 30/06/2025, we bill for June 2025 (01/06 to 30/06)
                target_month = next_invoice_date
                
                # Get the first and last day of the target month
                period_start = target_month.replace(day=1)
                last_day_of_month = calendar.monthrange(target_month.year, target_month.month)[1]
                period_end = target_month.replace(day=last_day_of_month)
            else:
                # Fallback: use current month if no next_invoice_date
                today = fields.Date.today()
                period_start = today.replace(day=1)
                last_day_of_month_num = calendar.monthrange(today.year, today.month)[1]
                period_end = today.replace(day=last_day_of_month_num)
            
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
