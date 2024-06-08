from .... import models, fields, api


class TransportVehicle(models.Model):
    _name = "transport.vehicle"
    _description = "transport vehicle"
    _rec_name = "unique_iden"

    unique_iden = fields.Char(string='unique_iden', default="New", required=True,readonly=True)
    plate_number = fields.Char(string='License Number', required=True)
    vehicle_type = fields.Selection([('bus', 'Bus'), ('car', 'Car')], string='Vehicle Type', required=True)
    capacity = fields.Integer(string="Capacity",store=True)
    driver_id = fields.Many2one('res.users', string='Driver')


    def compute_vehicle_capacity(self):
        for vehicle in self:
            if vehicle.vehicle_type == "bus":
                vehicle.capacity = 30

            if vehicle.vehicle_type == "car":
                vehicle.capacity = 10


