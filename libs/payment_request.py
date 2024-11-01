from sslcommerz_lib import SSLCOMMERZ
from libs.auto_transaction_id_generate import generate_transaction_id
from libs.live_link import frontend_link


def payment_request(amount, user):
    settings = {'store_id': 'own671f4d7ec684f', 'store_pass': 'own671f4d7ec684f@ssl', 'issandbox': True}
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = generate_transaction_id()
    post_body['success_url'] = f"{frontend_link}/transaction"
    post_body['fail_url'] = f"{frontend_link}/fail"
    post_body['cancel_url'] = f"{frontend_link}/cancel"
    post_body['emi_option'] = 0
    post_body['cus_name'] = user.username
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = "01740786762"
    post_body['cus_add1'] = "Dhaka, Bangladesh"
    post_body['cus_city'] = "Dhaka, Bangladesh"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Transaction"
    post_body['product_category'] = "Deposit"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)  # API response

    return response['GatewayPageURL']



