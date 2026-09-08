# Lorana Casa & Obras — Guia de Integração para o Front-end

Este documento descreve a API REST do backend (FastAPI) para quem vai construir o front-end do
e-commerce. Use-o em conjunto com o protótipo visual no Figma — o Figma define **layout, fluxo de
telas e identidade visual**; este documento define **quais dados existem, em qual rota buscar cada
um, e quais regras de negócio o front precisa respeitar**.

**Protótipo (Figma):** https://www.figma.com/make/uBGbmA17KYyrxdeN4umweY/E-commerce-Lorana-Casa---Obras?t=KQ72qbi2kDUp3qN7-1

---

## 1. Como rodar a API localmente

```bash
docker compose up -d --build
```

- API: `http://localhost:8000`
- Docs interativas (Swagger): `http://localhost:8000/docs` — dá para testar todas as rotas direto no navegador, com botão "Authorize" para colar o token JWT.
- Banco: MariaDB em `localhost:3306` (acessível via HeidiSQL, usuário `root`, sem senha).

Já existe um usuário **admin** seedado automaticamente (via migration), para testes do painel administrativo:

```
email: admin@lorana.com.br
senha: admin123
```
(definidos em `ADMIN_EMAIL`/`ADMIN_PASSWORD` no `.env` — troque antes de subir em produção).

---

## 2. Convenções gerais

### Formato de resposta

Toda resposta de sucesso tem o formato:
```json
{ "status": "success", "data": { ... } }
```
ou, em operações de exclusão:
```json
{ "status": "success", "message": "Categoria deletada com sucesso" }
```

Toda resposta de erro de regra de negócio (validação, permissão, registro não encontrado) vem com
status HTTP `400`, `401` ou `403` e corpo:
```json
{ "status": "error", "message": "Descrição do erro em português" }
```

Erros de schema/payload inválido (campo faltando, tipo errado) retornam `422` no formato padrão do
FastAPI/Pydantic (`detail: [...]`).

### Paginação

Toda rota de listagem (`POST /<entidade>/list`) aceita `page` (default 1) e `page_size` (default 10,
máx. 100) e retorna:
```json
{
  "status": "success",
  "data": {
    "total": 42,
    "page": 1,
    "page_size": 10,
    "data": [ ... ]
  }
}
```

### Autenticação

JWT Bearer. Fluxo:

1. `POST /auth/login` com `email`/`password` → recebe `access_token`.
2. Enviar em toda rota protegida: header `Authorization: Bearer <access_token>`.
3. Token expira em `JWT_EXPIRE_MINUTES` (60 min por padrão) — ao expirar, a API responde `401` e o
   front deve redirecionar para o login.

Não existe refresh token nesta versão — ao expirar, é preciso logar novamente.

### Papéis (RBAC)

Todo usuário tem `role`: `admin` ou `cliente`. Cadastro público (`POST /users/create`) sempre cria
`cliente`. Rotas administrativas (gerenciar produto, categoria, seção, pedidos, relatórios,
dashboard) exigem `role: admin` e retornam `403` para quem não é admin — o front deve esconder/
bloquear essas telas (painel administrativo) para usuários `cliente`.

### CORS

CORS está liberado (`CORS_ORIGINS=*` no `.env` de desenvolvimento). Em produção, troque para a URL
real do front (`CORS_ORIGINS=https://lorana.com.br`).

---

## 3. Mapa do protótipo → API

Referência cruzada entre as telas do protótipo (Figma / Figuras 4–19 da ERS) e os endpoints que cada
uma consome.

| Tela do protótipo | Endpoints envolvidos |
|---|---|
| **Página inicial** (header/body/footer) | `POST /section/list`, `POST /category/list`, `POST /product/list` (destaques), `GET /cart` (contador do carrinho no header) |
| **Tela de produtos** (catálogo, filtros por categoria/seção, busca) | `POST /product/list` (filtros `category_id`, `nome`, `sku`, `status`), `POST /category/list`, `POST /section/list` |
| **Tela detalhada do produto** | `GET /product/{product_id}`, `POST /product-image/list` (`product_id`) |
| **Produtos relacionados** | `POST /product/list` filtrando por `category_id` do produto atual |
| **Carrinho de compras** | `GET /cart`, `POST /cart/add`, `PUT /cart/update-item`, `DELETE /cart/remove-item/{id}`, `DELETE /cart/clear` |
| **Finalização da compra** (endereço) | `POST /adress/list`, `POST /adress/create` |
| **Continuação da compra** (forma de pagamento) | escolha de `forma_pagamento` (`cartao`/`boleto`/`pix`) — usado no passo seguinte |
| **Pagamento** | `POST /order/checkout` (envia `adress_id` + `forma_pagamento`, recebe o pedido já com status e pagamento) |
| **Tela de pedidos** (cliente) | `POST /order/list` (cliente só vê os próprios), `GET /order/{order_id}` |
| **Tela de usuário** (perfil) | `PUT /users/update`, `POST /users/list` (filtrando o próprio e-mail/id) |
| **Tela de endereços** | `POST /adress/list`, `POST /adress/create`, `PUT /adress/update`, `DELETE /adress/delete/{id}` |
| **Dashboard administrativo** | `GET /dashboard` |
| **Gerenciamento de produtos** (admin) | CRUD completo de `/product`, `/category`, `/section`, `/product-image` |
| **Gerenciamento de pedidos** (admin) | `POST /order/list` (sem filtro de usuário, vê todos), `PUT /order/update-status`, `POST /order/{id}/confirm-payment` |

