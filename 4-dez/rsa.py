# Funções auxiliares
def mod_exp(base, expoente, modulo):
    """Expoenciação modular rápida (square-and-multiply)."""
    resultado = 1
    base = base % modulo

    while expoente > 0:
        if expoente % 2 == 1:      # se o expoente é ímpar
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        expoente //= 2

    return resultado

def egcd(a, b):
    """Algoritmo de Euclides estendido: retorna (g, x, y) tal que ax + by = g = mdc(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, m):
    """Calcula a inversa modular de a (mod m)."""
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("Inversa não existe (a e m não são coprimos)")
    return x % m

def text_to_number(text):
    """Converte uma string para inteiro usando base 256 (big-endian)."""
    byte_data = text.encode("utf-8")
    num = 0

    for b in byte_data:
        num = num * 256 + b   # ← ESSA é a linha chave da conversão

    return num

def number_to_text(num):
    """Converte um inteiro de volta para texto UTF-8."""
    if num < 0:
        raise ValueError("Número negativo não pode ser convertido em texto")

    if num == 0:
        return ""

    tamanho = (num.bit_length() + 7) // 8  # arredonda para múltiplos de 8 bits
    byte_data = num.to_bytes(tamanho, "big")
    return byte_data.decode("utf-8")

# Função para gerar chaves RSA
def gerar_chaves_rsa(p, q, e=None):
    """
    
    Args:
        p, q: números primos
        e: expoente público (se None, usa 65537 ou encontra um coprimo)
    
    Returns:
        (n, e, d): módulo público, expoente público, expoente privado
    """
    # Passo 2: Construir o módulo
    n = p * q
    
    # Passo 3: Calcular o(n)
    phi_n = (p - 1) * (q - 1)
    
    # Passo 4: Escolher e (coprimo com o(n))
    if e is None:
        # Tenta usar 65537 (valor comum) se for menor que phi_n
        if 65537 < phi_n and egcd(65537, phi_n)[0] == 1:
            e = 65537
        else:
            # Encontra um e coprimo começando de 3
            e = None
            for i in range(3, phi_n, 2):
                if egcd(i, phi_n)[0] == 1:
                    e = i
                    break
            if e is None:
                raise ValueError("Não foi possível encontrar e coprimo com o(n)")
    
    # Verifica se e é válido
    if e >= phi_n or egcd(e, phi_n)[0] != 1:
        raise ValueError("e deve ser coprimo com o(n) e menor que o(n)")
    
    # Passo 5: Calcular d (inversa de e mod o(n))
    d = mod_inverse(e, phi_n)
    
    return n, e, d

# Função de criptografia RSA
def criptografar_rsa(mensagem, n, e):
    """    
    Criptografia: c ≡ m^e (mod n)
    
    Args:
        mensagem: string a ser criptografada
        n: módulo público (produto de p e q)
        e: expoente público
    
    Returns:
        c: número criptografado
    """
    # Converte mensagem para número
    m = text_to_number(mensagem)
    
    # Verifica se m < n (requisito do RSA)
    if m >= n:
        raise ValueError(f"Mensagem muito grande. m={m} deve ser menor que n={n}")
    
    # Criptografia: c ≡ m^e (mod n)
    c = mod_exp(m, e, n)
    
    return c

if __name__ == "__main__":

    p = 50021
    q = 50023
    
    # Gera chaves
    n, e, d = gerar_chaves_rsa(p, q)
    print(f"Chaves geradas:")
    print(f"  n = {n}")
    print(f"  e = {e}")
    print(f"  d = {d}")
    
    # Mensagem a criptografar
    msg = "olá"
    print(f"\nMensagem original: {msg}")
    
    # Criptografa
    c = criptografar_rsa(msg, n, e)
    print(f"Mensagem criptografada (c): {c}")