# -*- coding: utf-8 -*-
{
    'name': 'Subscription End of Month Invoicing',
    'version': '1.1.1',
    'summary': 'Invoice subscriptions at the end of month for the current month period',
    'description': """
🗓️ **Professional End-of-Month Subscription Billing**

Transform your subscription billing workflow with precise end-of-month invoicing that aligns with your business needs.

**✨ Key Benefits:**
• **Simplified Accounting**: Bill for completed services at month-end
• **Better Cash Flow**: Invoice for delivered services, not future commitments  
• **Accurate Revenue Recognition**: Deferred revenue automatically calculated for current month periods
• **Professional Presentation**: Clean invoices with proper date ranges

**🚀 Features:**
• **Flexible Invoice Timing**: Choose between Regular or Current Month billing modes
• **Smart Date Management**: Automatic calculation of month periods (1st to last day)
• **Cron Protection**: Bulletproof logic that preserves your end-of-month dates
• **Seamless Integration**: Works perfectly with existing Odoo subscription workflows

**💼 Perfect For:**
- Service companies billing monthly
- SaaS businesses with month-end billing cycles  
- Consultancy firms tracking monthly deliveries
- Any business requiring precise monthly billing periods

**🔧 Technical Excellence:**
- Zero conflicts with standard Odoo functionality
- Robust protection against system overrides
- Clean, maintainable code following Odoo best practices
- Full compatibility with Odoo 18 subscription system

Transform your subscription billing today - professional, precise, and perfectly integrated.
    """,
    'category': 'Sales/Subscriptions',
    'author': 'Nicolas Brouwers',
    'website': '',
    'license': 'LGPL-3',
    'price': 39.00,
    'currency': 'EUR',
    'support': 'nicolas.b.95@hotmail.com',
    'depends': ['sale_subscription'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
