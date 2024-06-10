from .... import models, fields, api


class TransportVehicle(models.Model):
    _name = "transport.vehicle"
    _description = "transport vehicle"
    _rec_name = "unique_iden"

    unique_iden = fields.Char(string='unique_iden', default="New", required=True,readonly=True)
    plate_number = fields.Char(string='License Number', required=True)

    vehicle_type_id = fields.Many2one("transport.vehicle.type",string="Vehicle type",required=True)
    driver_id = fields.Many2one('res.users', string='Driver' ,domain = lambda self: [("groups_id","in",[self.env.ref("base.group_portal").id]),("groups_id","in",[self.env.ref("transport_system.transport_system_driver_access").id])])


    @api.model
    def create(self, vals_list):
        rec = super(TransportVehicle,self).create(vals_list)
        if rec.unique_iden == "New" and rec.vehicle_type_id.vehicle_type == "bus":
            rec.unique_iden = self.env["ir.sequence"].next_by_code("bus.seq")

        if rec.unique_iden == "New" and rec.vehicle_type_id.vehicle_type == "car":
            rec.unique_iden = self.env["ir.sequence"].next_by_code("car.seq")
        return rec


class TransportVehicleType(models.Model):
    _name = "transport.vehicle.type"
    _description = "transport vehicle type"
    _rec_name = "vehicle_type"

    vehicle_type = fields.Selection([('bus', 'Bus'), ('car', 'Car')], string='Vehicle Type', required=True)
    capacity = fields.Integer(string="Capacity",compute="_compute_vehicle_capacity",store=True)
    color = fields.Integer(string="Color",required=True)

    @api.depends("vehicle_type")
    def _compute_vehicle_capacity(self):
        for rec in self:
            if rec.vehicle_type == 'bus':
                rec.capacity = 30
            if rec.vehicle_type == 'car':
                rec.capacity = 15