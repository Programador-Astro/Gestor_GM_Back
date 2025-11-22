from django.db import transaction


def finalizar_producao(producao):

    if producao.status == "FINALIZADO":
        raise Exception("Esta produção já está finalizada.")

    itens = producao.itens.all()
    if not itens.exists():
        raise Exception("A produção não possui itens para finalizar.")

    with transaction.atomic():
        for item in itens:
            esperado = item.quantidade_esperada
            conferido = item.quantidade_conferida

            # Atualiza status do item
            if conferido == esperado:
                item.status = "OK"
            else:
                item.status = "DIVERGENTE"

            # ENTRADA REAL NO ESTOQUE
            produto = item.produto
            produto.estoque_atual += conferido
            produto.save()

            item.save()

        producao.status = "FINALIZADO"
        producao.save()

    return producao
