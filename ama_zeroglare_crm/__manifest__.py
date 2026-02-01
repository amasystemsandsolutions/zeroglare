# -*- coding: utf-8 -*-
{
    'name': "A M A CRM",
    'version': '19.0.1.0.0',
    "version": "18.1",
    "license": "AGPL-3",
    "author": "A M A Systems and Solutions",
    "website": "https://amasystemsandsolutions.com/",
    'depends': ['base', 'crm', 'mail', 'uom'],
    'category': 'Sales',
    'data': [
        'security/ir.model.access.csv',

        'views/crm_estimation_views.xml',
        'views/shipping_mode_views.xml',
        'views/menu_views.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False
}
