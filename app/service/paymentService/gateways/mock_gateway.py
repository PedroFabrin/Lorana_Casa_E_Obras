import uuid
from app.model.paymentModel.payment_model import PaymentStatus
from app.service.paymentService.gateways.base import PaymentGateway, PaymentResult


class MockPaymentGateway(PaymentGateway):
    """Simula o comportamento de um gateway real (ex.: Mercado Pago) sem credenciais externas.

    Cartão e PIX são aprovados de imediato; boleto fica pendente até confirmação
    (ver order_service.confirm_payment), espelhando o comportamento típico desses meios de pagamento.
    """

    def process_payment(self, order, forma_pagamento: str) -> PaymentResult:
        transaction_id = f"mock_{uuid.uuid4().hex[:16]}"
        if forma_pagamento == "boleto":
            return PaymentResult(PaymentStatus.pendente, transaction_id)
        return PaymentResult(PaymentStatus.aprovado, transaction_id)
