import os
import requests
from app.model.paymentModel.payment_model import PaymentStatus
from app.service.paymentService.gateways.base import PaymentGateway, PaymentResult

BASE_URL = "https://api.checkout.infinitepay.io"


class InfinitePayGateway(PaymentGateway):
    """Integração via link de checkout da InfinitePay: cria um link de pagamento (POST /links)
    e devolve a URL para o comprador finalizar a compra na própria InfinitePay. A confirmação
    chega depois via webhook (ver order_service.handle_infinitepay_webhook), mas como a
    InfinitePay não assina o webhook, o pagamento é sempre revalidado via /payment_check antes
    de aprovar o pedido."""

    def _handle(self) -> str:
        handle = os.environ.get("INFINITEPAY_HANDLE")
        if not handle:
            raise RuntimeError("INFINITEPAY_HANDLE não configurado")
        return handle

    def _headers(self) -> dict:
        if os.environ.get("INFINITEPAY_TEST_MODE", "false").lower() in ("1", "true", "yes"):
            return {"Env": "mock"}
        return {}

    def process_payment(self, order, forma_pagamento: str) -> PaymentResult:
        payload = {
            "handle": self._handle(),
            "order_nsu": str(order.id),
            "items": [
                {
                    "quantity": int(item.quantidade),
                    "price": int(round(float(item.preco_unitario) * 100)),
                    "description": item.product.nome,
                }
                for item in order.items
            ],
            "customer": {
                "name": order.user.name,
                "email": order.user.email,
            },
        }
        redirect_url = os.environ.get("INFINITEPAY_REDIRECT_URL")
        if redirect_url:
            payload["redirect_url"] = redirect_url
        webhook_url = os.environ.get("INFINITEPAY_WEBHOOK_URL")
        if webhook_url:
            payload["webhook_url"] = webhook_url

        response = requests.post(f"{BASE_URL}/links", json=payload, headers=self._headers(), timeout=15)
        if response.status_code not in (200, 201):
            raise RuntimeError(f"Erro ao criar link de pagamento na InfinitePay: {response.status_code} {response.text}")

        data = response.json()
        checkout_url = data.get("url") or data.get("checkout_url") or data.get("payment_url") or data.get("link")
        if not checkout_url:
            raise RuntimeError(f"Resposta inesperada da InfinitePay ao criar link de pagamento: {data}")

        # A InfinitePay só revela o slug/transaction_nsu depois, no retorno ao redirect_url ou
        # no webhook — não há como obtê-los no momento da criação do link.
        return PaymentResult(PaymentStatus.pendente, None, checkout_url)

    def check_payment(self, order_nsu: str, transaction_nsu: str, slug: str) -> dict:
        """Confirma diretamente com a InfinitePay se um pagamento foi realmente aprovado, já que
        o webhook não vem assinado e não deve ser confiado sem essa revalidação."""
        payload = {
            "handle": self._handle(),
            "order_nsu": order_nsu,
            "transaction_nsu": transaction_nsu,
            "slug": slug,
        }
        response = requests.post(f"{BASE_URL}/payment_check", json=payload, headers=self._headers(), timeout=15)
        if response.status_code != 200:
            raise RuntimeError(f"Erro ao consultar pagamento na InfinitePay: {response.status_code} {response.text}")
        return response.json()
