import re 

def format_cpf(cpf: str) -> str:
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) >= 3:
        cpf = cpf[:3] + "." + cpf[3:]
    if len(cpf) >= 7:
        cpf = cpf[:7] + "." + cpf[7:]
    if len(cpf) >= 11:
        cpf = cpf[:11] + "-" + cpf[11:]
    return cpf[:14]

def format_celular(numero: str) -> str:
    digits = re.sub(r"\D", "", numero)

    digits = digits[:11]

    if len(digits) >= 2:
        formatted = f"({digits[:2]}) "
    else:
        return digits

    if len(digits) >= 7:
        if len(digits) == 11:
            formatted += digits[2:7] + "-" + digits[7:]
        else:
            formatted += digits[2:6] + "-" + digits[6:]
    else:
        formatted += digits[2:]

    return formatted