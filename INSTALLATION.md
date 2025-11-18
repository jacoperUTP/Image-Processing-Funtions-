# 📦 Guía de Instalación - IP Functions

Guía completa para instalar IP Functions en diferentes escenarios y sistemas operativos.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación Rápida](#instalación-rápida)
3. [Instalación Detallada](#instalación-detallada)
4. [Instalación en Entornos Específicos](#instalación-en-entornos-específicos)
5. [Verificación de Instalación](#verificación-de-instalación)
6. [Solución de Problemas](#solución-de-problemas)

---

## ✅ Requisitos Previos

### Python

- **Versión mínima:** Python 3.6
- **Versiones recomendadas:** Python 3.8, 3.9, 3.10, 3.11, 3.12

### Verificar versión de Python

```bash
python --version
# o
python3 --version
```

### Dependencias

- **NumPy** >= 1.19.0
- **Matplotlib** >= 3.3.0

Estas se instalan automáticamente con IP Functions.

---

## 🚀 Instalación Rápida

### Método 1: Desde GitHub (Recomendado)

```bash
pip install git+https://github.com/jacoperUTP/CV.git
```

### Método 2: Clonar y instalar

```bash
git clone https://github.com/jacoperUTP/CV.git
cd CV
pip install -e .
```

---

## 📚 Instalación Detallada

### Opción A: Instalación para Usuarios

**Paso 1:** Instalar directamente desde GitHub

```bash
pip install git+https://github.com/jacoperUTP/CV.git
```

**Paso 2:** Verificar instalación

```python
import ip_functions
print("✅ IP Functions instalado correctamente")
print(f"Ubicación: {ip_functions.__file__}")
```

---

### Opción B: Instalación para Desarrollo (Editable)

**Paso 1:** Clonar el repositorio

```bash
git clone https://github.com/jacoperUTP/CV.git
cd CV
```

**Paso 2:** Instalar en modo editable

```bash
pip install -e .
```

> **Nota:** El flag `-e` (editable) permite que los cambios en el código fuente se reflejen inmediatamente sin necesidad de reinstalar.

**Paso 3:** (Opcional) Instalar dependencias de desarrollo

```bash
pip install -e ".[dev]"
```

---

### Opción C: Instalación desde Zip

Si no tienes Git instalado:

**Paso 1:** Descargar el repositorio

1. Ir a https://github.com/jacoperUTP/CV
2. Click en "Code" → "Download ZIP"
3. Extraer el archivo ZIP

**Paso 2:** Instalar

```bash
cd ruta/a/CV-main
pip install .
```

---

## 🖥️ Instalación en Entornos Específicos

### Windows

#### Desde CMD o PowerShell

```cmd
# Verificar Python
python --version

# Instalar IP Functions
pip install git+https://github.com/jacoperUTP/CV.git

# O desde directorio local
cd C:\ruta\a\CV
pip install -e .
```

#### Desde Anaconda Prompt

```bash
# Activar entorno (si usas uno)
conda activate mi_entorno

# Instalar
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Linux / macOS

#### Desde Terminal

```bash
# Verificar Python
python3 --version

# Instalar IP Functions
pip3 install git+https://github.com/jacoperUTP/CV.git

# O desde directorio local
cd ~/ruta/a/CV
pip3 install -e .
```

#### Si necesitas permisos de administrador

```bash
sudo pip3 install git+https://github.com/jacoperUTP/CV.git
```

> **Recomendación:** Es mejor usar entornos virtuales que instalar con sudo.

---

### Jupyter Notebook / JupyterLab

#### Método 1: Desde una celda de Jupyter

```python
# Instalar directamente
!pip install git+https://github.com/jacoperUTP/CV.git

# Verificar
import ip_functions
print("✅ Instalado correctamente")
```

#### Método 2: Desde terminal antes de abrir Jupyter

```bash
# Instalar
pip install git+https://github.com/jacoperUTP/CV.git

# Luego abrir Jupyter
jupyter notebook
# o
jupyter lab
```

---

### Google Colab

```python
# En la primera celda del notebook
!pip install git+https://github.com/jacoperUTP/CV.git

# Importar y usar
from ip_functions import *
print("✅ IP Functions instalado en Colab")
```

---

### Anaconda / Conda

```bash
# Activar entorno
conda activate mi_entorno

# Instalar usando pip (dentro del entorno conda)
pip install git+https://github.com/jacoperUTP/CV.git
```

> **Nota:** No hay paquete conda para IP Functions, pero pip funciona dentro de entornos conda.

---

### PyCharm

**Paso 1:** Abrir configuración de proyecto
- File → Settings → Project → Python Interpreter

**Paso 2:** Instalar desde repositorio
- Click en "+" (Add)
- Buscar "git+https://github.com/jacoperUTP/CV.git"
- Click "Install Package"

O desde la terminal integrada de PyCharm:

```bash
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### VS Code

**Opción 1:** Desde terminal integrada

```bash
# Ctrl + ` para abrir terminal
pip install git+https://github.com/jacoperUTP/CV.git
```

**Opción 2:** Usando extensión de Python

1. Instalar extensión "Python" de Microsoft
2. Abrir Command Palette (Ctrl+Shift+P)
3. Buscar "Python: Create Environment"
4. En la terminal del entorno: `pip install git+https://github.com/jacoperUTP/CV.git`

---

## 🔧 Instalación con Entornos Virtuales

### venv (Python estándar)

```bash
# Crear entorno virtual
python -m venv mi_entorno

# Activar
# Windows:
mi_entorno\Scripts\activate
# Linux/macOS:
source mi_entorno/bin/activate

# Instalar IP Functions
pip install git+https://github.com/jacoperUTP/CV.git

# Verificar
python -c "from ip_functions import *; print('✅ Instalado')"

# Desactivar cuando termines
deactivate
```

### virtualenv

```bash
# Instalar virtualenv si no lo tienes
pip install virtualenv

# Crear entorno
virtualenv mi_entorno

# Activar
# Windows:
mi_entorno\Scripts\activate
# Linux/macOS:
source mi_entorno/bin/activate

# Instalar IP Functions
pip install git+https://github.com/jacoperUTP/CV.git
```

### pipenv

```bash
# Crear proyecto con pipenv
pipenv --python 3.10

# Activar entorno
pipenv shell

# Instalar
pip install git+https://github.com/jacoperUTP/CV.git

# O agregar al Pipfile
pipenv install git+https://github.com/jacoperUTP/CV.git
```

### conda

```bash
# Crear entorno conda
conda create -n ip_env python=3.10

# Activar
conda activate ip_env

# Instalar
pip install git+https://github.com/jacoperUTP/CV.git
```

---

## ✅ Verificación de Instalación

### Test Básico

```python
# Test 1: Importar
import ip_functions
print("✅ Módulo importado correctamente")

# Test 2: Verificar ubicación
print(f"Ubicación: {ip_functions.__file__}")

# Test 3: Probar funciones básicas
from ip_functions import imread, rgb2gray, bwlabel
print("✅ Funciones principales disponibles")
```

### Test Completo

```python
import numpy as np
from ip_functions import bwlabel, regionprops, label2rgb
import matplotlib.pyplot as plt

# Crear imagen de prueba
test_image = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0]
], dtype=bool)

# Etiquetar componentes
labels, num = bwlabel(test_image, EE=8)
print(f"✅ bwlabel: {num} objetos detectados")

# Calcular propiedades
props = regionprops(labels, properties=['Area', 'Centroid', 'Perimeter'])
print(f"✅ regionprops: {len(props)} regiones analizadas")

# Visualizar
rgb_labels = label2rgb(labels, 'jet', 'k', 'shuffle')
plt.imshow(rgb_labels)
plt.title('Test de Instalación - IP Functions v2.0')
plt.axis('off')
plt.show()

print("\n🎉 ¡IP Functions v2.0 instalado y funcionando correctamente!")
```

### Test de Corrección de bwlabel (v2.0)

```python
import numpy as np
from ip_functions import bwlabel

# Test crítico: objeto en forma de L
# Debe detectar 1 componente (no 2)
test = np.array([
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=4)

if num == 1:
    print("✅ bwlabel v2.0 funcionando correctamente")
    print("   (Objeto conectado detectado como 1 componente)")
else:
    print(f"❌ Problema: detectó {num} componentes (debería ser 1)")
    print("   Puede que tengas v1.0 instalada")
```

---

## 🔧 Solución de Problemas

### Problema 1: "pip: command not found"

**Causa:** pip no está instalado o no está en PATH

**Solución:**

```bash
# Verificar si pip está instalado
python -m pip --version

# Si funciona, usa siempre:
python -m pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 2: "error: Microsoft Visual C++ 14.0 is required" (Windows)

**Causa:** Falta compilador de C++ para compilar NumPy

**Solución 1:** Instalar Build Tools

1. Descargar [Build Tools para Visual Studio](https://visualstudio.microsoft.com/downloads/)
2. Instalar "Desktop development with C++"

**Solución 2:** Usar Anaconda

```bash
conda install numpy matplotlib
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 3: "Permission denied" (Linux/macOS)

**Solución 1:** Usar `--user`

```bash
pip install --user git+https://github.com/jacoperUTP/CV.git
```

**Solución 2:** Usar entorno virtual (recomendado)

```bash
python3 -m venv mi_entorno
source mi_entorno/bin/activate
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 4: "ModuleNotFoundError: No module named 'numpy'"

**Causa:** Dependencias no se instalaron correctamente

**Solución:**

```bash
# Instalar dependencias manualmente
pip install numpy>=1.19.0 matplotlib>=3.3.0

# Luego instalar IP Functions
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 5: "fatal: unable to access... SSL certificate problem"

**Causa:** Problema con certificado SSL de Git

**Solución 1:** Descargar ZIP en lugar de clonar

```bash
# Descargar manualmente desde GitHub
# Luego:
cd CV-main
pip install .
```

**Solución 2:** Configurar Git

```bash
git config --global http.sslVerify false
```

---

### Problema 6: Múltiples versiones de Python

**Identificar cuál Python usa pip:**

```bash
# Ver qué Python usa pip
pip --version

# Si tienes Python 3.x, usa:
pip3 install git+https://github.com/jacoperUTP/CV.git

# O explícitamente:
python3 -m pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 7: Error en Jupyter - "No module named 'ip_functions'"

**Causa:** Jupyter usa un kernel diferente

**Solución:**

```bash
# Instalar en el Python que usa Jupyter
python -m pip install git+https://github.com/jacoperUTP/CV.git

# O desde una celda de Jupyter:
import sys
!{sys.executable} -m pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 8: Instalación lenta

**Solución:** Usar mirror de PyPI más rápido

```bash
pip install --index-url https://pypi.org/simple git+https://github.com/jacoperUTP/CV.git
```

---

## 🔄 Actualización

### Actualizar a la última versión

```bash
pip install --upgrade git+https://github.com/jacoperUTP/CV.git
```

### Forzar reinstalación

```bash
pip install --force-reinstall git+https://github.com/jacoperUTP/CV.git
```

### Actualizar en modo editable

```bash
cd ruta/a/CV
git pull origin main
# No necesitas reinstalar - los cambios se reflejan automáticamente
```

---

## 🗑️ Desinstalación

```bash
pip uninstall ip_functions -y
```

---

## 📞 Soporte

Si encuentras problemas no cubiertos en esta guía:

1. **Issues de GitHub:** https://github.com/jacoperUTP/CV/issues
2. **Email:** jacoper@utp.edu.co
3. **Documentación:** [README.md](README.md)

---

## ✅ Checklist de Instalación

- [ ] Python >= 3.6 instalado
- [ ] pip funcionando correctamente
- [ ] IP Functions instalado sin errores
- [ ] Test básico pasado (import funciona)
- [ ] Test de bwlabel pasado (detecta 1 componente en objeto L)
- [ ] Funciones principales probadas

---

**¡Instalación completada! Ya puedes usar IP Functions para procesamiento de imágenes.** 🎉

---

*Última actualización: Noviembre 2025*