---

## 4. Referência de endpoints

> Convenção de rota: `create`/`list`/`update` são sempre `POST`/`POST`/`PUT` com corpo JSON;
> `delete` é sempre `DELETE` com o ID na URL. Atualizações (`update`) sempre levam o ID **no corpo**,
> não na URL (ex.: `{"product_id": 5, "nome": "Novo nome"}`).

### Auth (`/auth`) — público

| Método | Rota | Corpo | Observação |
|---|---|---|---|
| POST | `/auth/login` | `{ email, password }` | Retorna `{ access_token, token_type }` |

### Usuários (`/users`)

| Método | Rota | Acesso | Corpo |
|---|---|---|---|
| POST | `/users/create` | público | `{ name, email, cpf, password }` — sempre cria `role: cliente` |
| POST | `/users/list` | autenticado | filtros: `name`, `email`, `cpf`, `role` |
| PUT | `/users/update` | autenticado | `{ user_id, name?, email?, cpf?, password?, role? }` |
| DELETE | `/users/delete/{user_id}` | autenticado | — |

Regras: usuário `cliente` só pode atualizar/excluir a **própria** conta e nunca pode alterar o
próprio `role`. Admin pode tudo, incluindo promover outro usuário a admin via `role`.

Campos de `UserResponse`: `id, name, email, cpf, role`.

### Endereços (`/adress`) — autenticado

| Método | Rota | Corpo |
|---|---|---|
| POST | `/adress/create` | `{ rua, numero, cep, cidade, uf }` (sempre vinculado ao usuário logado) |
| POST | `/adress/list` | filtros: `user_id`, `cidade`, `uf`, `cep` |
| PUT | `/adress/update` | `{ adress_id, rua?, numero?, cep?, cidade?, uf? }` |
| DELETE | `/adress/delete/{adress_id}` | — |

> ⚠️ **Observação de segurança**: hoje `list`/`update`/`delete` de endereço **não restringem** ao
> dono do endereço — qualquer usuário autenticado pode operar sobre o ID de outro, se souber/
> adivinhar o ID. Recomenda-se que o backend passe a filtrar sempre por `user_id == current_user.id`
> (exceto para admin) antes de ir para produção. Por ora, o front deve sempre filtrar por
> `user_id` do usuário logado ao montar a tela de endereços.

### Seções (`/section`)

| Método | Rota | Acesso | Corpo |
|---|---|---|---|
| POST | `/section/create` | admin | `{ nome, descricao?, status? }` (`status`: `ativo`\|`inativo`, default `ativo`) |
| POST | `/section/list` | autenticado | filtros: `nome`, `status` |
| GET | `/section/{section_id}` | autenticado | — |
| PUT | `/section/update` | admin | `{ section_id, nome?, descricao?, status? }` |
| DELETE | `/section/delete/{section_id}` | admin | bloqueado se houver categoria **ativa** vinculada |

### Categorias (`/category`)

| Método | Rota | Acesso | Corpo |
|---|---|---|---|
| POST | `/category/create` | admin | `{ section_id, nome, descricao?, status? }` |
| POST | `/category/list` | autenticado | filtros: `section_id`, `nome`, `status` |
| GET | `/category/{category_id}` | autenticado | — |
| PUT | `/category/update` | admin | `{ category_id, section_id?, nome?, descricao?, status? }` |
| DELETE | `/category/delete/{category_id}` | admin | bloqueado se houver produto **ativo** vinculado |

### Produtos (`/product`)

| Método | Rota | Acesso | Corpo |
|---|---|---|---|
| POST | `/product/create` | admin | ver campos abaixo |
| POST | `/product/list` | autenticado | filtros: `category_id`, `nome`, `sku`, `status` |
| GET | `/product/{product_id}` | autenticado | — |
| PUT | `/product/update` | admin | mesmos campos, todos opcionais + `product_id` |
| DELETE | `/product/delete/{product_id}` | admin | — |

