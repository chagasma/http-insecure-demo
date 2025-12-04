# RSA - Criptografia Assimétrica

## Descrição

Implementação educacional do algoritmo RSA em Python puro, sem dependências externas.

## Como executar

```bash
python 4-dez/rsa.py
```

## O que o script faz

1. Gera um par de chaves RSA usando dois números primos grandes (p e q)
2. Calcula as chaves pública (n, e) e privada (n, d)
3. Executa três testes de criptografia/descriptografia:
   - Mensagem curta em português
   - Mensagem ASCII
   - Múltiplas mensagens variadas

## Funções principais

- `gerar_chaves_rsa(p, q, e)`: Gera par de chaves RSA
- `criptografar_rsa(mensagem, n, e)`: Criptografa texto usando chave pública
- `descriptografar_rsa(c, n, d)`: Descriptografa usando chave privada
- `text_to_number(text)`: Converte texto para número
- `number_to_text(num)`: Converte número para texto

## Limitações

- Mensagens devem ser menores que o módulo n
- Não implementa padding (inseguro para produção)
- Apenas para fins educacionais
