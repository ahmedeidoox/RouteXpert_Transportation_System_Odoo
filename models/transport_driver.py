from .... import models,fields


class TransportDriver(models.Model):
    _inherit = "res.users"

    license_number = fields.Char(string='License Number', required=True)
    national_id = fields.Char(string='National ID', required=True)