Campos de `ProductCreate`/`ProductResponse`:

```
category_id, nome, descricao?, preco, preco_promocional?, sku, quantidade_estoque,
estoque_minimo (default 5), peso?, dimensoes?, status (ativo|inativo, default ativo)
```

- `preco_promocional`, se definido, **precisa ser menor** que `preco` (senão a API rejeita).
- Quando o produto tem `preco_promocional` ativo e menor que `preco`, é esse o preço usado no
  carrinho/checkout — o front deve exibir o preço promocional como "preço atual" e o `preco` normal
  riscado, quando aplicável.
- `sku` é único.
- Produto com `status: inativo` não pode ser adicionado ao carrinho.

### Imagens de produto (`/product-image`)

| Método | Rota | Acesso | Corpo |
|---|---|---|---|
| POST | `/product-image/create` | admin | `{ product_id, url, principal? }` |
| POST | `/product-image/list` | autenticado | filtros: `product_id`, `principal` |
| PUT | `/product-image/update` | admin | `{ product_image_id, url?, principal? }` |
| DELETE | `/product-image/delete/{product_image_id}` | admin | — |

- `principal: true` marca a imagem de destaque do produto (capa). Ao marcar uma como principal, a
  API automaticamente desmarca as demais do mesmo produto.
- Cada produto pode ter até 5 imagens (regra de negócio da ERS — **validação ainda não aplicada no
  backend**, recomenda-se o front limitar o upload a 5 por enquanto).
- A API armazena apenas a **URL** da imagem — o upload/hospedagem do arquivo em si (S3, Cloudinary
  etc.) é responsabilidade do front ou de um serviço externo a ser definido.

### Carrinho (`/cart`) — autenticado, sempre o carrinho do usuário logado

| Método | Rota | Corpo |
|---|---|---|
| GET | `/cart` | — |
| POST | `/cart/add` | `{ product_id, quantidade }` |
| PUT | `/cart/update-item` | `{ cart_item_id, quantidade }` |
| DELETE | `/cart/remove-item/{cart_item_id}` | — |
| DELETE | `/cart/clear` | — |

Resposta (`CartResponse`):
```json
{
  "id": 1,
  "items": [
    { "id": 10, "product_id": 3, "product_nome": "Tubo PVC 100mm", "quantidade": 2, "preco_unitario": 50.0, "subtotal": 100.0 }
  ],
  "total": 100.0
}
```

Validações: bloqueia se o produto estiver `inativo` ou se a quantidade solicitada (somada à já
existente no carrinho) exceder o estoque disponível.

### Pedidos (`/order`)

| Método | Rota | Acesso | Corpo |
|---|---|---|---|
| POST | `/order/checkout` | cliente | `{ adress_id, forma_pagamento: "cartao"\|"boleto"\|"pix" }` |
| POST | `/order/list` | autenticado | cliente vê só os próprios; admin vê todos e pode filtrar por `user_id`, `status`, `data_inicio`, `data_fim` |
| GET | `/order/{order_id}` | autenticado | dono do pedido ou admin |
| PUT | `/order/update-status` | admin | `{ order_id, status }` |
| POST | `/order/{order_id}/confirm-payment` | admin | `{ aprovado: true\|false }` |
| POST | `/order/webhook/mercadopago` | público (Mercado Pago) | notificação de pagamento; não usado pelo front |

`status` do pedido (`OrderStatus`): `pendente`, `pago`, `em_separacao`, `enviado`, `entregue`,
`cancelado`, `nao_aprovado`.

Transições válidas (a API rejeita qualquer outra com `400`):
```
pendente      → cancelado
pago          → em_separacao | cancelado
em_separacao  → enviado | cancelado
enviado       → entregue | cancelado
entregue, cancelado, nao_aprovado → (finais, sem transição)
```

Comportamento do checkout depende do gateway ativo (`PAYMENT_GATEWAY` no `.env`, ver seção 5):

- **`mock`** (padrão, sem credenciais): `cartao`/`pix` aprovam imediatamente (`status: pago`,
  estoque já decrementado); `boleto` fica `pendente` até um admin chamar `confirm-payment`.
- **`mercadopago`** (real): o pedido é criado como `pendente` e a resposta traz `payment.gateway:
  "mercadopago"` e um campo extra **`checkout_url`** — a URL de Checkout Pro do Mercado Pago. O
  front deve abrir essa URL na modal/tela de pagamento do Mercado Pago (SDK JS `mp.checkout({
  preference: { id: payment.transaction_id }, autoOpen: true })` ou redirecionamento simples). A
  confirmação real do pagamento chega depois, de forma assíncrona, via webhook direto do Mercado
  Pago para a API — o front deve fazer polling em `GET /order/{order_id}` (ou aguardar o
  `back_urls.success` configurado) até o `status` mudar de `pendente` para `pago`/`nao_aprovado`.

