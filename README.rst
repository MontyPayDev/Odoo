.. image:: static/description/icon.png

===================================================
MontyPay Payment Gateway for Odoo
===================================================

This module integrates MontyPay with Odoo, allowing merchants to securely accept
online payments through MontyPay's hosted checkout page — across eCommerce,
invoices, and any other Odoo payment flow.

No sensitive card details are stored on your server. MontyPay handles all payment
data securely on their infrastructure.

Features
========

* Hosted, secure checkout page (no card data touches your server)
* Works across eCommerce, customer invoices, and all Odoo payment flows
* Credit and debit card payments (Visa, Mastercard, American Express)
* Apple Pay and Google Pay support
* Webhook-based payment confirmation (server-to-server callback)
* Hash signature verification on all callbacks

Configuration
=============

1. Go to **Accounting → Configuration → Payment Providers** or **Website → Configuration → Payment Providers**.
2. Select **MontyPay** and enter your **Merchant Key** and **Merchant Password**.
3. Copy the **Webhook URL** shown in the credentials tab and send it to MontyPay support to configure your callback endpoint.
4. In the **Configuration** tab, enable the MontyPay payment method and select a Payment Journal.

External Services
=================

This module connects to MontyPay's hosted checkout service to process payments.
When a customer initiates a payment, the following data is transmitted to MontyPay:

* Transaction amount and currency
* Order reference ID
* Customer name, email, and billing address
* Callback URLs and session tokens

The customer is then redirected to MontyPay's secure hosted page to enter their
payment details. No card data is ever sent to or stored on your server.

**API Endpoints used:**

* https://checkout.montypay.com/api/v1/session
* https://checkout.montypay.com/*

**Legal:**

* Terms and Conditions: https://montypay.com/terms-and-conditions
* Privacy Policy: https://montypay.com/privacy-policy

By using this module, you agree to the transmission of payment-related data to
MontyPay in accordance with their terms and privacy policy.

Frequently Asked Questions
==========================

**How do I get my Merchant Key and Password?**
Contact the MontyPay sales team at https://www.montypay.com.

**Does this module store card data?**
No. Customers enter their payment details directly on MontyPay's hosted page.
No card information is ever sent to or stored on your Odoo server.

**What payment methods are supported?**
Visa, Mastercard, American Express, Apple Pay, and Google Pay — all through
MontyPay's secure hosted checkout page.

**Where do I find the webhook URL?**
It is displayed directly in the MontyPay credentials tab inside Odoo. Copy it and
provide it to MontyPay so they can send payment confirmations to your server.

**Where can I find MontyPay in Odoo?**
MontyPay appears as a payment provider under both **Accounting → Configuration → Payment Providers**
and **Website → Configuration → Payment Providers**.

Change Log
==========

19.0.1.0.0
----------
* March 2026
* Initial release