from odoo import api,fields, models,exceptions

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "EState Proprety model"
    property_status= fields.Char('Status', default="New")
    name = fields.Char('Proprety Name', required=True)
    postcode = fields.Char('Postcode')
    description = fields.Text('Description')
    date_availability = fields.Date('Date Availability',copy=False,default=(fields.Datetime.add(fields.Datetime.now(),months=3)))
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float('Selling Price',readonly=True, copy=False)
    bedrooms = fields.Integer('Number of bedrooms',default="2")
    living_area = fields.Integer('living area (Sqm)')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation',
    selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active',default=True)
    status = fields.Selection(string='Status',
    selection=[('new', 'New'), ('offer recieved', 'Offer Received '),('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Canceled','Canceled')], required= True, copy=False,default='new')
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer",copy=False)
    salesperson = fields.Many2one("res.users", string="Salesman", default= lambda self: self.env.uid)
    tag_ids = fields.Many2many("estate_property_tag", string="Tag")

    offer_ids = fields.One2many("estate_property_offer","property_id", string= "Offer")

    total_area = fields.Float("Total Area (Sqm)",compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0 ',
         'The Expected Price should be positif.'),(
            'check_selling_price', 'CHECK(selling_price >= 0 ',
            'The Selling Price should be positif.'
        )
    ]
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"),default=0.0)

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "north"

        else:
            self.garden_area = ""
            self.garden_orientation = ""

    def sold_property(self):
        for record in self:
            if record.property_status == 'New':
                record.property_status = "Sale"
            else:
                raise exceptions.UserError("Canceled Properties can't be SOld")
        return True

    def cancel_property(self):
        for record in self:
            if record.property_status == 'New':
                record.property_status = "Canceled"
            else:
                raise exceptions.UserError("Sold Properties can't be Canceled")

        return True
