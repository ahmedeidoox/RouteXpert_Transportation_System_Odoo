from .... import http
from ....http import request
import base64


class DriversApplicationController(http.Controller):

    @http.route('/drivers/application', type='http', auth='public', website=True)
    def driver_application_form(self):
        return request.render("transport_system.drivers_applications_page_template")

    ## Handle Driver Application Personal Application Form
    @http.route('/drivers/application/submit', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def driver_application_form_submit(self, **kwargs):
        driver = request.env["transport.driver.application"].sudo().create({
            "name": kwargs.get("name"),
            "email": kwargs.get("email"),
            "phone": kwargs.get("phone"),
            "license_number": kwargs.get("license_number"),
            "national_id": kwargs.get("national_id"),
        })

        return request.redirect("/drivers/application/verification?driver_id=%s" % driver.id)

    @http.route('/drivers/application/verification', type='http', auth='public', website=True)
    def submitting_driver_documents(self, driver_id):
        return request.render("transport_system.drivers_applications_verification_template", {"driver_id": driver_id})

    ## Handle Verification Documents Upload Form
    @http.route('/drivers/application/verification/submit', type='http', auth='public', website=True, csrf=False,
                methods=['POST'])
    def driver_verification_documents_form_submit(self, **kwargs):
        driver_id = int(kwargs.get("driver_id"))
        try:
            driver = request.env["transport.driver.application"].browse(driver_id)
            uploaded_files = request.httprequest.files

            if 'national_id_document' in uploaded_files:
                national_id_document = uploaded_files['national_id_document'].read()
                request.env['transport.driver.verification.document'].sudo().create({
                    'document_type': 'national_id',
                    'document_data': base64.b64encode(national_id_document),
                    'driver_id': driver.id,
                })

            if 'driving_license_document' in uploaded_files:
                driving_license_document = uploaded_files['driving_license_document'].read()
                request.env['transport.driver.verification.document'].sudo().create({
                    'document_type': 'driving_license',
                    'document_data': base64.b64encode(driving_license_document),
                    'driver_id': driver_id,
                })

            return request.redirect("/drivers/application/thank_you")

        except Exception as e:
            print("Error:", e)
            return request.redirect("/drivers/application/verification?driver_id=%s" % driver_id)


    @http.route('/drivers/application/thank_you', type='http', auth='public', website=True)
    def driver_application_thank_you(self):
        return request.render('transport_system.driver_application_thank_you')
