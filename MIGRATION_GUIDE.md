# 🔄 Guía de Migración - IP Functions v1.0 → v2.0

Esta guía te ayudará a actualizar tu instalación de IP Functions desde la versión 1.0 a la versión 2.0 con las correcciones críticas de `bwlabel` y mejoras en `regionprops`.

---

## 📋 Tabla de Contenidos

1. [¿Por qué actualizar?](#por-qué-actualizar)
2. [Verificación de versión actual](#verificación-de-versión-actual)
3. [Pasos de actualización](#pasos-de-actualización)
4. [Verificación de instalación](#verificación-de-instalación)
5. [Cambios principales](#cambios-principales)
6. [Actualización de scripts](#actualización-de-scripts)
7. [Solución de problemas](#solución-de-problemas)

---

## ❓ ¿Por qué actualizar?

### 🐛 Bug Crítico Corregido en `bwlabel`

La v1.0 tenía un bug que **fragmentaba incorrectamente objetos conectados** en componentes separados.

**Ejemplo del problema:**

```python
import numpy as np
from ip_functions import bwlabel

# Objeto en forma de L (debería ser 1 componente)
test = np.array([
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=4)

# v1.0: num = 2 ❌ (fragmentado incorrectamente)
# v2.0: num = 1 ✅ (correcto)
```

### ✨ Mejoras en `regionprops`

La v2.0 agrega propiedades geométricas avanzadas:
- **Perimeter** - Perímetro calculado correctamente
- **Eccentricity** - Excentricidad de la región
- **Orientation** - Ángulo de orientación
- **ConvexHull** - Envolvente convexa
- **Solidity** - Solidez (compacidad)
- Y más...

---

## 🔍 Verificación de Versión Actual

### Paso 1: Verificar si tienes IP Functions instalado

```python
import ip_functions
print(ip_functions.__file__)
```

Si ves una ruta, tienes IP Functions instalado.

### Paso 2: Verificar si tienes el bug de bwlabel

```python
import numpy as np
from ip_functions import bwlabel

test = np.array([
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=4)
print(f"Componentes detectados: {num}")

if num == 1:
    print("✅ Ya tienes v2.0 o superior")
elif num == 2:
    print("⚠️ Tienes v1.0 - NECESITAS ACTUALIZAR")
else:
    print("❓ Resultado inesperado - verifica tu instalación")
```

---

## 🚀 Pasos de Actualización

### Opción A: Actualización desde GitHub (Recomendado)

#### 1. Desinstalar versión anterior

```bash
pip uninstall ip_functions -y
```

#### 2. Clonar/actualizar repositorio

**Si ya tienes el repositorio clonado:**

```bash
cd ruta/a/CV
git pull origin main
```

**Si NO tienes el repositorio:**

```bash
git clone https://github.com/jacoperUTP/CV.git
cd CV
```

#### 3. Instalar nueva versión

```bash
pip install -e .
```

> **Nota:** El punto `.` al final es importante - instala el paquete en modo editable desde el directorio actual.

---

### Opción B: Actualización directa desde GitHub

```bash
pip uninstall ip_functions -y
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Opción C: Actualización manual (si usas instalador local)

Si instalaste IP Functions desde un directorio local (ej: `Ip_functions_installer`):

#### 1. Ubicar tu directorio de instalación

Ejemplo de estructura:
```
G:\Mi unidad\image_processing_UTP\flask_server\Ip_functions_installer\
├── ip_functions.py
├── setup.py
└── README.md
```

#### 2. Hacer backup (opcional pero recomendado)

```bash
cd "ruta\a\Ip_functions_installer"
copy setup.py setup.py.old
```

#### 3. Descargar archivos actualizados

Descarga de este repositorio:
- `setup.py` (versión 2.0.0)
- `ip_functions.py` (con bwlabel corregido)

#### 4. Verificar que `ip_functions.py` tiene la corrección

Abre `ip_functions.py` y busca en la función `bwlabel`:

```python
# Debe contener estas líneas dentro de bwlabel:
union(min_label, lbl, parent)
```

Si NO las tiene, reemplaza la función `bwlabel` completa con la versión corregida.

#### 5. Reinstalar el paquete

```bash
cd "ruta\a\Ip_functions_installer"
pip uninstall ip_functions -y
pip install -e .
```

---

## ✅ Verificación de Instalación

### Test 1: Verificar versión instalada

```python
import ip_functions
print(ip_functions.__file__)
```

Debe mostrar la ruta correcta donde instalaste el paquete.

### Test 2: Verificar corrección de bwlabel

```python
import numpy as np
from ip_functions import bwlabel

# Test con objeto en forma de L
test = np.array([
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=4)
print(f"Componentes: {num}")

if num == 1:
    print("✅ v2.0 instalada correctamente!")
else:
    print("⚠️ Problema con la instalación")
```

**Resultado esperado:** `Componentes: 1`

### Test 3: Verificar nuevas propiedades de regionprops

```python
import numpy as np
from ip_functions import bwlabel, regionprops

# Crear imagen de prueba
test = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
], dtype=bool)

labels, num = bwlabel(test, EE=8)

# Probar nuevas propiedades
props = regionprops(labels, properties=[
    'Area', 'Perimeter', 'Eccentricity', 
    'Orientation', 'ConvexArea', 'Solidity'
])

if len(props) > 0:
    p = props[0]
    print(f"✅ Área: {p['Area']}")
    print(f"✅ Perímetro: {p['Perimeter']:.2f}")
    print(f"✅ Excentricidad: {p['Eccentricity']:.3f}")
    print(f"✅ Solidez: {p['Solidity']:.3f}")
    print("\n✅ Todas las nuevas propiedades funcionan correctamente!")
else:
    print("⚠️ No se detectaron regiones")
```

---

## 📝 Cambios Principales

### ✅ `bwlabel` - Algoritmo Corregido

**Antes (v1.0):**
```python
# Implementación con bug - fragmentaba objetos
# Causaba: num = 2 para un solo objeto en forma de L
```

**Ahora (v2.0):**
```python
# Implementación con Union-Find robusto
# Resultado correcto: num = 1 para objetos conectados
```

### ✅ `regionprops` - Propiedades Adicionales

**Propiedades disponibles en v2.0:**

| Propiedad | Descripción | Nuevo en v2.0 |
|-----------|-------------|---------------|
| `Area` | Área en píxeles | No |
| `Centroid` | Centro de masa (y, x) | No |
| `BoundingBox` | Caja delimitadora | No |
| `Perimeter` | Perímetro (chain code) | ✅ Sí |
| `Eccentricity` | Excentricidad [0,1] | ✅ Sí |
| `Orientation` | Orientación en grados | ✅ Sí |
| `MajorAxisLength` | Eje mayor | ✅ Sí |
| `MinorAxisLength` | Eje menor | ✅ Sí |
| `ConvexArea` | Área convexa | ✅ Sí |
| `ConvexHull` | Puntos de envolvente | ✅ Sí |
| `ConvexImage` | Imagen convexa | ✅ Sí |
| `Solidity` | Area/ConvexArea | ✅ Sí |

**Ejemplo de uso:**

```python
props = regionprops(labels, properties=[
    'Area', 'Centroid', 'BoundingBox',
    'Perimeter', 'Eccentricity', 'Orientation',
    'MajorAxisLength', 'MinorAxisLength',
    'ConvexArea', 'ConvexHull', 'Solidity'
])

for p in props:
    print(f"Área: {p['Area']}")
    print(f"Perímetro: {p['Perimeter']:.2f}")
    print(f"Excentricidad: {p['Eccentricity']:.3f}")
    print(f"Orientación: {p['Orientation']:.1f}°")
    print(f"Solidez: {p['Solidity']:.3f}")
```

---

## 🔄 Actualización de Scripts

### ¿Necesito modificar mi código?

**NO** - La v2.0 mantiene **100% compatibilidad** con v1.0.

Todos tus scripts existentes funcionarán sin modificaciones. Sin embargo, ahora puedes:

### 1. Confiar en los resultados de bwlabel

```python
# Tu código existente funcionará MEJOR
labels, num = bwlabel(bw, EE=4)  # Ahora funciona correctamente
```

### 2. Aprovechar nuevas propiedades (opcional)

```python
# Antes (v1.0)
props = regionprops(labels, properties=['Area', 'Centroid'])

# Ahora (v2.0) - puedes agregar más propiedades
props = regionprops(labels, properties=[
    'Area', 'Centroid',
    'Perimeter', 'Eccentricity',  # ← NUEVAS
    'Orientation', 'Solidity'      # ← NUEVAS
])
```

### 3. Análisis más completo

```python
# Ejemplo: Filtrar objetos por forma
props = regionprops(labels, properties=[
    'Area', 'Eccentricity', 'Solidity'
])

# Filtrar objetos circulares (baja excentricidad, alta solidez)
objetos_circulares = [
    p for p in props 
    if p['Eccentricity'] < 0.5 and p['Solidity'] > 0.9
]

print(f"Objetos circulares: {len(objetos_circulares)}")
```

---

## 🔧 Solución de Problemas

### Problema 1: "SyntaxError" al hacer pip install

**Causa:** Ejecutaste `pip` dentro del intérprete de Python (`>>>`)

**Solución:** Ejecutar en la **terminal/CMD**, NO en Python:

```bash
# ❌ MAL - Dentro de Python
>>> pip install -e .
SyntaxError: invalid syntax

# ✅ BIEN - En terminal/CMD
C:\> cd ruta\a\CV
C:\> pip install -e .
```

---

### Problema 2: "ModuleNotFoundError: No module named 'ip_functions'"

**Solución 1:** Verificar instalación

```bash
pip show ip_functions
```

Si no aparece, reinstalar:

```bash
pip install -e .
```

**Solución 2:** Verificar que Python encuentra el módulo

```python
import sys
print('\n'.join(sys.path))
```

---

### Problema 3: bwlabel sigue fragmentando objetos

**Causa:** Python/Jupyter tiene la versión antigua cargada en memoria

**Solución:** Reiniciar Python o kernel

**En Jupyter Notebook:**
```
Kernel → Restart
```

**En Python:**
```python
exit()  # Cerrar y abrir nuevamente
```

**En script:**
```python
# Al inicio del archivo
import importlib
import ip_functions
importlib.reload(ip_functions)
from ip_functions import *
```

---

### Problema 4: No sé dónde está instalado ip_functions

**Solución:**

```python
import ip_functions
print(ip_functions.__file__)
```

Esto te muestra la ruta exacta del archivo `ip_functions.py` que está siendo usado.

---

### Problema 5: Tengo múltiples versiones instaladas

**Síntoma:** `pip show ip_functions` muestra una ubicación, pero `ip_functions.__file__` muestra otra.

**Solución:** Desinstalar todas las versiones y reinstalar limpiamente

```bash
# Desinstalar todas las instancias
pip uninstall ip_functions -y
pip uninstall ip_functions -y  # Repetir por si hay múltiples

# Limpiar cache de pip
pip cache purge

# Reinstalar desde GitHub
pip install git+https://github.com/jacoperUTP/CV.git
```

---

### Problema 6: Error al importar en Jupyter pero funciona en Python

**Causa:** Jupyter puede estar usando un kernel diferente o un entorno virtual diferente.

**Solución 1:** Verificar qué Python usa Jupyter

```python
import sys
print(sys.executable)
print(sys.version)
```

**Solución 2:** Instalar en el entorno correcto

```bash
# Encontrar qué pip usa tu Jupyter
python -m pip show jupyter

# Instalar ip_functions con ese Python
python -m pip install -e .
```

**Solución 3:** Reinstalar kernel de Jupyter

```bash
python -m ipykernel install --user --name=mi_entorno
```

---

## 📊 Comparación de Resultados v1.0 vs v2.0

### Test de bwlabel

```python
import numpy as np
from ip_functions import bwlabel

# Caso 1: Objeto en L
test1 = np.array([
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 1]
], dtype=bool)

labels1, num1 = bwlabel(test1, EE=4)
print(f"Objeto en L: {num1} componentes")
# v1.0: 2 ❌
# v2.0: 1 ✅

# Caso 2: Objeto en T
test2 = np.array([
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
], dtype=bool)

labels2, num2 = bwlabel(test2, EE=4)
print(f"Objeto en T: {num2} componentes")
# v1.0: 3 ❌
# v2.0: 1 ✅

# Caso 3: Dos objetos separados
test3 = np.array([
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1]
], dtype=bool)

labels3, num3 = bwlabel(test3, EE=4)
print(f"Dos objetos: {num3} componentes")
# v1.0: 2 ✅
# v2.0: 2 ✅
```

---

## 📞 Soporte

Si encuentras problemas durante la migración:

1. **Revisa esta guía** completa
2. **Consulta el [README.md](README.md)** principal
3. **Abre un issue:** https://github.com/jacoperUTP/CV/issues
4. **Contacto directo:** jacoper@utp.edu.co

---

## ✅ Checklist de Migración

Usa esta lista para verificar que completaste todos los pasos:

- [ ] Hice backup de mi versión anterior (opcional)
- [ ] Desinstalé ip_functions v1.0
- [ ] Descargué/actualicé el repositorio
- [ ] Instalé ip_functions v2.0
- [ ] Verifiqué que bwlabel funciona correctamente (test debe dar num=1)
- [ ] Verifiqué que regionprops tiene las nuevas propiedades
- [ ] Reinicié Python/Jupyter para cargar la nueva versión
- [ ] Probé mis scripts existentes (deben funcionar sin cambios)
- [ ] Actualicé mi código para usar nuevas propiedades (opcional)

---

**¡Felicitaciones! Ya tienes IP Functions v2.0 instalado y funcionando correctamente.** 🎉

---

*Última actualización: Noviembre 2025*
