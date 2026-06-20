from odoo import api, models, fields


class PropertyFollowUp(models.Model):
    _name = 'property.followup'
    _description = 'Property Follow Up'
    _rec_name = 'lead_id'
    _order = 'follow_up_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    lead_id = fields.Many2one(
        'property.lead',
        string='Lead',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    follow_up_date = fields.Date(
        string='Follow Up Date',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    follow_up_notes = fields.Text(string='Follow Up Notes', tracking=True)
    next_follow_up_date = fields.Date(string='Next Follow Up Date', tracking=True)
