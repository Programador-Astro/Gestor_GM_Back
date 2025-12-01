from django.db import transaction


def finalizar_producao(producao):

    if producao.status == "FINALIZADO":
        raise Exception("Esta produção já está finalizada.")

    itens = producao.itens.all()
    if not itens.exists():
        raise Exception("A produção não possui itens para finalizar.")

    # ✔️ Verifica divergência antes de abrir a transação
    divergentes = []
    for item in itens:
        esperado = item.quantidade_esperada
        conferido = item.quantidade_conferida_producao

        if esperado != conferido:
            divergentes.append({
                "produto": item.produto.nome,
                "esperado": float(esperado),
                "conferido": float(conferido)
            })

    if divergentes:
        raise Exception({
            "erro": "Existem itens divergentes. A produção não pode ser finalizada.",
            "itens": divergentes
        })

    # ✔️ Só atualiza estoque se TUDO estiver correto
    with transaction.atomic():
        for item in itens:
            esperado = item.quantidade_esperada
            conferido = item.quantidade_conferida_producao

            # Todos iguais → status OK
            item.status = "OK"

            # Entrada real no estoque
            produto = item.produto
            produto.estoque_atual += conferido
            produto.save()

            item.save()

        producao.status = "FINALIZADO"
        producao.save()

    return producao
