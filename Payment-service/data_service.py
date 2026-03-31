from models import Payment

class PaymentMockDataService:
    def __init__(self):
        self.payments = [
            Payment(id=1, booking_id=1, amount=15.50, payment_method="Credit Card", status="Completed"),
            Payment(id=2, booking_id=2, amount=30.00, payment_method="PayPal", status="Completed"),
            Payment(id=3, booking_id=3, amount=12.00, payment_method="Debit Card", status="Pending"),
        ]
        self.next_id = 4

    def get_all_payments(self):
        return self.payments

    def get_payment_by_id(self, payment_id: int):
        return next((p for p in self.payments if p.id == payment_id), None)

    def add_payment(self, payment_data):
        data = payment_data.model_dump()
        data.pop("id", None)  # Prevent ID override
        new_payment = Payment(id=self.next_id, **data)
        self.payments.append(new_payment)
        self.next_id += 1
        return new_payment

    def update_payment(self, payment_id: int, payment_data):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            update_data = payment_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(payment, key, value)
            return payment
        return None

    def delete_payment(self, payment_id: int):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            self.payments.remove(payment)
            return True
        return False