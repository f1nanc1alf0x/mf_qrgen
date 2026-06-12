#!/usr/bin/env python3
"""
Generador de QR codes desde CSV
Uso: python generar_qr.py archivo.csv --formato png|svg|jpg

Versión compilable a .exe para Windows.
Incluye pausa al final para que la ventana no se cierre sola
cuando se usa arrastrando el CSV sobre el ejecutable.
"""

import csv
import argparse
import sys
import os
import re

def instalar_dependencias():
    pass

def sanitizar_nombre(nombre):
    """Limpia el nombre para usarlo como nombre de archivo."""
    nombre = nombre.strip()
    nombre = re.sub(r'[\\/*?:"<>|]', "_", nombre)
    nombre = re.sub(r'\s+', "_", nombre)
    return nombre

def generar_qr_png_jpg(nombre, url, carpeta_salida, formato, size=1080):
    import qrcode
    from PIL import Image

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), Image.NEAREST)

    nombre_archivo = sanitizar_nombre(nombre)
    ext = "jpg" if formato == "jpg" else "png"
    ruta = os.path.join(carpeta_salida, f"{nombre_archivo}.{ext}")

    if formato == "jpg":
        img.save(ruta, "JPEG", quality=95)
    else:
        img.save(ruta, "PNG")

    return ruta

def generar_qr_svg(nombre, url, carpeta_salida):
    import qrcode
    import qrcode.image.svg

    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        image_factory=factory,
        box_size=10,
        border=0,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    nombre_archivo = sanitizar_nombre(nombre)
    ruta = os.path.join(carpeta_salida, f"{nombre_archivo}.svg")
    img.save(ruta)
    return ruta

def procesar_csv(ruta_csv, formato, carpeta_salida):
    if not os.path.exists(ruta_csv):
        print(f"❌ Error: No se encontró el archivo '{ruta_csv}'")
        sys.exit(1)

    os.makedirs(carpeta_salida, exist_ok=True)

    generados = []
    errores = []

    with open(ruta_csv, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        primera_fila = next(reader, None)
        if primera_fila is None:
            print("❌ El archivo CSV está vacío.")
            sys.exit(1)

        if primera_fila[1].strip().lower().startswith("http") or primera_fila[1].strip().lower().startswith("www"):
            filas = [primera_fila] + list(reader)
        else:
            print(f"   (Se omitió la fila de encabezado: {primera_fila})")
            filas = list(reader)

    total = len(filas)
    print(f"\n📄 CSV cargado: {total} fila(s) encontrada(s)")
    print(f"📁 Carpeta de salida: '{carpeta_salida}/'")
    print(f"🖼  Formato: {formato.upper()}\n")

    for i, fila in enumerate(filas, 1):
        if len(fila) < 2:
            print(f"  [{i}/{total}] ⚠️  Fila incompleta, se omite: {fila}")
            errores.append(fila)
            continue

        nombre = fila[0].strip()
        url    = fila[1].strip()

        if not nombre or not url:
            print(f"  [{i}/{total}] ⚠️  Nombre o URL vacío, se omite.")
            errores.append(fila)
            continue

        try:
            if formato in ("png", "jpg"):
                ruta = generar_qr_png_jpg(nombre, url, carpeta_salida, formato)
            else:
                ruta = generar_qr_svg(nombre, url, carpeta_salida)

            print(f"  [{i}/{total}] ✅  {nombre}  →  {os.path.basename(ruta)}")
            generados.append(ruta)

        except Exception as e:
            print(f"  [{i}/{total}] ❌  Error con '{nombre}': {e}")
            errores.append(fila)

    print(f"\n✨ Listo! {len(generados)} QR(s) generado(s), {len(errores)} error(es).")
    if generados:
        print(f"📂 Archivos guardados en: '{os.path.abspath(carpeta_salida)}/'")

def main():
    print("=" * 55)
    print("        🔲  Generador de QR desde CSV")
    print("=" * 55)

    parser = argparse.ArgumentParser(
        description="Genera QR codes a partir de un CSV con columnas: nombre, url"
    )
    parser.add_argument(
        "csv",
        help="Ruta al archivo CSV (columna 1: nombre, columna 2: URL)"
    )
    parser.add_argument(
        "--formato", "-f",
        choices=["png", "jpg", "svg"],
        default="png",
        help="Formato de salida: png (default), jpg o svg"
    )
    parser.add_argument(
        "--salida", "-o",
        default="qr_codes",
        help="Carpeta de salida (default: 'qr_codes/')"
    )

    args = parser.parse_args()

    # Si el CSV tiene ruta absoluta, guardar los QR en la misma carpeta del CSV
    # (comportamiento más amigable al hacer drag & drop en Windows)
    if os.path.isabs(args.csv) and args.salida == "qr_codes":
        carpeta_csv = os.path.dirname(args.csv)
        carpeta_salida = os.path.join(carpeta_csv, "qr_codes")
    else:
        carpeta_salida = args.salida

    print("\n⚙️  verificando dependencias...")
    instalar_dependencias()

    procesar_csv(args.csv, args.formato, carpeta_salida)

    # ── Pausa final ──────────────────────────────────────────────────────────
    # Evita que la ventana se cierre inmediatamente cuando se ejecuta
    # haciendo doble clic o arrastrando un archivo sobre el .exe en Windows.
    print("\n" + "─" * 55)
    input("  Presioná Enter para cerrar...")

if __name__ == "__main__":
    main()
