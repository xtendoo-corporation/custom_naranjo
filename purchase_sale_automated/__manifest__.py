# Copyright 2022 Xtendoo

{
    "name": "Purchase sale automated",
    "summary": """
        Purchase sale automated""",
    "version": "15.0",
    "depends": [
        "base",
        "sale",
        "purchase",
    ],
    "maintainers": ["dariocruzmauro"],
    "author": "Xtendoo",
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order.xml"
            ],
    "installable": True,
    "auto_install": True,
}

