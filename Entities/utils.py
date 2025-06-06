def verificar_cotaçoes(*, cotacoes_verificar:list, cotacoes_disponiveis:dict) -> bool:
    for cotacoes in cotacoes_verificar:
        try:
            cotacoes_disponiveis[cotacoes]
        except KeyError:
            return False
    return True