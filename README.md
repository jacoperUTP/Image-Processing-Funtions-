# IP Functions - Librería de Procesamiento de Imágenes

Librería completa de procesamiento de imágenes compatible con MATLAB.
Incluye más de 60 funciones para manipulación, análisis y visualización de imágenes.

## Funciones Disponibles (v2.0.0)

### 📷 Entrada/Salida
- `imread` - Leer imagen desde archivo
- `imwrite` - Guardar imagen en archivo
- `imshow` - Mostrar imagen (con soporte para tipos de datos y rangos)

### 🎨 Ajuste y Mejora
- `imadjust` - Ajuste de intensidad de imagen
- `histeq` - Ecualización de histograma
- `stretchlim` - Calcular límites de estiramiento de contraste
- `imcomplement` - Complemento de imagen (negativo)
- `imhist` - Calcular y mostrar histograma
- `mat2gray` - Convertir matriz a imagen en escala de grises [0,1]

### 🌈 Espacios de Color
- `rgb2gray` - Convertir RGB a escala de grises
- `imsplit` - Separar canales de color
- `rgb2hsv`, `hsv2rgb` - Convertir entre RGB y HSV
- `rgb2lab`, `lab2rgb` - Convertir entre RGB y CIELAB
- `rgb2xyz`, `xyz2rgb` - Convertir entre RGB y CIEXYZ
- `xyz2lab`, `lab2xyz` - Convertir entre CIEXYZ y CIELAB
- `rgb2ycbcr`, `ycbcr2rgb` - Convertir entre RGB y YCbCr

### ✂️ Transformaciones Geométricas
- `imresize` - Redimensionar imagen
- `imrotate` - Rotar imagen
- `imcrop` - Recortar imagen
- `imtranslate` - Trasladar imagen
- `imwarp` - Aplicar transformación geométrica proyectiva
- `fitgeotrans` - Estimar transformación geométrica a partir de puntos de control

### 🔍 Filtros Espaciales
- `imfilter` - Filtrado N-D de imágenes
- `fspecial` - Crear filtros 2D predefinidos (average, disk, gaussian, laplacian, etc.)
- `medfilt2` - Filtrado de mediana 2D
- `ordfilt2` - Filtrado de orden 2D (min, max, mediana)
- `modefilt` - Filtrado de moda
- `stdfilt` - Filtrado de desviación estándar local
- `entropyfilt` - Filtrado de entropía local
- `rangefilt` - Filtrado de rango local (max - min)
- `roifilt2` - Filtrado en Región de Interés (ROI)

### 🔲 Morfología Matemática
- `strel` - Crear elemento estructurante
- `imdilate` - Dilatación morfológica
- `imerode` - Erosión morfológica
- `imopen` - Apertura morfológica
- `imclose` - Cierre morfológico

### 🧩 Segmentación y Análisis
- `imbinarize` - Binarizar imagen por umbral (Global, Otsu, Adaptativo)
- `im2bw` - Convertir imagen a binaria con un umbral dado
- `graythresh` - Calcular umbral global de Otsu
- `adaptthresh` - Calcular umbral adaptativo
- `otsuthresh` - Calcular umbral de Otsu basado en histograma
- `edge` - Detectar bordes (Sobel, Prewitt, Roberts, Canny, LoG)
- `imgradient` - Calcular magnitud y dirección del gradiente
- `bwlabel` - Etiquetar componentes conectados en imagen binaria (Union-Find)
- `label2rgb` - Visualizar etiquetas como imagen RGB
- `regionprops` - Medir propiedades de regiones de imagen (Are, Perimetro, Centroide, BoundingBox, etc.)
- `invmoments` - Momentos invariantes de Hu

### 📐 Hough y Formas
- `hough` - Transformada de Hough para líneas
- `houghpeaks` - Identificar picos en la transformada de Hough
- `houghlines` - Extraer segmentos de línea de la transformada de Hough
- `imfindcircles` - Encontrar círculos usando la transformada de Hough circular
- `viscircles` - Visualizar círculos detectados
- `insertShape` - Insertar formas (rectángulos, círculos, líneas, polígonos) en una imagen
- `roipoly` - Definir ROI poligonal interactivamente o por coordenadas

### 📊 Transformadas de Frecuencia (Fourier / DCT)
- `fft`, `ifft` - Transformada Rápida de Fourier 1D (y inversa)
- `fft2`, `ifft2` - Transformada Rápida de Fourier 2D (y inversa)
- `fftshift`, `ifftshift` - Desplazar componente de frecuencia cero al centro
- `dft`, `idft` - Transformada Discreta de Fourier 1D (No optimizada)
- `dftshift`, `idftshift` - Desplazamiento para DFT
- `dftfreq` - Frecuencias de muestra de la DFT
- `dct`, `idct` - Transformada Discreta del Coseno 1D (y inversa)
- `dct2`, `idct2` - Transformada Discreta del Coseno 2D (y inversa)

### 🌀 Transformada de Radon
- `radon` - Transformada de Radon
- `iradon` - Transformada Inversa de Radon
- `phantom` - Generar fantasma de Shepp-Logan de prueba

### 🔧 Restauración y Calidad
- `deconvwnr` - Deconvolución de Wiener
- `immse` - Error Cuadrático Medio
- `psnr` - Relación Señal a Ruido Pico
- `ssim` - Índice de Similitud Estructural
- `imnoise` - Añadir ruido a una imagen (gaussian, salt & pepper, speckle, etc.)

### �️ Utilidades
- `non_overflowing_sum` - Suma segura sin desbordamiento
- `interp2` - Interpolación 2D (funcionalidad interna expuesta)

## Instalación

```bash
# Instalación local
pip install -e .

# Instalación desde GitHub
pip install git+https://github.com/jacoperUTP/Image-Processing-Funtions-.git
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