Resposta (`OrderResponse`) com gateway mock:
```json
{
  "id": 1, "user_id": 5, "adress_id": 2, "status": "pago",
  "subtotal": 100.0, "desconto": 0.0, "total": 100.0, "created_at": "...",
  "items": [{ "id": 1, "product_id": 3, "product_nome": "Tubo PVC 100mm", "quantidade": 2, "preco_unitario": 50.0, "subtotal": 100.0 }],
  "payment": { "id": 1, "gateway": "mock", "forma_pagamento": "cartao", "status": "aprovado", "transaction_id": "mock_...", "valor": 100.0 },
  "checkout_url": null
}
```

Resposta com gateway `mercadopago`:
```json
{
  "id": 1, "user_id": 5, "adress_id": 2, "status": "pendente",
  "subtotal": 100.0, "desconto": 0.0, "total": 100.0, "created_at": "...",
  "items": [{ "id": 1, "product_id": 3, "product_nome": "Tubo PVC 100mm", "quantidade": 2, "preco_unitario": 50.0, "subtotal": 100.0 }],
  "payment": { "id": 1, "gateway": "mercadopago", "forma_pagamento": "cartao", "status": "pendente", "transaction_id": "<preference_id>", "valor": 100.0 },
  "checkout_url": "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=..."
}
```

### Relatórios (`/report`) — admin

| Método | Rota | Corpo / Query |
|---|---|---|
| POST | `/report/sales` | `{ data_inicio?, data_fim?, status? }` → JSON |
| GET | `/report/sales/csv` | `?data_inicio=&data_fim=&status_filtro=` → download CSV |

Sem `status` informado, o relatório considera apenas pedidos pagos/em andamento (exclui `pendente`,
`cancelado`, `nao_aprovado`) — equivale ao "faturado".

### Dashboard (`/dashboard`) — admin

`GET /dashboard` → `{ faturamento_7_dias, faturamento_30_dias, pedidos_pendentes, pedidos_pagos, pedidos_enviados, produtos_estoque_baixo: [{id, nome, sku, quantidade_estoque, estoque_minimo}], total_usuarios }`

---

## 5. O que está mockado / simplificado nesta fase

O front deve saber disso para não montar telas que dependam de comportamento real ainda não
implementado:

- **Gateway de pagamento**: existe integração real com Mercado Pago (Checkout Pro), mas ela só fica
  ativa quando `PAYMENT_GATEWAY=mercadopago` e as credenciais (`MERCADOPAGO_ACCESS_TOKEN`,
  `MERCADOPAGO_WEBHOOK_SECRET`, etc.) estiverem preenchidas no `.env` — ainda não temos essas
  credenciais de teste do Mercado Pago, então em produção o gateway continua como `mock` (aprova
  cartão/PIX de imediato, deixa boleto pendente) até isso ser configurado. Quando o gateway real
  estiver ativo, o checkout devolve um `checkout_url` (ver seção 4) que o front abre na modal do
  Mercado Pago; a confirmação chega depois via webhook (`POST /order/webhook/mercadopago`, sem
  autenticação, chamado pelo próprio Mercado Pago).
- **E-mails** (confirmação de pedido, alerta de estoque baixo): apenas logados no servidor, não
  enviados de fato. Não há tela ou endpoint de "reenviar e-mail" hoje.
- **Frete**: não existe cálculo de frete (fora do escopo da ERS atual). O campo `total` do pedido é
  igual ao `subtotal` (sem `desconto` automático além do preço promocional do produto).
- **Cupom de desconto**: não existe (adiado pela própria ERS).
- **Upload de imagem**: a API só guarda a URL; o upload do arquivo em si precisa de uma solução
  separada (serviço de storage) a ser definida com o time.

---

## 6. Próximos passos sugeridos para o front

1. Montar a camada de API client (ex.: Axios/Fetch) com interceptor que injeta o `Authorization`
   header e trata `401` redirecionando para login.
2. Implementar as telas públicas (catálogo, detalhe do produto, carrinho) sem exigir login até o
   checkout, como indicado na ERS — chamadas de catálogo hoje exigem token (`get_current_user`) para
   todo `list`/`get`; combinar com o time se isso deve abrir para visitantes não autenticados.
3. Esconder rotas/menus administrativos com base no `role` retornado no login/perfil do usuário.
