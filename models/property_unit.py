import string

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PropertyUnit(models.Model):
    _name = 'property.unit'
    _description = 'Property Unit'
    _rec_name = 'property_code'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    property_code = fields.Char(string='Property Code', readonly=True, copy=False, default='New')
    property_for = fields.Selection([
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ], string="Property For", tracking=True, required=True)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land'),
        ('office', 'Office'),
        ('shop', 'Shop')
    ], string='Property Type', tracking=True)
    # governorate = fields.Char(string='Governorate', tracking=True)
    # address = fields.Char(string='Address', tracking=True)

    governorate_id = fields.Many2one('property.location', string='Governorate', domain=[('type', '=', 'governorate')],
                                     invisible=True)

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

    owner_price = fields.Float(string="Owner Price")
    commission = fields.Float(string="Commission")

    paid_to_owner = fields.Float(string="Paid to Owner")
    paid_to_owner_date = fields.Date(string="Payment Date")
    remaining_to_owner = fields.Float(
        string="Remaining Amount",
        compute="_compute_remaining",
        store=True
    )
    profit = fields.Float(
        string="Profit",
        compute="_compute_profit",
        store=True
    )

    posted_by_id = fields.Many2one(
        'res.users',
        string="Posted By (Sales Agent)"
    )

    posted_date = fields.Date(string="Posted Date")
    due_payment_date = fields.Date(string="Due Payment Date")

    _sql_constraints = [
        ('unique_property_code',
         'unique(property_code)',
         'Property code must be unique!')
    ]

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['posted_by_id'] = self.env.user.id
        return res

    @api.depends('owner_price', 'paid_to_owner')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining_to_owner = rec.owner_price - rec.paid_to_owner

    @api.depends('price', 'owner_price', 'commission')
    def _compute_profit(self):
        for rec in self:
            rec.profit = rec.price - rec.owner_price - rec.commission

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
                    "⚠️ يوجد عقار مشابه بالفعل. يرجى مراجعة السجلات الموجودة."
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

    def action_create_due_payment_reminder(self):

        activity_type = self.env.ref('mail.mail_activity_data_todo')
        model_id = self.env['ir.model']._get('property.unit').id

        for rec in self:

            # =========================
            # 1. Prevent duplicates
            # =========================
            existing_activity = self.env['mail.activity'].search([
                ('res_model_id', '=', model_id),
                ('res_id', '=', rec.id),
                ('summary', '=', '💰 Owner Payment Due Reminder'),
            ], limit=1)

            if not existing_activity:
                # =========================
                # 2. Create Activity
                # =========================
                self.env['mail.activity'].create({
                    'activity_type_id': activity_type.id,
                    'res_model_id': model_id,
                    'res_id': rec.id,
                    'summary': '💰 Owner Payment Due Reminder',
                    'note': (
                        f"Payment is due for property: {rec.property_code}\n"
                        f"Amount: {rec.owner_price}\n"
                        f"Due Date: {rec.due_payment_date}"
                    ),
                    'user_id': rec.posted_by_id.id or self.env.user.id,
                    'date_deadline': rec.due_payment_date,
                })

            # =========================
            # 3. Notification (Bell + Chatter)
            # =========================
            rec.message_post(
                body=f"""
                    <b>💰 Owner Payment Due Reminder</b><br/>
                    Property: {rec.property_code}<br/>
                    Amount: {rec.owner_price}<br/>
                    Due Date: {rec.due_payment_date}
                """,
                partner_ids=[rec.posted_by_id.partner_id.id] if rec.posted_by_id else [],
                message_type='notification',
            )

    @api.model
    def _cron_due_payment_reminders(self):

        today = fields.Date.today()

        records = self.search([
            ('due_payment_date', '=', today)
        ])

        for rec in records:
            rec.action_create_due_payment_reminder()
