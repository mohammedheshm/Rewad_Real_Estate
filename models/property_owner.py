from odoo import fields, models


class PropertyOwner(models.Model):
    _name = 'property.owner'
    _description = 'Property Owner'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Owner Name', required=True,tracking=True)
    mobile = fields.Char(string='Mobile Number',tracking=True)
    notes = fields.Text(string='Notes',tracking=True)
    property_ids = fields.One2many('property.unit', 'owner_id', string='Properties',tracking=True)

    property_count = fields.Integer(compute="_compute_property_count",tracking=True)

    def _compute_property_count(self):
        for rec in self:
            rec.property_count = self.env['property.unit'].search_count([
                ('owner_id', '=', rec.id),
            ])

    def action_view_properties(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'res_model': 'property.unit',
            'view_mode': 'tree,form',
            'domain': [('owner_id', '=', self.id)],
            'context': {'default_owner_id': self.id},
        }
