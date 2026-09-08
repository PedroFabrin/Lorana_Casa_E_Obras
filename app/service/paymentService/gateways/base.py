from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from app.model.paymentModel.payment_model import PaymentStatus


@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: Optional[str] = None
    checkout_url: Optional[str] = None


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, order, forma_pagamento: str) -> PaymentResult:
        """Processa o pagamento de um pedido e retorna o resultado do gateway."""
        raise NotImplementedError
