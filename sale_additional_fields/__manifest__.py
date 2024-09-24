# Copyright 2022 Xtendoo

{
    "name": "Sale Additional Fields",
    "summary": """
        Sale Additional Fields""",
    "version": "15.0",
    "depends": [
        "sale_management",
        "contacts",
        "purchase",
    ],
    "maintainers": ["dariocruzmauro"],
    "author": "Xtendoo",
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/account_move.xml",
        "views/sale_order.xml",
        "views/purchase_order_views.xml",
        "views/res_partner_view.xml",
        "views/licence_car_view.xml",
        "views/purchase_view_kpis_tree.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": True,
}

