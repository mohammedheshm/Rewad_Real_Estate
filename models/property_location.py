from odoo import models, fields


class PropertyLocation(models.Model):
    _name = 'property.location'
    _description = 'Property Location'

    name = fields.Char(required=True)
    type = fields.Selection([
        ('governorate', 'Governorate'),
        ('address', 'Address'),
    ], required=True)
