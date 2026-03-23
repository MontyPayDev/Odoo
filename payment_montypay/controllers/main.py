# -*- coding: utf-8 -*-

import hashlib
import logging

from odoo import http
from odoo.http import request
from urllib.parse import parse_qs, unquote_plus

_logger = logging.getLogger(__name__)


class MontyPayController(http.Controller):

    # ---------------------------------------------------------
    # SUCCESS RETURN (User Redirect)
    # ---------------------------------------------------------

    @http.route('/payment/montypay/success', type='http', auth='public', csrf=False)
    def montypay_success(self, **data):
        reference = data.get('order_number')

        tx = request.env['payment.transaction'].sudo().search([
            ('reference', '=', reference)
        ], limit=1)

        if not tx:
            return request.redirect('/payment/status')

        # Do NOT mark as done here.
        # Wait for webhook confirmation.

        return request.redirect('/payment/status')

    # ---------------------------------------------------------
    # CANCEL RETURN
    # ---------------------------------------------------------

    @http.route('/payment/montypay/cancel', type='http', auth='public', csrf=False)
    def montypay_cancel(self, **data):
        reference = data.get('order_number')

        tx = request.env['payment.transaction'].sudo().search([
            ('reference', '=', reference)
        ], limit=1)

        if tx:
            tx._set_canceled("Customer canceled payment.")

        return request.redirect('/payment/status')

    # ---------------------------------------------------------
    # WEBHOOK (SERVER TO SERVER - SECURE)
    # ---------------------------------------------------------
    @http.route('/payment/montypay/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def montypay_webhook(self, **post):

        _logger.warning("MontyPay Webhook POST:\n%s", post)

        if not post:
            return "No data received"

        # Decode URL-encoded values
        from urllib.parse import unquote_plus

        data = {
            k: unquote_plus(v)
            for k, v in post.items()
        }

        _logger.warning("Decoded Data:\n%s", data)

        reference = data.get('order_number')
        received_hash = data.get('hash')

        if not reference:
            return "Missing reference"

        tx = request.env['payment.transaction'].sudo().search([
            ('reference', '=', reference)
        ], limit=1)

        if not tx:
            _logger.error("Transaction not found for reference %s", reference)
            return "Transaction not found"

        # -----------------------------
        # STATUS HANDLING
        # -----------------------------

        status = (data.get('status') or '').lower()
        order_status = (data.get('order_status') or '').lower()
        payment_type = (data.get('type') or '').lower()

        if payment_type == 'sale' and order_status == 'settled':
            tx._set_done()
            return "OK"

        elif status == 'declined':
            tx._set_error("Declined")
            return "Declined"

        elif status == 'fail':
            tx._set_error("Failed")
            return "Failed"

        elif status in ['waiting', 'redirect']:
            tx._set_pending()
            return "Pending"

        tx._set_pending()
        return "Unhandled status"