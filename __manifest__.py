{
    "name": "RouteXpert Transportation Management System",
    "author":"Ahmed Eid Abdallah",
    "category":"",
    "version":"17.0.0.1.0",
    "depends":["base"],
    "data":[
        "security/ir.model.access.csv",
        "views/base_menu.xml",
        "views/drivers_applications_view.xml",
        "views/vehicles_view.xml",
        "views/drivers_applications_website_template.xml",

        ],
    "assets":{
        "web.assets_frontend":[
            "transport_system/static/src/css/frontend/drivers_application_styling.css",
        ]
    },

    "application":True,




}