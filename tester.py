import re
from pygments import highlight
from pygments.lexers import CLexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter

def resaltar_codigo(texto, lenguaje='c'):
    codigo_regex = re.compile(r'```(.*?)```', re.DOTALL)
    codigos = codigo_regex.findall(texto)

    for codigo in codigos:
        codigo_resaltado = highlight(codigo, get_lexer_by_name(lenguaje), TerminalFormatter())
        texto = texto.replace(f'```{codigo}```', codigo_resaltado.strip())

    print(texto)

texto = '''
La función "printf()" :

```
#include <stdio.h>

int main() {
   printf("Hola, mundo!");
   return 0;
}
```

La salida de este programa sería:

```
Hola, mundo!
```

En resumen, la función "printf()" se utiliza para imprimir texto en la pantalla en el lenguaje de programación C.

'''

resaltar_codigo(texto, 'c')