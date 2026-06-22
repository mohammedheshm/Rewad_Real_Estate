from odoo import fields, models, api


class PropertyOwner(models.Model):
    _name = 'property.owner'
    _description = 'Property Owner'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Owner Name', required=True, tracking=True)
    mobile = fields.Char(string='Mobile Number', tracking=True)
    notes = fields.Text(string='Notes', tracking=True)
    property_ids = fields.One2many('property.unit', 'owner_id', string='Properties', tracking=True)

    property_count = fields.Integer(compute="_compute_property_count", tracking=True)

    total_value = fields.Float(
        string="Total Properties Value",
        compute="_compute_totals",
        store=True
    )

    total_paid = fields.Float(
        string="Total Paid",
        compute="_compute_totals",
        store=True
    )

    total_remaining = fields.Float(
        string="Total Remaining",
        compute="_compute_totals",
        store=True
    )

    total_commission = fields.Float(
        string="Total Commission",
        compute="_compute_totals",
        store=True
    )

    @api.depends('property_ids.owner_price',
                 'property_ids.paid_to_owner',
                 'property_ids.commission')
    def _compute_totals(self):
        for rec in self:
            rec.total_value = sum(rec.property_ids.mapped('owner_price'))
            rec.total_paid = sum(rec.property_ids.mapped('paid_to_owner'))
            rec.total_commission = sum(rec.property_ids.mapped('commission'))
            rec.total_remaining = rec.total_value - rec.total_paid

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
