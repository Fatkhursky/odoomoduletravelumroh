# -*- coding: utf-8 -*-

{
    'name': "Travel Umroh",

    'summary': """ Modul yang berfungsi untuk mengelola bisnis travel umroh """,

    'description': """
        Modul ini memiliki fitur :
        1. blablabla
        2. loremipsum
    """,

    'author': "PT. Ismata Nusantara Abadi",

    'website': "https://ismata.co.id/",

    'category': 'Services',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'mrp', 'sale_management', 'report_xlsx'],

    # always loaded
    'data': [
        'report/report_travel_invoice.xml',
        'report/report_travel_umroh.xml',
        'security/security.xml',
        'security/ir.model.access.csv',     
        'report/report_action.xml',
        'views/jamaah_views.xml',
        'views/hotels_views.xml',
        'views/airlines_views.xml',
        'views/travel_package_views.xml',
        'views/sale_order_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence.xml',
        


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

     'application': True,
}
