# Copyright 2022 Xtendoo

{
    "name": "Sale Additional Fields",
    "summary": """
        Sale Additional Fields""",
    "version": "15.0",
    "depends": ["sale_management", "purchase"],
    "maintainers": ["dariocruzmauro"],
    "author": "Xtendoo",
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order.xml",
        "views/purchase_order_views.xml"
            ],
    "installable": True,
    "auto_install": True,
}

