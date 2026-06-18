from odoo import api, fields, models


class PropertyPriceSearchWizard(models.TransientModel):
    _name = 'property.price.search.wizard'
    _description = 'Property Price Search Wizard'

    price_from = fields.Float(string="Price From")
    price_to = fields.Float(string="Price To")

    def action_search(self):
        domain = []
        if self.price_from:
            domain.append(('price', '>=', self.price_from))
        if self.price_to:
            domain.append(('price', '<=', self.price_to))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Properties',
            'res_model': 'property.unit',
            'view_mode': 'tree,form',
            'domain': domain,
        }
