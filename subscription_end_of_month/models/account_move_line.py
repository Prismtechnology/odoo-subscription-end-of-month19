# -*- coding: utf-8 -*-

import calendar
from odoo import api, fields, models


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    #####################################################
    #                     Fields                       #
    #####################################################

    #####################################################
    #                      Model                       #
    #####################################################

    @api.model_create_multi
    def create(self, vals_list):
        """Override to set correct deferred dates for current_month subscription invoices."""
        for vals in vals_list:
            if vals.get('move_id'):
                move = self.env['account.move'].browse(vals['move_id'])
                # Check if this is a subscription invoice from an order with current_month timing
                if (move.invoice_origin and 
                    self.env['sale.order'].search([
                        ('name', '=', move.invoice_origin),
                        ('invoice_timing', '=', 'current_month'),
                        ('plan_id', '!=', False)
                    ], limit=1)):
                    # Set deferred dates to current month period (1st to last day)
                    today = fields.Date.today()
                    month_start = today.replace(day=1)
                    last_day = calendar.monthrange(today.year, today.month)[1]
                    month_end = today.replace(day=last_day)
                    
                    vals['deferred_start_date'] = month_start
                    vals['deferred_end_date'] = month_end
        
        return super().create(vals_list)

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
    
    #####################################################
    #                     Actions                       #
    #####################################################
