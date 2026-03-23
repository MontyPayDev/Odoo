{
    "name": "MontyPay",
    "version": "19.0.1.0.0",
    "category": "Accounting/Payment Providers",
    "sequence": 350,
    "summary": "Integrate MontyPay as a payment provider in Odoo.",
    "description": """
MontyPay Payment Provider
=========================

This module integrates MontyPay with Odoo and allows merchants to
process online payments through the MontyPay platform.
""",
    "author": "MontyPay Technical Team",
    "website": "https://www.montypay.com",
    "license": "LGPL-3",
    "depends": ["payment"],
    "data": [
        "data/payment_provider_data.xml",
        "data/payment_method_data.xml",
        "views/payment_provider_views.xml",
        "views/payment_montypay_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
