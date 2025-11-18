# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.0.0] - 2025-11-17

### 🔧 Corregido (Critical Fixes)

- **`bwlabel`**: Corregido bug crítico que causaba fragmentación incorrecta de objetos conectados
  - Implementación robusta con algoritmo **Union-Find**
  - Previene la división incorrecta de objetos en forma de L, T, o con geometrías complejas
  - Conectividad de 4 y 8 vecinos ahora funciona correctamente
  - Los objetos conectados se etiquetan como una sola región
  
  **Ejemplo del problema corregido:**
  ```python
  # Antes (v1.0): Fragmentaba el objeto en 2 componentes ❌
  # Ahora (v2.0): Reconoce correctamente como 1 componente ✅
  test = np.array([
      [0, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 1, 1, 1]
  ], dtype=bool)
  
  labels, num = bwlabel(test, EE=4)  
  # v1.0: num = 2 (incorrecto)
  # v2.0: num = 1 (correcto) ✅
  ```

### ✨ Agregado (New Features)

- **`regionprops`**: Propiedades geométricas adicionales
  - `Perimeter`: Perímetro calculado correctamente usando chain code
  - `Eccentricity`: Excentricidad de la región (0=círculo, 1=línea)
  - `Orientation`: Ángulo de orientación del eje mayor en grados
  - `MajorAxisLength`: Longitud del eje mayor
  - `MinorAxisLength`: Longitud del eje menor
  - `ConvexHull`: Puntos de la envolvente convexa
  - `ConvexArea`: Área de la envolvente convexa
  - `ConvexImage`: Imagen binaria de la envolvente convexa
  - `Solidity`: Solidez (Area/ConvexArea)
  
  **Uso mejorado:**
  ```python
  props = regionprops(labels, properties=[
      'Area', 'Centroid', 'BoundingBox',
      'Perimeter', 'Eccentricity', 'Orientation',
      'MajorAxisLength', 'MinorAxisLength',
      'ConvexArea', 'ConvexHull', 'Solidity'
  ])
  ```

### 📝 Documentación

- README.md completo y profesional con badges
- Ejemplos de uso actualizados
- Guía de migración desde v1.0
- CHANGELOG.md con historial de versiones
- LICENSE (MIT) agregada
- Documentación mejorada en setup.py

### 🔄 Cambios Internos

- Refactorización del algoritmo de etiquetado en `bwlabel`
- Optimización del cálculo de perímetro en `regionprops`
- Mejoras en la gestión de memoria para imágenes grandes
- Tests agregados para validar correcciones

### ⚠️ Breaking Changes

Ninguno. La versión 2.0 mantiene **100% compatibilidad** con código existente.
Todos los scripts que funcionaban en v1.0 funcionan en v2.0 sin modificaciones.

---

## [1.0.0] - 2024-XX-XX

### ✨ Lanzamiento Inicial

Primera versión pública de IP Functions con más de 60 funciones de procesamiento de imágenes.

#### Funciones Implementadas

**Entrada/Salida:**
- `imread`, `imwrite`, `imshow`

**Ajuste de Imágenes:**
- `imadjust`, `histeq`, `stretchlim`, `imcomplement`, `imhist`, `mat2gray`

**Conversión de Color:**
- `rgb2gray`, `rgb2hsv`, `hsv2rgb`
- `rgb2lab`, `lab2rgb`
- `rgb2xyz`, `xyz2rgb`
- `xyz2lab`, `lab2xyz`

**Transformaciones Geométricas:**
- `imrotate`, `imresize`, `imcrop`, `imtranslate`
- `imwarp`, `fitgeotrans`

**Filtros:**
- `imfilter`, `medfilt2`, `ordfilt2`, `modefilt`
- `stdfilt`, `entropyfilt`, `rangefilt`, `fspecial`

**Morfología:**
- `strel`, `imdilate`, `imerode`, `imopen`, `imclose`

**Segmentación:**
- `imbinarize`, `graythresh`, `adaptthresh`, `im2bw`
- `edge`, `imgradient`

**Componentes Conectados:**
- `bwlabel`, `label2rgb`, `regionprops`

**Transformada de Hough:**
- `hough`, `houghpeaks`, `houghlines`
- `imfindcircles`, `viscircles`

**Transformada de Fourier:**
- `fft`, `ifft`, `fft2`, `ifft2`
- `fftshift`, `ifftshift`

**Restauración y Métricas:**
- `deconvwnr`, `immse`, `psnr`, `ssim`

**Ruido:**
- `imnoise`

**Utilidades:**
- `imsplit`, `non_overflowing_sum`

#### Características
- Compatibilidad sintáctica con MATLAB Image Processing Toolbox
- Sin dependencias pesadas (solo NumPy y Matplotlib)
- Código educativo y comprensible
- Documentación inline completa

#### Problemas Conocidos
- ⚠️ `bwlabel` con bug de fragmentación (corregido en v2.0)
- ⚠️ `regionprops` con propiedades geométricas limitadas (mejorado en v2.0)

---

## [Unreleased]

### En Desarrollo

Funciones planificadas para futuras versiones:

- `watershed` - Segmentación por watershed
- `imreconstruct` - Reconstrucción morfológica
- `bwmorph` - Operaciones morfológicas binarias adicionales
- `imregionalmax`/`imregionalmin` - Máximos/mínimos regionales
- `bwperim` - Perímetro de objetos binarios
- `bwarea` - Área de objetos binarios
- Más métodos de segmentación avanzada
- Soporte para procesamiento de video

---

## Notas de Versión

### Política de Versiones

Este proyecto sigue [Semantic Versioning](https://semver.org/):

- **MAJOR (X.0.0)**: Cambios incompatibles con versiones anteriores
- **MINOR (0.X.0)**: Nueva funcionalidad compatible con versiones anteriores
- **PATCH (0.0.X)**: Corrección de bugs compatible con versiones anteriores

### Soporte

- **v2.0.x**: Soporte activo con actualizaciones y correcciones
- **v1.0.x**: Soporte de seguridad únicamente (se recomienda actualizar a v2.0)

### Migración entre Versiones

Para migrar de v1.0 a v2.0, consulta la [Guía de Migración](MIGRATION_GUIDE.md).

### Contribuciones

Para reportar bugs o sugerir mejoras:
- 🐛 [Issues en GitHub](https://github.com/jacoperUTP/CV/issues)
- 📧 Email: jacoper@utp.edu.co

---

*Última actualización: 17 de Noviembre, 2025*
