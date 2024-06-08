from .... import models,fields


class TransportDriverApplication(models.Model):
    _name = "transport.driver.application"
    _description =  "transport driver application"

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    license_number = fields.Char(string='License Number', required=True)
    national_id = fields.Char(string='National ID', required=True)
    creation_date = fields.Datetime("Creation Date", default =fields.Datetime.now,readonly = True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Status', default='pending')

    verification_documents = fields.One2many("transport.driver.verification.document","driver_id")



    def accept_driver_application(self):
        self.status = 'accepted'
        self.env["transport.driver"].create({
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "license_number":self.license_number,
            "national_id":self.national_id,
        })
    def reject_driver_application(self):
        self.status = 'rejected'
class TransportDriverVerificationDocuments(models.Model):
    _name = "transport.driver.verification.document"
    _description = "transport driver verification document"

    document_type = fields.Selection([
        ('national_id', 'National ID'),
        ('driving_license', 'Driving License')
    ], string='Type', default='national_id',required=True)

    document_data = fields.Binary(string="Document", required=True)

    driver_id = fields.Many2one("transport.driver.application")