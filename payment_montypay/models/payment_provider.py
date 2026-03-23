# -*- coding: utf-8 -*-

import requests
import hashlib
import logging

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('montypay', "MontyPay")],
        ondelete={'montypay': 'set default'}
    )

    montypay_merchant_key = fields.Char(
        string="Merchant Key",
        required_if_provider='montypay'
    )

    montypay_merchant_password = fields.Char(
        string="Merchant Password",
        required_if_provider='montypay',
        groups='base.group_system'
    )

    montypay_webhook_url = fields.Char(
        string="Webhook URL",
        compute="_compute_montypay_webhook_url",
    )

    @api.depends('company_id')
    def _compute_montypay_webhook_url(self):
        for provider in self:
            base_url = provider.env['ir.config_parameter'].sudo().get_param('web.base.url')
            provider.montypay_webhook_url = f"{base_url}/payment/montypay/webhook"

    # ---------------------------------------------------------
    # API URL
    # ---------------------------------------------------------

    def _get_montypay_api_url(self):
        return "https://checkout.montypay.com/api/v1"

    # ---------------------------------------------------------
    # Hash Generator (MD5 -> SHA1)
    # ---------------------------------------------------------

    def _generate_montypay_hash(self, order_number, amount, currency, description):
        self.ensure_one()

        to_md5 = f"{order_number}{amount}{currency}{description}{self.montypay_merchant_password}"
        to_md5 = to_md5.upper()

        md5_hash = hashlib.md5(to_md5.encode('utf-8')).hexdigest()
        sha1_hash = hashlib.sha1(md5_hash.encode('utf-8')).hexdigest()

        return sha1_hash

    # ---------------------------------------------------------
    # API Request
    # ---------------------------------------------------------

    def _montypay_make_request(self, endpoint, payload=None, method='POST'):
        self.ensure_one()

        url = f"{self._get_montypay_api_url()}{endpoint}"

        headers = {
            "Content-Type": "application/json",
        }

        try:
            if method == 'GET':
                response = requests.get(
                    url,
                    params=payload,
                    headers=headers,
                    timeout=15
                )
            else:
                response = requests.post(
                    url,
                    json=payload or {},
                    headers=headers,
                    timeout=15
                )

            _logger.warning("MontyPay Request to %s\nPayload:\n%s", endpoint, payload)

            response.raise_for_status()

        except requests.exceptions.HTTPError:
            _logger.exception("MontyPay API error at %s", url)
            raise ValidationError(
                _("MontyPay API Error:\n%s") % response.text
            )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("MontyPay connection error")
            raise ValidationError(
                _("MontyPay: Could not connect to the API.")
            )

        return response.json()

    def _compute_feature_support_fields(self):
        super()._compute_feature_support_fields()
        for provider in self:
            if provider.code == 'montypay':
                provider.support_refund = 'partial'
                provider.support_tokenization = False