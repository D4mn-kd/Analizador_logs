# Analizador de Logs

Este script en Python permite analizar y filtrar logs de un archivo de registros de servidor. Puedes filtrar los logs por dirección IP, código de estado HTTP, método HTTP y fecha.

## Requisitos

- Python 3.10 o superior 

## Uso

1. Clona este repositorio o descarga los archivos `analizador_logs.py` y `server_logs.log`.
2. Abre una terminal y navega hasta el directorio donde se encuentra el archivo `analizador_logs.py`.
3. Ejecuta el script con el siguiente comando:

```sh
python analizador_logs.py -logfile <ruta_del_archivo_de_logs> -filter <filtro>
```
Si necesitas ayuda puedes ejecutar
```sh
python analizador_logs.py -h
```
Nota: El archivo `server_logs.log` es un archivo de prueba, puedes cambiarlo para tu archivo de logs
