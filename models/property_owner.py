from odoo import fields, models


class PropertyOwner(models.Model):
    _name = 'property.owner'
    _description = 'Property Owner'
    _rec_name = 'name'

    name = fields.Char(string='Owner Name', required=True)
    mobile = fields.Char(string='Mobile Number')
    notes = fields.Text(string='Notes')
    property_ids = fields.One2many('property.unit', 'owner_id', string='Properties')
    