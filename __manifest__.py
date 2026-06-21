{
    'name': "Rewad Real estate App",
    'author': "Mohammed Hesham",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'contacts', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/property_sequence.xml',
        'data/lead_sequence.xml',
        'views/rewad_real_estate_menu.xml',
        'views/property_unit_view.xml',
        'views/property_owner_view.xml',
        'views/property_lead_views.xml',
        'views/property_followup_views.xml',
        'wizard/price_search_wizard_view.xml',
        'reports/property_report.xml',
        'reports/lead_report.xml',
        'reports/followup_report.xml',

    ],
    'application': True,
}
