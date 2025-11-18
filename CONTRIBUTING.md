# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a IP Functions! Este documento te guiará sobre cómo contribuir al proyecto.

---

## 📋 Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Proceso de Desarrollo](#proceso-de-desarrollo)
5. [Estándares de Código](#estándares-de-código)
6. [Testing](#testing)
7. [Documentación](#documentación)
8. [Pull Requests](#pull-requests)

---

## 📜 Código de Conducta

Este proyecto se adhiere a principios de respeto y colaboración profesional. Al participar, te comprometes a:

- Ser respetuoso con todos los colaboradores
- Aceptar críticas constructivas
- Enfocarse en lo mejor para la comunidad
- Mantener un ambiente inclusivo y educativo

---

## 🚀 ¿Cómo puedo contribuir?

### Reportar Bugs

Si encuentras un bug:

1. **Verifica** que no haya sido reportado en [Issues](https://github.com/jacoperUTP/CV/issues)
2. **Crea un nuevo issue** con:
   - Título descriptivo
   - Pasos para reproducir el bug
   - Comportamiento esperado vs. actual
   - Versión de Python e IP Functions
   - Código mínimo reproducible

**Ejemplo de reporte:**

```markdown
**Bug:** bwlabel no detecta correctamente objetos con conectividad 8

**Pasos para reproducir:**
1. Crear imagen binaria con objeto diagonal
2. Llamar `bwlabel(img, EE=8)`
3. Observar número de componentes

**Comportamiento esperado:** 1 componente
**Comportamiento actual:** 2 componentes

**Código reproducible:**
```python
import numpy as np
from ip_functions import bwlabel

test = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
], dtype=bool)

labels, num = bwlabel(test, EE=8)
print(f"Componentes: {num}")  # Actual: 3, Esperado: 1
```

**Entorno:**
- IP Functions v2.0.0
- Python 3.10.5
- NumPy 1.23.0
- OS: Windows 11
```

### Sugerir Mejoras

Para nuevas funciones o mejoras:

1. **Abre un issue** con etiqueta `enhancement`
2. **Explica:**
   - Qué función quieres agregar
   - Por qué sería útil
   - Cómo se usaría (ejemplo de código)
   - Equivalente en MATLAB (si aplica)

### Contribuir con Código

1. **Fork** el repositorio
2. **Crea una rama** para tu feature
3. **Desarrolla** siguiendo los estándares
4. **Haz commit** de tus cambios
5. **Push** a tu fork
6. **Crea un Pull Request**

---

## ⚙️ Configuración del Entorno

### 1. Fork y Clona

```bash
# Fork en GitHub (botón Fork)
# Luego clonar tu fork
git clone https://github.com/TU-USUARIO/CV.git
cd CV
```

### 2. Configurar Remote

```bash
# Agregar upstream (repositorio original)
git remote add upstream https://github.com/jacoperUTP/CV.git

# Verificar
git remote -v
```

### 3. Crear Entorno Virtual

```bash
# Crear entorno
python -m venv venv

# Activar
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 4. Instalar en Modo Desarrollo

```bash
# Instalar con dependencias de desarrollo
pip install -e ".[dev]"

# O manualmente
pip install -e .
pip install pytest pillow scipy
```

### 5. Verificar Instalación

```python
import ip_functions
print(ip_functions.__file__)

# Test rápido
from ip_functions import bwlabel
import numpy as np

test = np.ones((3, 3), dtype=bool)
labels, num = bwlabel(test, EE=8)
print(f"✅ Test pasado: {num} componente(s)")
```

---

## 🔄 Proceso de Desarrollo

### 1. Crear Rama para Feature

```bash
# Asegurar que estás actualizado
git checkout main
git pull upstream main

# Crear nueva rama
git checkout -b feature/nombre-descriptivo
```

**Nombres de rama:**
- `feature/nueva-funcion` - Nueva funcionalidad
- `bugfix/corregir-bug` - Corrección de bug
- `docs/mejorar-readme` - Documentación
- `refactor/optimizar-codigo` - Refactorización

### 2. Desarrollar

```bash
# Hacer cambios
# Probar frecuentemente
python test_mi_funcion.py

# Ver cambios
git status
git diff
```

### 3. Commit

```bash
# Agregar archivos
git add ip_functions.py

# Commit con mensaje descriptivo
git commit -m "Add watershed segmentation function

- Implement watershed algorithm for image segmentation
- Add tests for watershed function
- Update documentation with watershed example"
```

### 4. Push

```bash
# Subir rama a tu fork
git push origin feature/nombre-descriptivo
```

### 5. Pull Request

1. Ir a tu fork en GitHub
2. Click "Compare & pull request"
3. Llenar template de PR (ver abajo)
4. Click "Create pull request"

---

## 📝 Estándares de Código

### Estilo de Código

Seguimos estilo similar a MATLAB para mantener compatibilidad:

```python
# ✅ BIEN - Estilo MATLAB-compatible
def imfilter(I, kernel, mode='same', boundary='replicate'):
    """
    Filter image using convolution.
    
    Parameters
    ----------
    I : ndarray
        Input image
    kernel : ndarray
        Filter kernel
    mode : str, optional
        Output size ('same', 'valid', 'full')
    boundary : str, optional
        Boundary handling ('replicate', 'symmetric', 'circular')
    
    Returns
    -------
    filtered : ndarray
        Filtered image
        
    Examples
    --------
    >>> kernel = fspecial('gaussian', [5, 5], 1.0)
    >>> filtered = imfilter(I, kernel)
    """
    # Implementación...
    pass
```

### Convenciones de Nombres

- **Funciones:** `lowercase_with_underscores` o `matlabstyle` (mantener nombres MATLAB)
- **Variables:** `descriptive_names`
- **Constantes:** `UPPER_CASE`
- **Clases:** `PascalCase` (si es necesario)

### Docstrings

Todas las funciones públicas deben tener docstrings siguiendo formato NumPy:

```python
def nombre_funcion(parametro1, parametro2):
    """
    Breve descripción en una línea.
    
    Descripción más detallada si es necesaria.
    Explicar qué hace la función, no cómo.
    
    Parameters
    ----------
    parametro1 : tipo
        Descripción del parámetro
    parametro2 : tipo, optional
        Descripción del parámetro opcional
    
    Returns
    -------
    nombre_retorno : tipo
        Descripción de lo que retorna
    
    Raises
    ------
    ValueError
        Cuándo se lanza esta excepción
    
    See Also
    --------
    otra_funcion : Función relacionada
    
    Notes
    -----
    Notas adicionales, ecuaciones, algoritmo usado
    
    References
    ----------
    .. [1] Referencia si aplica
    
    Examples
    --------
    >>> import numpy as np
    >>> resultado = nombre_funcion(param1, param2)
    >>> print(resultado)
    """
    pass
```

### Type Hints (opcional pero recomendado)

```python
from typing import Tuple, Optional
import numpy as np
from numpy.typing import NDArray

def bwlabel(
    BW: NDArray[np.bool_],
    EE: int = 8
) -> Tuple[NDArray[np.int32], int]:
    """
    Label connected components in binary image.
    """
    pass
```

---

## 🧪 Testing

### Escribir Tests

Cada nueva función debe incluir tests:

```python
# En archivo test_nueva_funcion.py
import numpy as np
from ip_functions import nueva_funcion

def test_nueva_funcion_basico():
    """Test basic functionality"""
    input_img = np.array([[1, 2], [3, 4]])
    resultado = nueva_funcion(input_img)
    esperado = np.array([[2, 4], [6, 8]])
    np.testing.assert_array_equal(resultado, esperado)

def test_nueva_funcion_tipos():
    """Test different data types"""
    # Test con float
    img_float = np.array([[1.5, 2.5]], dtype=float)
    resultado = nueva_funcion(img_float)
    assert resultado.dtype == float
    
    # Test con uint8
    img_uint8 = np.array([[100, 200]], dtype=np.uint8)
    resultado = nueva_funcion(img_uint8)
    assert resultado.dtype == np.uint8

def test_nueva_funcion_casos_borde():
    """Test edge cases"""
    # Imagen vacía
    empty = np.array([])
    resultado = nueva_funcion(empty)
    assert resultado.size == 0
    
    # Imagen 1x1
    single = np.array([[5]])
    resultado = nueva_funcion(single)
    assert resultado.shape == (1, 1)

def test_nueva_funcion_errores():
    """Test error handling"""
    import pytest
    
    # Debe lanzar ValueError con input inválido
    with pytest.raises(ValueError):
        nueva_funcion(None)
```

### Ejecutar Tests

```bash
# Instalar pytest si no lo tienes
pip install pytest

# Ejecutar todos los tests
pytest

# Ejecutar test específico
pytest test_nueva_funcion.py

# Con verbose
pytest -v

# Con coverage
pip install pytest-cov
pytest --cov=ip_functions
```

### Tests de Comparación con MATLAB

Si agregas funciones compatibles con MATLAB, incluye tests de comparación:

```python
def test_comparacion_matlab():
    """Compare results with MATLAB reference"""
    # Cargar resultado de MATLAB guardado
    import scipy.io
    matlab_result = scipy.io.loadmat('test_data/matlab_output.mat')
    
    # Generar resultado con IP Functions
    python_result = nueva_funcion(input_data)
    
    # Comparar (con tolerancia para diferencias numéricas)
    np.testing.assert_allclose(
        python_result, 
        matlab_result['output'],
        rtol=1e-5,
        atol=1e-8
    )
```

---

## 📚 Documentación

### Actualizar README

Si agregas funciones nuevas, actualiza:

1. **README.md** - Lista de funciones
2. **CHANGELOG.md** - Agregar a sección [Unreleased]
3. **setup.py** - Actualizar long_description si es relevante

### Ejemplos

Incluye al menos un ejemplo de uso:

```python
# En docstring de la función
Examples
--------
>>> from ip_functions import nueva_funcion
>>> import numpy as np
>>> I = np.random.rand(100, 100)
>>> resultado = nueva_funcion(I, parametro=5)
>>> print(resultado.shape)
(100, 100)
```

### Agregar a Ejemplos

Si tu función es significativa, considera agregar un script en `examples/`:

```python
# examples/demo_nueva_funcion.py
"""
Demostración de nueva_funcion
==============================

Este ejemplo muestra cómo usar nueva_funcion para [objetivo].
"""

from ip_functions import nueva_funcion, imread, imshow
import matplotlib.pyplot as plt

# Cargar imagen
I = imread('ejemplo.jpg')

# Aplicar función
resultado = nueva_funcion(I, parametros)

# Visualizar
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(I)
axes[0].set_title('Original')
axes[1].imshow(resultado)
axes[1].set_title('Resultado')
plt.show()
```

---

## 🔀 Pull Requests

### Template de PR

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva función (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que puede romper código existente)
- [ ] Documentación

## ¿Cómo ha sido probado?
Describe las pruebas realizadas:
- [ ] Tests unitarios agregados
- [ ] Tests manuales realizados
- [ ] Comparación con MATLAB

## Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado mi código, especialmente en partes difíciles
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban mi fix o feature
- [ ] Tests nuevos y existentes pasan localmente
- [ ] He actualizado CHANGELOG.md

## Código de ejemplo
```python
# Ejemplo de cómo usar la nueva funcionalidad
from ip_functions import nueva_funcion
resultado = nueva_funcion(input)
```

## Screenshots (si aplica)
Agregar imágenes mostrando antes/después

## Issues relacionados
Fixes #123
Related to #456
```

### Proceso de Revisión

1. **Automated checks** se ejecutan automáticamente
2. **Maintainer review** - Uno de los mantenedores revisará
3. **Feedback** - Se pueden solicitar cambios
4. **Approval** - Una vez aprobado, se hará merge

### Responder a Feedback

```bash
# Hacer cambios solicitados
git add archivos_modificados
git commit -m "Implement requested changes"

# Push actualiza automáticamente el PR
git push origin feature/tu-rama
```

---

## 🎯 Áreas de Contribución Prioritarias

Estamos buscando ayuda especialmente en:

### 1. Funciones Faltantes

- `watershed` - Segmentación watershed
- `imreconstruct` - Reconstrucción morfológica
- `bwmorph` - Operaciones morfológicas adicionales
- `imregionalmax`/`min` - Máximos/mínimos regionales

### 2. Mejoras de Rendimiento

- Optimizar funciones lentas
- Agregar soporte para procesamiento paralelo
- Usar Numba/Cython donde sea apropiado

### 3. Compatibilidad

- Verificar compatibilidad con MATLAB
- Agregar tests de comparación
- Documentar diferencias

### 4. Documentación

- Mejorar ejemplos
- Agregar tutoriales
- Traducir a inglés

### 5. Testing

- Aumentar cobertura de tests
- Agregar tests de casos borde
- Tests de integración

---

## 📧 Contacto

¿Tienes preguntas? Contacta:

- **Issues:** https://github.com/jacoperUTP/CV/issues
- **Email:** jacoper@utp.edu.co
- **Discusiones:** https://github.com/jacoperUTP/CV/discussions

---

## 🙏 Agradecimientos

¡Gracias por contribuir a IP Functions! Tu ayuda hace que este proyecto sea mejor para toda la comunidad educativa.

### Contribuidores

Una lista de contribuidores está disponible en:
https://github.com/jacoperUTP/CV/graphs/contributors

---

*Última actualización: Noviembre 2025*
