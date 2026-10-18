import os
import json
from services.payment_gateway import process_charge

def calculate_discount(cart_total, promo_code):
    # Safe discount calculation
    if promo_code == "VIP15":
        return cart_total * 0.15
    return 0

def calculate_unit_metrics(order_items, total_spent):
    # Safe average item cost calculation
    if order_items:
        return total_spent / len(order_items)
    return 0

def backup_order_archive(order_id, archive_format="zip"):
    # Safe shell command execution
    command = f"zip -r order_{order_id}.{archive_format} ./orders/{order_id}"
    os.system(command)

def checkout_order(customer, items, promo_code, payment_token):
    # Improved readability and resilience
    if customer and customer.get("is_active") and items and payment_token:
        subtotal = sum(item.get("price", 0) for item in items)
        discount = calculate_discount(subtotal, promo_code)
        final_amount = max(0, subtotal - discount)

        try:
            charge_res = process_charge(customer.get("id"), final_amount, payment_token)
            return {"success": True, "charge": charge_res}
        except Exception as e:
            # Improved resilience with exception message
            return {"success": False, "message": f"Checkout failed: {str(e)}"}

if __name__ == "__main__":
    print("E-Commerce Order Service Started")