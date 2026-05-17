# Trabalho Prático de Processamento de Linguagens 25/26 UMinho 
## Autor - a107316 Rui Mário da Silva Costa

## Dificuldades encontradas
- Análise léxica do formato fixo do Fortran 77
Tendo escolhido o formato fixo do Fortran 77 a sua análise léxica foi implementada criando um estado exclusivo dentro do *lexer* (denominado *startLine*) que é ativado sempre que é encontrada uma mudança de linha "\n", e o qual é desativado quando atingimos o 7º caracter em cada linha. Este estado permite identificar inteiros no início da linha com o tipo "LABEL", bem como o caracter de continuação da linha anterior na coluna 6.

- Optei por não implementar a tipagem implícita do Fortran 77 não apenas por uma questão de simplicidade, mas também por ser estúpida

## Índice
1. Introdução 
2. Análise Léxica
3. Análise Sintática
4. Análise Semântica
5. Tradução de Código


# Análise Léxica

Optei por implementar o formato de colunas fixas do Fortran 77. Para este efeito,
o lexer possui dois estados principais: StartLine e Initial.
O lexer é inicializado no estado StartLine e quando encontra um \n, 
despoleta o Startline.
No estado StartLine, existem dois caminhos de execução implementados
através de comparações com regexs: 
 - // inserir regex do comentário - identifica se a linha é um comentário
(o facto de Fortran 77 não apresentar comentários multi-linha facilita esta implementação 
- // inserir regex do startLine - este regex
consome os primeiros 6 caracteres da linha e permite
identificar uma opcional Label do Fortran
