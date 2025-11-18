# IP Functions - Librería de Procesamiento de Imágenes 🖼️

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/jacoperUTP/CV/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MATLAB Compatible](https://img.shields.io/badge/MATLAB-compatible-orange.svg)](https://www.mathworks.com/products/image.html)

**Librería completa de procesamiento de imágenes en Python, 100% compatible con MATLAB Image Processing Toolbox.**

Desarrollada por la **Universidad Tecnológica de Pereira** para facilitar la transición de código MATLAB a Python manteniendo la misma sintaxis y funcionalidad.

---

## 🎯 Características Principales

- **60+ funciones** de procesamiento de imágenes
- **Sintaxis idéntica a MATLAB** - copia/pega tu código MATLAB y funciona
- **Sin dependencias pesadas** - solo NumPy y Matplotlib
- **Bien documentada** - cada función con docstrings detallados
- **Educativa** - código claro y comprensible para aprendizaje
- **v2.0 con correcciones críticas** - `bwlabel` y `regionprops` mejorados

---

## 📦 Instalación

### Desde GitHub (Recomendado para desarrollo)

```bash
git clone https://github.com/jacoperUTP/CV.git
cd CV
pip install -e .
```

### Instalación directa

```bash
pip install git+https://github.com/jacoperUTP/CV.git
```

### Requisitos

- Python >= 3.6
- NumPy >= 1.19.0
- Matplotlib >= 3.3.0

---

## 🚀 Uso Rápido

```python
from ip_functions import *
import numpy as np

# Leer y visualizar imagen
I = imread('imagen.jpg')
imshow(I, 'Imagen Original')

# Convertir a escala de grises
gray = rgb2gray(I)

# Segmentación automática con Otsu
umbral = graythresh(gray)
bw = im2bw(gray, umbral)

# Operaciones morfológicas
se = strel('disk', 5)
bw_clean = imopen(bw, se)

# Etiquetar componentes conectados (v2.0 CORREGIDO)
labels, num_objects = bwlabel(bw_clean, EE=8)
print(f"Objetos detectados: {num_objects}")

# Analizar propiedades geométricas
props = regionprops(labels, properties=[
    'Area', 'Centroid', 'BoundingBox', 
    'Perimeter', 'Eccentricity', 'Orientation'
])

for i, p in enumerate(props, 1):
    print(f"Objeto {i}:")
    print(f"  Área: {p['Area']} píxeles")
    print(f"  Centro: {p['Centroid']}")
    print(f"  Perímetro: {p['Perimeter']:.2f}")

# Visualizar resultados con colores
rgb_labels = label2rgb(labels, 'jet', 'k', 'shuffle')
imshow(rgb_labels, 'Objetos Etiquetados')
```

---

## 📚 Categorías de Funciones

### 🖼️ Entrada/Salida
- `imread` - Leer imágenes
- `imwrite` - Guardar imágenes  
- `imshow` - Visualizar imágenes (sintaxis MATLAB)

### 🎨 Ajuste y Mejora
- `imadjust` - Ajuste de intensidad con mapeo no lineal
- `histeq` - Ecualización de histograma
- `stretchlim` - Límites de estiramiento automático
- `imcomplement` - Complemento de imagen
- `imhist` - Histograma
- `mat2gray` - Normalización a [0,1]

### 🌈 Conversión de Espacios de Color
- `rgb2gray`, `rgb2hsv`, `hsv2rgb`
- `rgb2lab`, `lab2rgb`
- `rgb2xyz`, `xyz2rgb`
- `xyz2lab`, `lab2xyz`

### ✂️ Transformaciones Geométricas
- `imrotate` - Rotar imagen
- `imresize` - Cambiar tamaño
- `imcrop` - Recortar región
- `imtranslate` - Trasladar imagen
- `imwarp` - Transformación con matriz homográfica
- `fitgeotrans` - Calcular transformación entre puntos

### 🔍 Filtros Espaciales
- `imfilter` - Convolución con kernel personalizado
- `medfilt2` - Filtro de mediana
- `ordfilt2` - Filtro de orden estadístico
- `modefilt` - Filtro de moda
- `stdfilt` - Filtro de desviación estándar
- `entropyfilt` - Filtro de entropía local
- `rangefilt` - Filtro de rango
- `fspecial` - Crear kernels especiales (gaussian, laplacian, sobel, etc.)

### 🔲 Morfología Matemática
- `strel` - Crear elementos estructurantes
- `imdilate` - Dilatación
- `imerode` - Erosión
- `imopen` - Apertura (erosión + dilatación)
- `imclose` - Cierre (dilatación + erosión)

### ✂️ Segmentación
- `imbinarize` - Binarización (Otsu automático o manual)
- `graythresh` - Umbral de Otsu
- `adaptthresh` - Umbralización adaptativa
- `im2bw` - Conversión a binario
- `edge` - Detección de bordes (Sobel, Prewitt, Roberts, Canny, LoG)
- `imgradient` - Gradiente de imagen

### 🏷️ Análisis de Componentes Conectados
- **`bwlabel`** ⭐ - Etiquetar componentes (v2.0 CORREGIDO)
- `label2rgb` - Visualizar etiquetas en pseudocolor
- **`regionprops`** ⭐ - Propiedades geométricas completas

### 🔍 Transformada de Hough
- `hough` - Transformada de Hough para líneas
- `houghpeaks` - Detectar picos
- `houghlines` - Extraer segmentos de línea
- `imfindcircles` - Detectar círculos (Phase Code y Two-Stage)
- `viscircles` - Visualizar círculos detectados

### 📊 Transformada de Fourier
- `fft`, `ifft` - FFT 1D
- `fft2`, `ifft2` - FFT 2D (compatible con MATLAB)
- `fftshift`, `ifftshift` - Centrar espectro

### 🔧 Restauración y Métricas de Calidad
- `deconvwnr` - Deconvolución Wiener
- `immse` - Error cuadrático medio
- `psnr` - Relación señal-ruido pico
- `ssim` - Índice de similitud estructural

### 🎲 Generación de Ruido
- `imnoise` - Agregar ruido (gaussian, salt & pepper, poisson, speckle)

---

## ⭐ Novedades en v2.0.0

### ✅ `bwlabel` CORREGIDO

La versión 2.0 corrige un **bug crítico** en `bwlabel` que causaba fragmentación incorrecta de objetos conectados.

**Problema en v1.0:**
```python
# Objeto en forma de L se fragmentaba en 2 componentes
test = np.array([
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=4)  # v1.0 retornaba num=2 ❌
```

**Solución en v2.0:**
- Implementación robusta con **algoritmo Union-Find**
- Unión correcta de componentes durante escaneo
- Resultado: `num=1` (correcto) ✅

### ✅ `regionprops` MEJORADO

Nuevas propiedades geométricas disponibles:

```python
props = regionprops(labels, properties=[
    'Area',              # Área en píxeles
    'Centroid',          # Centro de masa (y, x)
    'BoundingBox',       # Caja delimitadora
    'Perimeter',         # ⭐ Perímetro (chain code)
    'Eccentricity',      # ⭐ Excentricidad [0,1]
    'Orientation',       # ⭐ Orientación en grados
    'MajorAxisLength',   # ⭐ Eje mayor
    'MinorAxisLength',   # ⭐ Eje menor
    'ConvexArea',        # ⭐ Área de envolvente convexa
    'ConvexHull',        # ⭐ Puntos de envolvente
    'Solidity',          # ⭐ Solidez (Area/ConvexArea)
])
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Detección y Conteo de Objetos

```python
from ip_functions import *

# Leer imagen
I = imread('monedas.jpg')
gray = rgb2gray(I)

# Segmentación
bw = imbinarize(gray, 'otsu')

# Limpieza morfológica
se = strel('disk', 3)
bw = imopen(bw, se)
bw = imclose(bw, se)

# Etiquetar y contar
labels, num_monedas = bwlabel(bw, EE=8)
print(f"Monedas detectadas: {num_monedas}")

# Analizar cada moneda
props = regionprops(labels, properties=['Area', 'Centroid', 'Perimeter'])

for i, p in enumerate(props, 1):
    print(f"Moneda {i}: Área={p['Area']}, Perímetro={p['Perimeter']:.1f}")
    
# Visualizar
rgb_labels = label2rgb(labels, 'jet', 'k', 'shuffle')
imshow(rgb_labels, 'Monedas Etiquetadas')
```

### Ejemplo 2: Detección de Líneas con Hough

```python
from ip_functions import *

# Leer y detectar bordes
I = imread('edificio.jpg')
gray = rgb2gray(I)
edges = edge(gray, 'canny')

# Transformada de Hough
H, theta, rho = hough(edges)

# Detectar picos
peaks = houghpeaks(H, 5)  # Top 5 líneas

# Extraer líneas
lines = houghlines(edges, theta, rho, peaks)

# Visualizar
imshow(I)
for line in lines:
    x1, y1 = line['point1']
    x2, y2 = line['point2']
    plt.plot([x1, x2], [y1, y2], 'r-', linewidth=2)
plt.title(f'{len(lines)} líneas detectadas')
plt.show()
```

### Ejemplo 3: Análisis Morfológico

```python
from ip_functions import *

# Imagen binaria de texto
I = imread('texto.png')
bw = imbinarize(I, 'otsu')

# Diferentes elementos estructurantes
se_line = strel('line', 15, 0)    # Línea horizontal
se_disk = strel('disk', 3)         # Disco

# Operaciones morfológicas
dilated = imdilate(bw, se_line)    # Conectar caracteres
eroded = imerode(bw, se_disk)      # Adelgazar
opened = imopen(bw, se_disk)       # Eliminar ruido
closed = imclose(bw, se_disk)      # Cerrar huecos

# Comparar resultados
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes[0, 0].imshow(bw, cmap='gray')
axes[0, 0].set_title('Original')
axes[0, 1].imshow(dilated, cmap='gray')
axes[0, 1].set_title('Dilatación')
axes[0, 2].imshow(eroded, cmap='gray')
axes[0, 2].set_title('Erosión')
axes[1, 0].imshow(opened, cmap='gray')
axes[1, 0].set_title('Apertura')
axes[1, 1].imshow(closed, cmap='gray')
axes[1, 1].set_title('Cierre')
plt.tight_layout()
plt.show()
```

---

## 🔄 Migración desde v1.0

Si ya tienes `ip_functions` v1.0 instalado, consulta la [**Guía de Migración**](MIGRATION_GUIDE.md) para actualizar a v2.0 sin problemas.

**Resumen rápido:**

```bash
# 1. Desinstalar versión anterior
pip uninstall ip_functions -y

# 2. Instalar v2.0
cd ruta/al/repositorio/CV
pip install -e .

# 3. Verificar instalación
python -c "from ip_functions import bwlabel; print('✅ v2.0 instalada')"
```

---

## 📋 Compatibilidad MATLAB

Esta librería replica fielmente la funcionalidad de MATLAB Image Processing Toolbox:

| MATLAB | IP Functions | Estado |
|--------|--------------|--------|
| `imread('img.jpg')` | `imread('img.jpg')` | ✅ Idéntico |
| `imshow(I)` | `imshow(I)` | ✅ Idéntico |
| `bwlabel(BW, 8)` | `bwlabel(BW, EE=8)` | ✅ Compatible |
| `regionprops(L, 'all')` | `regionprops(L, properties='all')` | ✅ Compatible |
| `strel('disk', 5)` | `strel('disk', 5)` | ✅ Idéntico |
| `fft2(I)` | `fft2(I)` | ✅ Idéntico |

---

## 🧪 Testing

```python
# Test básico de bwlabel v2.0
import numpy as np
from ip_functions import bwlabel

# Objeto en forma de L
test = np.array([
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=4)
print(f"Componentes: {num}")  # Debe ser 1 en v2.0 ✅

assert num == 1, "bwlabel no está funcionando correctamente"
print("✅ Test pasado - bwlabel v2.0 funciona correctamente")
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Si encuentras un bug o tienes una sugerencia:

1. Abre un [Issue](https://github.com/jacoperUTP/CV/issues)
2. Haz un Fork del repositorio
3. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
4. Commit: `git commit -am 'Agregar nueva funcionalidad'`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍🏫 Autor

**Universidad Tecnológica de Pereira**  
Grupo de Investigación en Robótica Aplicada  
Programa de Maestría en Instrumentación Física

**Contacto:**  
📧 jacoper@utp.edu.co  
🌐 [GitHub](https://github.com/jacoperUTP)  
🏛️ [Universidad Tecnológica de Pereira](https://www.utp.edu.co)

---

## 📚 Recursos Adicionales

- [📖 Guía de Instalación Detallada](INSTALLATION.md)
- [🔄 Guía de Migración v1.0 → v2.0](MIGRATION_GUIDE.md)
- [📝 Historial de Cambios](CHANGELOG.md)
- [🐛 Reportar Bugs](https://github.com/jacoperUTP/CV/issues)

---

## 🌟 Agradecimientos

Desarrollado con fines educativos para facilitar la enseñanza de procesamiento de imágenes y visión por computador en la Universidad Tecnológica de Pereira.

**Si este proyecto te es útil, considera darle una ⭐ en GitHub!**

---

*Última actualización: Noviembre 2025 - Versión 2.0.0*
