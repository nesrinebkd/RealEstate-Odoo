from odoo import  fields, models

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = " Define the type of a property "

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('type_property_uniq', 'unique (name,id)', 'The type name of the property must be unique  !')
    ]