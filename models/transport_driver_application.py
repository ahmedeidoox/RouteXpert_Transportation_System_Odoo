from .... import models,fields
import string,random

class TransportDriverApplication(models.Model):
    _name = "transport.driver.application"
    _description =  "transport driver application"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
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

    def generate_random_password(self, length=12):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    def accept_driver_application(self):
        self.status = 'accepted'
        portal_group = self.env.ref("base.group_portal")
        transport_driver_group = self.env.ref('transport_system.transport_system_driver_access')  # Reference to the Transport Driver Access group
        password = self.generate_random_password()
        print(password)
        user_vals = {
            "name": self.name,
            "email": self.email,
            "login": self.email,  # Using email as login
            "phone": self.phone,
            "license_number": self.license_number,
            "national_id": self.national_id,
            "groups_id": [(6, 0, [portal_group.id, transport_driver_group.id])],  # Assign the portal group and Transport Driver Access group
            "password":password,
        }
        self.env['res.users'].sudo().create(user_vals)

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