╔══════════════════════════════════════════════════════════════════════╗
║              GUIA DE ACTUALIZACION - IP_FUNCTIONS v2.0               ║
╚══════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│ PASO 1: UBICAR TU PROYECTO                                           │
└──────────────────────────────────────────────────────────────────────┘

Tu estructura actual:
    G:\Mi unidad\image_processing_UTP\flask_server\Ip_functions_installer\
    ├── ip_functions.py          ← TU ARCHIVO
    ├── setup.py                 ← REEMPLAZAR CON NUEVO
    └── README.md (opcional)     ← AGREGAR


┌──────────────────────────────────────────────────────────────────────┐
│ PASO 2: REEMPLAZAR ARCHIVOS                                          │
└──────────────────────────────────────────────────────────────────────┘

1. BACKUP (por seguridad):
   - Copiar tu setup.py actual a setup.py.old

2. DESCARGAR los archivos nuevos de la carpeta outputs:
   - setup.py              → Versión actualizada
   - README_PROYECTO.md    → Documentación completa

3. COPIAR al directorio Ip_functions_installer:
   - setup.py              → Reemplazar el actual
   - README_PROYECTO.md    → Renombrar a README.md


┌──────────────────────────────────────────────────────────────────────┐
│ PASO 3: VERIFICAR ip_functions.py                                    │
└──────────────────────────────────────────────────────────────────────┘

Tu archivo ip_functions.py YA TIENE la versión corregida de bwlabel.
Verificación rápida:

Busca en ip_functions.py la línea:
    union(min_label, lbl, parent)

Si existe → ✅ Ya está corregido (no necesitas cambiar nada)
Si NO existe → ⚠️ Reemplazar función bwlabel con la de bwlabel_limpio.py


┌──────────────────────────────────────────────────────────────────────┐
│ PASO 4: REINSTALAR EL PAQUETE                                        │
└──────────────────────────────────────────────────────────────────────┘

OPCIÓN A - Desde Terminal/CMD (RECOMENDADO):

    1. Abrir terminal (CMD, PowerShell, o Git Bash)
    
    2. Navegar al directorio:
       cd "G:\Mi unidad\image_processing_UTP\flask_server\Ip_functions_installer"
    
    3. Desinstalar versión anterior (opcional):
       pip uninstall ip_functions -y
    
    4. Instalar nueva versión:
       pip install -e .
    
    ⚠️ IMPORTANTE: El punto "." al final es necesario


OPCIÓN B - Desde Python (alternativa):

    import subprocess
    import os
    
    os.chdir(r"G:\Mi unidad\image_processing_UTP\flask_server\Ip_functions_installer")
    subprocess.run(["pip", "uninstall", "ip_functions", "-y"])
    subprocess.run(["pip", "install", "-e", "."])


┌──────────────────────────────────────────────────────────────────────┐
│ PASO 5: VERIFICAR INSTALACIÓN                                        │
└──────────────────────────────────────────────────────────────────────┘

Ejecutar en Python:

    import ip_functions
    print(ip_functions.__file__)
    # Debe mostrar la ruta correcta
    
    from ip_functions import bwlabel
    import numpy as np
    
    # Test rápido
    test = np.array([
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1]
    ], dtype=bool)
    
    labels, num = bwlabel(test, EE=4)
    print(f"Componentes: {num}")  # Debe ser 1
    
    if num == 1:
        print("✅ Versión 2.0 instalada correctamente!")
    else:
        print("⚠️ Verificar instalación")


┌──────────────────────────────────────────────────────────────────────┐
│ PASO 6: ACTUALIZAR TUS SCRIPTS (opcional)                            │
└──────────────────────────────────────────────────────────────────────┘

Tus scripts existentes NO necesitan cambios.
La nueva versión mantiene compatibilidad total.

Sin embargo, ahora puedes aprovechar mejoras:

    # regionprops con más propiedades
    props = regionprops(labels, properties=[
        'Area', 'Centroid', 'BoundingBox',
        'Perimeter', 'Eccentricity', 'Orientation',
        'MajorAxisLength', 'MinorAxisLength',
        'ConvexArea', 'ConvexHull', 'Solidity'
    ])


╔══════════════════════════════════════════════════════════════════════╗
║                    CAMBIOS EN LA VERSIÓN 2.0                          ║
╚══════════════════════════════════════════════════════════════════════╝

✅ bwlabel CORREGIDO
   - Union-Find apropiado
   - Sin fragmentación de objetos conectados
   - Más robusto y confiable

✅ regionprops MEJORADO
   - Perimeter calculado correctamente (chain code)
   - ConvexHull, ConvexArea, Solidity
   - Eccentricity, Orientation
   - MajorAxisLength, MinorAxisLength

✅ setup.py ACTUALIZADO
   - Versión 2.0.0
   - Documentación completa
   - Lista de funciones actualizada
   - Clasificadores mejorados


╔══════════════════════════════════════════════════════════════════════╗
║                      SOLUCIÓN DE PROBLEMAS                            ║
╚══════════════════════════════════════════════════════════════════════╝

PROBLEMA: "SyntaxError: invalid syntax" al hacer pip install

CAUSA: Ejecutaste pip en el intérprete de Python (>>>)

SOLUCIÓN: Ejecutar en la TERMINAL, NO en Python:
    # Terminal/CMD
    cd "G:\Mi unidad\image_processing_UTP\flask_server\Ip_functions_installer"
    pip install -e .

─────────────────────────────────────────────────────────────────────

PROBLEMA: "ModuleNotFoundError: No module named 'ip_functions'"

SOLUCIÓN 1 - Verificar instalación:
    pip show ip_functions

SOLUCIÓN 2 - Reinstalar:
    cd "ruta\a\Ip_functions_installer"
    pip install -e . --force-reinstall

─────────────────────────────────────────────────────────────────────

PROBLEMA: "bwlabel sigue fragmentando objetos"

CAUSA: Versión antigua aún cargada en memoria

SOLUCIÓN: Reiniciar Python o kernel de Jupyter:
    # En Jupyter
    Kernel → Restart
    
    # En Python
    exit()  # Cerrar y abrir nuevamente

─────────────────────────────────────────────────────────────────────

PROBLEMA: No sé dónde está instalado ip_functions

SOLUCIÓN:
    import ip_functions
    print(ip_functions.__file__)
    # Te muestra la ruta exacta


╔══════════════════════════════════════════════════════════════════════╗
║                         ARCHIVOS ENTREGADOS                                               ║
╚══════════════════════════════════════════════════════════════════════╝

📄 setup.py                  → Archivo de instalación actualizado v2.0
📄 README_PROYECTO.md         → Documentación completa del proyecto
📄 bwlabel_limpio.py         → Función bwlabel corregida (si necesitas)
📄 resultado_herramientas.png → Prueba con tu imagen
📄 GUIA_ACTUALIZACION.txt    → Este archivo


╔══════════════════════════════════════════════════════════════════════╗
║                           CONTACTO                                                        ║
╚══════════════════════════════════════════════════════════════════════╝

Universidad Tecnológica de Pereira
Email: jacoper@utp.edu.co

