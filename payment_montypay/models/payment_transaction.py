from odoo import models
from odoo.exceptions import ValidationError
import logging
import re

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        if self.provider_code != 'montypay':
            return super()._get_specific_rendering_values(processing_values)

        provider = self.provider_id
        # ---------------------------------------------------------
        # GET REAL CUSTOMER (Invoice Partner)
        # ---------------------------------------------------------

        invoice = self.invoice_ids[:1]
        partner = invoice.partner_id if invoice else self.partner_id

        if not partner:
            raise ValidationError("No customer found for this transaction.")

        # ---------------------------------------------------------
        # VALIDATION
        # ---------------------------------------------------------

        if not partner.name or len(partner.name.strip()) < 2:
            raise ValidationError("Customer name must contain at least 2 characters.")

        if not partner.email:
            raise ValidationError("Customer email is required for MontyPay.")

        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, partner.email):
            raise ValidationError("Customer email format is invalid.")

        if not partner.phone or len(partner.phone.strip()) < 6:
            raise ValidationError("Customer phone must contain at least 6 characters.")

        if not partner.street or len(partner.street.strip()) < 2:
            raise ValidationError("Customer street address must contain at least 2 characters.")

        if not partner.city or len(partner.city.strip()) < 2:
            raise ValidationError("Customer city must contain at least 2 characters.")

        if not partner.country_id or not partner.country_id.code:
            raise ValidationError("Customer country is required.")

        if self.amount <= 0:
            raise ValidationError("Payment amount must be greater than 0.")

        if not self.currency_id:
            raise ValidationError("Currency is missing on the transaction.")

        # ---------------------------------------------------------
        # PREPARE DATA
        # ---------------------------------------------------------
        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        success_url = f"{base_url}/payment/montypay/success"
        cancel_url = f"{base_url}/payment/montypay/cancel"

        order_number = self.reference
        order_amount = "%.2f" % self.amount
        order_currency = self.currency_id.name
        order_description = self.reference

        session_hash = provider._generate_montypay_hash(
            order_number,
            order_amount,
            order_currency,
            order_description,
        )
        invoice = self.invoice_ids[:1]
        partner = invoice.partner_id if invoice else self.partner_id

        customer_name = partner.name
        customer_email = partner.email
        billing_country = partner.country_id.code if partner.country_id else "LB"
        billing_city = partner.city
        billing_address = partner.street
        billing_phone = partner.phone
        
        payload = {
            "merchant_key": provider.montypay_merchant_key,
            "operation": "purchase",
            "cancel_url": cancel_url,
            "success_url": success_url,
            "methods": ["card"],
            "hash": session_hash,
            "order": {
                "description": order_description,
                "number": order_number,
                "amount": order_amount,
                "currency": order_currency,
            },
            "customer": {
                "name": customer_name or "Customer",
                "email": customer_email or "",
            },
            "billing_address": {
                "country": billing_country,
                "city": billing_city or "",
                "address": billing_address or "",
                "phone": billing_phone or "",
            }
        }

        response = provider._montypay_make_request("/session", payload)

        redirect_url = response.get("redirect_url")

        if not redirect_url:
            raise ValidationError("MontyPay did not return redirect_url.")

        _logger.warning("Redirecting to MontyPay: %s", redirect_url)

        return {
            'api_url': redirect_url,
        }