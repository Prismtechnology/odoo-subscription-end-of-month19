# -*- coding: utf-8 -*-

import calendar
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

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

    def _post(self, soft=True):
        """Override to calculate next_invoice_date based on billing period after invoice posting."""
        # Call parent method first
        result = super()._post(soft=soft)
        
        # After invoice posting, calculate next_invoice_date using billing period
        # ONLY for current_month timing mode
        for move in self:
            if move.invoice_origin:
                subscription = self.env['sale.order'].search([
                    ('name', '=', move.invoice_origin),
                    ('plan_id', '!=', False),
                    ('invoice_timing', '=', 'current_month')
                ], limit=1)
                
                if subscription and subscription.plan_id:
                    # Use billing period from plan
                    val = subscription.plan_id.billing_period_value or 1
                    unit = (subscription.plan_id.billing_period_unit or 'month').lower()
                    # Use today as base instead of current next_invoice_date to avoid double increment
                    base = fields.Date.today()
                    
                    if unit == 'day':
                        next_date = base + timedelta(days=val)
                    elif unit == 'week':
                        next_date = base + timedelta(weeks=val)
                    elif unit == 'month':
                        next_date = base + relativedelta(months=val)
                        # For monthly billing, set to last day of the target month
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
                    
                    subscription.next_invoice_date = next_date
        
        return result
    
    #####################################################
    #                     Actions                       #
    #####################################################
