import hashlib
import hmac
import os
from typing import Optional
from app.model.paymentModel.payment_model import PaymentStatus
from app.service.paymentService.gateways.base import PaymentGateway, PaymentResult

try:
    import mercadopago
except ImportError:
    mercadopago = None

MP_STATUS_MAP = {
    "approved": PaymentStatus.aprovado,
    "pending": PaymentStatus.pendente,
    "in_process": PaymentStatus.pendente,
    "in_mediation": PaymentStatus.pendente,
    "authorized": PaymentStatus.pendente,
    "rejected": PaymentStatus.recusado,
    "cancelled": PaymentStatus.recusado,
    "refunded": PaymentStatus.recusado,
    "charged_back": PaymentStatus.recusado,
}


class MercadoPagoGateway(PaymentGateway):
    """Integração real via Checkout Pro: cria uma preferência de pagamento e devolve a URL
    (init_point/sandbox_init_point) que o front abre em modal/redirect para o comprador pagar
    dentro da própria tela do Mercado Pago. A confirmação do pagamento chega depois, de forma
    assíncrona, via webhook (ver get_payment_status / verify_notification_signature)."""

    def _access_token(self) -> str:
        token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN")
        if not token:
            raise RuntimeError("MERCADOPAGO_ACCESS_TOKEN não configurado")
        return token

    def _sdk(self):
        if mercadopago is None:
            raise RuntimeError("Biblioteca 'mercadopago' não instalada")
        return mercadopago.SDK(self._access_token())

    def process_payment(self, order, forma_pagamento: str) -> PaymentResult:
        sdk = self._sdk()

        back_urls = {
            "success": os.environ.get("MERCADOPAGO_SUCCESS_URL", ""),
            "failure": os.environ.get("MERCADOPAGO_FAILURE_URL", ""),
            "pending": os.environ.get("MERCADOPAGO_PENDING_URL", ""),
        }
        request = {
            "items": [
                {
                    "id": str(item.product_id),
                    "title": item.product.nome,
                    "quantity": int(item.quantidade),
                    "currency_id": "BRL",
                    "unit_price": float(item.preco_unitario),
                }
                for item in order.items
            ],
            "payer": {"email": order.user.email},
            "back_urls": back_urls,
            "external_reference": str(order.id),
            "notification_url": os.environ.get("MERCADOPAGO_NOTIFICATION_URL"),
            "statement_descriptor": "LORANA CASA E OBRAS",
        }
        if back_urls["success"]:
            request["auto_return"] = "approved"

        response = sdk.preference().create(request)
        preference = response["response"]
        if response.get("status") not in (200, 201):
            raise RuntimeError(f"Erro ao criar preferência de pagamento no Mercado Pago: {preference}")
        checkout_url = preference.get("init_point") or preference.get("sandbox_init_point")

        return PaymentResult(PaymentStatus.pendente, preference.get("id"), checkout_url)

    def get_payment_status(self, payment_id: str) -> tuple[PaymentStatus, Optional[str], Optional[str]]:
        """Consulta um pagamento na API do Mercado Pago e retorna (status, external_reference, payment_id)."""
        sdk = self._sdk()
        response = sdk.payment().get(payment_id)
        payment = response["response"]
        if response.get("status") not in (200, 201):
            raise RuntimeError(f"Erro ao consultar pagamento {payment_id} no Mercado Pago: {payment}")
        status = MP_STATUS_MAP.get(payment.get("status"), PaymentStatus.pendente)
        return status, payment.get("external_reference"), str(payment.get("id"))

    def verify_notification_signature(self, x_signature: Optional[str], x_request_id: Optional[str], data_id: str) -> bool:
        """Valida a assinatura HMAC do webhook, conforme a documentação do Mercado Pago, para
        garantir que a notificação realmente veio do Mercado Pago (e não de um terceiro tentando
        marcar um pedido como pago)."""
        secret = os.environ.get("MERCADOPAGO_WEBHOOK_SECRET")
        if not secret:
            raise RuntimeError("MERCADOPAGO_WEBHOOK_SECRET não configurado")
        if not x_signature or not x_request_id or not data_id:
            return False

        parts = dict(p.strip().split("=", 1) for p in x_signature.split(",") if "=" in p)
        ts = parts.get("ts")
        v1 = parts.get("v1")
        if not ts or not v1:
            return False

        manifest = f"id:{str(data_id).lower()};request-id:{x_request_id};ts:{ts};"
        computed = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(computed, v1)
