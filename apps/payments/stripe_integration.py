import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount_cents, currency='usd'):
    return stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        payment_method_types=['card'],
    )
