# 🔲 Generador de QR desde CSV
## Este codigo fue generado enteramente mediante vibecoding en claude.ai y puede(muy probablemente) contener errores.

Herramienta de línea de comandos para generar códigos QR en lote a partir de un archivo CSV.
Disponible como **script Python** o como **ejecutable `.exe` para Windows** (sin instalar nada).

---

## ✨ Características

- Genera QR en formato **PNG**, **JPG** o **SVG**
- Procesamiento en lote desde un CSV simple (nombre, URL)
- Detección automática de fila de encabezado
- Nombres de archivo saneados (sin caracteres inválidos)
- Alta corrección de errores (nivel H) para mayor robustez
- Salida organizada en carpeta configurable
- En Windows: **arrastrá el CSV directo al `.exe`**

---

## 📋 Formato del CSV

El archivo debe tener **dos columnas**: nombre y URL.
Puede tener o no fila de encabezado; el script la detecta automáticamente.

```csv
nombre,url
Google,https://www.google.com
GitHub,https://github.com
Mi Sitio,https://misitioweb.com.ar
```

> **Nota:** el separador es coma (`,`). Codificación recomendada: UTF-8.

---

## 🚀 Uso

### Opción A — Ejecutable Windows (recomendado para usuarios finales)

> Ver sección [Compilar a .exe](#-compilar-a-exe-para-windows) más abajo.

Una vez que tenés el `generar_qr.exe`:

**Arrastrando el CSV al exe:**
Simplemente arrastrá tu archivo `.csv` sobre el ícono del ejecutable.
Los QR se guardarán en una carpeta `qr_codes/` junto al CSV.

**Desde la terminal (más opciones):**
```
generar_qr.exe miarchivo.csv
generar_qr.exe miarchivo.csv --formato jpg
generar_qr.exe miarchivo.csv --formato svg --salida mis_qr
```

---

### Opción B — Script Python

**Requisitos:** Python 3.8 o superior.

**Instalación de dependencias:**
```bash
pip install "qrcode[pil]" Pillow lxml
```

> Las dependencias también se instalan automáticamente al ejecutar el script por primera vez.

**Uso básico:**
```bash
python generar_qr.py clientes.csv
```

**Todas las opciones:**
```bash
python generar_qr.py <archivo.csv> [--formato png|jpg|svg] [--salida carpeta]
```

| Argumento | Descripción | Default |
|-----------|-------------|---------|
| `archivo.csv` | Ruta al CSV de entrada | *(requerido)* |
| `--formato` / `-f` | Formato de imagen: `png`, `jpg`, `svg` | `png` |
| `--salida` / `-o` | Carpeta donde se guardan los QR | `qr_codes/` |

**Ejemplos:**
```bash
# PNG en carpeta por defecto
python generar_qr.py links.csv

# JPG en carpeta personalizada
python generar_qr.py links.csv --formato jpg --salida imagenes/qr

# SVG
python generar_qr.py links.csv -f svg -o vectores
```

---

## 📂 Estructura de salida

```
qr_codes/
├── Google.png
├── GitHub.png
└── Mi_Sitio.png
```

Cada archivo se nombra según la primera columna del CSV, con espacios reemplazados por `_` y caracteres inválidos eliminados.

---

## 🏗️ Compilar a `.exe` para Windows

Esta sección es para quien quiere **distribuir el ejecutable** a sus compañeros.
Solo hay que hacerlo una vez; el `.exe` resultante funciona en cualquier PC con Windows sin instalar Python.

### Prerrequisitos (solo para quien compila)

1. Python 3.8+ instalado
2. Instalar PyInstaller y las dependencias del proyecto:

```bash
pip install pyinstaller "qrcode[pil]" Pillow lxml
```

### Compilar

Desde la carpeta del proyecto, ejecutar el script incluido:

```bash
build_windows.bat
```

O manualmente:

```bash
pyinstaller --onefile --console --name generar_qr generar_qr.py
```

El ejecutable queda en:
```
dist/
└── generar_qr.exe   ← este es el archivo a distribuir
```

### ¿Qué hace el `.bat` de build?

```
build_windows.bat
├── Instala dependencias automáticamente
├── Limpia compilaciones anteriores
├── Ejecuta PyInstaller con los flags correctos
└── Copia el .exe a la raíz del proyecto para fácil acceso
```

### Drag & drop en Windows

Cuando un usuario **arrastra un CSV sobre el `.exe`**, Windows pasa la ruta del archivo como primer argumento — exactamente lo que el script espera.
Los QR se generan en `qr_codes/` dentro de la misma carpeta donde está el CSV.

> Una ventana de consola se abre, muestra el progreso y **espera que presiones Enter** antes de cerrarse, para que puedas ver si hubo errores.

---

## 🖥️ Ejemplo de salida en consola

```
=======================================================
        🔲  Generador de QR desde CSV
=======================================================

⚙️  Instalando/verificando dependencias...

📄 CSV cargado: 3 fila(s) encontrada(s)
📁 Carpeta de salida: 'qr_codes/'
🖼  Formato: PNG

  [1/3] ✅  Google  →  Google.png
  [2/3] ✅  GitHub  →  GitHub.png
  [3/3] ✅  Mi Sitio  →  Mi_Sitio.png

✨ Listo! 3 QR(s) generado(s), 0 error(es).
📂 Archivos guardados en: 'C:\Users\...\qr_codes\'
```

---

## ⚠️ Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `El archivo CSV no se encontró` | Ruta incorrecta o el CSV tiene espacios en el nombre | Encerrá la ruta entre comillas: `"mi archivo.csv"` |
| QR generado pero no escaneable | URL malformada en el CSV | Verificá que las URLs empiecen con `https://` |
| El `.exe` no abre | Antivirus bloqueando | Agregá el `.exe` como excepción en el antivirus |
| Error de codificación | CSV no está en UTF-8 | Guardá el CSV como UTF-8 desde Excel: *Guardar como → CSV UTF-8* |
| `Fila incompleta, se omite` | La fila tiene menos de 2 columnas | Revisá que no haya filas vacías o con una sola columna en el CSV |

---

## 🛠️ Desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/generador-qr-csv.git
cd generador-qr-csv

# Instalar dependencias
pip install "qrcode[pil]" Pillow lxml

# Ejecutar
python generar_qr.py ejemplo.csv
```

### Estructura del proyecto

```
generador-qr-csv/
├── generar_qr.py        # Script principal
├── generar_qr_win.py    # Versión para compilar a .exe (con pausa al final)
├── build_windows.bat    # Script de compilación para Windows
├── ejemplo.csv          # CSV de ejemplo
└── README.md
```

---

## 📄 Licencia

MIT — libre para uso personal y comercial.
