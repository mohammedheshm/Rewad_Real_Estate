from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyLead(models.Model):
    _name = 'property.lead'
    _description = 'Property Lead'
    _rec_name = 'name'

    lead_code = fields.Char(string='Lead Code', default='New', readonly=True, copy=False)
    name = fields.Char(string='Customer Name', required=True)
    mobile = fields.Char(string='Mobile Number', required=True)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land'),
        ('office', 'Office'),
        ('shop', 'Shop')
    ], string='Required Property Type')

    required_area = fields.Char(string='Required Area')
    budget = fields.Float(string='Budget')

    status = fields.Selection([
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('closed', 'Closed')
    ], string='Lead Status', default='new')

    notes = fields.Text(string='Notes')

    followup_ids = fields.One2many(
        'property.followup',
        'lead_id',
        string='Follow Ups'
    )

    property_unit_id = fields.Many2one(
        'property.unit',
        string='Selected Property'
    )

    def action_set_new(self):
        self.status = 'new'

    def action_set_contacted(self):
        self.status = 'contacted'

    def action_set_interested(self):
        self.status = 'interested'

    def action_set_not_interested(self):
        self.status = 'not_interested'

    def action_set_closed(self):
        self.status = 'closed'

    @api.model
    def create(self, vals):
        if vals.get('lead_code', 'New') == 'New':
            vals['lead_code'] = self.env['ir.sequence'].next_by_code('lead_seq')
        return super(PropertyLead, self).create(vals)

    def action_mark_as_sold(self):
        for rec in self:

            if not rec.property_unit_id:
                raise UserError("Please select a property first.")

            property_unit = rec.property_unit_id

            if property_unit.status == 'sold':
                raise UserError("Sorry, this property is already SOLD.")

            if property_unit.status == 'reserved':
                raise UserError("Sorry, this property is RESERVED and cannot be sold directly.")

            if property_unit.status == 'available':
                property_unit.status = 'sold'
                rec.status = 'closed'
                return

            raise UserError("Invalid property status.")
