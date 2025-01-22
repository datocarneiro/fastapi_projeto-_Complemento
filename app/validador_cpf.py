from fastapi import HTTPException
from validate_docbr import CPF

def validar_cpf(cpf_value):
    cpf_value_limpo = ''.join(filter(str.isdigit, cpf_value))
    validador = CPF()
    # Formata o CPF para o formato padrão
    cpf_formatado = validador.mask(cpf_value_limpo)
    # Verifica se o CPF tem exatamente 11 dígitos
    if len(cpf_value_limpo) != 11:
        # Levanta a exceção com o status 400 e a mensagem de erro
        raise HTTPException(status_code=400, detail=f"O CPF informado '{cpf_value}' é inválido! O CPF deve ter 11 dígitos numéricos.")
    
    # Verifica se o CPF é válido
    if not validador.validate(cpf_value_limpo):
        # Formata o CPF
        raise HTTPException(status_code=400, detail=f"O CPF '{cpf_formatado}' é inválido!")
    
    # Retorna o CPF formatado no padrão XXX.XXX.XXX-XX
    return validador.mask(cpf_value_limpo)
