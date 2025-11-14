# -*- coding: utf-8 -*-
{
    'name': 'Subscription End of the Month',
    'version': '1.1.2',
    'summary': 'Invoice subscriptions at the end of month for the current month period',
    'description': """
Allows you to invoice subscriptions at the end of the month for the current month period.
    """,
    'category': 'Sales/Subscriptions',
    'author': 'Nicolas Brouwers',
    'website': '',
    'license': 'LGPL-3',
    'price': 39.00,
    'currency': 'EUR',
    'support': 'nicolas.b.95@hotmail.com',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale_subscription'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
