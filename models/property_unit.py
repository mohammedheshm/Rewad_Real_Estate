from odoo import fields, models, api
from odoo.exceptions import ValidationError


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
    # governorate = fields.Char(string='Governorate', tracking=True)
    # address = fields.Char(string='Address', tracking=True)

    governorate_id = fields.Many2one('property.location', string='Governorate', domain=[('type', '=', 'governorate')])

    address_id = fields.Many2one('property.location', string='Address', domain=[('type', '=', 'address')])

    floor = fields.Char(string='Floor', tracking=True)
    area_size = fields.Float(string='Area Size (sqm)', tracking=True)
    price = fields.Float(string='Price', tracking=True)
    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('installment', 'Installment')
    ], string='Payment Type', tracking=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold',)
    ], string='Status', default='available', tracking=True)
    notes = fields.Text(string='Notes', tracking=True)
    image = fields.Image(string='Image', tracking=True)
    owner_id = fields.Many2one('property.owner', string='Owner', tracking=True)

    _sql_constraints = [
        ('unique_property_code',
         'unique(property_code)',
         'Property code must be unique!')
    ]

    @api.constrains('address_id', 'floor', 'area_size')
    def _check_duplicate(self):
        for rec in self:

            duplicate = self.search([
                ('address_id', '=', rec.address_id.id),
                ('floor', '=', rec.floor),
                ('area_size', '=', rec.area_size),
                ('id', '!=', rec.id),
            ], limit=1)

            if duplicate:
                raise ValidationError(
                    "⚠️ Similar property already exists. Please check existing records."
                )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            if vals.get('property_code', 'New') == 'New':
                vals['property_code'] = self.env['ir.sequence'].next_by_code('property_seq')

            if vals.get('governorate_id') and isinstance(vals['governorate_id'], str):

                name = vals['governorate_id']

                loc = self.env['property.location'].search([
                    ('name', '=', name),
                    ('type', '=', 'governorate')
                ], limit=1)

                if not loc:
                    loc = self.env['property.location'].create({
                        'name': name,
                        'type': 'governorate'
                    })

                vals['governorate_id'] = loc.id

            if vals.get('address_id') and isinstance(vals['address_id'], str):

                name = vals['address_id']

                loc = self.env['property.location'].search([
                    ('name', '=', name),
                    ('type', '=', 'address')
                ], limit=1)

                if not loc:
                    loc = self.env['property.location'].create({
                        'name': name,
                        'type': 'address'
                    })

                vals['address_id'] = loc.id

        return super(PropertyUnit, self).create(vals_list)

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
