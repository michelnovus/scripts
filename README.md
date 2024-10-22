# Scripts

## Qué contiene el repositorio?

Es un repositorio donde guardo utilidades que voy creando con el tiempo y 
considere relevante guardar.  
Son posiblemente solo ejecutables en el sistema GNU/Linux (y quizá WSL en 
Windows).

Por ahora el repositorio tiene los siguientes programas:

- `rebaptizer`: Renombra rapidamente un conjunto de archivos siguiendo 
    algún patron.
- `mkbkp`: Crea copias de respaldo en un directorio "aislado" según un
    filtro de reglas. Lo desarrollé con el objetivo de tener una copia rápida
    de mis archivos del directorio HOME en un lugar separado de las acciones
    que causan los programas del entorno usuario.
- `screenshot`: Envoltorio del programa scrot para capturar un área de la
    pantalla mediante algún botón del teclado como atajo.
- `watermark`: Genera y estampa marcas de agua en imágenes.

## Construcción:

Los *archivos* que se encuentran en el directorio `sources/` pueden ejecutarse 
directamente si tiene las dependencias necesarias en el sistema, por ejemplo, 
un bash script necesita tener el programa Bash y probablemente las herramientas 
GNU instaladas en el PATH del sistema, mientras que un python script necesita 
sólo tener el intérprete de Python en el PATH.

Los *directorios* dentro de `sources/` necesitan ser construidos o preparados
de alguna manera entes de poder usarlos.  

> [!IMPORTANT]
> Se considera que el directorio de trabajo siempre es la raíz del repositorio.

### Paquetes Python
Los directorios que contengan un archivo *pyproject.toml* son paquetes de python
ejecutables, puedes generar fácilmente un solo archivo ejecutable con todas sus dependencias (excepto el propio intérprete, que debes tener instalado en el
sistema) mediante el programa `pex` de la sigiente manera:  
`$ pex --project {sources/pkg_name/} -e 'pkg_name' -o pkg_name.pex`  
donde "pkg_name" es el nombre del paquete.  

La documentación sobre `pex` y como instalarlo en https://github.com/pex-tool/pex.

## Licencia:

Si algún programa te es útil, eres libre de usarlo; el repositorio está
licenciado con `MIT License` pero algunas utilidades pueden estarlo con otras
como `GLP3` (en las primeras líneas del programa se indica de ser oportuno).
