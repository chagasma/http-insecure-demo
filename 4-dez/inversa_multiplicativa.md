# Inversa Multiplicativa

## Definição

A **inversa multiplicativa** de um número $a$ é um número $b$ tal que:

$$a \times b = 1$$

Esse número $b$ é chamado de **inverso multiplicativo** de $a$, e é denotado por $a^{-1}$ ou $\frac{1}{a}$.

## Exemplo Simples

Para $a = 5$:

$$5 \times \frac{1}{5} = 1$$

Logo, $\frac{1}{5}$ é a inversa multiplicativa de $5$.

## Inversa Multiplicativa Modular

Em aritmética modular, a inversa multiplicativa de $a$ módulo $n$ é um número $x$ tal que:

$$a \times x \equiv 1 \pmod{n}$$

**Importante:** A inversa só existe se $a$ e $n$ são **coprimos** (ou seja, $\gcd(a, n) = 1$).

### Exemplo Modular

Encontrar a inversa de $3$ módulo $7$:

$$3 \times x \equiv 1 \pmod{7}$$

Testando valores:

- $3 \times 1 = 3 \equiv 3 \pmod{7}$
- $3 \times 2 = 6 \equiv 6 \pmod{7}$
- $3 \times 3 = 9 \equiv 2 \pmod{7}$
- $3 \times 4 = 12 \equiv 5 \pmod{7}$
- $3 \times 5 = 15 \equiv 1 \pmod{7}$

Logo, $3^{-1} \equiv 5 \pmod{7}$.

## Aplicação em Criptografia

A inversa multiplicativa modular é fundamental em algoritmos como **RSA**, onde é usada para calcular a chave privada $d$ a partir da chave pública $e$:

$$e \times d \equiv 1 \pmod{\phi(n)}$$

Onde $\phi(n)$ é a função totiente de Euler.

## Números sem inverso multiplicativo

No sistema numérico padrão, o número zero ($0$) é o único que não possui inversa multiplicativa.
Motivo: Por definição, a inversa $b$ de $0$ teria que satisfazer:$$0 \times b = 1$$

No entanto, qualquer número multiplicado por zero resulta em zero ($0 \times b = 0$). Como $0 \neq 1$, a equação é impossível. Portanto, a divisão por zero é indefinida.2. Na Aritmética ModularEm um sistema módulo $n$, um número $a$ não possui inversa se $a$ e $n$ compartilharem algum divisor comum maior que 1. Ou seja, se:
$$\gcd(a, n) > 1$$

Neste caso, $a$ é chamado de divisor de zero (ou simplesmente não invertível) naquele anel modular. Exemplo de InexistênciaVamos tentar encontrar a inversa de $2$ módulo $6$. Procuramos um $x$ tal que:
$$2 \times x \equiv 1 \pmod{6}$$

Vamos testar os valores possíveis em:
- $2 \times 1 = 2 \equiv 2 \pmod{6}$
- $2 \times 2 = 4 \equiv 4 \pmod{6}$
- $2 \times 3 = 6 \equiv 0 \pmod{6}$
- $2 \times 4 = 8 \equiv 2 \pmod{6}$
- $2 \times 5 = 10 \equiv 4 \pmod{6}$

Observação: Os resultados alternam entre $0, 2, 4$. O valor $1$ nunca é alcançado.
Isso acontece porque $\gcd(2, 6) = 2$, e $2 \neq 1$. Portanto, $2$ não tem inversa módulo $6$.

### Consequência para a Criptografia 
Nnexistência de inversas para números não coprimos é a razão pela qual a escolha de números primos é crucial em algoritmos como o RSA.
- Se escolhermos um valor público $e$ que não seja coprimo com $\phi(n)$, a chave privada $d$ (que é a inversa de $e$) não poderá ser calculada.
- Sem $d$, é impossível descriptografar a mensagem matematicamente.