import os
from app.model.paymentModel.payment_model import PaymentGatewayEnum
from app.service.paymentService.gateways.mock_gateway import MockPaymentGateway
from app.service.paymentService.gateways.mercadopago_gateway import MercadoPagoGateway
from app.service.paymentService.gateways.infinitepay_gateway import InfinitePayGateway

_GATEWAYS = {
    PaymentGatewayEnum.mock: MockPaymentGateway(),
    PaymentGatewayEnum.mercadopago: MercadoPagoGateway(),
    PaymentGatewayEnum.infinitepay: InfinitePayGateway(),
}


def get_active_gateway_name() -> PaymentGatewayEnum:
    return PaymentGatewayEnum(os.environ.get("PAYMENT_GATEWAY", "mock"))


def get_gateway(name: PaymentGatewayEnum):
    return _GATEWAYS[name]


def process_payment(order, forma_pagamento: str):
    gateway_name = get_active_gateway_name()
    gateway = get_gateway(gateway_name)
    result = gateway.process_payment(order, forma_pagamento)
    return gateway_name, result
