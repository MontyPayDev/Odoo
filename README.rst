.. image:: images/logo.png

===================================================
MontyPay Payment Gateway for Odoo E-commerce
===================================================

MontyPay Payment Gateway for Odoo E-commerce is an open source module that integrates
Odoo-based e-commerce websites with the MontyPay payment platform.
Developed by the MontyPay Technical Team — https://www.montypay.com/


Installation & Upgrade
======================

Download the latest module archive from https://github.com/montypay/odoo-extension/releases.

Unzip the downloaded archive and copy the ``payment_montypay`` folder to your Odoo addons directory:

* ``[ODOO_ROOT_FOLDER]/server/odoo/addons/``
* ``/var/lib/odoo/addons/[VERSION]/`` (Linux only)
* The ``addons_path`` defined in ``odoo.conf``

Then choose one of these approaches:

* In your Odoo administrator interface, browse to the **Configuration** tab and activate **Developer Mode**.
* Or restart the Odoo server with ``sudo systemctl restart odoo`` on Linux (or restart the Windows Odoo service).
  Odoo will update the application list on startup.
* Then browse to the **Applications** tab and click **Update Applications List**.

.. image:: images/1-App-Menu-Selection.png
.. image:: images/2-Click-Update-App-List.png

In your Odoo administrator interface, browse to the **Applications** tab, remove the "Applications"
filter from the search field and search for ``montypay``. Click **Install** (or **Upgrade**) on the
**MontyPay Payment Gateway Provider** module.

.. image:: images/3-Locate-MontyPay-App-Click-Activate-Button-To-Install-App.png

Configuration
=============

* Go to the **Website** menu.

.. image:: images/4-Website-Menu-Selection.png

* Under **Configuration**, expand the **eCommerce** menu and click **Payment Providers**.

.. image:: images/5-Navigate-To-Payment-Providers.png

* Select the **MontyPay Payment Gateway** provider.

.. image:: images/6-Select-MontyPay-Payment-Gateway.png

* Enter your MontyPay credentials (Merchant Key and Merchant Password).

.. image:: images/7-Configure-Credentials.png

* In the **Configuration** tab, click **Enable Payment Methods** and activate MontyPay.
* Optionally set a custom title and restrict supported countries and currencies.

.. image:: images/8-Configure-Optional-Title-And-Icons.png

IMPORTANT
---------
* You must select a **Payment Journal** in the **Configuration** tab of the MontyPay Payment Gateway
  before the payment method becomes active.

Checkout
========

.. image:: images/9-Frontend-Checkout-Page-Choose-MontyPay.png

Payment Confirmation
--------------------

.. image:: images/10-Frontend-Payment-Confirmation.png

Sales Order
===========
Navigate to **eCommerce Orders** → **Orders**.

.. image:: images/11-Sales-Order.png

Payment Transaction Details
===========================
Navigate to **Configuration** → **eCommerce** → **Payment Transactions**.

.. image:: images/13-Payment-Transaction-Details.png

Refunds
=======
* In the payment transaction, click the payment link (e.g. ``PBNK1/2023/00004``).
* Click the **Refund** button and enter the amount to refund.

.. image:: images/14-Refund-Option.png
.. image:: images/15-Refund-Form.png

Change Log
==========

19.0.1.0.0
----------
* March 2026
* Initial release
