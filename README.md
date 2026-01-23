# IP Functions - Librería de Procesamiento de Imágenes 🖼️

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.2-green.svg)](https://github.com/jacoperUTP/CV/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MATLAB Compatible](https://img.shields.io/badge/MATLAB-compatible-orange.svg)](https://www.mathworks.com/products/image.html)

**Librería integral de procesamiento de imágenes en Python, diseñada para replicar la funcionalidad y sintaxis del Image Processing Toolbox de MATLAB con fines educativos y de investigación.**

Desarrollada por el **Grupo de Investigación en Robótica Aplicada** de la **Universidad Tecnológica de Pereira**, esta herramienta facilita la migración de algoritmos clásicos a entornos Python/NumPy sin perder la claridad didáctica.

---

## 🎯 Características Principales

- **Sintaxis MATLAB-like**: Diseñada para que la transición de código `m` a `py` sea casi directa.
- **Sin cajas negras**: Implementaciones abiertas y legibles (NumPy + Matplotlib).
- **Tomografía Computarizada**: Soporte completo para Proyecciones (Radon) y Retroproyección Filtrada (Inverse Radon).
- **Morfología y Análisis**: Herramientas robustas para segmentación, etiquetado y descripción de formas.
- **Documentación integrada**: Docstrings detallados en español con ejemplos ejecutables.

---

## ⭐ Novedades en v2.0.2 (Enero 2026)

### 1) Tomografía y Reconstrucción (CT)
Se incorporan herramientas fundamentales para el procesamiento de imágenes médicas y reconstrucción:
- **`radon`**: Transformada de Radon para generar sinogramas (proyecciones).
- **`iradon`**: Transformada inversa de Radon mediante Retroproyección Filtrada (FBP), con filtros 'Ram-Lak'.

### 2) Dibujo y Anotación
- **`insertShape`**: Permite dibujar primitivas geométricas (círculos, rectángulos, elipses, líneas, polígonos) directamente sobre la matriz de imagen, útil para generar *Ground Truth* o visualizar detecciones.

### 3) Descriptores de Forma
- **`invmoments`**: Cálculo de los 7 momentos invariantes de Hu, esenciales para el reconocimiento de patrones independiente de escala, rotación y traslación.

### 4) Mejoras de Estabilidad
- Actualización de metadatos y validación de tipos en funciones de transformación geométrica.

---

## 📦 Instalación

### Desde Repositorio (Recomendado)

```bash
pip install git+[https://github.com/jacoperUTP/Image-Processing-Funtions-.git](https://github.com/jacoperUTP/Image-Processing-Funtions-.git)

