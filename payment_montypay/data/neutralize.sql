-- disable montypay payment provider
UPDATE payment_provider
   SET montypay_merchant_key = NULL,
       montypay_merchant_password = NULL;
