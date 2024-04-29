from odoo import fields, models, api
from datetime import datetime, timedelta
class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "EState Proprety Offer model"

    price = fields.Float("Price")
    status = fields.Selection(string='Status',selection=[('A', 'Accepted'), ('R', 'Refused')])
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate_property',string = "Property", required=True)
    validity = fields.Integer(string='Validity', default='7')
    date_deadline = fields.Date("Date Deadline", compute="_compute_dead_line", inverse="_inverse_dead_line",store=True)

    _sql_constraints = [('check_price', 'CHECK(price >= 0 ',
         'The Offer Price should be positif.')
    ]
    @api.depends("validity")
    def _compute_dead_line(self):
        for record in self:
            record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_dead_line(self):
        for record in self:
            record.validity = (datetime.combine(record.date_deadline, datetime.min.time()) - datetime.now()).days

    def action_accept(self):
        for record in self:
            record.status ='A'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
        other_records = self.env['estate_property_offer'].search([('id', '!=', self.id)])
        for record in other_records:
            record.status = 'R'
        return True

    def action_refuse(self):
        for record in self:
            record.status ='R'
        return True

