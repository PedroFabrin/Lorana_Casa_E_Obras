"""Popula o catálogo (seções, categorias, produtos e imagens) para deixar a loja
com uma vitrine completa para demonstração/apresentação.

Idempotente: pode ser executado várias vezes sem duplicar seções, categorias ou
produtos (identificados por nome/SKU). Se a imagem de um produto estiver ausente
ou desatualizada em relação ao mapeamento IMAGE_URLS, ela é substituída.

Uso (dentro do container da API):
    docker exec lorana_api python scripts/seed_catalog.py

Cada produto tem 1 foto real (não fictícia) hospedada no Wikimedia Commons
(licença livre), escolhida e conferida visualmente uma a uma para condizer com
o produto — a API só guarda a URL, não faz upload de arquivo (ver
docs/FRONTEND_HANDOFF.md). Alguns produtos correlatos (ex.: variações de cabo
elétrico, ou o kit de acabamento reaproveitando a foto de torneira) reaproveitam
a mesma foto de um produto vizinho quando não existe imagem específica e
verificada disponível com licença livre.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.model.sectionModel.section_model import SectionModel
from app.model.categoryModel.category_model import CategoryModel
from app.model.productModel.product_model import ProductModel
from app.model.productImageModel.product_image_model import ProductImageModel

SECTIONS = [
    {"nome": "Ferramentas", "descricao": "Furadeiras, parafusadeiras, serras e tudo para quem trabalha manualmente ou com energia elétrica."},
    {"nome": "Material de Construção", "descricao": "Cimento, argamassa, revestimentos e madeiras para obra e reforma."},
    {"nome": "Elétrica", "descricao": "Fios, cabos, iluminação e proteção para instalações elétricas residenciais e comerciais."},
    {"nome": "Hidráulica", "descricao": "Tubos, conexões, louças e metais para instalações hidráulicas."},
    {"nome": "Tintas e Acabamentos", "descricao": "Tintas, vernizes e acessórios de pintura para dar o acabamento final na sua obra."},
    {"nome": "Jardim e Área Externa", "descricao": "Ferramentas de jardinagem e irrigação para cuidar das áreas externas."},
]

CATEGORIES = [
    {"section": "Ferramentas", "nome": "Ferramentas Elétricas", "descricao": "Furadeiras, serras e lixadeiras elétricas para agilizar qualquer serviço."},
    {"section": "Ferramentas", "nome": "Ferramentas Manuais", "descricao": "Martelos, chaves, alicates e outras ferramentas de uso manual."},
    {"section": "Ferramentas", "nome": "Medição e Nivelamento", "descricao": "Trenas, níveis e esquadros para medições precisas."},
    {"section": "Material de Construção", "nome": "Cimento, Argamassa e Agregados", "descricao": "Insumos básicos para alvenaria, reboco e assentamento."},
    {"section": "Material de Construção", "nome": "Pisos e Revestimentos", "descricao": "Porcelanatos, azulejos e pisos laminados para todos os ambientes."},
    {"section": "Material de Construção", "nome": "Madeiras e Compensados", "descricao": "Painéis, tábuas e vigas de madeira para estrutura e acabamento."},
    {"section": "Elétrica", "nome": "Fios e Cabos", "descricao": "Cabos flexíveis, fios paralelos e acessórios para instalação elétrica."},
    {"section": "Elétrica", "nome": "Iluminação", "descricao": "Lâmpadas, luminárias e fitas de LED para todos os ambientes."},
    {"section": "Elétrica", "nome": "Disjuntores e Quadros de Distribuição", "descricao": "Disjuntores, DRs e quadros para proteção da instalação elétrica."},
    {"section": "Hidráulica", "nome": "Tubos e Conexões", "descricao": "Tubos de PVC, joelhos, registros e adaptadores hidráulicos."},
    {"section": "Hidráulica", "nome": "Louças e Metais", "descricao": "Vasos sanitários, cubas, torneiras e chuveiros."},
    {"section": "Tintas e Acabamentos", "nome": "Tintas", "descricao": "Tintas látex, acrílicas, esmaltes e vernizes para todo tipo de superfície."},
    {"section": "Tintas e Acabamentos", "nome": "Pincéis, Rolos e Acessórios", "descricao": "Rolos, pincéis, fitas e demais acessórios para pintura."},
    {"section": "Jardim e Área Externa", "nome": "Ferramentas de Jardim", "descricao": "Cortadores de grama, pás, tesouras de poda e carrinhos de mão."},
    {"section": "Jardim e Área Externa", "nome": "Irrigação", "descricao": "Mangueiras, aspersores e acessórios para irrigação do jardim."},
]

# preco_promocional=None quando o produto não está em promoção.
# estoque/estoque_minimo com margem apertada em alguns itens (marcados com "*")
# para demonstrar o alerta de estoque baixo (order_service._notify_low_stock)
# assim que um pedido decrementar esse produto.
PRODUCTS = [
    # Ferramentas Elétricas
    {"categoria": "Ferramentas Elétricas", "nome": "Furadeira de Impacto 750W", "sku": "FE-001",
     "descricao": "Furadeira de impacto 750W com mandril de 13mm, ideal para perfurar concreto, madeira e metal.",
     "preco": 349.90, "preco_promocional": 299.90, "estoque": 42, "estoque_minimo": 5, "peso": 1.8, "dimensoes": "35x22x10 cm"},
    {"categoria": "Ferramentas Elétricas", "nome": "Parafusadeira/Furadeira a Bateria 20V", "sku": "FE-002",
     "descricao": "Parafusadeira e furadeira sem fio, bateria de lítio 20V, com estojo e duas baterias inclusas.",
     "preco": 459.00, "preco_promocional": None, "estoque": 28, "estoque_minimo": 5, "peso": 2.1, "dimensoes": "30x25x10 cm"},
    {"categoria": "Ferramentas Elétricas", "nome": "Serra Circular Elétrica 1500W", "sku": "FE-003",
     "descricao": "Serra circular 1500W com disco de 7.1/4\", guia paralelo e ajuste de profundidade e inclinação.",
     "preco": 599.00, "preco_promocional": None, "estoque": 15, "estoque_minimo": 4, "peso": 3.9, "dimensoes": "35x30x22 cm"},
    {"categoria": "Ferramentas Elétricas", "nome": "Esmerilhadeira Angular 4.1/2\" 850W", "sku": "FE-004",
     "descricao": "Esmerilhadeira angular 850W para corte e desbaste de metais, concreto e cerâmica.",
     "preco": 259.90, "preco_promocional": None, "estoque": 33, "estoque_minimo": 5, "peso": 1.9, "dimensoes": "28x11x10 cm"},
    {"categoria": "Ferramentas Elétricas", "nome": "Lixadeira Orbital 220W", "sku": "FE-005",
     "descricao": "Lixadeira orbital 220W com sistema de aspiração de pó e base para lixas de velcro.",
     "preco": 219.90, "preco_promocional": None, "estoque": 24, "estoque_minimo": 5, "peso": 1.3, "dimensoes": "24x12x12 cm"},

    # Ferramentas Manuais
    {"categoria": "Ferramentas Manuais", "nome": "Martelo Unha 27mm Cabo Fibra", "sku": "FM-001",
     "descricao": "Martelo unha cabeça 27mm, cabo em fibra de vidro com empunhadura emborrachada antiderrapante.",
     "preco": 49.90, "preco_promocional": None, "estoque": 80, "estoque_minimo": 10, "peso": 0.6, "dimensoes": "33x12x3 cm"},
    {"categoria": "Ferramentas Manuais", "nome": "Kit Chaves de Fenda e Phillips 6 Peças", "sku": "FM-002",
     "descricao": "Kit com 6 chaves de fenda e Phillips de tamanhos variados, cabo emborrachado antideslizante.",
     "preco": 39.90, "preco_promocional": None, "estoque": 95, "estoque_minimo": 10, "peso": 0.5, "dimensoes": "25x15x4 cm"},
    {"categoria": "Ferramentas Manuais", "nome": "Alicate Universal 8\"", "sku": "FM-003",
     "descricao": "Alicate universal 8 polegadas em aço cromo-vanádio, cabo bicomponente isolado até 1000V.",
     "preco": 34.90, "preco_promocional": None, "estoque": 6, "estoque_minimo": 5, "peso": 0.3, "dimensoes": "20x8x2 cm"},
    {"categoria": "Ferramentas Manuais", "nome": "Serrote para Madeira 22\"", "sku": "FM-004",
     "descricao": "Serrote 22 polegadas com dentes tratados termicamente e cabo ergonômico bimaterial.",
     "preco": 44.90, "preco_promocional": None, "estoque": 40, "estoque_minimo": 8, "peso": 0.4, "dimensoes": "56x15x3 cm"},
    {"categoria": "Ferramentas Manuais", "nome": "Jogo de Chaves Combinadas 8-19mm", "sku": "FM-005",
     "descricao": "Jogo com 8 chaves combinadas (boca/estrela) de 8 a 19mm em aço cromo-vanádio, com estojo.",
     "preco": 129.90, "preco_promocional": None, "estoque": 22, "estoque_minimo": 5, "peso": 1.1, "dimensoes": "30x18x5 cm"},

    # Medição e Nivelamento
    {"categoria": "Medição e Nivelamento", "nome": "Trena a Laser 40m", "sku": "MN-001",
     "descricao": "Trena a laser com alcance de até 40m, memória de medições e cálculo automático de área e volume.",
     "preco": 249.00, "preco_promocional": None, "estoque": 18, "estoque_minimo": 5, "peso": 0.2, "dimensoes": "12x6x3 cm"},
    {"categoria": "Medição e Nivelamento", "nome": "Nível de Bolha Profissional 60cm", "sku": "MN-002",
     "descricao": "Nível de bolha em alumínio de 60cm, com 3 fiolas de alta precisão e superfície fresada.",
     "preco": 59.90, "preco_promocional": None, "estoque": 36, "estoque_minimo": 6, "peso": 0.5, "dimensoes": "62x5x3 cm"},
    {"categoria": "Medição e Nivelamento", "nome": "Trena Manual 5m", "sku": "MN-003",
     "descricao": "Trena manual de 5 metros com trava automática, fita de aço revestida e clip para cinto.",
     "preco": 19.90, "preco_promocional": None, "estoque": 120, "estoque_minimo": 15, "peso": 0.2, "dimensoes": "7x6x4 cm"},
    {"categoria": "Medição e Nivelamento", "nome": "Esquadro de Aço 30cm", "sku": "MN-004",
     "descricao": "Esquadro de aço carbono 30cm com escala graduada em milímetros dos dois lados.",
     "preco": 24.90, "preco_promocional": None, "estoque": 55, "estoque_minimo": 8, "peso": 0.3, "dimensoes": "30x20x1 cm"},
    {"categoria": "Medição e Nivelamento", "nome": "Prumo de Centro em Aço", "sku": "MN-005",
     "descricao": "Prumo de centro em aço zincado com ponta cônica, ideal para verificação de verticalidade.",
     "preco": 14.90, "preco_promocional": None, "estoque": 60, "estoque_minimo": 10, "peso": 0.2, "dimensoes": "8x4x4 cm"},

    # Cimento, Argamassa e Agregados
    {"categoria": "Cimento, Argamassa e Agregados", "nome": "Cimento CP II 50kg", "sku": "CA-001",
     "descricao": "Cimento Portland composto CP II, saco de 50kg, indicado para uso geral em obras.",
     "preco": 38.90, "preco_promocional": None, "estoque": 200, "estoque_minimo": 30, "peso": 50.0, "dimensoes": "60x40x10 cm"},
    {"categoria": "Cimento, Argamassa e Agregados", "nome": "Argamassa Colante AC-I 20kg", "sku": "CA-002",
     "descricao": "Argamassa colante tipo AC-I para assentamento de revestimentos cerâmicos em áreas internas.",
     "preco": 24.90, "preco_promocional": None, "estoque": 150, "estoque_minimo": 20, "peso": 20.0, "dimensoes": "40x30x8 cm"},
    {"categoria": "Cimento, Argamassa e Agregados", "nome": "Areia Média Ensacada 20kg", "sku": "CA-003",
     "descricao": "Areia média lavada, ensacada em pacotes de 20kg, ideal para reboco e contrapiso.",
     "preco": 12.90, "preco_promocional": None, "estoque": 180, "estoque_minimo": 25, "peso": 20.0, "dimensoes": "40x30x8 cm"},
    {"categoria": "Cimento, Argamassa e Agregados", "nome": "Cal Hidratada 20kg", "sku": "CA-004",
     "descricao": "Cal hidratada CH-I, saco de 20kg, usada em argamassas de assentamento e pintura.",
     "preco": 16.90, "preco_promocional": None, "estoque": 140, "estoque_minimo": 20, "peso": 20.0, "dimensoes": "40x28x8 cm"},
    {"categoria": "Cimento, Argamassa e Agregados", "nome": "Rejunte Flexível 1kg", "sku": "CA-005",
     "descricao": "Rejunte flexível com resistência a fungos e mofo, disponível em cinza, saco de 1kg.",
     "preco": 18.90, "preco_promocional": None, "estoque": 90, "estoque_minimo": 15, "peso": 1.0, "dimensoes": "15x10x5 cm"},

    # Pisos e Revestimentos
    {"categoria": "Pisos e Revestimentos", "nome": "Porcelanato Acetinado 60x60cm (caixa 2,16m²)", "sku": "PR-001",
     "descricao": "Porcelanato acetinado retificado 60x60cm, caixa com 2,16m², indicado para pisos e paredes.",
     "preco": 89.90, "preco_promocional": 74.90, "estoque": 60, "estoque_minimo": 10, "peso": 32.0, "dimensoes": "60x60x1 cm"},
    {"categoria": "Pisos e Revestimentos", "nome": "Azulejo Branco Brilhante 30x40cm (caixa 1,92m²)", "sku": "PR-002",
     "descricao": "Azulejo branco brilhante 30x40cm, caixa com 1,92m², ideal para cozinhas e banheiros.",
     "preco": 49.90, "preco_promocional": None, "estoque": 70, "estoque_minimo": 10, "peso": 24.0, "dimensoes": "40x30x1 cm"},
    {"categoria": "Pisos e Revestimentos", "nome": "Piso Laminado Clicado 8mm (caixa 2,4m²)", "sku": "PR-003",
     "descricao": "Piso laminado clicado 8mm, textura amadeirada, caixa com 2,4m², fácil instalação sem cola.",
     "preco": 119.90, "preco_promocional": None, "estoque": 45, "estoque_minimo": 8, "peso": 18.0, "dimensoes": "120x20x1 cm"},
    {"categoria": "Pisos e Revestimentos", "nome": "Rodapé de MDF Branco 7cm (barra 2,40m)", "sku": "PR-004",
     "descricao": "Rodapé em MDF revestido branco, altura 7cm, barra com 2,40m de comprimento.",
     "preco": 22.90, "preco_promocional": None, "estoque": 100, "estoque_minimo": 15, "peso": 1.2, "dimensoes": "240x7x1 cm"},
    {"categoria": "Pisos e Revestimentos", "nome": "Pastilha de Vidro Mosaico 30x30cm", "sku": "PR-005",
     "descricao": "Placa de pastilha de vidro mosaico 30x30cm, ideal para painéis decorativos e áreas molhadas.",
     "preco": 34.90, "preco_promocional": None, "estoque": 50, "estoque_minimo": 8, "peso": 1.5, "dimensoes": "30x30x1 cm"},

    # Madeiras e Compensados
    {"categoria": "Madeiras e Compensados", "nome": "Compensado Multilaminado 15mm (2,20x1,60m)", "sku": "MC-001",
     "descricao": "Chapa de compensado multilaminado 15mm, medindo 2,20x1,60m, resistente para estruturas e forros.",
     "preco": 189.90, "preco_promocional": 169.90, "estoque": 25, "estoque_minimo": 5, "peso": 28.0, "dimensoes": "220x160x1.5 cm"},
    {"categoria": "Madeiras e Compensados", "nome": "Sarrafo de Pinus 5x2,5cm (3m)", "sku": "MC-002",
     "descricao": "Sarrafo de pinus aparelhado 5x2,5cm, barra de 3 metros, usado em estruturas leves e forros.",
     "preco": 14.90, "preco_promocional": None, "estoque": 200, "estoque_minimo": 30, "peso": 2.5, "dimensoes": "300x5x2.5 cm"},
    {"categoria": "Madeiras e Compensados", "nome": "Painel de MDF Cru 15mm (2,75x1,83m)", "sku": "MC-003",
     "descricao": "Painel de MDF cru 15mm, medindo 2,75x1,83m, pronto para pintura ou revestimento.",
     "preco": 249.90, "preco_promocional": None, "estoque": 20, "estoque_minimo": 5, "peso": 35.0, "dimensoes": "275x183x1.5 cm"},
    {"categoria": "Madeiras e Compensados", "nome": "Tábua de Pinus Aparelhada 20x2,5cm (3m)", "sku": "MC-004",
     "descricao": "Tábua de pinus aparelhada 20x2,5cm, barra de 3 metros, para marcenaria e acabamentos.",
     "preco": 39.90, "preco_promocional": None, "estoque": 90, "estoque_minimo": 15, "peso": 6.5, "dimensoes": "300x20x2.5 cm"},
    {"categoria": "Madeiras e Compensados", "nome": "Viga de Madeira Eucalipto 6x12cm (3m)", "sku": "MC-005",
     "descricao": "Viga de eucalipto tratado 6x12cm, barra de 3 metros, indicada para estruturas de telhado.",
     "preco": 79.90, "preco_promocional": None, "estoque": 35, "estoque_minimo": 8, "peso": 18.0, "dimensoes": "300x12x6 cm"},

    # Fios e Cabos
    {"categoria": "Fios e Cabos", "nome": "Cabo Flexível 2,5mm² (rolo 100m)", "sku": "FC-001",
     "descricao": "Cabo flexível de cobre 2,5mm², rolo com 100 metros, isolação em PVC 750V, cor preta.",
     "preco": 159.90, "preco_promocional": None, "estoque": 40, "estoque_minimo": 8, "peso": 3.2, "dimensoes": "30x30x15 cm"},
    {"categoria": "Fios e Cabos", "nome": "Cabo Flexível 4,0mm² (rolo 100m)", "sku": "FC-002",
     "descricao": "Cabo flexível de cobre 4,0mm², rolo com 100 metros, isolação em PVC 750V, cor azul.",
     "preco": 239.90, "preco_promocional": None, "estoque": 30, "estoque_minimo": 6, "peso": 4.8, "dimensoes": "32x32x16 cm"},
    {"categoria": "Fios e Cabos", "nome": "Fio Paralelo 2x1,5mm² (rolo 50m)", "sku": "FC-003",
     "descricao": "Fio paralelo 2x1,5mm², rolo com 50 metros, indicado para instalações de baixa potência.",
     "preco": 89.90, "preco_promocional": None, "estoque": 55, "estoque_minimo": 10, "peso": 1.4, "dimensoes": "20x20x10 cm"},
    {"categoria": "Fios e Cabos", "nome": "Cabo PP 3x2,5mm² (rolo 20m)", "sku": "FC-004",
     "descricao": "Cabo PP 3x2,5mm², rolo com 20 metros, indicado para ligação de equipamentos e extensões.",
     "preco": 129.90, "preco_promocional": None, "estoque": 25, "estoque_minimo": 5, "peso": 2.0, "dimensoes": "22x22x12 cm"},
    {"categoria": "Fios e Cabos", "nome": "Fita Isolante Antichama 20m", "sku": "FC-005",
     "descricao": "Fita isolante antichama, alta aderência, rolo com 20 metros, cor preta.",
     "preco": 9.90, "preco_promocional": None, "estoque": 300, "estoque_minimo": 40, "peso": 0.1, "dimensoes": "5x5x2 cm"},

    # Iluminação
    {"categoria": "Iluminação", "nome": "Lâmpada LED Bulbo 12W Branca", "sku": "IL-001",
     "descricao": "Lâmpada LED bulbo 12W, luz branca 6500K, soquete E27, baixo consumo de energia.",
     "preco": 14.90, "preco_promocional": None, "estoque": 250, "estoque_minimo": 30, "peso": 0.1, "dimensoes": "12x6x6 cm"},
    {"categoria": "Iluminação", "nome": "Painel LED de Embutir 24W Quadrado", "sku": "IL-002",
     "descricao": "Painel LED de embutir quadrado 24W, luz branca neutra, para forros de gesso e PVC.",
     "preco": 39.90, "preco_promocional": None, "estoque": 90, "estoque_minimo": 15, "peso": 0.5, "dimensoes": "30x30x3 cm"},
    {"categoria": "Iluminação", "nome": "Refletor LED Holofote 50W", "sku": "IL-003",
     "descricao": "Refletor LED holofote 50W, à prova d'água (IP65), ideal para áreas externas e fachadas.",
     "preco": 69.90, "preco_promocional": 54.90, "estoque": 60, "estoque_minimo": 10, "peso": 0.9, "dimensoes": "20x15x5 cm"},
    {"categoria": "Iluminação", "nome": "Luminária Pendente Industrial", "sku": "IL-004",
     "descricao": "Luminária pendente estilo industrial em metal preto fosco, compatível com lâmpada E27.",
     "preco": 129.90, "preco_promocional": None, "estoque": 20, "estoque_minimo": 5, "peso": 1.2, "dimensoes": "25x25x30 cm"},
    {"categoria": "Iluminação", "nome": "Fita LED 5m com Fonte", "sku": "IL-005",
     "descricao": "Fita de LED 5 metros, luz branca fria, acompanha fonte bivolt e controle liga/desliga.",
     "preco": 59.90, "preco_promocional": None, "estoque": 75, "estoque_minimo": 12, "peso": 0.3, "dimensoes": "15x10x5 cm"},

    # Disjuntores e Quadros de Distribuição
    {"categoria": "Disjuntores e Quadros de Distribuição", "nome": "Disjuntor Monopolar 20A", "sku": "DQ-001",
     "descricao": "Disjuntor termomagnético monopolar 20A, padrão DIN, para proteção de circuitos residenciais.",
     "preco": 12.90, "preco_promocional": None, "estoque": 150, "estoque_minimo": 20, "peso": 0.1, "dimensoes": "8x4x7 cm"},
    {"categoria": "Disjuntores e Quadros de Distribuição", "nome": "Disjuntor Bipolar 40A", "sku": "DQ-002",
     "descricao": "Disjuntor termomagnético bipolar 40A, padrão DIN, indicado para chuveiros e ar-condicionado.",
     "preco": 34.90, "preco_promocional": None, "estoque": 7, "estoque_minimo": 5, "peso": 0.2, "dimensoes": "8x8x7 cm"},
    {"categoria": "Disjuntores e Quadros de Distribuição", "nome": "Quadro de Distribuição 12 Disjuntores", "sku": "DQ-003",
     "descricao": "Quadro de distribuição de embutir para até 12 disjuntores DIN, com barramento incluso.",
     "preco": 89.90, "preco_promocional": None, "estoque": 30, "estoque_minimo": 6, "peso": 2.5, "dimensoes": "40x30x10 cm"},
    {"categoria": "Disjuntores e Quadros de Distribuição", "nome": "DR Interruptor Diferencial Residual 40A", "sku": "DQ-004",
     "descricao": "Interruptor diferencial residual (DR) 40A bipolar 30mA, proteção contra choques elétricos.",
     "preco": 149.90, "preco_promocional": None, "estoque": 18, "estoque_minimo": 5, "peso": 0.3, "dimensoes": "9x9x7 cm"},
    {"categoria": "Disjuntores e Quadros de Distribuição", "nome": "Barramento Trifásico para Quadro", "sku": "DQ-005",
     "descricao": "Barramento trifásico de cobre estanhado para quadros de distribuição de até 12 polos.",
     "preco": 44.90, "preco_promocional": None, "estoque": 40, "estoque_minimo": 8, "peso": 0.4, "dimensoes": "25x3x2 cm"},

    # Tubos e Conexões
    {"categoria": "Tubos e Conexões", "nome": "Tubo PVC Soldável 25mm (barra 3m)", "sku": "TC-001",
     "descricao": "Tubo de PVC soldável 25mm, barra de 3 metros, para instalações hidráulicas de água fria.",
     "preco": 19.90, "preco_promocional": None, "estoque": 120, "estoque_minimo": 20, "peso": 1.1, "dimensoes": "300x2.5x2.5 cm"},
    {"categoria": "Tubos e Conexões", "nome": "Tubo PVC Esgoto 100mm (barra 3m)", "sku": "TC-002",
     "descricao": "Tubo de PVC para esgoto 100mm, barra de 3 metros, série normal conforme NBR 5688.",
     "preco": 59.90, "preco_promocional": 49.90, "estoque": 70, "estoque_minimo": 12, "peso": 3.5, "dimensoes": "300x10x10 cm"},
    {"categoria": "Tubos e Conexões", "nome": "Joelho 90° PVC Soldável 25mm", "sku": "TC-003",
     "descricao": "Conexão joelho 90 graus em PVC soldável, diâmetro 25mm, para mudança de direção da tubulação.",
     "preco": 2.90, "preco_promocional": None, "estoque": 400, "estoque_minimo": 50, "peso": 0.05, "dimensoes": "5x5x5 cm"},
    {"categoria": "Tubos e Conexões", "nome": "Registro de Gaveta 3/4\"", "sku": "TC-004",
     "descricao": "Registro de gaveta bruto 3/4 de polegada, corpo em latão, para controle de fluxo de água.",
     "preco": 29.90, "preco_promocional": None, "estoque": 60, "estoque_minimo": 10, "peso": 0.3, "dimensoes": "10x6x6 cm"},
    {"categoria": "Tubos e Conexões", "nome": "Adaptador PVC Roscável 25mm", "sku": "TC-005",
     "descricao": "Adaptador soldável x roscável em PVC, diâmetro 25mm x 3/4 de polegada, com anel de vedação.",
     "preco": 4.90, "preco_promocional": None, "estoque": 250, "estoque_minimo": 30, "peso": 0.05, "dimensoes": "6x4x4 cm"},

    # Louças e Metais
    {"categoria": "Louças e Metais", "nome": "Vaso Sanitário com Caixa Acoplada", "sku": "LM-001",
     "descricao": "Vaso sanitário com caixa acoplada em louça branca, sistema de dupla descarga economizador.",
     "preco": 449.90, "preco_promocional": 399.90, "estoque": 20, "estoque_minimo": 4, "peso": 22.0, "dimensoes": "68x36x76 cm"},
    {"categoria": "Louças e Metais", "nome": "Cuba de Apoio para Banheiro", "sku": "LM-002",
     "descricao": "Cuba de apoio em louça branca, formato oval, para bancadas de banheiro.",
     "preco": 189.90, "preco_promocional": None, "estoque": 25, "estoque_minimo": 5, "peso": 6.5, "dimensoes": "45x35x15 cm"},
    {"categoria": "Louças e Metais", "nome": "Torneira de Mesa para Cozinha", "sku": "LM-003",
     "descricao": "Torneira de mesa para cozinha, bica alta móvel, acabamento cromado.",
     "preco": 119.90, "preco_promocional": None, "estoque": 35, "estoque_minimo": 6, "peso": 0.8, "dimensoes": "20x8x35 cm"},
    {"categoria": "Louças e Metais", "nome": "Chuveiro Elétrico 220V 5500W", "sku": "LM-004",
     "descricao": "Chuveiro elétrico com 3 temperaturas, potência 5500W, tensão 220V, corpo em ABS.",
     "preco": 89.90, "preco_promocional": None, "estoque": 7, "estoque_minimo": 5, "peso": 0.7, "dimensoes": "25x12x12 cm"},
    {"categoria": "Louças e Metais", "nome": "Kit Acabamento para Registro", "sku": "LM-005",
     "descricao": "Kit de acabamento cromado para registro de pressão ou gaveta, com canopla e manípulo.",
     "preco": 39.90, "preco_promocional": None, "estoque": 50, "estoque_minimo": 8, "peso": 0.3, "dimensoes": "10x10x5 cm"},

    # Tintas
    {"categoria": "Tintas", "nome": "Tinta Látex PVA Branca 18L", "sku": "TN-001",
     "descricao": "Tinta látex PVA branca fosca, lata de 18 litros, rendimento de até 300m² por demão.",
     "preco": 189.90, "preco_promocional": 159.90, "estoque": 45, "estoque_minimo": 8, "peso": 20.0, "dimensoes": "30x30x35 cm"},
    {"categoria": "Tintas", "nome": "Tinta Acrílica Fosca Cores 3,6L", "sku": "TN-002",
     "descricao": "Tinta acrílica fosca, disponível em diversas cores, lata de 3,6 litros, uso interno e externo.",
     "preco": 99.90, "preco_promocional": None, "estoque": 60, "estoque_minimo": 10, "peso": 4.2, "dimensoes": "18x18x20 cm"},
    {"categoria": "Tintas", "nome": "Esmalte Sintético Brilhante 900ml", "sku": "TN-003",
     "descricao": "Esmalte sintético brilhante, alta durabilidade, lata de 900ml, ideal para madeira e metal.",
     "preco": 44.90, "preco_promocional": None, "estoque": 70, "estoque_minimo": 10, "peso": 1.1, "dimensoes": "10x10x14 cm"},
    {"categoria": "Tintas", "nome": "Verniz Marítimo Brilhante 900ml", "sku": "TN-004",
     "descricao": "Verniz marítimo brilhante, proteção UV, lata de 900ml, indicado para áreas externas e madeiras.",
     "preco": 54.90, "preco_promocional": None, "estoque": 40, "estoque_minimo": 8, "peso": 1.1, "dimensoes": "10x10x14 cm"},
    {"categoria": "Tintas", "nome": "Massa Corrida PVA 25kg", "sku": "TN-005",
     "descricao": "Massa corrida PVA para nivelamento de paredes internas antes da pintura, balde de 25kg.",
     "preco": 79.90, "preco_promocional": None, "estoque": 35, "estoque_minimo": 6, "peso": 25.0, "dimensoes": "35x35x30 cm"},

    # Pincéis, Rolos e Acessórios
    {"categoria": "Pincéis, Rolos e Acessórios", "nome": "Rolo de Lã para Tinta 23cm", "sku": "PA-001",
     "descricao": "Rolo de lã de carneiro sintética 23cm, ideal para aplicação de tintas látex e acrílicas.",
     "preco": 19.90, "preco_promocional": None, "estoque": 150, "estoque_minimo": 20, "peso": 0.2, "dimensoes": "25x8x8 cm"},
    {"categoria": "Pincéis, Rolos e Acessórios", "nome": "Pincel Trincha 2\"", "sku": "PA-002",
     "descricao": "Pincel trincha 2 polegadas, cerdas sintéticas, ideal para acabamentos e cantos.",
     "preco": 9.90, "preco_promocional": None, "estoque": 200, "estoque_minimo": 25, "peso": 0.1, "dimensoes": "20x5x2 cm"},
    {"categoria": "Pincéis, Rolos e Acessórios", "nome": "Bandeja Plástica para Pintura", "sku": "PA-003",
     "descricao": "Bandeja plástica para pintura com rolo, rampa texturizada para melhor distribuição de tinta.",
     "preco": 14.90, "preco_promocional": None, "estoque": 100, "estoque_minimo": 15, "peso": 0.3, "dimensoes": "35x25x6 cm"},
    {"categoria": "Pincéis, Rolos e Acessórios", "nome": "Fita Crepe para Pintura 48mm", "sku": "PA-004",
     "descricao": "Fita crepe para pintura, largura 48mm, rolo com 50 metros, fácil remoção sem resíduos.",
     "preco": 12.90, "preco_promocional": None, "estoque": 180, "estoque_minimo": 25, "peso": 0.1, "dimensoes": "10x10x5 cm"},
    {"categoria": "Pincéis, Rolos e Acessórios", "nome": "Lixa para Parede Grão 120 (kit 5un)", "sku": "PA-005",
     "descricao": "Kit com 5 folhas de lixa para parede, grão 120, ideal para preparação antes da pintura.",
     "preco": 16.90, "preco_promocional": None, "estoque": 90, "estoque_minimo": 15, "peso": 0.2, "dimensoes": "23x9x1 cm"},

    # Ferramentas de Jardim
    {"categoria": "Ferramentas de Jardim", "nome": "Cortador de Grama Elétrico 1200W", "sku": "FJ-001",
     "descricao": "Cortador de grama elétrico 1200W, cesto coletor de 35L e altura de corte ajustável.",
     "preco": 549.90, "preco_promocional": 479.90, "estoque": 14, "estoque_minimo": 4, "peso": 9.5, "dimensoes": "100x40x100 cm"},
    {"categoria": "Ferramentas de Jardim", "nome": "Pá de Jardinagem com Cabo", "sku": "FJ-002",
     "descricao": "Pá de jardinagem com lâmina em aço carbono e cabo em madeira, ideal para plantio e transplante.",
     "preco": 34.90, "preco_promocional": None, "estoque": 60, "estoque_minimo": 10, "peso": 0.8, "dimensoes": "90x15x10 cm"},
    {"categoria": "Ferramentas de Jardim", "nome": "Tesoura de Poda Profissional", "sku": "FJ-003",
     "descricao": "Tesoura de poda profissional com lâmina em aço carbono e trava de segurança.",
     "preco": 49.90, "preco_promocional": None, "estoque": 45, "estoque_minimo": 8, "peso": 0.3, "dimensoes": "20x8x3 cm"},
    {"categoria": "Ferramentas de Jardim", "nome": "Ancinho de Jardim 14 Dentes", "sku": "FJ-004",
     "descricao": "Ancinho de jardim com 14 dentes em aço e cabo longo em madeira, para limpeza de folhas e gramados.",
     "preco": 39.90, "preco_promocional": None, "estoque": 40, "estoque_minimo": 8, "peso": 0.9, "dimensoes": "150x35x5 cm"},
    {"categoria": "Ferramentas de Jardim", "nome": "Carrinho de Mão Reforçado", "sku": "FJ-005",
     "descricao": "Carrinho de mão reforçado com caçamba de 60 litros e pneu inflável, ideal para obras e jardim.",
     "preco": 249.90, "preco_promocional": None, "estoque": 20, "estoque_minimo": 4, "peso": 12.0, "dimensoes": "130x60x60 cm"},

    # Irrigação
    {"categoria": "Irrigação", "nome": "Mangueira de Jardim 20m com Esguicho", "sku": "IR-001",
     "descricao": "Mangueira de jardim trançada 20 metros, acompanha esguicho regulável e engates rápidos.",
     "preco": 89.90, "preco_promocional": None, "estoque": 50, "estoque_minimo": 8, "peso": 3.5, "dimensoes": "35x35x12 cm"},
    {"categoria": "Irrigação", "nome": "Kit Aspersor Automático", "sku": "IR-002",
     "descricao": "Kit aspersor automático oscilante para irrigação de jardins e gramados de médio porte.",
     "preco": 59.90, "preco_promocional": None, "estoque": 35, "estoque_minimo": 6, "peso": 0.6, "dimensoes": "25x15x10 cm"},
    {"categoria": "Irrigação", "nome": "Timer para Irrigação Automática", "sku": "IR-003",
     "descricao": "Timer digital para irrigação automática, programável, acoplável direto à torneira.",
     "preco": 129.90, "preco_promocional": None, "estoque": 25, "estoque_minimo": 5, "peso": 0.3, "dimensoes": "12x8x6 cm"},
    {"categoria": "Irrigação", "nome": "Regador Plástico 5L", "sku": "IR-004",
     "descricao": "Regador plástico com capacidade de 5 litros e crivo removível para rega uniforme.",
     "preco": 24.90, "preco_promocional": None, "estoque": 6, "estoque_minimo": 5, "peso": 0.4, "dimensoes": "35x18x22 cm"},
    {"categoria": "Irrigação", "nome": "Engate Rápido para Mangueira", "sku": "IR-005",
     "descricao": "Kit de engate rápido para mangueira de jardim, em latão, com vedação em borracha.",
     "preco": 9.90, "preco_promocional": None, "estoque": 200, "estoque_minimo": 25, "peso": 0.1, "dimensoes": "6x6x4 cm"},
]


def get_or_create_section(db, nome, descricao):
    section = db.query(SectionModel).filter(SectionModel.nome == nome, SectionModel.deleted_at == None).first()
    if section:
        return section, False
    section = SectionModel(nome=nome, descricao=descricao)
    db.add(section)
    db.flush()
    return section, True


def get_or_create_category(db, section_id, nome, descricao):
    category = db.query(CategoryModel).filter(CategoryModel.nome == nome, CategoryModel.deleted_at == None).first()
    if category:
        return category, False
    category = CategoryModel(section_id=section_id, nome=nome, descricao=descricao)
    db.add(category)
    db.flush()
    return category, True


def get_or_create_product(db, category_id, item):
    product = db.query(ProductModel).filter(ProductModel.sku == item["sku"], ProductModel.deleted_at == None).first()
    if product:
        return product, False
    product = ProductModel(
        category_id=category_id,
        nome=item["nome"],
        descricao=item["descricao"],
        preco=item["preco"],
        preco_promocional=item["preco_promocional"],
        sku=item["sku"],
        quantidade_estoque=item["estoque"],
        estoque_minimo=item["estoque_minimo"],
        peso=item["peso"],
        dimensoes=item["dimensoes"],
    )
    db.add(product)
    db.flush()
    return product, True


# Fotos reais (licença livre, Wikimedia Commons) escolhidas e conferidas visualmente uma a uma
# para cada produto — ver docs/CHANGELOG_BACKEND.md ou o histórico do script para o processo de
# curadoria (a busca automática por palavra-chave errava bastante: trazia fotos de museu, de
# eventos históricos e até um controle de Xbox para "timer de irrigação").
IMAGE_URLS = {
    "FE-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Cordless%20electric%20(screw)%20drill.jpg?width=800",
    "FE-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Panasonic%20Cordless%20Drill%20%26%20Driver%20EY1DD2%2C%20Ottobrunn%20(20250410-P1046293).jpg?width=800",
    "FE-003": "https://commons.wikimedia.org/wiki/Special:FilePath/DeWalt%20circular%20saw%20in%20use.jpg?width=800",
    "FE-004": "https://commons.wikimedia.org/wiki/Special:FilePath/2%20%D8%A7%D9%84%D8%AD%D8%AF%D8%A7%D8%AF.jpg?width=800",
    "FE-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Lijadora%20orbital%20L%C3%BCsqtoff.jpg?width=800",
    "FM-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Stanley%20graphite%20claw%20hammer.jpg?width=800",
    "FM-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Screwdriver%20set%20with%20great%20variety%20of%20bits%20and%20ratchet%20screwdriver.jpg?width=800",
    "FM-003": "https://commons.wikimedia.org/wiki/Special:FilePath/2023%20Kombinerki%20(1).jpg?width=800",
    "FM-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Woodworking%20hand%20tools%20on%20timber%20planks%2002.jpg?width=800",
    "FM-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Gedore%20No.%207%20combination%20wrenches%206%E2%80%9319%20mm.jpg?width=800",
    "MN-001": "https://commons.wikimedia.org/wiki/Special:FilePath/2024-09-14%20PA%20Laser%20Rangefinder%20003.jpg?width=800",
    "MN-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Waterpass.jpg?width=800",
    "MN-003": "https://commons.wikimedia.org/wiki/Special:FilePath/B%26Q%20Tape%20Measure.jpg?width=800",
    "MN-004": "https://commons.wikimedia.org/wiki/Special:FilePath/1980%20stainless%20steel%20try%20square%20by%20Swedish%20tool%20manufacturer%20Kamasa%20Tools.jpg?width=800",
    "MN-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Plumb%20bob.jpg?width=800",
    "CA-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Portland%20cement%20CEM%20I%2042%2C5%20R%20(bag).jpg?width=800",
    "CA-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Durastop%20firestop%20mortar%20bag.jpg?width=800",
    "CA-003": "https://commons.wikimedia.org/wiki/Special:FilePath/-2019-11-06%20Jewson%20grab-bag%20of%20building%20sand%2C%20Trimingham.JPG?width=800",
    "CA-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Moderately%20hydraulic%20lime%20(NHL%203.5).jpg?width=800",
    "CA-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Applying%20grout.jpg?width=800",
    "PR-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Polished%20Porcelain%20Floor%20Tiling.jpg?width=800",
    "PR-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Ceramic%20tile%20rectangle%20white%20fabric%20pattern.jpg?width=800",
    "PR-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Laminate%20flooring%20assembly.JPG?width=800",
    "PR-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Beaded%20baseboard%20molding%20(5080100256).jpg?width=800",
    "PR-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Hakatai%20mosaic%20glass%20tile%20mural.jpg?width=800",
    "MC-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Plywood.jpg?width=800",
    "MC-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Stack%20of%20wooden%20planks%20-%20close-up%2001.jpg?width=800",
    "MC-003": "https://commons.wikimedia.org/wiki/Special:FilePath/MDF%20Aluminiumbeschichtet%202009.jpg?width=800",
    "MC-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Stack%20of%20wooden%20planks%20-%20close-up%2001.jpg?width=800",
    "MC-005": "https://commons.wikimedia.org/wiki/Special:FilePath/005%20Logging%20industry%20in%20New%20Zealand%20-%20tree%20trunk%20piles%2C%20timber%20logs%20stockpile.jpg?width=800",
    "FC-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Cable%20wires.jpg?width=800",
    "FC-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Cable%20wires.jpg?width=800",
    "FC-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Cable%20wires.jpg?width=800",
    "FC-004": "https://commons.wikimedia.org/wiki/Special:FilePath/NEMA-1%20extension%20cord.jpg?width=800",
    "FC-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Ca%201970%20roll%20of%20polyethylene%20electrical%20insulating%20tape%20by%20Norgesplaster%20AS%20Mosby%20Norway.jpg?width=800",
    "IL-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Low-key%20photograph%20of%20light%20bulb%2C%20Straume%2C%20Norway%20julesvernex2.jpg?width=800",
    "IL-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Industrial%20Holophane%20pendant%20light.jpg?width=800",
    "IL-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Moscow%2C%20Novospassky%20Bridge%20-%20LED%20floodlights%20-%20heatsinks%2002.jpg?width=800",
    "IL-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Industrial%20Holophane%20pendant%20light.jpg?width=800",
    "IL-005": "https://commons.wikimedia.org/wiki/Special:FilePath/LED%20Light%20Strip%20Huaqiangbei%20July%202024.jpg?width=800",
    "DQ-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Circuit%20breaker%202%20pole%20on%20DIN%20rail.JPG?width=800",
    "DQ-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Eaton%20circuit%20breaker%20panel%20open.JPG?width=800",
    "DQ-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Electrical%20panel%20opened.jpg?width=800",
    "DQ-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Residual%20current%20device%202pole.jpg?width=800",
    "DQ-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Busbar%20for%20zero%20wires%20distribution.JPG?width=800",
    "TC-001": "https://commons.wikimedia.org/wiki/Special:FilePath/1%20inch%20PVC%20Valve%20and%20pipe-IMG%201061.jpg?width=800",
    "TC-002": "https://commons.wikimedia.org/wiki/Special:FilePath/U.S.%20Army%20Spc.%20Emanuel%20Walton%2C%20a%20plumber%2C%20with%20the%20758th%20Engineer%20Company%2C%20primes%20a%20PVC%20(Polyvinyl%20chloride)%20pipe%20for%20a%20new%20sewer%20line%20during%20the%20Innovative%20Readiness%20Training%20with%20Rebuilding%20Miami%20Together%20130613-A-XA929-013.jpg?width=800",
    "TC-003": "https://commons.wikimedia.org/wiki/Special:FilePath/PVC%20plumbing%20fittings%20in%20Awka.jpg?width=800",
    "TC-004": "https://commons.wikimedia.org/wiki/Special:FilePath/MunicipalGateValve.JPG?width=800",
    "TC-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Pipe%20elbow.png?width=800",
    "LM-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Avocado%20toilet%20bowl%20June%2022.jpg?width=800",
    "LM-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Sink%20and%20taps%20in%20the%20men%27s%20locker%20room%203%20BW.jpg?width=800",
    "LM-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Kitchen%20water%20tap%2020190408.jpg?width=800",
    "LM-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Showerhead.JPG?width=800",
    "LM-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Kitchen%20water%20tap%2020190408.jpg?width=800",
    "TN-001": "https://commons.wikimedia.org/wiki/Special:FilePath/White%20primer%20bucket.jpg?width=800",
    "TN-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Grey%20acrylic%20paint.jpg?width=800",
    "TN-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Used%20paint%20cans%20after%20renovation%20of%20a%20small%20company%20building%20in%20Shibuya-ku.jpg?width=800",
    "TN-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Grey%20acrylic%20paint.jpg?width=800",
    "TN-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Kitchen%20renovation%20spackling%20to%20cover%20holes%20and%20tape%20between%20sheetrock%20boards.JPG?width=800",
    "PA-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Paint-roller%20(23956075297).jpg?width=800",
    "PA-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Paint%20brushes%20(30804).jpg?width=800",
    "PA-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Paint%20Tray%20(1535689884).jpg?width=800",
    "PA-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Masking%20tape%20on%20canvas.jpg?width=800",
    "PA-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Schleifpapier%20verschiedene%20Sorten.jpg?width=800",
    "FJ-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Electric%20lawn%20mower%20IMG%205496.JPG?width=800",
    "FJ-002": "https://commons.wikimedia.org/wiki/Special:FilePath/T%20-%20spade%20and%20garden%20fork.jpg?width=800",
    "FJ-003": "https://commons.wikimedia.org/wiki/Special:FilePath/My%20trusty%20gardening%20gloves%20%26%20secateurs%20which%20need%20a%20good%20clean%20by%20the%20look%20of%20them%20(8711272274).jpg?width=800",
    "FJ-004": "https://commons.wikimedia.org/wiki/Special:FilePath/Small%20pink%20leaf%20rake.jpg?width=800",
    "FJ-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Wheelbarrow%20Outdoors.JPG?width=800",
    "IR-001": "https://commons.wikimedia.org/wiki/Special:FilePath/Melnor%20Garden%20Hose%20Water%20Nozzle%205%20LR.jpg?width=800",
    "IR-002": "https://commons.wikimedia.org/wiki/Special:FilePath/Impact%20Sprinkler%20Mechanism%202.jpg?width=800",
    "IR-003": "https://commons.wikimedia.org/wiki/Special:FilePath/Impact%20Sprinkler%20Mechanism%202.jpg?width=800",
    "IR-004": "https://commons.wikimedia.org/wiki/Special:FilePath/-2022-05-30%20Red%20plastic%20watering%20can%2C%20Trimingham%2C%20Norfolk.JPG?width=800",
    "IR-005": "https://commons.wikimedia.org/wiki/Special:FilePath/Garden%20watering%20hose%20lying%20on%20grassy%20lawn.jpg?width=800",
}


def ensure_images(db, product):
    url = IMAGE_URLS.get(product.sku)
    if not url:
        url = f"https://picsum.photos/seed/{product.sku.lower()}/800/800"

    existing = db.query(ProductImageModel).filter(
        ProductImageModel.product_id == product.id, ProductImageModel.deleted_at == None,
    ).all()
    already_correct = len(existing) == 1 and existing[0].url == url
    if already_correct:
        return 0

    for img in existing:
        db.delete(img)

    db.add(ProductImageModel(product_id=product.id, url=url, principal=True))
    return 1


def main():
    db = SessionLocal()
    stats = {"sections": 0, "categories": 0, "products": 0, "images": 0}

    try:
        section_ids = {}
        for s in SECTIONS:
            section, created = get_or_create_section(db, s["nome"], s["descricao"])
            section_ids[s["nome"]] = section.id
            stats["sections"] += created

        category_ids = {}
        for c in CATEGORIES:
            category, created = get_or_create_category(db, section_ids[c["section"]], c["nome"], c["descricao"])
            category_ids[c["nome"]] = category.id
            stats["categories"] += created

        for p in PRODUCTS:
            product, created = get_or_create_product(db, category_ids[p["categoria"]], p)
            stats["products"] += created
            stats["images"] += ensure_images(db, product)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    print("Seed do catálogo concluída.")
    print(f"  Seções novas:    {stats['sections']} (de {len(SECTIONS)} no total)")
    print(f"  Categorias novas:{stats['categories']} (de {len(CATEGORIES)} no total)")
    print(f"  Produtos novos:  {stats['products']} (de {len(PRODUCTS)} no total)")
    print(f"  Imagens criadas: {stats['images']}")
    print()
    print("Produtos com estoque próximo do mínimo (para testar o alerta de estoque baixo")
    print("ao finalizar um pedido): FM-003, DQ-002, LM-004, IR-004.")


if __name__ == "__main__":
    main()
