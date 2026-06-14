from odoo import fields, models, api


class PropertyUnit(models.Model):
    _name = 'property.unit'
    _description = 'Property Unit'
    _rec_name = 'property_code'

    property_code = fields.Char(string='Property Code', required=True, copy=False, default='New')
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land'),
        ('office', 'Office'),
        ('shop', 'Shop')
    ], string='Property Type')
    governorate = fields.Char(string='Governorate')
    area = fields.Char(string='Area')
    address = fields.Char(string='Address')
    floor = fields.Char(string='Floor')
    area_size = fields.Float(string='Area Size (sqm)')
    price = fields.Float(string='Price')
    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('installment', 'Installment')
    ], string='Payment Type')
    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold')
    ], string='Status', default='available')
    notes = fields.Text(string='Notes')
    image = fields.Image(string='Image')
    owner_id = fields.Many2one('property.owner', string='Owner')

    @api.model
    def create(self, vals):
        if vals.get('property_code', 'New') == 'New':
            vals['property_code'] = self.env['ir.sequence'].next_by_code('property_seq')
        return super(PropertyUnit, self).create(vals)

    def action_available(self):
        self.status = 'available'

    def action_reserved(self):
        self.status = 'reserved'

    def action_sold(self):
        self.status = 'sold'
