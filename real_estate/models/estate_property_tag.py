from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name= "estate_property_tag"
    _description = "Define the estate property tag "

    name = fields.Char("Name")

    _sql_constraints = [
        ('tag_property_uniq', 'unique (name,id)', 'The tag name of the property must be unique  !')
    ]
