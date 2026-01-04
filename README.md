# IP Functions - Librería de Procesamiento de Imágenes 🖼️

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.1-green.svg)](https://github.com/jacoperUTP/CV/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MATLAB Compatible](https://img.shields.io/badge/MATLAB-compatible-orange.svg)](https://www.mathworks.com/products/image.html)

**Librería completa de procesamiento de imágenes en Python, compatible con MATLAB Image Processing Toolbox, priorizando claridad de implementación y funcionamiento sobre eficiencia extrema.**

Desarrollada por la **Universidad Tecnológica de Pereira** para facilitar la transición de código MATLAB a Python manteniendo una sintaxis familiar, un flujo de trabajo equivalente y resultados consistentes en contextos educativos e investigativos.

---

## 🎯 Características Principales

- **60+ funciones** de procesamiento de imágenes
- **Sintaxis alineada con MATLAB** para migración rápida (flujo similar a copiar/pegar)
- **Dependencias ligeras**: énfasis en **NumPy** y **Matplotlib**
- **Bien documentada**: docstrings claros, ejemplos y validación de parámetros
- **Educativa**: implementaciones legibles y trazables
- **v2.0** con correcciones críticas: `bwlabel` y `regionprops` mejorados
- **v2.0.1** con mejoras geométricas: `interp2` MATLAB-like y transformaciones “en una sola pasada”

---

## ⭐ Novedades en v2.0.1

### 1) Interpolación 2D tipo MATLAB: `interp2`
Se incorpora `interp2` con convención **1-based** (coordenadas estilo MATLAB) y métodos:

- `nearest`
- `linear` / `bilinear`
- `cubic` / `bicubic`

Incluye `extrapval` para definir el valor fuera de la imagen. Soporta imágenes 2D y 3D (interpolación canal a canal).

### 2) Transformaciones geométricas sin bucles por píxel
Las funciones geométricas pasan a un flujo estándar de mapeo inverso:

1. Construcción de una malla de salida `(Xp, Yp)`
2. Mapeo inverso a coordenadas de entrada `(Xq, Yq)`
3. Evaluación con `interp2` sobre la malla completa

Esto evita bloqueos en imágenes medianas/grandes cuando se emplea interpolación y mantiene claridad matemática.

Funciones beneficiadas: `imrotate`, `imresize`, `imtranslate`, `imwarp`.

---

## 📦 Instalación

### Desde GitHub (recomendado para desarrollo)

    git clone https://github.com/jacoperUTP/CV.git
    cd CV
    pip install -e .

### Instalación directa

    pip install git+https://github.com/jacoperUTP/CV.git

### Requisitos

- Python >= 3.6
- NumPy >= 1.19.0
- Matplotlib >= 3.3.0

---

## 🔄 Actualización recomendada (evitar caché)

    pip uninstall ip_functions -y
    pip install --no-cache-dir --upgrade --force-reinstall git+https://github.com/jacoperUTP/CV.git

Verificación de la ruta del paquete (útil en Colab/Jupyter):

    python -c "import ip_functions, inspect; print(inspect.getfile(ip_functions))"

---

## 🚀 Uso Rápido

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

---

## ✂️ Ejemplo v2.0.1: rotación con interpolación bilinear

    from ip_functions import *
    import matplotlib.pyplot as plt
    import numpy as np

    RGB = imread('imagen.jpg')
    Rotado = imrotate(RGB, 60, method='bilinear', extrapval=0.0)

    plt.figure(1)
    plt.imshow(Rotado.astype(np.uint8))
    plt.axis('off')
    plt.show()

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
- `imrotate` - Rotar imagen (v2.0.1: interpolación y malla completa)
- `imresize` - Cambiar tamaño (v2.0.1: interpolación y malla completa)
- `imcrop` - Recortar región
- `imtranslate` - Trasladar imagen (v2.0.1: interpolación y malla completa)
- `imwarp` - Transformación con matriz homográfica (v2.0.1: interpolación y malla completa)
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
- **`bwlabel`** - Etiquetar componentes (v2.0 CORREGIDO)
- `label2rgb` - Visualizar etiquetas en pseudocolor
- **`regionprops`** - Propiedades geométricas completas

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

## ⭐ Novedades en v2.0.0 (referencia)

### ✅ `bwlabel` CORREGIDO
La versión 2.0 corrige un bug crítico en `bwlabel` que causaba fragmentación incorrecta de objetos conectados.

Problema típico en v1.0 (fragmentación):
    import numpy as np
    from ip_functions import bwlabel

    test = np.array([
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 1]
    ], dtype=bool)

    labels, num = bwlabel(test, EE=4)

### ✅ `regionprops` MEJORADO
Ejemplo de propiedades ampliadas:
    props = regionprops(labels, properties=[
        'Area', 'Centroid', 'BoundingBox',
        'Perimeter', 'Eccentricity', 'Orientation',
        'MajorAxisLength', 'MinorAxisLength',
        'ConvexArea', 'ConvexHull', 'Solidity',
    ])

---

## 🧪 Testing

    import numpy as np
    from ip_functions import bwlabel

    test = np.array([
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1]
    ], dtype=bool)

    labels, num = bwlabel(test, EE=4)
    print(f"Componentes: {num}")
    assert num == 1, "bwlabel no está funcionando correctamente"
    print("Test pasado: bwlabel funciona correctamente")

---

## 🤝 Contribuciones

1. Abrir un Issue: https://github.com/jacoperUTP/CV/issues
2. Fork del repositorio
3. Crear rama: `git checkout -b feature/nueva-funcionalidad`
4. Commit: `git commit -am 'Agregar nueva funcionalidad'`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍🏫 Autor

**Universidad Tecnológica de Pereira**  
Grupo de Investigación en Robótica Aplicada  
Programa de Maestría en Instrumentación Física

Contacto:  
- jacoper@utp.edu.co  
- GitHub: https://github.com/jacoperUTP  
- Universidad: https://www.utp.edu.co

---

## 📚 Recursos

- Releases: https://github.com/jacoperUTP/CV/releases
- Issues: https://github.com/jacoperUTP/CV/issues

---

Última actualización: Enero 2026 - Versión 2.0.1

