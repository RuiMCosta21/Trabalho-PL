# Trabalho Prático de Processamento de Linguagens 25/26 UMinho 
## Autor - a107316 Rui Mário da Silva Costa

## Dificuldades encontradas
- Análise léxica do formato fixo do Fortran 77
Tendo escolhido o formato fixo do Fortran 77 a sua análise léxica foi implementada criando um estado exclusivo dentro do *lexer* (denominado *startLine*) que é ativado sempre que é encontrada uma mudança de linha "\n", e o qual é desativado quando atingimos o 7º caracter em cada linha. Este estado permite identificar inteiros no início da linha com o tipo "LABEL", bem como o caracter de continuação da linha anterior na coluna 6.

- Optei por não implementar a tipagem implícita do Fortran 77 não apenas por uma questão de simplicidade, mas também por ser estúpida