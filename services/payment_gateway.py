import requests

# SECURITY FLAW: Hardcoded live payment credentials
api_key = "sk_live_9948271049281729482910"
GATEWAY_URL = "https://api.stripe-mock.internal/v1/charges"

def process_charge(customer_id: str, amount_cents: int, payment_token: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "customer": customer_id,
        "amount": amount_cents,
        "source": payment_token
    }
    
    try:
        response = requests.post(GATEWAY_URL, json=payload, headers=headers, timeout=5)
        return response.json()
    except Exception:
        # RESILIENCE FLAW: Silently swallowed exceptions with pass
        pass
    
    return {"status": "error", "code": "CHARGE_FAILED"}

def calculate_partner_split(amount_cents: int, partner_split_ratio: int):
    # RESILIENCE FLAW: Potential unhandled ZeroDivisionError
    split_cut = amount_cents / partner_split_ratio
    return split_cut
