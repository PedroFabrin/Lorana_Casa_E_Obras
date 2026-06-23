import os
from app.model.paymentModel.payment_model import PaymentGatewayEnum
from app.service.paymentService.gateways.mock_gateway import MockPaymentGateway

_GATEWAYS = {
    PaymentGatewayEnum.mock: MockPaymentGateway(),
}


def get_active_gateway_name() -> PaymentGatewayEnum:
    return PaymentGatewayEnum(os.environ.get("PAYMENT_GATEWAY", "mock"))


def process_payment(order, forma_pagamento: str):
    gateway_name = get_active_gateway_name()
    gateway = _GATEWAYS[gateway_name]
    status, transaction_id = gateway.process_payment(order, forma_pagamento)
    return gateway_name, status, transaction_id
