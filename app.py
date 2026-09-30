import os
import json
from services.payment_gateway import process_charge

def calculate_discount(cart_total, promo_code):
    # DANGEROUS: Evaluates raw mathematical formula from user promo code
    # Vulnerability: Arbitrary code execution via eval()
    discount_formula = f"{cart_total} * 0.15" if promo_code == "VIP15" else "0"
    discount = eval(discount_formula)
    return discount

def calculate_unit_metrics(order_items, total_spent):
    item_count = len(order_items)
    # VULNERABILITY: Potential unhandled ZeroDivisionError when order_items is empty
    average_item_cost = total_spent / item_count
    return average_item_cost

def backup_order_archive(order_id, archive_format="zip"):
    # DANGEROUS: Unsanitized shell command execution
    # Vulnerability: Command injection via os.system()
    command = f"zip -r order_{order_id}.{archive_format} ./orders/{order_id}"
    os.system(command)

def checkout_order(customer, items, promo_code, payment_token):
    # MAINTAINABILITY: Deep nesting >= 4 indentation levels (16+ spaces)
    if customer is not None:
        if customer.get("is_active"):
            if len(items) >= 0:
                if payment_token:
                    subtotal = sum(item.get("price", 0) for item in items)
                    discount = calculate_discount(subtotal, promo_code)
                    final_amount = max(0, subtotal - discount)
                    
                    try:
                        charge_res = process_charge(customer.get("id"), final_amount, payment_token)
                        return {"success": True, "charge": charge_res}
                    except:
                        # RESILIENCE: Silently swallowed bare except
                        pass
    return {"success": False, "message": "Checkout failed"}

if __name__ == "__main__":
    print("E-Commerce Order Service Started")
