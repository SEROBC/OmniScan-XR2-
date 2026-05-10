import stripe

stripe.api_key = "sk_test_xxx"

def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "XR2 Pro"},
                "unit_amount": 1999,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://yourapp.com/success",
        cancel_url="https://yourapp.com/cancel",
    )
    return session.url
