# Trabalho Prático de Processamento de Linguagens 25/26 UMinho 
## Autor - a107316 Rui Mário da Silva Costa

## Dificuldades encontradas
- Análise léxica do formato fixo do Fortran 77
Tendo escolhido o formato fixo do Fortran 77 a sua análise léxica foi implementada criando um estado exclusivo dentro do *lexer* (denominado *startLine*) que é ativado sempre que é encontrada uma mudança de linha "\n", e o qual é desativado quando atingimos o 7º caracter em cada linha. Este estado permite identificar inteiros no início da linha com o tipo "LABEL", bem como o caracter de continuação da linha anterior na coluna 6.

- Funções pré-definidas (I/O, funções matemáticas) são idenficadas como tokens 
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
identificar uma opcional Label do Fortran, bem como
um possível caracter de continuação da linha anterior.
Para lidar com este último caso, criei uma função que restaura
o estado anterior ao atual. Deste modo a execução da linha anterior
não é interrompida pela mudança para o estado StartLine despoletada pela mudança de linha.

No estado inicial, foram implementadas flags para resolver certas ambiguidades de tokens:

- Conflito entre um inteiro e uma Label: 
O lexer diferencia entre uma Label e um inteiro para facilitar a análise sintática.
Deste modo:
1. um inteiro no estado startLine é uma Label.
2. Um "DO" levanta a flag ... que identifica o próximo inteiro como uma Label.

- Conflito no literal "/"
O literal "/" serve como operador de divisão, mas também serve de
separador numa declaração de um bloco COMMON. Foi também criada uma diferenciação entre os dois.




NOTA: Segundo a bibliografia consultada, um identificador em Fortran 77 tem um limite
de //inserir n caracteres.
Por isso, ao identificar uma string de caracteres, palavras reservadas com comprimento
menor que // n são resolvidas fazendo match com a lista. Palavras
maiores que // n possuem a sua própria regra.