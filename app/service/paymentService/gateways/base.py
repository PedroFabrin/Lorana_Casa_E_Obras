from abc import ABC, abstractmethod
from app.model.paymentModel.payment_model import PaymentStatus


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, order, forma_pagamento: str) -> tuple[PaymentStatus, str | None]:
        """Processa o pagamento de um pedido e retorna (status, transaction_id)."""
        raise NotImplementedError
