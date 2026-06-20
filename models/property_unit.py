from odoo import fields, models, api


class PropertyUnit(models.Model):
    _name = 'property.unit'
    _description = 'Property Unit'
    _rec_name = 'property_code'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    property_code = fields.Char(string='Property Code', readonly=True, copy=False, default='New')
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land'),
        ('office', 'Office'),
        ('shop', 'Shop')
    ], string='Property Type', tracking=True)
    governorate = fields.Char(string='Governorate',tracking=True)
    area = fields.Char(string='Area',tracking=True)
    address = fields.Char(string='Address',tracking=True)
    floor = fields.Char(string='Floor',tracking=True)
    area_size = fields.Float(string='Area Size (sqm)',tracking=True)
    price = fields.Float(string='Price',tracking=True)
    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('installment', 'Installment')
    ], string='Payment Type',tracking=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold',)
    ], string='Status', default='available',tracking=True)
    notes = fields.Text(string='Notes',tracking=True)
    image = fields.Image(string='Image',tracking=True)
    owner_id = fields.Many2one('property.owner', string='Owner',tracking=True)

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

    def open_price_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Search by Price',
            'res_model': 'property.price.search.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
