# Manual de Uso - IP Functions v2.0

Esta guía detalla el uso, parámetros y ejemplos para cada función de la librería `ip_functions`.
Es compatible con la sintaxis de MATLAB para facilitar la migración de código.

## Índice
1. [Entrada y Salida](#1-entrada-y-salida)
2. [Ajuste y Mejora](#2-ajuste-y-mejora)
3. [Espacios de Color](#3-espacios-de-color)
4. [Transformaciones Geométricas](#4-transformaciones-geométricas)
5. [Filtros Espaciales](#5-filtros-espaciales)
6. [Morfología Matemática](#6-morfología-matemática)
7. [Segmentación y Análisis](#7-segmentación-y-análisis)
8. [Transformada de Hough](#8-transformada-de-hough)
9. [Formas y ROI](#9-formas-y-roi)
10. [Frecuencia (Fourier/DCT)](#10-frecuencia-fourierdct)
11. [Transformada de Radon](#11-transformada-de-radon)
12. [Restauración y Calidad](#12-restauración-y-calidad)

---

## 1. Entrada y Salida

### `imread`
Lee una imagen desde un archivo.
- **Parámetros**:
  - `filename`: Ruta del archivo de imagen (str).
- **Retorna**: Array numpy (uint8).
- **Ejemplo**:
  ```python
  I = imread('imagen.jpg')
  ```

### `imshow`
Muestra una imagen en una ventana.
- **Parámetros**:
  - `I`: Imagen a mostrar (MxN o MxNx3).
  - `show`: (Opcional) Si es True, llama a `plt.show()` (bool, default=True).
  - `cmap`: (Opcional) Mapa de color para imágenes en escala de grises (str, default='gray').
- **Ejemplo**:
  ```python
  imshow(I)
  ```

### `imwrite`
Guarda una imagen en un archivo.
- **Parámetros**:
  - `I`: Imagen a guardar.
  - `filename`: Nombre del archivo de salida.
  - `cmap`: (Opcional) Mapa de color.
- **Ejemplo**:
  ```python
  imwrite(I, 'resultado.png')
  ```

---

## 2. Ajuste y Mejora

### `imadjust`
Ajusta los valores de intensidad de una imagen para mejorar el contraste.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `[low_in, high_in]`: Rango de entrada a mapear (0.0-1.0). Default `[0, 1]`.
  - `[low_out, high_out]`: Rango de salida (0.0-1.0). Default `[0, 1]`.
  - `gamma`: Curva de mapeo (gamma < 1 aclara, gamma > 1 oscurece). Default `1`.
- **Ejemplo**:
  ```python
  # Aumentar contraste
  J = imadjust(I, [0.3, 0.7], [0.0, 1.0])
  ```

### `histeq`
Realiza ecualización del histograma para mejorar el contraste.
- **Parámetros**:
  - `I`: Imagen de entrada (escala de grises).
  - `hR`: (Opcional) Histograma de referencia para especificación de histograma.
- **Ejemplo**:
  ```python
  J = histeq(I)
  ```

### `stretchlim`
Calcula los límites de intensidad que estiran el contraste (usado comúnmente con `imadjust`).
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `Tol`: Tolerancia de saturación (default 0.01, es decir 1%).
- **Ejemplo**:
  ```python
  limites = stretchlim(I)
  J = imadjust(I, limites, [0, 1])
  ```

### `bat2gray` (Ver `mat2gray`)
### `mat2gray`
Convierte una matriz arbitraria a una imagen en escala de grises [0, 1].
- **Parámetros**:
  - `I`: Matriz de entrada.
  - `limits`: (Opcional) `[min, max]` para escalar. Si no se da, usa el min/max de la matriz.
- **Ejemplo**:
  ```python
  J = mat2gray(I)
  ```

### `imcomplement`
Calcula el negativo de la imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
- **Ejemplo**:
  ```python
  J = imcomplement(I)
  ```

### `imhist`
Calcula y muestra el histograma de la imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `ax`: (Opcional) Eje de matplotlib donde dibujar.
  - `ver`: Si es True, muestra el gráfico. Si es False, retorna los conteos (default True).
- **Ejemplo**:
  ```python
  imhist(I)
  counts = imhist(I, ver=False)
  ```

---

## 3. Espacios de Color

### `rgb2gray`
Convierte imagen RGB a escala de grises (luminancia).
- **Parámetros**:
  - `RGB`: Imagen de color MxNx3.
- **Ejemplo**:
  ```python
  gray = rgb2gray(RGB)
  ```

### `imsplit`
Separa una imagen RGB en sus tres canales.
- **Parámetros**:
  - `I`: Imagen RGB.
- **Retorna**: `r, g, b` (tres arrays 2D).
- **Ejemplo**:
  ```python
  r, g, b = imsplit(RGB)
  ```

### `rgb2hsv` / `hsv2rgb`
Conversión entre RGB y HSV (Matiz, Saturación, Valor).
- **Parámetros**: `I` (Imagen de entrada).
- **Ejemplo**:
  ```python
  hsv = rgb2hsv(rgb)
  rgb_rec = hsv2rgb(hsv)
  ```

### `rgb2lab` / `lab2rgb`
Conversión entre RGB y CIELAB (Luminosidad, a, b).
- **Ejemplo**:
  ```python
  lab = rgb2lab(rgb)
  ```

### `rgb2xyz` / `xyz2rgb`
Conversión entre RGB y CIE XYZ.
- **Ejemplo**:
  ```python
  xyz = rgb2xyz(rgb)
  ```

### `rgb2ycbcr` / `ycbcr2rgb`
Conversión entre RGB y YCbCr (Luminancia, Crominancia azul, Crominancia roja).
- **Ejemplo**:
  ```python
  ycbcr = rgb2ycbcr(rgb)
  ```


---

## 4. Transformaciones Geométricas

### `imresize`
Redimensiona una imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `S`: Factor de escala (float) o tamaño `[rows, cols]`.
  - `method`: (Opcional) 'bicubic', 'bilinear', 'nearest'. Default='bicubic'.
- **Ejemplo**:
  ```python
  J = imresize(I, 0.5)      # Mitad de tamaño
  J = imresize(I, [100, 100]) # Tamaño fijo
  ```

### `imrotate`
Rota una imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `degrees`: Grados de rotación (horario).
  - `method`: 'nearest', 'bilinear', 'bicubic'. Default='nearest'.
- **Ejemplo**:
  ```python
  J = imrotate(I, 45) # 45 grados (horario)
  ```

### `imcrop`
Recorta una región rectangular de la imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `x`: Coordenada x de la esquina superior izquierda.
  - `y`: Coordenada y de la esquina superior izquierda.
  - `w`: Ancho del rectángulo.
  - `h`: Alto del rectángulo.
- **Ejemplo**:
  ```python
  J = imcrop(I, 100, 100, 50, 50)
  ```

### `imtranslate`
Traslada una imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `translation`: `[tx, ty]` (desplazamiento en x e y).
  - `method`: 'bilinear'.
  - `extrapval`: Valor para rellenar bordes (default 0).
- **Ejemplo**:
  ```python
  J = imtranslate(I, [10, -5]) # X+10, Y-5
  ```

### `imwarp`
Aplica una transformación geométrica general (homografía) 3x3.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `H`: Matriz de transformación 3x3.
- **Ejemplo**:
  ```python
  H = np.eye(3) # Identidad
  J = imwarp(I, H)
  ```

### `fitgeotrans`
Estima una transformación geométrica a partir de pares de puntos correspondientes.
- **Parámetros**:
  - `fixedPoints`: Puntos en la imagen destino (Nx2).
  - `movingPoints`: Puntos en la imagen origen (Nx2).
  - `type`: 'projective' (default).
- **Ejemplo**:
  ```python
  H = fitgeotrans(pts_dst, pts_src, 'projective')
  ```

---

## 5. Filtros Espaciales

### `imfilter`
Filtra una imagen con un kernel de convolución multidimensional (equivalente a `conv2` o `ndimage.convolve`).
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `K`: Kernel de filtrado.
  - `salida`: 'same' (mismo tamaño), 'full', 'valid'. Default='same'.
  - `tipodepad`: 'symmetric', 'replicate', 'circular', 0. Default='symmetric'.
- **Ejemplo**:
  ```python
  h = fspecial('average', 3)
  J = imfilter(I, h)
  ```

### `fspecial`
Crea filtros predefinidos para usar con `imfilter`.
- **Parámetros**:
  - `type`: 'average', 'disk', 'gaussian', 'laplacian', 'log', 'motion', 'prewitt', 'sobel'.
  - `hsize`: Tamaño del filtro (escalar o [h, w]).
  - `sigma`: (Opcional, para gaussian/log) Desviación estándar. Default=0.5.
- **Ejemplo**:
  ```python
  h = fspecial('gaussian', 5, 1.0)
  ```

### `medfilt2`
Filtro de mediana 2D para eliminar ruido "sal y pimienta" preservando bordes.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `[m, n]`: Tamaño del vecindario. Default `[3, 3]`.
- **Ejemplo**:
  ```python
  J = medfilt2(I, [3, 3])
  ```

### `ordfilt2`
Filtro de orden estadístico 2D.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `order`: Rango del valor a seleccionar (mínimo=1, mediana=(m*n)/2, máximo=m*n).
  - `domain`: Máscara del vecindario (matriz 1s y 0s).
- **Ejemplo**:
  ```python
  # Filtro de mínimo (erosión)
  J = ordfilt2(I, 1, np.ones((3,3)))
  ```

### `stdfilt` / `entropyfilt` / `rangefilt`
Filtros de textura local.
- **Parámetros**: `I` (Imagen), `nhood` (Vecindario, default 3x3).
- **Ejemplo**:
  ```python
  J = stdfilt(I)     # Desviación estándar local
  J = entropyfilt(I) # Entropía local
  J = rangefilt(I)   # Rango (max - min) local
  ```

### `roifilt2`
Filtra una región de interés definida por una máscara binaria.
- **Parámetros**:
  - `h`: Filtro o función handle.
  - `I`: Imagen de entrada.
  - `BW`: Máscara binaria (True donde se debe filtrar).
- **Ejemplo**:
  ```python
  h = fspecial('average', 5)
  J = roifilt2(h, I, BW)
  ```

---

## 6. Morfología Matemática

### `strel`
Crea un elemento estructurante morfológico.
- **Parámetros**:
  - `shape`: 'disk', 'line', 'square', 'diamond', 'rectangle'.
  - `parameters`: Radio (disk), Longitud/Ángulo (line), Lado (square/diamond), [h, w] (rectangle).
- **Ejemplo**:
  ```python
  se = strel('disk', 5)
  se_line = strel('line', 10, 45) # Longitud 10, ángulo 45°
  ```

### `imdilate`
Dilatación morfológica (expande regiones blancas).
- **Parámetros**:
  - `I`: Imagen binaria o de grises.
  - `SE`: Elemento estructurante (matriz lógica o uint8).
- **Ejemplo**:
  ```python
  J = imdilate(BW, se)
  ```

### `imerode`
Erosión morfológica (contrae regiones blancas).
- **Parámetros**:
  - `I`: Imagen.
  - `SE`: Elemento estructurante.
- **Ejemplo**:
  ```python
  J = imerode(BW, se)
  ```

### `imopen`
Apertura morfológica (Erosión seguida de Dilatación). Elimina objetos pequeños.
- **Parámetros**: `I`, `SE`.
- **Ejemplo**:
  ```python
  J = imopen(BW, se)
  ```

### `imclose`
Cierre morfológico (Dilatación seguida de Erosión). Rellena agujeros pequeños.
- **Parámetros**: `I`, `SE`.
- **Ejemplo**:
  ```python
  J = imclose(BW, se)
  ```


---

## 7. Segmentación y Análisis

### `imbinarize`
Binariza una imagen usando un método específico.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `method`: 'global' (Otsu, por defecto) o 'adaptive'.
  - `threshold`: (Opcional) Valor manual de umbral.
- **Ejemplo**:
  ```python
  BW = imbinarize(I)                   # Otsu
  BW = imbinarize(I, 0.5)             # Manual
  BW = imbinarize(I, 'adaptive')      # Adaptativo
  ```

### `graythresh` / `otsuthresh`
Calcula el umbral global usando el método de Otsu.
- `graythresh(I)` calcula sobre la imagen.
- `otsuthresh(histogram)` calcula sobre un histograma.
- **Ejemplo**:
  ```python
  level = graythresh(I)
  BW = im2bw(I, level)
  ```

### `edge`
Detecta bordes en una imagen.
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `method`: 'sobel', 'prewitt', 'roberts', 'log', 'canny'. Default='canny'.
- **Ejemplo**:
  ```python
  BW = edge(I, 'canny')
  ```

### `imgradient`
Calcula la magnitud y dirección del gradiente.
- **Parámetros**: `I`, `method` ('sobel', 'prewitt').
- **Retorna**: `Gmag, Gdir`.
- **Ejemplo**:
  ```python
  Gmag, Gdir = imgradient(I)
  ```

### `bwlabel`
Etiqueta componentes conectados en una imagen binaria 2D.
- **Parámetros**:
  - `BW`: Imagen binaria.
  - `EE`: Conectividad (4 u 8). Default=4.
- **Retorna**: `labels` (imagen etiquetada), `num` (cantidad de objetos).
- **Ejemplo**:
  ```python
  L, n = bwlabel(BW, 8)
  ```

### `label2rgb`
Visualiza una imagen etiquetada usando color.
- **Parámetros**:
  - `L`: Matriz de etiquetas.
  - `colormap`: 'jet', 'hsv', etc.
  - `bgcolor`: Color de fondo (default k=negro).
  - `order`: 'shuffle' o 'noshuffle'.
- **Ejemplo**:
  ```python
  RGB = label2rgb(L, 'jet', 'k', 'shuffle')
  ```

### `regionprops`
Mide propiedades de regiones en una imagen etiquetada.
- **Parámetros**:
  - `L`: Matriz de etiquetas.
  - `properties`: Lista de propiedades (['Area', 'Centroid', 'BoundingBox', ...]) o 'all'.
- **Propiedades soportadas**: Area, Perimeter, BoundingBox, Centroid, Eccentricity, Orientation, MajorAxisLength, MinorAxisLength, ConvexArea, ConvexHull, Solidity, Extent.
- **Ejemplo**:
  ```python
  props = regionprops(L, properties=['Area', 'Centroid'])
  print(props[0]['Area'])
  ```

---

## 8. Transformada de Hough

### `hough`
Calcula la transformada de Hough para detección de líneas.
- **Parámetros**:
  - `BW`: Imagen binaria de bordes.
  - `Theta`: (Opcional) Rango de ángulos en grados.
  - `RhoResolution`: Resolución de rho (default 1).
- **Retorna**: `H` (Matriz acumuladora), `theta`, `rho`.
- **Ejemplo**:
  ```python
  H, theta, rho = hough(BW)
  ```

### `houghpeaks`
Identifica picos en la transformada de Hough.
- **Parámetros**:
  - `H`: Transformada de Hough.
  - `numpeaks`: Número máximo de picos a encontrar.
- **Ejemplo**:
  ```python
  P = houghpeaks(H, 5)
  ```

### `houghlines`
Extrae segmentos de línea basados en los picos de Hough.
- **Parámetros**: `BW`, `theta`, `rho`, `peaks`.
- **Ejemplo**:
  ```python
  lines = houghlines(BW, theta, rho, P)
  # lines es una lista de diccionarios con 'point1', 'point2', 'theta', 'rho'
  ```

### `imfindcircles`
Detecta círculos usando la Transformada de Hough.
- **Parámetros**:
  - `BW`: Imagen binaria (bordes).
  - `radius_range`: `[rmin, rmax]`.
  - `Sensitivity`: (0-1).
- **Retorna**: `centers`, `radii`, `metric`.
- **Ejemplo**:
  ```python
  centers, radii, _ = imfindcircles(BW, [20, 60])
  ```

### `viscircles`
Dibuja círculos sobre ejes actuales.
- **Parámetros**: `centers`, `radii`, `Color`, `LineWidth`.
- **Ejemplo**:
  ```python
  imshow(I)
  viscircles(centers, radii, Color='b')
  ```

---

## 9. Formas y ROI

### `insertShape`
Dibuja formas en una imagen.
- **Parámetros**:
  - `I`: Imagen.
  - `type`: 'Rectangle', 'Circle', 'Line', 'Polygon'.
  - `position`: Coordenadas [x, y, w, h] o [x, y, r] etc.
- **Ejemplo**:
  ```python
  J = insertShape(I, 'Rectangle', [10, 10, 50, 50], Color='red')
  ```

### `roipoly`
Define una Región de Interés (ROI) poligonal.
- **Parámetros**:
  - `I`: Imagen.
  - `c`, `r`: Coordenadas X e Y de los vértices.
- **Retorna**: Máscara binaria.
- **Ejemplo**:
  ```python
  mask = roipoly(I, [10, 50, 10], [10, 10, 50])
  ```

---

## 10. Frecuencia (Fourier/DCT)

### `fft` / `ifft`
Transformada Rápida de Fourier 1D y su inversa.
- **Uso**: `out = fft(x)`.

### `fft2` / `ifft2`
Transformada Rápida de Fourier 2D y su inversa.
- **Parámetros**:
  - `X`: Imagen entrada.
  - `M`, `N`: (Opcional) Tamaño de pad.
- **Ejemplo**:
  ```python
  F = fft2(I)
  F_shifted = fftshift(F) # Centrar bajas frecuencias
  imshow(np.log(abs(F_shifted) + 1), [])
  ```

### `fftshift` / `ifftshift`
Desplaza la componente de frecuencia cero al centro del espectro.

### `dct2` / `idct2`
Transformada Discreta del Coseno 2D y su inversa.
- **Ejemplo**:
  ```python
  C = dct2(I)
  I_rec = idct2(C)
  ```


---

## 11. Transformada de Radon

### `radon`
Calcula la Transformada de Radon (proyecciones).
- **Parámetros**:
  - `I`: Imagen de entrada.
  - `theta`: Array de ángulos (grados). Default: 0 a 179.
- **Retorna**: `R` (Sinograma), `xp` (coordenadas radiales).
- **Ejemplo**:
  ```python
  theta = np.linspace(0., 180., max(I.shape), endpoint=False)
  R, _ = radon(I, theta)
  imshow(R)
  ```

### `iradon`
Reconstruye una imagen a partir de sus proyecciones (Transformada Inversa de Radon).
- **Parámetros**:
  - `R`: Sinograma.
  - `theta`: Ángulos correspondientes.
  - `filter`: Tipo de filtro ('Ram-Lak', 'Shepp-Logan', etc). Default='Ram-Lak'.
- **Ejemplo**:
  ```python
  I_rec = iradon(R, theta)
  ```

### `phantom`
Genera el fantasma de Shepp-Logan (imagen de prueba).
- **Parámetros**: `n` (Tamaño NxN).
- **Ejemplo**:
  ```python
  I = phantom(256)
  ```

---

## 12. Restauración y Calidad

### `imnoise`
Agrega ruido a una imagen.
- **Parámetros**:
  - `I`: Imagen.
  - `type`: 'gaussian', 'salt & pepper', 'speckle', 'poisson'.
  - `var`/`amount`: Parámetros del ruido.
- **Ejemplo**:
  ```python
  # Ruido gaussiano con media 0 y varianza 0.01
  J = imnoise(I, 'gaussian', 0, 0.01)
  ```

### `deconvwnr`
Restaura una imagen degradada usando el filtro de Wiener.
- **Parámetros**:
  - `I`: Imagen degradada.
  - `dPSF`: Función de dispersión de punto (kernel de desenfoque).
  - `NSR`: Relación Ruido-Señal (escalar o array).
- **Ejemplo**:
  ```python
  psf = fspecial('motion', 21, 11)
  J = deconvwnr(I_blurred, psf, 0.01)
  ```

### `immse`
Calcula el Error Cuadrático Medio (MSE) entre dos imágenes.
- **Uso**: `err = immse(Iref, I)`.

### `psnr`
Calcula la proporción Pico Señal-Ruido.
- **Uso**: `p = psnr(Iref, I)`.

### `ssim`
Calcula el Índice de Similitud Estructural.
- **Uso**: `score = ssim(Iref, I)`.

---

## 13. Utilidades

### `non_overflowing_sum`
Suma dos imágenes evitando el desbordamiento (clipping inteligente).
- **Uso**: `S = non_overflowing_sum(A, B)`.

### `interp2`
Interpolación 2D de valores (similar a MATLAB interp2).
- **Parámetros**: `V`, `Xq`, `Yq`, `method`.

# Fin del Manual
Para más detalles o reportar errores, visita el repositorio en GitHub.



