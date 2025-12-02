from django.db import transaction

def finalizar_producao(producao):

    if producao.status == "FINALIZADO":
        raise Exception("Esta produção já está finalizada.")

    itens = producao.itens.all()
    if not itens.exists():
        raise Exception("A produção não possui itens para finalizar.")

    # --------------------------------------------
    # ✔️ VALIDAÇÃO COMPLETA ANTES DE FINALIZAR
    # --------------------------------------------
    divergentes = []

    for item in itens:
        esperado = item.quantidade_esperada
        prod = item.quantidade_conferida_producao or 0
        cam = item.quantidade_conferida_camara or 0

        if esperado != prod or esperado != cam:
            divergentes.append({
                "produto": item.produto.nome,
                "esperado": float(esperado),
                "producao": float(prod),
                "camara": float(cam)
            })

    # Se houver um único item divergente → NÃO finaliza
    if divergentes:
        raise Exception({
            "erro": "Existem itens divergentes. A produção não pode ser finalizada.",
            "itens": divergentes
        })

    # --------------------------------------------
    # ✔️ TUDO VALIDO → FINALIZA OFICIALMENTE
    # --------------------------------------------
    with transaction.atomic():
        for item in itens:
            conferido = item.quantidade_conferida_producao

            # Marca status como OK (já passou nas validações)
            item.status = "OK"
            item.save()

            # Atualiza estoque
            produto = item.produto
            produto.estoque_atual += conferido
            produto.save()

        producao.status = "FINALIZADO"
        producao.save()

    return producao
