from setuptools import setup

setup(
    name="ip_functions",
    version="2.0.0",  # Versión actualizada con bwlabel corregido
    py_modules=["ip_functions"],
    description="Librería completa de procesamiento de imágenes - Compatible con MATLAB",
    author="Universidad Tecnológica de Pereira",
    author_email="jacoper@utp.edu.co",
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pillow>=8.0',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
    ],
    keywords="image processing, matlab, computer vision, segmentation, morphology, filters, transforms",
    long_description="""
# IP Functions - Librería de Procesamiento de Imágenes

Librería completa de procesamiento de imágenes compatible con MATLAB.
Incluye más de 60 funciones para manipulación, análisis y visualización de imágenes.

## Funciones Principales (v2.0.0)

### 📷 Entrada/Salida
- `imread` - Leer imágenes desde disco
- `imwrite` - Guardar imágenes
- `imshow` - Visualizar imágenes (compatible con MATLAB)

### 🎨 Ajuste de Imágenes
- `imadjust` - Ajuste de intensidad con mapeo no lineal
- `histeq` - Ecualización de histograma
- `stretchlim` - Límites de estiramiento automático
- `imcomplement` - Complemento de imagen
- `imhist` - Histograma de imagen
- `mat2gray` - Normalización a [0,1]

### 🌈 Conversión de Color
- `rgb2gray` - RGB a escala de grises
- `rgb2hsv`, `hsv2rgb` - Conversión HSV
- `rgb2lab`, `lab2rgb` - Conversión CIE Lab
- `rgb2xyz`, `xyz2rgb` - Conversión XYZ
- `xyz2lab`, `lab2xyz` - Lab ↔ XYZ

### ✂️ Transformaciones Geométricas
- `imrotate` - Rotar imagen
- `imresize` - Cambiar tamaño
- `imcrop` - Recortar región
- `imtranslate` - Trasladar imagen
- `imwarp` - Transformación geométrica con matriz homográfica
- `fitgeotrans` - Calcular transformación entre puntos

### 🔍 Filtros y Convolución
- `imfilter` - Filtrado con kernel personalizado
- `medfilt2` - Filtro de mediana (reducción de ruido)
- `ordfilt2` - Filtro de orden
- `modefilt` - Filtro de moda
- `stdfilt` - Filtro de desviación estándar
- `entropyfilt` - Filtro de entropía
- `rangefilt` - Filtro de rango
- `fspecial` - Crear kernels especiales (gaussian, laplacian, sobel, prewitt, etc.)

### 🔲 Morfología Matemática
- `strel` - Crear elemento estructurante
- `imdilate` - Dilatación morfológica
- `imerode` - Erosión morfológica
- `imopen` - Apertura (erosión + dilatación)
- `imclose` - Cierre (dilatación + erosión)

### ✂️ Segmentación
- `imbinarize` - Binarización con método automático u manual
- `graythresh` - Umbral de Otsu
- `adaptthresh` - Umbralización adaptativa
- `im2bw` - Conversión a binario con umbral
- `edge` - Detección de bordes (Sobel, Prewitt, Roberts, Canny, LoG)
- `imgradient` - Gradiente de imagen

### 🏷️ Análisis de Componentes
- `bwlabel` - Etiquetar componentes conectados (v2.0 CORREGIDO con Union-Find)
- `label2rgb` - Convertir etiquetas a pseudocolor
- `regionprops` - Propiedades de regiones (Area, Centroid, BoundingBox, Perimeter,
  Eccentricity, Orientation, MajorAxisLength, MinorAxisLength, ConvexArea,
  ConvexHull, ConvexImage, Solidity, Extent, PixelIdxList, PixelList, etc.)

### 📐 Transformada de Hough
- `hough` - Transformada de Hough para líneas
- `houghpeaks` - Detectar picos en espacio de Hough
- `houghlines` - Detectar segmentos de línea
- `imfindcircles` - Detectar círculos (Phase Code y Two-Stage)
- `viscircles` - Visualizar círculos

### 📊 Transformada de Fourier
- `fft`, `ifft` - FFT 1D y su inversa
- `fft2`, `ifft2` - FFT 2D y su inversa (compatible con MATLAB)
- `fftshift`, `ifftshift` - Centrar espectro de frecuencias

### 🔧 Restauración y Métricas
- `deconvwnr` - Deconvolución Wiener
- `immse` - Error cuadrático medio
- `psnr` - Relación señal-ruido pico
- `ssim` - Índice de similitud estructural

### 🎲 Ruido
- `imnoise` - Agregar ruido (gaussian, salt & pepper, poisson, speckle)

### 🔧 Utilidades
- `imsplit` - Separar canales RGB
- `non_overflowing_sum` - Suma sin desbordamiento

## Nuevas Características en v2.0.0

✅ **bwlabel CORREGIDO**: Implementación robusta con Union-Find que previene
   la fragmentación incorrecta de objetos conectados

✅ **regionprops MEJORADO**: Cálculo completo de propiedades geométricas
   incluyendo ConvexHull, Eccentricity, Orientation, etc.

✅ **Compatibilidad mejorada** con sintaxis MATLAB

## Instalación

```bash
pip install -e .
```

## Uso Básico

```python
from ip_functions import *
import numpy as np

# Leer y mostrar imagen
I = imread('imagen.jpg')
imshow(I)

# Segmentación
gray = rgb2gray(I)
umbral = graythresh(gray)
bw = im2bw(gray, umbral)

# Etiquetar componentes (CORREGIDO en v2.0)
labels, num = bwlabel(bw, EE=8)
print(f"Objetos detectados: {num}")

# Analizar regiones
props = regionprops(labels, properties=['Area', 'Centroid', 'BoundingBox'])
for p in props:
    print(f"Área: {p['Area']}, Centro: {p['Centroid']}")

# Visualizar resultados
rgb_labels = label2rgb(labels, 'jet', 'k', 'shuffle')
imshow(rgb_labels)
```

## Requisitos

- Python >= 3.6
- numpy >= 1.19.0
- matplotlib >= 3.3.0

## Compatibilidad

Esta librería replica la funcionalidad de las funciones de Image Processing
Toolbox de MATLAB, permitiendo una transición fácil entre ambas plataformas.

## Autor

Universidad Tecnológica de Pereira
Contacto: jacoper@utp.edu.co

## Licencia

MIT License
""",
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/ip_functions",  # Actualizar con tu URL
    project_urls={
        "Bug Reports": "https://github.com/tu-usuario/ip_functions/issues",
        "Source": "https://github.com/tu-usuario/ip_functions",
        "Documentation": "https://github.com/tu-usuario/ip_functions/wiki",
    },
)