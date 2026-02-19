#19/febrero/2026 7:20am Colombia


__version__ = "2.0.3"          # Actualizar
__author__  = "Jimy Alexander Cortés-Osorio, Francisco Alejandro Medina-Aguirre,  UTP"
__date__    = "2026-02-03"     # Fecha de la última edición

def version():
    """
    Retorna metadatos básicos para verificar qué versión está cargada.
    """
    import inspect
    return {
        "module": __name__,
        "version": __version__,
        "file": inspect.getfile(inspect.currentframe())
    }


import numpy as np
import random
import matplotlib as mpl
from matplotlib import pyplot as plt, image as mpimg, transforms as mtransforms
from matplotlib.patches import Rectangle, Ellipse, Polygon
from matplotlib.lines import Line2D
from matplotlib.path import Path  # Necesario para roipoly



# ====================================================================
#  Entrada / Salida
# ====================================================================

def imread(filename):
    """
    Lee una imagen desde disco (similar a MATLAB imread).

    Parámetros
    ----------
    filename : str
        Parámetro filename.

    Retorna
    -------
    out : ndarray
        Resultado de imread.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imread(filename)
    """
    I = mpimg.imread(filename)
    # Normalizar a [0,255] si está en float (como PNG en matplotlib)
    if I.dtype == np.float32 or I.dtype == np.float64:
        if I.max() <= 1.0:
            I = (I * 255).astype(np.uint8)
    return I

def imwrite(I, filename, cmap=None):
    """
    Escribe una imagen en disco (similar a MATLAB imwrite).

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    filename : str
        Parámetro filename.
    cmap : objeto
        Parámetro cmap.

    Retorna
    -------
    out : None
        Resultado de imwrite.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imwrite(I, filename, cmap)
    """
    if I.dtype != np.uint8:
        I = np.clip(I, 0, 255).astype(np.uint8)
    plt.imsave(filename, I, cmap=cmap if cmap else None)

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

def imshow(I, *args, show=True):
    """
    Muestra una imagen usando Matplotlib (sintaxis tipo MATLAB).
    Ahora retorna el 'mappable' (handle) para poder usar colorbar().
    """

    if not isinstance(I, np.ndarray):
        I = np.array(I)

    display_range = None
    cmap = None
    xdata = None
    ydata = None

    args_list = list(args)
    i = 0
    while i < len(args_list):
        a = args_list[i]

        if isinstance(a, (list, tuple, np.ndarray)) and not isinstance(a, str):
            arr = np.asarray(a)
            if arr.size == 0:
                display_range = 'auto'
            elif arr.size == 2:
                display_range = [float(arr.ravel()[0]), float(arr.ravel()[1])]
            i += 1
            continue

        if isinstance(a, str):
            key = a.strip().lower()
            if key in ['xdata', 'ydata'] and (i + 1) < len(args_list):
                val = args_list[i + 1]
                if key == 'xdata':
                    xdata = np.asarray(val, dtype=float).ravel()
                else:
                    ydata = np.asarray(val, dtype=float).ravel()
                i += 2
                continue

            if key == 'initialmagnification' and (i + 1) < len(args_list):
                i += 2
                continue

            cmap = a
            i += 1
            continue

        i += 1

    # CASO 1: RGB
    if I.ndim == 3 and I.shape[2] in [3, 4]:
        if I.dtype == np.uint8:
            I_display = I.astype(np.float32) / 255.0
        elif I.dtype in [np.float32, np.float64]:
            I_display = I / 255.0 if I.max() > 1.0 else I
        else:
            I_display = I

        h = plt.imshow(np.clip(I_display, 0, 1))
        plt.axis('off')
        if show:
            plt.show()
        return h

    # CASO 2: 2D
    if I.ndim == 2:
        es_binaria = (I.dtype == bool) or (np.array_equal(I, I.astype(bool)))
        if cmap is None:
            cmap = 'gray'

        if display_range is None:
            if es_binaria:
                vmin, vmax = 0, 1
            elif I.dtype == np.uint8:
                vmin, vmax = 0, 255
            elif I.dtype in [np.float32, np.float64]:
                vmin, vmax = (0.0, 1.0) if I.max() <= 1.0 else (float(I.min()), float(I.max()))
            else:
                vmin, vmax = float(I.min()), float(I.max())
        elif display_range == 'auto':
            vmin, vmax = float(I.min()), float(I.max())
        else:
            vmin, vmax = float(display_range[0]), float(display_range[1])

        use_extent = (xdata is not None) or (ydata is not None)
        if use_extent:
            if xdata is None:
                xdata = np.arange(I.shape[1], dtype=float)
            if ydata is None:
                ydata = np.arange(I.shape[0], dtype=float)

            extent = [float(xdata[0]), float(xdata[-1]), float(ydata[0]), float(ydata[-1])]
            h = plt.imshow(I, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto', extent=extent, origin='upper')
            plt.axis('on')
        else:
            h = plt.imshow(I, cmap=cmap, vmin=vmin, vmax=vmax)
            plt.axis('off')

        if show:
            plt.show()
        return h

    raise ValueError(f"Dimensiones {I.shape} no soportadas")


# ====================================================================
#  Ajuste y Mejora de Intensidad
# ====================================================================

def mat2gray(I, limits=None):
    """
    Normaliza una matriz de imagen al rango [0,1].

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    limits : objeto
        Parámetro limits.

    Retorna
    -------
    out : objeto
        Resultado de mat2gray.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = mat2gray(I, limits)
    """
    I = np.asarray(I, dtype=np.float64)
    
    if limits is None:
        I_min, I_max = I.min(), I.max()
    else:
        I_min, I_max = float(limits[0]), float(limits[1])
    
    if I_max > I_min:
        return (I - I_min) / (I_max - I_min)
    else:
        return np.zeros_like(I, dtype=np.float64)

#---------------------------------------------------------------------------
def imhist(r, ax=None, ver=True):
    """
    Calcula o grafica el histograma de una imagen de 8 bits.

    Parámetros
    ----------
    r : objeto
        Parámetro r.
    ax : matplotlib.axes.Axes
        Parámetro ax.
    ver : objeto
        Parámetro ver.

    Retorna
    -------
    out : ndarray or None
        Resultado de imhist.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imhist(r, ax, ver)
    """
    h = np.zeros([256, 1])
    i, j = r.shape
    for x in range(i):
        for y in range(j):
            h[r[x, y]] += 1
    
    if ver:
        x = range(256)
        hbar = np.reshape(h, 256)
        if ax is None:
            ax = plt.gca()
        ax.bar(x, hbar)
        norm = mpl.colors.Normalize(vmin=0, vmax=255)
        escala = plt.cm.ScalarMappable(cmap='gray', norm=norm)
        escala.set_array([])
        plt.colorbar(escala, ax=ax, orientation="horizontal", ticks=[0, 50, 100, 150, 200, 255])
        ax.set_xlabel("Intensidades")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Histograma")
        ax.set_xlim(0, 255)
        ax.set_ylim(0, np.amax(h) * 0.3)
        ax.grid(True)
    else:
        return h
    


               
              
def stretchlim(I,Tol=0.01):
    """
    Estima límites de estiramiento de intensidad.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    Tol : objeto
        Parámetro Tol.

    Retorna
    -------
    out : objeto
        Resultado de stretchlim.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = stretchlim(I, Tol)
    """
    
    Em=0
    EM=255
    h=imhist(I,None,False)
    i,j=np.shape(I)
    ha=np.zeros([256,1])
    hp=np.zeros([256,1])
    L=256
    for k in range(L):
        ha[k]=np.sum(h[0:k+1])
        hp[k]=ha[k]/(i*j)
        if hp[k]<=Tol:
             Em=k
        if hp[k]<=1-Tol:
             EM=k              
    return Em/255,EM/255    
    

def imadjust(I,E,S=(0,1),n=1):
    """
    Ajusta la intensidad de una imagen al estilo MATLAB imadjust.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    E : objeto
        Parámetro E.
    S : objeto
        Parámetro S.
    1) : objeto
        Parámetro 1).
    n : objeto
        Parámetro n.

    Retorna
    -------
    out : objeto
        Resultado de imadjust.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imadjust(I, E, S, 1), n)
    """
    Em=E[0]*255
    EM=E[1]*255
    Sm=S[0]*255
    SM=S[1]*255
    I=np.float16(I)
    Is=((SM-Sm)/(EM-Em)**n)*(np.absolute(I-Em))**n+Sm
    #Ajusta el overflow de los valores
    Is[np.where(Is>255)] = 255
    return np.uint8(Is)
        
        
  
  
def histeq(I, hR=None):
    """
    Realiza ecualización o especificación de histograma.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    hR : objeto
        Parámetro hR.

    Retorna
    -------
    out : objeto
        Resultado de histeq.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = histeq(I, hR)
    """
        # Determinar el histograma de la imagen de entrada I
    hI= imhist(I,None,False)
        
        # Calcula la CDF de la imagen de entrada I
    cdfI = np.cumsum(hI) / np.sum(hI)
        
    if hR is None:
        # Se realiza la ecualización normal
        LUT = np.uint8(255 * cdfI)
    else:
        # Se hace la especificación del histograma
        # Calcula la CDF de la imagen de referencia
        cdfR = np.cumsum(hR) / np.sum(hR)
            
        # Tabla de búsqueda (LUT) por proximidad
        LUT = np.zeros(256, dtype=np.uint8)
        for idx in range(256):
            minIndex = np.argmin(np.abs(cdfR - cdfI[idx]))
            LUT[idx] = minIndex  # Se indexa desde 0
        
        # Aplica la LUT a toda la imagen de entrada usando indexación directa
    S = LUT[I]
        
    return S
  
    
    
    
def imcomplement(I):
    """
    Calcula el complemento de la imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : objeto
        Resultado de imcomplement.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imcomplement(I)
    """
    if I.dtype == np.bool_:
        return ~I
    if np.issubdtype(I.dtype, np.floating):
        return 1.0 - I
    if I.dtype == np.uint8:
        return 255 - I
    # Caso general: usar rango máximo del tipo
    info = np.iinfo(I.dtype)
    return info.max - I




# ====================================================================
#  Conversión de Espacios de Color
# ====================================================================

def imsplit(I):
    """
    Separa una imagen RGB en sus tres canales.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : objeto
        Resultado de imsplit.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imsplit(I)
    """
    r=np.array(I[:,:,0])
    g=np.array(I[:,:,1])
    b=np.array(I[:,:,2])
    return r,g,b



def rgb2gray(RGB):
    """
    Convierte una imagen RGB a escala de grises.

    Parámetros
    ----------
    RGB : ndarray
        Parámetro RGB.

    Retorna
    -------
    out : objeto
        Resultado de rgb2gray.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = rgb2gray(RGB)
    """
    r,g,b=imsplit(RGB)
    gris=np.uint8(0.299*np.double(r)+0.587*np.double(g)+0.114*np.double(b))
    return gris

def rgb2hsv(I):
    """
    Convierte una imagen RGB a espacio HSV.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : objeto
        Resultado de rgb2hsv.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = rgb2hsv(I)
    """
    I=I/255
    r,g,b=imsplit(I)
    [fil,col,pro]=np.shape(I)
    Cmax=np.zeros((fil,col))
    Cmin=np.zeros((fil,col))
    d=np.zeros((fil,col))
    H=np.zeros((fil,col))
    S=np.zeros((fil,col))
    V=np.zeros((fil,col))
    for i in range(fil):
        for j in range(col):
            maximo=max([r[i,j],g[i,j],b[i,j]])
            minimo=min([r[i,j],g[i,j],b[i,j]])
            Cmax[i,j]=maximo
            Cmin[i,j]=minimo
            d[i,j]=maximo-minimo
            if d[i,j]==0:
                H[i,j]=0
            elif maximo==r[i,j]:
                H[i,j]=60*(((g[i,j]-b[i,j])/d[i,j])%6)
            elif maximo==g[i,j]:
                H[i,j]=60*(((g[i,j]-b[i,j])/d[i,j])+2)
            elif maximo==b[i,j]:
                H[i,j]=60*(((g[i,j]-b[i,j])/d[i,j])+4)
            if maximo==0:
                S[i,j]=0
            else:
                S[i,j]=d[i,j]/maximo
            V[i,j]=maximo
    H=H/360.0
    hsv=np.dstack((H,S,V))
    return hsv





def hsv2rgb(H):
    """
    Convierte una imagen HSV a espacio RGB.

    Parámetros
    ----------
    H : ndarray
        Parámetro H.

    Retorna
    -------
    out : objeto
        Resultado de hsv2rgb.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = hsv2rgb(H)
    """
    h,s,v=imsplit(H)
    N,M,L=np.shape(H)
    X=np.zeros((N,M))
    m=np.zeros((N,M))
    r=np.zeros((N,M))
    g=np.zeros((N,M))
    b=np.zeros((N,M))
    h=h*360
    C=np.zeros((N,M)) #s*v
    for i in range(N):
      for j in range(M):
        C[i,j]=v[i,j]*s[i,j]
        X[i,j]=C[i,j]*(1-abs((h[i,j]/60)%2-1))
        m[i,j]=v[i,j]-C[i,j]
        if 0<=h[i,j] and h[i,j]<60:
          r[i,j],g[i,j],b[i,j]=C[i,j],X[i,j],0
        elif 60<=h[i,j] and h[i,j]<120:
          r[i,j],g[i,j],b[i,j]=X[i,j],C[i,j],0
        elif 120<=h[i,j] and h[i,j]<180:
          r[i,j],g[i,j],b[i,j]=0,C[i,j],X[i,j]
        elif 180<=h[i,j] and h[i,j]<240:
          r[i,j],g[i,j],b[i,j]=0,X[i,j],C[i,j]
        elif 240<=h[i,j] and h[i,j]<300:
          r[i,j],g[i,j],b[i,j]=X[i,j],0,C[i,j]
        elif 300<=h[i,j] and h[i,j]<360:
          r[i,j],g[i,j],b[i,j]=C[i,j],0,X[i,j]
    R,G,B=255*(r+m),255*(g+m),255*(b+m)
    RGB=np.dstack((R,G,B))
    RGB=np.uint8(RGB)
    return RGB
  
  
def rgb2lab(RGB):
    """
    Convierte una imagen RGB al espacio CIELAB.

    Parámetros
    ----------
    RGB : ndarray
        Parámetro RGB.

    Retorna
    -------
    out : objeto
        Resultado de rgb2lab.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = rgb2lab(RGB)
    """
    F, C, L = np.shape(RGB)
    if L != 3:
        raise ValueError('rgb2lab: La imagen debe ser MxNx3')
    
    xyz = rgb2xyz(RGB)
    CIEL = xyz2lab(xyz)
    
    return CIEL
    
def lab2rgb(LAB):
    """
    Convierte una imagen CIELAB al espacio RGB.

    Parámetros
    ----------
    LAB : ndarray
        Parámetro LAB.

    Retorna
    -------
    out : objeto
        Resultado de lab2rgb.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = lab2rgb(LAB)
    """
    # Verificar si la entrada es una matriz MxNx3
    F, C, L = np.shape(LAB)
    if L != 3:
        raise ValueError('lab2rgb: La imagen debe ser MxNx3')
    
    # Paso 1: Convertir de LAB a XYZ
    xyz = lab2xyz(LAB)
    
    # Paso 2: Convertir de XYZ a RGB
    RGB = xyz2rgb(xyz)
    
    return RGB


def rgb2xyz(RGB):
    """
    Convierte una imagen RGB al espacio de color CIE XYZ.

    Parámetros
    ----------
    RGB : ndarray
        Parámetro RGB.

    Retorna
    -------
    out : objeto
        Resultado de rgb2xyz.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = rgb2xyz(RGB)
    """
    F, C, L = RGB.shape
    if L != 3:
        raise ValueError('rgb2xyz: La imagen debe ser MxNx3')
    
    if RGB.dtype == np.uint8:
        RGB = RGB.astype(np.float64)
        div = 255
    else:
        div = 1
    
    sR = RGB[:,:,0]
    sG = RGB[:,:,1]
    sB = RGB[:,:,2]
    
    var_R = sR / div
    var_G = sG / div
    var_B = sB / div
    
    def evaluar(x):
        return np.where(x > 0.04045, ((x + 0.055) / 1.055) ** 2.4, x / 12.92)
    
    var_R = evaluar(var_R)
    var_G = evaluar(var_G)
    var_B = evaluar(var_B)
    
    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])
    
    XYZ = np.zeros((F, C, L))
    
    for i in range(F):
        for j in range(C):
            var_RGB = M @ np.array([var_R[i,j], var_G[i,j], var_B[i,j]])
            XYZ[i,j,:] = var_RGB
    
    return XYZ
    


def xyz2rgb(XYZ):
    """
    Convierte una imagen XYZ al espacio RGB sRGB.

    Parámetros
    ----------
    XYZ : ndarray
        Parámetro XYZ.

    Retorna
    -------
    out : objeto
        Resultado de xyz2rgb.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = xyz2rgb(XYZ)
    """
    # Asegurarse de que el último eje tenga tamaño 3
    if XYZ.shape[-1] != 3:
        raise ValueError("El último eje debe tener tamaño 3 (X, Y, Z)")

    def evaluar(x):
        return np.where(x > 0.0031308,
                        1.055 * np.power(np.maximum(x, 0), 1 / 2.4) - 0.055,
                        12.92 * x)

    M = np.array([
        [ 3.2404542, -1.5371385, -0.4985314],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0556434, -0.2040259,  1.0572252]
    ])

    var_RGB = np.dot(XYZ, M.T)
    var_RGB = np.clip(var_RGB, 0, None)  # Asegura que no haya valores negativos

    RGB = evaluar(var_RGB)
    RGB = (RGB * 255).astype(np.uint8)

    return RGB

    
    

def xyz2lab(myXYZ):
    """
    Convierte una imagen XYZ al espacio CIELAB.

    Parámetros
    ----------
    myXYZ : ndarray
        Parámetro myXYZ.

    Retorna
    -------
    out : objeto
        Resultado de xyz2lab.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = xyz2lab(myXYZ)
    """
    F, C, L = myXYZ.shape
    if L != 3:
        raise ValueError('xyz2lab: La imagen debe ser MxNx3')
    
    X = myXYZ[:,:,0]
    Y = myXYZ[:,:,1]
    Z = myXYZ[:,:,2]
    
    CIELAB = np.zeros((F, C, L))
    CIEL = np.zeros((F, C))
    CIEa = np.zeros((F, C))
    CIEb = np.zeros((F, C))
    
    # D65
    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])
    
    Reference = M @ np.array([100, 100, 100])  # Respecto a 100 en D65
    ReferenceX, ReferenceY, ReferenceZ = Reference / 100
    
    var_X = X / ReferenceX
    var_Y = Y / ReferenceY
    var_Z = Z / ReferenceZ
    
    def evaluar(x):
        return np.where(x > 0.008856, x**(1/3), 7.787 * x + 16/116)
    
    var_X = evaluar(var_X)
    var_Y = evaluar(var_Y)
    var_Z = evaluar(var_Z)
    
    CIEL = 116 * var_Y - 16
    CIEa = 500 * (var_X - var_Y)
    CIEb = 200 * (var_Y - var_Z)
    
    CIELAB[:,:,0] = CIEL
    CIELAB[:,:,1] = CIEa
    CIELAB[:,:,2] = CIEb
    
    return CIELAB.astype(np.float64)
    


def lab2xyz(lab):
    """
    Convierte una imagen CIELAB al espacio XYZ.

    Parámetros
    ----------
    lab : objeto
        Parámetro lab.

    Retorna
    -------
    out : objeto
        Resultado de lab2xyz.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = lab2xyz(lab)
    """
    # Asegurarse de que el último eje tenga tamaño 3
    if lab.shape[-1] != 3:
        raise ValueError("El último eje debe tener tamaño 3 (L*, a*, b*)")

    # Referencia D65 a 2 grados
    Reference = np.array([0.950456, 1.000000, 1.088754])

    def evaluar(x):
        return np.where(x > 0.008856, x ** 3, (x - 16 / 116) / 7.787)

    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]

    nL = (L + 16) / 116
    na = a / 500
    nb = b / 200

    var_X = evaluar(nL + na)
    var_Y = evaluar(nL)
    var_Z = evaluar(nL - nb)

    XYZ = np.zeros_like(lab)
    XYZ[..., 0] = Reference[0] * var_X
    XYZ[..., 1] = Reference[1] * var_Y
    XYZ[..., 2] = Reference[2] * var_Z

    return XYZ




def rgb2ycbcr(RGB):
    """
    Convierte una imagen RGB al espacio de color YCbCr.
    
    Parámetros
    ----------
    RGB : ndarray
        Imagen RGB de tamaño MxNx3 (uint8).
    
    Retorna
    -------
    YCBCR : ndarray
        Imagen en espacio de color YCbCr (uint8) con las mismas dimensiones
        que la entrada.
    
    Ejemplo
    -------
    >>> # uso básico
    >>> YCBCR = rgb2ycbcr(RGB)
    """
    if RGB.ndim != 3 or RGB.shape[2] != 3:
        raise ValueError('rgb2ycbcr: La imagen debe ser MxNx3')
    
    if RGB.dtype != np.uint8:
        raise ValueError('rgb2ycbcr: La imagen debe ser uint8')
    
    F, C, L = RGB.shape
    
    # Convertir a float64 para cálculos
    RGB_float = RGB.astype(np.float64)
    
    # Offset para YCbCr
    T = np.array([16, 128, 128])
    
    # Matriz de transformación RGB a YCbCr (estándar ITU-R BT.601)
    M = np.array([
        [65.481, 128.553, 24.966],
        [-37.797, -74.203, 112.0],
        [112.0, -93.786, -18.214]
    ])
    
    YCBCR = np.zeros((F, C, L))
    
    for i in range(F):
        for j in range(C):
            rgb_pixel = np.array([RGB_float[i,j,0], RGB_float[i,j,1], RGB_float[i,j,2]])
            ycbcr_pixel = M @ rgb_pixel + T
            YCBCR[i,j,:] = ycbcr_pixel
    
    # Convertir de vuelta a uint8 con clipping
    YCBCR = np.clip(YCBCR, 0, 255).astype(np.uint8)
    
    return YCBCR


def ycbcr2rgb(YCBCR):
    """
    Convierte una imagen YCbCr al espacio de color RGB.
    
    Parámetros
    ----------
    YCBCR : ndarray
        Imagen YCbCr de tamaño MxNx3 (uint8).
    
    Retorna
    -------
    RGB : ndarray
        Imagen RGB (uint8) con las mismas dimensiones que la entrada.
    
    Ejemplo
    -------
    >>> # uso básico
    >>> RGB = ycbcr2rgb(YCBCR)
    """
    if YCBCR.ndim != 3 or YCBCR.shape[2] != 3:
        raise ValueError('ycbcr2rgb: La imagen debe ser MxNx3')
    
    if YCBCR.dtype != np.uint8:
        raise ValueError('ycbcr2rgb: La imagen debe ser uint8')
    
    F, C, L = YCBCR.shape
    
    # Convertir a float64 para cálculos
    YCBCR_float = YCBCR.astype(np.float64)
    
    # Offset para YCbCr
    T = np.array([16, 128, 128])
    
    # Matriz de transformación inversa YCbCr a RGB
    M_inv = np.array([
        [0.00456621, 0.0, 0.00625893],
        [0.00456621, -0.00153632, -0.00318811],
        [0.00456621, 0.00791071, 0.0]
    ])
    
    RGB = np.zeros((F, C, L))
    
    for i in range(F):
        for j in range(C):
            ycbcr_pixel = np.array([YCBCR_float[i,j,0], YCBCR_float[i,j,1], YCBCR_float[i,j,2]])
            rgb_pixel = M_inv @ (ycbcr_pixel - T)
            RGB[i,j,:] = rgb_pixel
    
    # Convertir de vuelta a uint8 con clipping
    RGB = np.clip(RGB, 0, 255).astype(np.uint8)
    
    return RGB



# ====================================================================
# Transformaciones Geométricas
# ====================================================================

def imcrop(I, x, y, w, h):
    """
    Recorta una región rectangular de la imagen.
    (No requiere interpolación: es indexación directa.)
    """
    if I.ndim not in [2, 3]:
        raise ValueError("La imagen debe ser 2D (escala de grises) o 3D (color)")
    
    height, width = I.shape[:2]
    
    # Validar los límites del recorte
    if x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("Los parámetros de recorte están fuera de los límites de la imagen")
    
    if I.ndim == 2:
        return I[y:y+h, x:x+w]
    else:
        return I[y:y+h, x:x+w, :]





def imresize(I, S, method='bicubic', extrapval=0.0):
    """
    Redimensiona una imagen a un nuevo tamaño o escala.

    Cambio clave: construir Xq,Yq como matrices y llamar interp2 UNA sola vez.
    """
    import numpy as np

    # Tamaño original
    if I.ndim == 2:
        N, M = I.shape  # N=alto, M=ancho
    else:
        N, M, _ = I.shape

    # Factores de escala
    if np.isscalar(S):
        Sx = Sy = float(S)
    elif len(S) == 2:
        if isinstance(S[0], int) and isinstance(S[1], int):
            # S=(nuevo_alto, nuevo_ancho)
            Sy = S[0] / N
            Sx = S[1] / M
        else:
            # S=(factor_x, factor_y)
            Sx, Sy = float(S[0]), float(S[1])
    else:
        raise ValueError("S debe ser escalar o tupla de 2 elementos")

    # Nuevo tamaño (directo y consistente)
    Np = int(np.ceil(N * Sy))  # nueva altura
    Mp = int(np.ceil(M * Sx))  # nuevo ancho

    # Malla de salida (0-based) y mapeo inverso (0-based)
    xp = np.arange(Mp, dtype=float)
    yp = np.arange(Np, dtype=float)
    Xp, Yp = np.meshgrid(xp, yp)  # (Np, Mp)

    x = Xp / Sx
    y = Yp / Sy

    # interp2 usa 1-based (MATLAB)
    Xq = x + 1.0
    Yq = y + 1.0

    out = interp2(I, Xq, Yq, method, extrapval)
    return out.astype(I.dtype)



def imrotate(I, grados, method='nearest', extrapval=0.0):
    """
    Rota una imagen un ángulo dado en grados.

    Cambio clave: construir Xq,Yq como matrices y llamar interp2 UNA sola vez.
    (Se evita R_inv @ tensor 3D para no tener errores de matmul.)
    """
    import numpy as np

    theta = -grados * np.pi / 180.0
    c = np.cos(theta)
    s = np.sin(theta)

    # Dimensiones de entrada
    if I.ndim == 2:
        M, N = I.shape  # M=alto, N=ancho
    else:
        M, N, _ = I.shape

    # Centros (mismo criterio)
    pcx, pcy = (N / 2.0), (M / 2.0)

    # Tamaño de salida "loose"
    Np = int(np.ceil(abs(c) * N + abs(s) * M))  # nuevo ancho
    Mp = int(np.ceil(abs(s) * N + abs(c) * M))  # nueva altura

    pcx_p, pcy_p = (Np / 2.0), (Mp / 2.0)

    # Malla de salida (0-based)
    xp = np.arange(Np, dtype=float)
    yp = np.arange(Mp, dtype=float)
    Xp, Yp = np.meshgrid(xp, yp)  # (Mp, Np)

    # Relativas al centro de salida
    xr = Xp - pcx_p
    yr = Yp - pcy_p

    # Mapeo inverso: R_inv = [[c, s], [-s, c]]
    x = c * xr + s * yr + pcx
    y = -s * xr + c * yr + pcy

    # interp2 usa 1-based (MATLAB)
    Xq = x + 1.0
    Yq = y + 1.0

    out = interp2(I, Xq, Yq, method, extrapval)
    return out.astype(I.dtype)



def imtranslate(I, translation, mode='same', method='bilinear', extrapval=0.0):
    """
    Traslada una imagen por un vector de desplazamiento.

    Cambio clave: construir Xq,Yq como matrices y llamar interp2 UNA sola vez.
    """
    import numpy as np

    if I.ndim == 2:
        N, M = I.shape
    else:
        N, M, _ = I.shape

    tx, ty = float(translation[0]), float(translation[1])

    if mode == 'same':
        Mp, Np = M, N
        x_out0 = 0.0
        y_out0 = 0.0
    elif mode == 'full':
        Mp = int(np.ceil(M + abs(tx)))
        Np = int(np.ceil(N + abs(ty)))
        x_out0 = 0.0
        y_out0 = 0.0
    else:
        raise ValueError("El modo debe ser 'same' o 'full'")

    # Malla de salida (0-based)
    xp = np.arange(Mp, dtype=float) + x_out0
    yp = np.arange(Np, dtype=float) + y_out0
    Xp, Yp = np.meshgrid(xp, yp)  # (Np, Mp)

    # Mapeo inverso: entrada = salida - t
    x = Xp - tx
    y = Yp - ty

    # interp2 usa 1-based (MATLAB)
    Xq = x + 1.0
    Yq = y + 1.0

    out = interp2(I, Xq, Yq, method, extrapval)
    return out.astype(I.dtype)


def fitgeotrans(puntos_iniciales, puntos_finales, transformation_type='projective'):
    """
    Ajusta una transformación geométrica a pares de puntos.
    (No requiere interpolación: solo estima H.)
    """
    import numpy as np

    # Número de puntos
    n = puntos_iniciales.shape[0]
    
    if transformation_type == 'affine':
        num_params = 6
        A = np.zeros((2 * n, num_params))
        b = np.zeros(2 * n)
        
        for i in range(n):
            x, y = puntos_iniciales[i]
            x_prime, y_prime = puntos_finales[i]
            A[2*i, :] = [x, y, 1, 0, 0, 0]
            b[2*i] = x_prime
            A[2*i+1, :] = [0, 0, 0, x, y, 1]
            b[2*i+1] = y_prime
        
        h = np.linalg.lstsq(A, b, rcond=None)[0]
        H = np.array([[h[0], h[1], h[2]], 
                      [h[3], h[4], h[5]], 
                      [0, 0, 1]])

    elif transformation_type == 'projective':
        num_params = 8
        A = np.zeros((2 * n, num_params))
        b = np.zeros(2 * n)
        
        for i in range(n):
            x, y = puntos_iniciales[i]
            x_prime, y_prime = puntos_finales[i]
            A[2*i, :] = [x, y, 1, 0, 0, 0, -x_prime * x, -x_prime * y]
            b[2*i] = x_prime
            A[2*i+1, :] = [0, 0, 0, x, y, 1, -y_prime * x, -y_prime * y]
            b[2*i+1] = y_prime
        
        h = np.linalg.lstsq(A, b, rcond=None)[0]
        H = np.array([[h[0], h[1], h[2]], 
                      [h[3], h[4], h[5]], 
                      [h[6], h[7], 1]])

    else:
        raise ValueError("Tipo de transformación no soportado. Use 'affine' o 'projective'.")
    
    return H




def imwarp(I, H, method='bilinear', extrapval=0.0):
    """
    Aplica una transformación geométrica homogénea a una imagen.

    Cambio clave: construir Xq,Yq como matrices y llamar interp2 UNA sola vez.
    (Se evita H_inv @ tensor 3D; se usa forma cerrada con den.)
    """
    import numpy as np

    # Dimensiones entrada
    if I.ndim == 2:
        N, M = I.shape
    else:
        N, M, _ = I.shape

    # Esquinas en 1-based (como su versión original)
    corners = np.array([
        [1, 1, 1],
        [M, 1, 1],
        [1, N, 1],
        [M, N, 1]
    ], dtype=float).T

    tc = H @ corners
    tc /= tc[2, :]

    x_min, y_min = np.min(tc[:2, :], axis=1)
    x_max, y_max = np.max(tc[:2, :], axis=1)

    Np = int(np.ceil(y_max - y_min + 1))
    Mp = int(np.ceil(x_max - x_min + 1))

    # Malla de salida en coordenadas 1-based del plano destino
    x_out = x_min + np.arange(Mp, dtype=float)
    y_out = y_min + np.arange(Np, dtype=float)
    Xp, Yp = np.meshgrid(x_out, y_out)  # (Np, Mp)

    H_inv = np.linalg.inv(H)

    den = H_inv[2,0]*Xp + H_inv[2,1]*Yp + H_inv[2,2]
    Xq  = (H_inv[0,0]*Xp + H_inv[0,1]*Yp + H_inv[0,2]) / den
    Yq  = (H_inv[1,0]*Xp + H_inv[1,1]*Yp + H_inv[1,2]) / den

    out = interp2(I, Xq, Yq, method, extrapval)
    return out.astype(I.dtype)


# ====================================================================
#  Filtros Espaciales
# ====================================================================

def imfilter(I, K, salida='same', tipodepad='symmetric', method='conv', astype_out='auto'):
    """
    Filtra una imagen 2D con un kernel dado.
    (Compatibilidad: por defecto mantiene el comportamiento típico para imágenes enteras,
    y permite salida float para cálculos como SSIM.)
    """
    if K is None:
        raise ValueError('Es necesario el Kernel')

    pad_mode_map = {
        'replicate': 'edge',
        'symmetric': 'symmetric',
        'circular': 'wrap',
        'constant': 'constant'
    }

    if tipodepad in pad_mode_map:
        tipodepad_numpy = pad_mode_map[tipodepad]
    else:
        tipodepad_numpy = tipodepad

    # ---- NUEVO: guardar dtype original antes de pasar a float ----
    I0_dtype = np.asarray(I).dtype

    # Convertir imagen a float para los calculos (se mantiene)
    I = np.asarray(I, dtype=float)

    Tx, Ty = K.shape
    Finix = (Tx - 1) // 2
    Ciniy = (Ty - 1) // 2

    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))

    If = np.pad(I, pad_width, mode=tipodepad_numpy)

    if If.ndim == 2:
        If = If[..., np.newaxis]

    if method == 'conv':
        K = np.rot90(K, 2)

    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1

    If_temp = If.copy()

    for i in range(Finix, M - Finix):
        for j in range(Ciniy, N - Ciniy):
            for canal in range(L):
                W = If[i - Finix:i + Finix + 1, j - Ciniy:j + Ciniy + 1, canal]
                If_temp[i, j, canal] = np.sum(W * K)

    If = If_temp

    if salida == 'same':
        If = If[Finix:-Finix, Ciniy:-Ciniy]

    if L == 1:
        If = If[..., 0]

    # ---- CAMBIO CLAVE: salida configurable / auto ----
    if astype_out == 'uint8':
        If = np.clip(If, 0, 255).astype(np.uint8)

    elif astype_out == 'float':
        If = If.astype(np.float64, copy=False)

    else:  # 'auto'
        if np.issubdtype(I0_dtype, np.integer):
            If = np.clip(If, 0, 255).astype(I0_dtype)
        else:
            If = If.astype(np.float64, copy=False)

    return If

    
    
    
    

def ordfilt2(I, Orden, K, salida='same', tipodepad='symmetric'):
    """
    Aplica un filtro de orden 2D a una imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    Orden : objeto
        Parámetro Orden.
    K : objeto
        Parámetro K.
    salida : objeto
        Parámetro salida.
    tipodepad : objeto
        Parámetro tipodepad.

    Retorna
    -------
    out : objeto
        Resultado de ordfilt2.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = ordfilt2(I, Orden, K, salida, tipodepad)
    """

    
    # Parámetros del Kernel
    Tx, Ty = K.shape
    
    
    # Verificar argumentos necesarios
    if K is None:
        raise ValueError('Es necesario la máscara K')
    
    # Ajustar el orden si está fuera de rango
    num_elementos = Tx*Ty
    if Orden < 1 or Orden > num_elementos:
        raise ValueError(f'Orden debe estar entre 1 y {num_elementos}')
    
    
    
    
    Finix = (Tx - 1) // 2
    Ciniy = (Ty - 1) // 2
    
    # Ajustar el padding según las dimensiones de la imagen
    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))
    
    # Crear copia padded de la imagen (esta será nuestra salida para 'full')
    If = np.float64(np.pad(I, pad_width, mode=tipodepad))
    
    # Convertir a 3D si es necesario para procesamiento uniforme
    if If.ndim == 2:
        If = If[..., np.newaxis]
    
    # Obtener dimensiones
    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1
    
    # Copiar la imagen padded y solo modificar la región central
    If_temp = If.copy()
    
    # Aplicar el filtro de orden
    for i in range(Finix, M-Finix):
        for j in range(Ciniy, N-Ciniy):
            for canal in range(L):
                # Extraer la ventana
                W = If[i-Finix:i+Finix+1, j-Ciniy:j+Ciniy+1, canal]
                # Seleccionar los elementos definidos por el dominio
                elementos_validos = W[K.astype(bool)]
                # Ordenar y seleccionar el elemento según el orden
                elementos_ordenados = np.sort(elementos_validos)
                # El orden en Python es 0-based, por lo que restamos 1 al Orden
                If_temp[i, j, canal] = elementos_ordenados[Orden-1]
    
    # Ajustar el tamaño según el tipo de salida
    if salida == 'same':
        If = If_temp[Finix:-Finix, Ciniy:-Ciniy]
    else:
        If = If_temp
    
    # Volver a 2D si era 2D originalmente
    if L == 1:
        If = If[..., 0]
    
    # Normalizar y convertir a uint8
    If = np.clip(If, 0, 255).astype(np.uint8)
    
    return If



def medfilt2(I, FiltroTam=(3, 3), salida='same', tipodepad='symmetric'):
    """
    Aplica un filtro de mediana 2D.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    FiltroTam : objeto
        Parámetro FiltroTam.
    3) : objeto
        Parámetro 3).
    salida : objeto
        Parámetro salida.
    tipodepad : objeto
        Parámetro tipodepad.

    Retorna
    -------
    out : objeto
        Resultado de medfilt2.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = medfilt2(I, FiltroTam, 3), salida, tipodepad)
    """
    # Definir el tamaño del entorno (vecindad) y calcular el orden para la mediana
    m, n = FiltroTam
    K = np.ones((m, n))  # Crear una vecindad de 1s del tamaño especificado
    
    # Calcular la posición de la mediana en el entorno
    Elementos = m * n
    Orden = (Elementos + 1) // 2  # Calcular la posición central (mediana)
    
    # Llamar a la función ordfilt2 con la configuración adecuada
    return ordfilt2(I, Orden, K, salida, tipodepad)



def modefilt(I, FiltroTam=(3, 3), salida='same', tipodepad='symmetric'):
    """
    Aplica un filtro de moda 2D.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    FiltroTam : objeto
        Parámetro FiltroTam.
    3) : objeto
        Parámetro 3).
    salida : objeto
        Parámetro salida.
    tipodepad : objeto
        Parámetro tipodepad.

    Retorna
    -------
    out : objeto
        Resultado de modefilt.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = modefilt(I, FiltroTam, 3), salida, tipodepad)
    """
    # Definir el tamaño del entorno (vecindad)
    m, n = FiltroTam
    K = np.ones((m, n))  # Crear una vecindad de 1s del tamaño especificado
    
    # Ajustar el padding según las dimensiones de la imagen
    Finix = (m - 1) // 2
    Ciniy = (n - 1) // 2
    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))
    
    # Crear copia padded de la imagen
    If = np.float64(np.pad(I, pad_width, mode=tipodepad))
    
    # Convertir a 3D si es necesario para procesamiento uniforme
    if If.ndim == 2:
        If = If[..., np.newaxis]
    
    # Obtener dimensiones
    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1
    
    # Copiar la imagen padded y solo modificar la región central
    If_temp = If.copy()
    
    # Aplicar el filtro de moda
    for i in range(Finix, M - Finix):
        for j in range(Ciniy, N - Ciniy):
            for canal in range(L):
                # Extraer la ventana
                W = If[i - Finix:i + Finix + 1, j - Ciniy:j + Ciniy + 1, canal]
                # Seleccionar los elementos definidos por el dominio
                elementos_validos = W[K.astype(bool)]
                # Calcular la moda
                valores, cuentas = np.unique(elementos_validos, return_counts=True)
                moda = valores[np.argmax(cuentas)]
                If_temp[i, j, canal] = moda
    
    # Ajustar el tamaño según el tipo de salida
    if salida == 'same':
        If = If_temp[Finix:-Finix, Ciniy:-Ciniy]
    else:
        If = If_temp
    
    # Volver a 2D si era 2D originalmente
    if L == 1:
        If = If[..., 0]
    
    # Normalizar y convertir a uint8
    If = np.clip(If, 0, 255).astype(np.uint8)
    
    return If
    
    
    
def stdfilt(I, FiltroTam=(3, 3), salida='same', tipodepad='symmetric'):
    """
    Calcula la desviación estándar local de la imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    FiltroTam : objeto
        Parámetro FiltroTam.
    3) : objeto
        Parámetro 3).
    salida : objeto
        Parámetro salida.
    tipodepad : objeto
        Parámetro tipodepad.

    Retorna
    -------
    out : objeto
        Resultado de stdfilt.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = stdfilt(I, FiltroTam, 3), salida, tipodepad)
    """
    # Definir el tamaño del entorno (vecindad)
    m, n = FiltroTam
    K = np.ones((m, n))  # Crear una vecindad de 1s del tamaño especificado
    
    # Ajustar el padding según las dimensiones de la imagen
    Finix = (m - 1) // 2
    Ciniy = (n - 1) // 2
    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))
    
    # Crear copia padded de la imagen
    If = np.float64(np.pad(I, pad_width, mode=tipodepad))
    
    # Convertir a 3D si es necesario para procesamiento uniforme
    if If.ndim == 2:
        If = If[..., np.newaxis]
    
    # Obtener dimensiones
    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1
    
    # Copiar la imagen padded y solo modificar la región central
    If_temp = If.copy()
    
    # Aplicar el filtro de desviación estándar
    for i in range(Finix, M - Finix):
        for j in range(Ciniy, N - Ciniy):
            for canal in range(L):
                # Extraer la ventana
                W = If[i - Finix:i + Finix + 1, j - Ciniy:j + Ciniy + 1, canal]
                # Seleccionar los elementos definidos por el dominio
                elementos_validos = W[K.astype(bool)]
                # Calcular la desviación estándar
                desviacion = np.std(elementos_validos)
                If_temp[i, j, canal] = desviacion
    
    # Ajustar el tamaño según el tipo de salida
    if salida == 'same':
        If = If_temp[Finix:-Finix, Ciniy:-Ciniy]
    else:
        If = If_temp
    
    # Volver a 2D si era 2D originalmente
    if L == 1:
        If = If[..., 0]


    
    return If
    
    
    

def entropyfilt(I, FiltroTam=(3, 3), salida='same', tipodepad='symmetric'):
    """
    Calcula la entropía local de la imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    FiltroTam : objeto
        Parámetro FiltroTam.
    3) : objeto
        Parámetro 3).
    salida : objeto
        Parámetro salida.
    tipodepad : objeto
        Parámetro tipodepad.

    Retorna
    -------
    out : objeto
        Resultado de entropyfilt.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = entropyfilt(I, FiltroTam, 3), salida, tipodepad)
    """
    # Definir el tamaño del entorno (vecindad)
    m, n = FiltroTam
    K = np.ones((m, n))  # Crear una vecindad de 1s del tamaño especificado
    
    # Ajustar el padding según las dimensiones de la imagen
    Finix = (m - 1) // 2
    Ciniy = (n - 1) // 2
    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))
    
    # Crear copia padded de la imagen
    If = np.pad(I, pad_width, mode=tipodepad).astype(np.float64)
    
    # Convertir a 3D si es necesario para procesamiento uniforme
    if If.ndim == 2:
        If = If[..., np.newaxis]
    
    # Obtener dimensiones
    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1
    
    # Copiar la imagen padded y solo modificar la región central
    If_temp = If.copy()
    
    # Aplicar el filtro de entropía
    for i in range(Finix, M - Finix):
        for j in range(Ciniy, N - Ciniy):
            for canal in range(L):
                # Extraer la ventana
                W = If[i - Finix:i + Finix + 1, j - Ciniy:j + Ciniy + 1, canal] * K
                # Calcular el histograma de la vecindad y las probabilidades
                p = np.histogram(W.flatten(), bins=256, range=(0, 255))[0] / (m * n)
                # Excluir probabilidades cero
                prob_no_cero = p[p > 0]
                # Calcular la entropía usando la fórmula de Shannon
                entropia = -np.sum(prob_no_cero * np.log2(prob_no_cero))
                # Asignar la entropía calculada al píxel de salida
                If_temp[i, j, canal] = entropia
    
    # Ajustar el tamaño según el tipo de salida
    if salida == 'same':
        If = If_temp[Finix:-Finix, Ciniy:-Ciniy]
    else:
        If = If_temp
    
    # Volver a 2D si era 2D originalmente
    if L == 1:
        If = If[..., 0]
    

    
    return If
    
    
    
    
def rangefilt(I, FiltroTam=(3, 3), salida='same', tipodepad='symmetric'):
    """
    Calcula el rango local (max-min) de la imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    FiltroTam : objeto
        Parámetro FiltroTam.
    3) : objeto
        Parámetro 3).
    salida : objeto
        Parámetro salida.
    tipodepad : objeto
        Parámetro tipodepad.

    Retorna
    -------
    out : objeto
        Resultado de rangefilt.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = rangefilt(I, FiltroTam, 3), salida, tipodepad)
    """
    # Definir el tamaño del entorno (vecindad)
    m, n = FiltroTam
    K = np.ones((m, n))  # Crear una vecindad de 1s del tamaño especificado
    
    # Ajustar el padding según las dimensiones de la imagen
    Finix = (m - 1) // 2
    Ciniy = (n - 1) // 2
    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))
    
    # Crear copia padded de la imagen
    If = np.pad(I, pad_width, mode=tipodepad).astype(np.float64)
    
    # Convertir a 3D si es necesario para procesamiento uniforme
    if If.ndim == 2:
        If = If[..., np.newaxis]
    
    # Obtener dimensiones
    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1
    
    # Copiar la imagen padded y solo modificar la región central
    If_temp = If.copy()
    
    # Aplicar el filtro de rango
    for i in range(Finix, M - Finix):
        for j in range(Ciniy, N - Ciniy):
            for canal in range(L):
                # Extraer la ventana
                W = If[i - Finix:i + Finix + 1, j - Ciniy:j + Ciniy + 1, canal] * K
                # Calcular el rango (diferencia entre el valor máximo y mínimo)
                rango = np.abs(np.max(W) - np.min(W))
                # Asignar el rango calculado al píxel de salida
                If_temp[i, j, canal] = rango
    
    # Ajustar el tamaño según el tipo de salida
    if salida == 'same':
        If = If_temp[Finix:-Finix, Ciniy:-Ciniy]
    else:
        If = If_temp
    
    # Volver a 2D si era 2D originalmente
    if L == 1:
        If = If[..., 0]
    
    # Normalizar y convertir a uint8
    If = np.clip(If, 0, 255).astype(np.uint8)
    
    return If
    
    
def fspecial(tipo, T=None, S=None):
    """
    Genera kernels clásicos de filtrado espacial.

    Parámetros
    ----------
    tipo : str
        Parámetro tipo.
    T : objeto
        Parámetro T.
    S : objeto
        Parámetro S.

    Retorna
    -------
    out : objeto
        Resultado de fspecial.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = fspecial(tipo, T, S)
    """
    tipo = tipo.lower()
    if tipo == 'average':
        T = 3 if T is None else T
        Tx, Ty = (T, T) if isinstance(T, int) else T
        return np.ones((Tx, Ty)) / (Tx * Ty)

    elif tipo == 'gaussian':
        if T is None: T = 3
        if hasattr(T, '__len__'): Tx, Ty = T[0], T[1]
        else: Tx = Ty = T
        
        S = 0.5 if S is None else S
        
        LimX = (Ty - 1) / 2.0
        LimY = (Tx - 1) / 2.0
        
        x = np.linspace(-LimX, LimX, Ty)
        y = np.linspace(-LimY, LimY, Tx)
        X, Y = np.meshgrid(x, y)
        
        Z = np.exp(-(X ** 2 + Y ** 2) / (2 * S ** 2))
        return Z / np.sum(Z)

    elif tipo == 'laplacian':
        A = 0.2 if T is None else T
        return (4 / (A + 1)) * np.array([[A / 4, (1 - A) / 4, A / 4],
                                         [(1 - A) / 4, -1, (1 - A) / 4],
                                         [A / 4, (1 - A) / 4, A / 4]])

    elif tipo == 'log':
        if T is None: T = 5
        if hasattr(T, '__len__'): Tx, Ty = T[0], T[1]
        else: Tx = Ty = T
        
        S = 0.5 if S is None else S
        
        LimX = (Ty - 1) / 2.0
        LimY = (Tx - 1) / 2.0
        
        x = np.linspace(-LimX, LimX, Ty)
        y = np.linspace(-LimY, LimY, Tx)
        X, Y = np.meshgrid(x, y)
        
        arg = -(X ** 2 + Y ** 2) / (2 * S ** 2)
        gau = np.exp(arg)
        gau[gau < np.finfo(gau.dtype).eps * np.max(gau)] = 0
        
        sumh = np.sum(gau)
        if sumh != 0: gau /= sumh
        
        f2 = (gau * (X ** 2 + Y ** 2 - (2 * S ** 2))) / (S ** 4)
        return f2 - np.sum(f2) / (Tx * Ty)


    elif tipo == 'motion':
        T = 9 if T is None else T
        
        angle = S if S is not None else 0  # Angle in degrees
        # Default motion filter: horizontal line
        kernel = np.ones((1, T))
        
        if angle != 0:
            # Calculate new kernel size to fit the rotated line completely (Arreglar para rotar vectores)
            kernel = imrotate(kernel, angle)
            
        return kernel / np.sum(kernel)
        
        
        
    elif tipo == 'prewitt':
        return np.array([[1, 1, 1],
                         [0, 0, 0],
                         [-1, -1, -1]])

    elif tipo == 'sobel':
        return np.array([[1, 2, 1],
                         [0, 0, 0],
                         [-1, -2, -1]])

    elif tipo == 'unsharp':
        A = 0.2 if T is None else T
        identity = np.array([[0, 0, 0],
                             [0, 1, 0],
                             [0, 0, 0]])
        laplacian = (4 / (A + 1)) * np.array([[A / 4, (1 - A) / 4, A / 4],
                                              [(1 - A) / 4, -1, (1 - A) / 4],
                                              [A / 4, (1 - A) / 4, A / 4]])
        return identity - A * laplacian

    else:
        raise ValueError(f"Unknown filter type: {tipo}")






# ====================================================================
#  Morfología Matemática
# ====================================================================

def strel(shape, size, angle=0):
    """
    Crea un elemento estructurante para morfología.

    Parámetros
    ----------
    shape : str
        Parámetro shape.
    size : int or tuple
        Parámetro size.
    angle : int or tuple
        Parámetro angle.

    Retorna
    -------
    out : objeto
        Resultado de strel.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = strel(shape, size, angle)
    """
    shape = shape.lower()
    
    # === Cuadrado: bloque n×n ===
    if shape == 'square':
        return np.ones((size, size), dtype=bool)
    
    # === Rectángulo: bloque m×n ===
    elif shape == 'rectangle':
        m, n = size
        return np.ones((m, n), dtype=bool)
    
    # === Disco: círculo discreto de radio r ===
    elif shape == 'disk':
        r = size
        y, x = np.ogrid[-r:r+1, -r:r+1]
        return (x**2 + y**2) <= r**2
    
    # === Diamante: basado en distancia de Manhattan (L1) ===
    elif shape == 'diamond':
        r = size
        y, x = np.ogrid[-r:r+1, -r:r+1]
        return (np.abs(x) + np.abs(y)) <= r
    
    # === Línea: segmento recto en ángulo definido ===
    elif shape == 'line':
        L = size
        # Crear una matriz lo suficientemente grande para contener la línea rotada
        if L < 3:
            L = 3
        SE = np.zeros((L, L), dtype=bool)
        cx = cy = L // 2
        theta = np.deg2rad(angle)
        
        # Generar puntos de la línea
        for i in range(L):
            offset = i - L // 2
            x = int(round(cx + offset * np.cos(theta)))
            y = int(round(cy + offset * np.sin(theta)))
            if 0 <= x < L and 0 <= y < L:
                SE[y, x] = True
        return SE
    
    # === Octágono: mezcla de disco y cuadrado ===
    elif shape == 'octagon':
        r = size
        y, x = np.ogrid[-r:r+1, -r:r+1]
        # Condición de círculo
        circle_mask = (x**2 + y**2) <= r**2
        # Condición de diamante expandido
        diamond_mask = (np.abs(x) + np.abs(y)) <= (r + r//2)
        return circle_mask | diamond_mask
    
    else:
        raise ValueError("Tipo no soportado. Use: "
                         "'square','rectangle','disk','diamond','line','octagon'")



def imdilate(Ibin, SE, pad=0):
    """
    Aplica dilatación morfológica a una imagen binaria.

    Parámetros
    ----------
    Ibin : ndarray
        Parámetro Ibin.
    SE : objeto
        Parámetro SE.
    pad : objeto
        Parámetro pad.

    Retorna
    -------
    out : objeto
        Resultado de imdilate.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imdilate(Ibin, SE, pad)
    """
    I = Ibin.astype(bool)
    B = SE.astype(bool)
    m, n = B.shape
    rf = (m - 1) // 2
    cf = (n - 1) // 2

    if pad is None:
        # Sin acolchar ni recortar: operar en sitio
        return _slide_bool(I, B, op_any=True)

    # Acolchado y recorte estándar
    A = np.pad(I, ((rf, rf), (cf, cf)), mode='constant', constant_values=int(pad))
    O = _slide_bool(A, B, op_any=True)
    return O[rf:O.shape[0]-rf, cf:O.shape[1]-cf]


def imerode(Ibin, SE, pad=0):
    """
    Aplica erosión morfológica a una imagen binaria.

    Parámetros
    ----------
    Ibin : ndarray
        Parámetro Ibin.
    SE : objeto
        Parámetro SE.
    pad : objeto
        Parámetro pad.

    Retorna
    -------
    out : objeto
        Resultado de imerode.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imerode(Ibin, SE, pad)
    """
    I = Ibin.astype(bool)
    B = SE.astype(bool)
    m, n = B.shape
    rf = (m - 1) // 2
    cf = (n - 1) // 2

    if pad is None:
        return _slide_bool(I, B, op_any=False)

    A = np.pad(I, ((rf, rf), (cf, cf)), mode='constant', constant_values=int(pad))
    O = _slide_bool(A, B, op_any=False)
    return O[rf:O.shape[0]-rf, cf:O.shape[1]-cf]


def imopen(Ibin, SE, pad=0):
    """
    Realiza apertura morfológica (erosión seguida de dilatación).

    Parámetros
    ----------
    Ibin : ndarray
        Parámetro Ibin.
    SE : objeto
        Parámetro SE.
    pad : objeto
        Parámetro pad.

    Retorna
    -------
    out : objeto
        Resultado de imopen.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imopen(Ibin, SE, pad)
    """
    I = Ibin.astype(bool)
    B = SE.astype(bool)
    m, n = B.shape
    rf = (m - 1) // 2
    cf = (n - 1) // 2

    if pad is None:
        # I ya acolchada; no recortar
        E = imerode(I, B, pad=None)
        D = imdilate(E, B, pad=None)
        return D

    # acolchado único
    A = np.pad(I, ((rf, rf), (cf, cf)), mode='constant', constant_values=int(pad))
    E = imerode(A, B, pad=None)
    D = imdilate(E, B, pad=None)
    # recorte único
    return D[rf:D.shape[0]-rf, cf:D.shape[1]-cf]


def imclose(Ibin, SE, pad=0):
    """
    Realiza cierre morfológico (dilatación seguida de erosión).

    Parámetros
    ----------
    Ibin : ndarray
        Parámetro Ibin.
    SE : objeto
        Parámetro SE.
    pad : objeto
        Parámetro pad.

    Retorna
    -------
    out : objeto
        Resultado de imclose.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imclose(Ibin, SE, pad)
    """
    I = Ibin.astype(bool)
    B = SE.astype(bool)
    m, n = B.shape
    rf = (m - 1) // 2
    cf = (n - 1) // 2

    if pad is None:
        D = imdilate(I, B, pad=None)
        E = imerode(D, B, pad=None)
        return E

    A = np.pad(I, ((rf, rf), (cf, cf)), mode='constant', constant_values=int(pad))
    D = imdilate(A, B, pad=None)
    E = imerode(D, B, pad=None)
    return E[rf:E.shape[0]-rf, cf:E.shape[1]-cf]


    
      



# ====================================================================
# ✂ Segmentación
# ====================================================================

def otsuthresh(h):
    """
    Función otsuthresh de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    h : objeto
        Parámetro h.

    Retorna
    -------
    out : float
        Resultado de otsuthresh.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = otsuthresh(h)
    """
    lh=len(h)
    tam=np.sum(h)
    maxV=0
    
    for T in np.arange(0,lh,1):
         Wb=np.sum(h[0:T])/tam
         Acub=np.sum(h[0:T])
         Acuf=np.sum(h[T+1:lh])
         if  Acub==0:
             Ub=0
         else:
             Ub=np.dot(np.arange(0,T,1),h[0:T])/Acub
         if Acuf==0:
             Uf=0
         else:
             Uf=np.dot(np.arange(T+1,lh,1),h[T+1:lh])/Acuf
         Wf=1-Wb
         BCV=Wb*Wf*(Ub-Uf)**2;
         
         if BCV>=maxV:
                maxV=BCV
                umbral=(T+1)/255
    return umbral


    
def graythresh(I):
    """
    Calcula el umbral de Otsu a partir de una imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : float
        Resultado de graythresh.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = graythresh(I)
    """
    h=imhist(I,None,False)
    return otsuthresh(h)


def adaptthresh(I, P=None, V=None):
    """
    Calcula un umbral adaptativo local.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    P : objeto
        Parámetro P.
    V : objeto
        Parámetro V.

    Retorna
    -------
    out : ndarray
        Resultado de adaptthresh.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = adaptthresh(I, P, V)
    """
    # Valores por defecto
    S = 0.5  # Sensibilidad por defecto
    W = 2 * np.floor(np.array(I.shape) / 16).astype(int) + 1  # Tamaño de ventana por defecto

    # Si no se proporciona V, usar la fórmula por defecto
    if V is None:
        V = W

    # Si no se proporciona P, usar el valor por defecto
    if P is None:
        P = S

    # Parámetros de la ventana
    Tx, Ty = V
    Finix = (Tx + 1) // 2
    Ciniy = (Ty + 1) // 2
    Ffinx = Finix - 1
    Cfiny = Ciniy - 1

    # Preparar la imagen con padarray replicado
    Io = I.copy()
    I_padded = np.pad(Io, ((Ffinx, Ffinx), (Cfiny, Cfiny)), mode='edge')
    F, C = Io.shape
    T = np.zeros((F, C))

    # Calcular el umbral local
    for i in range(Finix, F - Ffinx):
        for j in range(Ciniy, C - Cfiny):
            # Definir límites del vecindario
            start_i = i - Ffinx
            end_i = i + Ffinx + 1
            start_j = j - Cfiny
            end_j = j + Cfiny + 1

            # Extraer el vecindario y calcular el umbral local
            W = I_padded[start_i:end_i, start_j:end_j]
            T[i, j] = np.mean(W) * (1 - P)  # Aplicar la sensibilidad P al cálculo del umbral


    return T/255



def im2bw(I, threshold):
    """
    Convierte una imagen de nivel de gris a binaria.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    threshold : objeto
        Parámetro threshold.

    Retorna
    -------
    out : ndarray
        Resultado de im2bw.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = im2bw(I, threshold)
    """
    # Convierte la imagen I a binaria usando el umbral especificado
    return (I >= threshold * 255).astype(bool)



def imbinarize(I, *args):
    """
    Binariza una imagen usando umbral fijo o adaptativo.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    args : tuple
        Argumentos variables para imbinarize.

    Retorna
    -------
    out : ndarray
        Resultado de imbinarize.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imbinarize(I, *args)
    """
    # Comprobar si el primer argumento es un escalar (umbral)
    if len(args) == 1 and isinstance(args[0], (int, float, np.ndarray)):
        T = args[0]
        return im2bw(I, T)
    
    mode = args[0].lower() if len(args) > 0 and isinstance(args[0], str) else 'global'
    kwargs = dict(zip(args[1::2], args[2::2]))  # Extraer argumentos adicionales
    
    # Convertir todas las claves de kwargs a minúsculas
    kwargs = {k.lower(): v for k, v in kwargs.items()}

    if mode == 'global':
        # Umbral global utilizando el método de Otsu
        Thres = graythresh(I)
        bw = im2bw(I, Thres)
    elif mode == 'adaptive':
        # Umbral adaptativo utilizando el método de Bradley
        sensitivity = kwargs.get('sensitivity', 0.5)  # Usar 0.5 si no se proporciona
        window_size = kwargs.get('windowsize', None)
        Tadap = adaptthresh(I, P=sensitivity, V=window_size)
        bw = im2bw(I, Tadap)
    else:
        raise ValueError("Modo no válido. Debe ser 'global', 'adaptive' o proporcionar el umbral T.")
    
    return bw




def imgradient(I, method='sobel'):
    """
    Calcula el gradiente de una imagen (magnitud y dirección).

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    method : str
        Parámetro method.

    Retorna
    -------
    out : tuple[ndarray, ndarray]
        Resultado de imgradient.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imgradient(I, method)
    """
    I = np.asarray(I, dtype=np.float64)
    
    method = method.lower()
    
    # Seleccionar kernels segun metodo
    if method == 'sobel':
        Kx = fspecial('sobel')
        Ky = Kx.T
    elif method == 'prewitt':
        Kx = fspecial('prewitt')
        Ky = Kx.T
    elif method == 'roberts':
        Kx = np.array([[1, 0], [0, -1]], dtype=np.float64)
        Ky = np.array([[0, 1], [-1, 0]], dtype=np.float64)
    elif method == 'central':
        # Diferencias centrales: [-1 0 1]/2
        Kx = np.array([[-0.5, 0, 0.5]], dtype=np.float64)
        Ky = Kx.T
    elif method == 'intermediate':
        # MATLAB intermediate: promedio de diferencias
        Kx = np.array([[0, 0], [0, 0], [-1, 1]], dtype=np.float64) / 2
        Ky = np.array([[0, 0, -1], [0, 0, 1]], dtype=np.float64) / 2
    else:
        raise ValueError(f"Metodo '{method}' no soportado. Use: 'sobel', 'prewitt', 'roberts', 'central', 'intermediate'")
    
    # Calcular gradientes en x e y
    if I.dtype == np.uint8:
        I_filt = I
    else:
        I_filt = I.astype(np.uint8)
    
    Gx = imfilter(I_filt, Kx, salida='same', tipodepad='replicate')
    Gy = imfilter(I_filt, Ky, salida='same', tipodepad='replicate')
    
    # Convertir a float64 (como MATLAB)
    Gx = Gx.astype(np.float64)
    Gy = Gy.astype(np.float64)
    
    # Magnitud del gradiente
    Gmag = np.sqrt(Gx**2 + Gy**2)
    
    # Direccion del gradiente en grados [-180, 180]
    Gdir = np.arctan2(Gy, Gx) * 180.0 / np.pi
    
    return Gmag, Gdir


def edge(I, method='canny', thresh=None, sigma=None, direction='both', tsize=None):
    """
    Detecta bordes en una imagen (Sobel, Prewitt, Canny, etc.).

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    method : str
        Parámetro method.
    thresh : objeto
        Parámetro thresh.
    sigma : objeto
        Parámetro sigma.
    direction : objeto
        Parámetro direction.
    tsize : objeto
        Parámetro tsize.

    Retorna
    -------
    out : ndarray
        Resultado de edge.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = edge(I, method, thresh, sigma, direction, tsize)
    """
    
    # Validar entrada
    if I.ndim != 2:
        raise ValueError("Input image must be 2-D (grayscale)")
    
    # Convertir a float64 si es necesario
    if I.dtype == np.uint8:
        I_work = I.astype(np.float64) / 255.0  # Normalizar [0,1] como MATLAB
    else:
        I_work = I.astype(np.float64)
    
    method = method.lower()
    
    # Manejar thresh como lista vacia (MATLAB permite [])
    if isinstance(thresh, (list, tuple)) and len(thresh) == 0:
        thresh = None
    
    # ========================================================================
    # CANNY - Compatible 100% con MATLAB
    # ========================================================================
    if method == 'canny':
        # Sigma por defecto (MATLAB usa sqrt(2))
        if sigma is None:
            sigma = np.sqrt(2)
        
        # ETAPA 1: Suavizado Gaussiano
        tam_kernel = int(np.ceil(6 * sigma))
        if tam_kernel % 2 == 0:
            tam_kernel += 1
        h_gauss = fspecial('gaussian', tam_kernel, sigma)
        I_smooth = imfilter((I_work * 255).astype(np.uint8), h_gauss, 
                           salida='same', tipodepad='replicate')
        
        # ETAPA 2: Calculo del gradiente
        Gmag, Gdir = imgradient(I_smooth, method='sobel')
        
        # ETAPA 3: Supresion no maxima
        I_nms = _non_maximum_suppression(Gmag, Gdir)
        
        # ETAPA 4: Calcular umbrales (NORMALIZADOS [0,1] como MATLAB)
        max_grad = np.max(I_nms)
        
        if thresh is None:
            # Automatico: MATLAB usa histograma
            valores_no_cero = I_nms[I_nms > 0]
            if len(valores_no_cero) == 0:
                return np.zeros(I.shape, dtype=bool)
            
            # Percentiles similares a MATLAB
            T_high = np.percentile(valores_no_cero, 70)
            T_low = 0.4 * T_high
            
        elif np.isscalar(thresh):
            # Un umbral normalizado [0,1]
            T_high = float(thresh) * max_grad
            T_low = 0.4 * T_high
            
        elif isinstance(thresh, (list, tuple, np.ndarray)) and len(thresh) == 2:
            # Dos umbrales normalizados [0,1]
            T_low = float(thresh[0]) * max_grad
            T_high = float(thresh[1]) * max_grad
        else:
            raise ValueError("thresh debe ser None, escalar, o [low, high]")
        
        # ETAPA 5: Histeresis
        BW = _hysteresis_threshold(I_nms, T_low, T_high)
        return BW
    
    # ========================================================================
    # SOBEL
    # ========================================================================
    elif method == 'sobel':
        Gmag, _ = imgradient((I_work * 255).astype(np.uint8), method='sobel')
        
        # Aplicar direccion
        if direction == 'horizontal':
            Kx = fspecial('sobel')
            Gx = imfilter((I_work * 255).astype(np.uint8), Kx, 
                         salida='same', tipodepad='replicate')
            Gmag = np.abs(Gx.astype(np.float64))
        elif direction == 'vertical':
            Ky = fspecial('sobel').T
            Gy = imfilter((I_work * 255).astype(np.uint8), Ky, 
                         salida='same', tipodepad='replicate')
            Gmag = np.abs(Gy.astype(np.float64))
        
        # Umbral normalizado [0,1]
        if thresh is None:
            # MATLAB usa Otsu para sobel
            thresh = graythresh(Gmag.astype(np.uint8))
        
        max_grad = np.max(Gmag)
        T = float(thresh) * max_grad if max_grad > 0 else 0
        
        BW = Gmag > T
        return BW
    
    # ========================================================================
    # PREWITT
    # ========================================================================
    elif method == 'prewitt':
        Gmag, _ = imgradient((I_work * 255).astype(np.uint8), method='prewitt')
        
        # Aplicar direccion
        if direction == 'horizontal':
            Kx = fspecial('prewitt')
            Gx = imfilter((I_work * 255).astype(np.uint8), Kx, 
                         salida='same', tipodepad='replicate')
            Gmag = np.abs(Gx.astype(np.float64))
        elif direction == 'vertical':
            Ky = fspecial('prewitt').T
            Gy = imfilter((I_work * 255).astype(np.uint8), Ky, 
                         salida='same', tipodepad='replicate')
            Gmag = np.abs(Gy.astype(np.float64))
        
        if thresh is None:
            thresh = graythresh(Gmag.astype(np.uint8))
        
        max_grad = np.max(Gmag)
        T = float(thresh) * max_grad if max_grad > 0 else 0
        
        BW = Gmag > T
        return BW
    
    # ========================================================================
    # ROBERTS
    # ========================================================================
    elif method == 'roberts':
        Gmag, _ = imgradient((I_work * 255).astype(np.uint8), method='roberts')
        
        if thresh is None:
            thresh = graythresh(Gmag.astype(np.uint8))
        
        max_grad = np.max(Gmag)
        T = float(thresh) * max_grad if max_grad > 0 else 0
        
        BW = Gmag > T
        return BW
    
    # ========================================================================
    # LOG - Laplaciano de Gaussiano
    # ========================================================================
    elif method == 'log':
        # Sigma por defecto
        if sigma is None:
            sigma = 2.0
        
        # Tamano del filtro
        if tsize is None:
            tam = int(np.ceil(6 * sigma))
            if tam % 2 == 0:
                tam += 1
        else:
            tam = int(tsize)
            if tam % 2 == 0:
                tam += 1
        
        # Crear y aplicar filtro LoG
        h_log = fspecial('log', tam, sigma)
        I_log = imfilter((I_work * 255).astype(np.uint8), h_log, 
                        salida='same', tipodepad='replicate')
        I_log = I_log.astype(np.float64)
        
        # Detectar cruces por cero
        BW = _detectar_cruces_cero(I_log)
        
        # Aplicar umbral si se especifica
        if thresh is not None:
            # MATLAB usa umbral absoluto para LoG
            BW = BW & (np.abs(I_log) > float(thresh))
        
        return BW
    
    # ========================================================================
    # ZEROCROSS - Cruces por cero con filtro personalizado
    # ========================================================================
    elif method == 'zerocross':
        # Si no se proporciona filtro, usar LoG por defecto
        if sigma is None:
            sigma = 1.0
        
        if tsize is None:
            tam = 5
        else:
            tam = int(tsize)
            if tam % 2 == 0:
                tam += 1
        
        h = fspecial('log', tam, sigma)
        
        I_filtered = imfilter((I_work * 255).astype(np.uint8), h, 
                             salida='same', tipodepad='replicate')
        I_filtered = I_filtered.astype(np.float64)
        
        BW = _detectar_cruces_cero(I_filtered)
        
        if thresh is not None:
            BW = BW & (np.abs(I_filtered) > float(thresh))
        
        return BW
    
    else:
        raise ValueError(f"Unknown method '{method}'. Use: 'canny', 'sobel', 'prewitt', 'roberts', 'log', 'zerocross'")


# ============================================================================
# FUNCIONES AUXILIARES (PRIVADAS - no expuestas por MATLAB)
# ============================================================================



# ====================================================================
# 🏷 Análisis de Componentes Conectados
# ====================================================================

def bwlabel(I, EE=4):
    """
    Etiqueta componentes conectados en una imagen binaria.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    EE : objeto
        Parámetro EE.

    Retorna
    -------
    out : tuple[ndarray, int]
        Resultado de bwlabel.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = bwlabel(I, EE)
    """
    if not isinstance(I, np.ndarray):
        raise TypeError("I debe ser un numpy array")
    
    if I.dtype != bool or I.ndim != 2:
        raise ValueError("La imagen debe ser binaria (bool) y 2D")
    
    if EE not in [4, 8]:
        raise ValueError("EE debe ser 4 u 8")
    
    M, N = I.shape
    if not I.any():
        return np.zeros((M, N), dtype=int), 0
    
    # Definir vecindad
    if EE == 4:
        vecinos = [(-1, 0), (0, -1)]
    else:
        vecinos = [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
    
    # Union-Find
    def find(x, parent):
        if parent[x] != x:
            parent[x] = find(parent[x], parent)
        return parent[x]
    
    def union(x, y, parent):
        root_x = find(x, parent)
        root_y = find(y, parent)
        if root_x != root_y:
            if root_x < root_y:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
    
    # Primera pasada
    Labels = np.zeros((M, N), dtype=int)
    next_label = 1
    parent = {}
    
    for i in range(M):
        for j in range(N):
            if I[i, j]:
                vecino_labels = []
                for di, dj in vecinos:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < M and 0 <= nj < N and Labels[ni, nj] > 0:
                        vecino_labels.append(Labels[ni, nj])
                
                if not vecino_labels:
                    Labels[i, j] = next_label
                    parent[next_label] = next_label
                    next_label += 1
                else:
                    min_label = min(vecino_labels)
                    Labels[i, j] = min_label
                    for lbl in vecino_labels:
                        if lbl != min_label:
                            union(min_label, lbl, parent)
    
    # Segunda pasada
    for i in range(M):
        for j in range(N):
            if Labels[i, j] > 0:
                Labels[i, j] = find(Labels[i, j], parent)
    
    # Renumeracion
    etiquetas_unicas = np.unique(Labels[Labels > 0])
    mapeo = {old: new for new, old in enumerate(etiquetas_unicas, start=1)}
    
    Labels_final = np.zeros_like(Labels)
    for i in range(M):
        for j in range(N):
            if Labels[i, j] > 0:
                Labels_final[i, j] = mapeo[Labels[i, j]]
    
    Num = len(etiquetas_unicas)
    return Labels_final, Num





def label2rgb(L, colormap='jet', bgcolor=None, order='noshuffle'):
    """
    Convierte etiquetas de región a una imagen en color falso.

    Parámetros
    ----------
    L : ndarray
        Parámetro L.
    colormap : str
        Parámetro colormap.
    bgcolor : objeto
        Parámetro bgcolor.
    order : objeto
        Parámetro order.

    Retorna
    -------
    out : ndarray
        Resultado de label2rgb.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = label2rgb(L, colormap, bgcolor, order)
    """
    
    # ========================================================================
    # VALIDAR ENTRADA
    # ========================================================================
    if L.ndim != 2:
        raise ValueError("L debe ser 2D")
    
    M, N = L.shape
    etiquetas = np.unique(L[L > 0])  # Solo regiones (sin fondo)
    num_regiones = len(etiquetas)
    
    # ========================================================================
    # INICIALIZAR IMAGEN RGB (negro por defecto)
    # ========================================================================
    RGB = np.zeros((M, N, 3))
    
    # ========================================================================
    # APLICAR COLOR DE FONDO
    # ========================================================================
    if bgcolor is not None:
        # Diccionario de colores básicos
        colores_basicos = {
            'k': [0,0,0], 'w': [1,1,1], 'r': [1,0,0], 
            'g': [0,1,0], 'b': [0,0,1], 'c': [0,1,1],
            'm': [1,0,1], 'y': [1,1,0]
        }
        
        if isinstance(bgcolor, str):
            if bgcolor.lower() in colores_basicos:
                color_fondo = np.array(colores_basicos[bgcolor.lower()])
            else:
                raise ValueError(f"Color '{bgcolor}' no reconocido")
        else:
            color_fondo = np.array(bgcolor).flatten()
            if len(color_fondo) != 3:
                raise ValueError("Color debe tener 3 valores RGB")
            if color_fondo.max() > 1:
                color_fondo = color_fondo / 255.0
            color_fondo = np.clip(color_fondo, 0, 1)
        
        RGB[:, :, :] = color_fondo
    
    # ========================================================================
    # SI NO HAY REGIONES, DEVOLVER SOLO FONDO
    # ========================================================================
    if num_regiones == 0:
        return RGB
    
    # ========================================================================
    # OBTENER COLORES DEL COLORMAP
    # ========================================================================
    if isinstance(colormap, (list, np.ndarray)):
        # Colormap es array de colores directos
        colores = np.array(colormap)
        if colores.ndim != 2 or colores.shape[1] != 3:
            raise ValueError("Colormap debe ser N×3")
        if colores.max() > 1:
            colores = colores / 255.0
        colores = np.clip(colores, 0, 1)
    
    elif isinstance(colormap, str):
        # Colormap es nombre de matplotlib
        cmap = plt.get_cmap(colormap, num_regiones)
        colores = np.array([cmap(i)[:3] for i in range(num_regiones)])
    
    else:
        raise ValueError("colormap debe ser string o array N×3")
    
    # ========================================================================
    # ALEATORIZAR COLORES SI SE SOLICITA
    # ========================================================================
    if order == 'shuffle':
        np.random.shuffle(colores)
    
    # ========================================================================
    # ASIGNAR COLOR A CADA REGIÓN
    # ========================================================================
    for i, etiqueta in enumerate(etiquetas):
        mascara = (L == etiqueta)
        RGB[mascara] = colores[i]
    
    return RGB

def regionprops(L, properties=None):
    """
    Calcula propiedades geométricas de regiones etiquetadas.

    Parámetros
    ----------
    L : ndarray
        Parámetro L.
    properties : objeto
        Parámetro properties.

    Retorna
    -------
    out : objeto
        Resultado de regionprops.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = regionprops(L, properties)
    """
    
    if properties is None:
        properties = ['Area', 'Centroid', 'BoundingBox']
    elif isinstance(properties, str):
        properties = [properties]
    
    # Normalizar nombres de propiedades
    properties = [prop.lower() for prop in properties]
    
    # Obtener etiquetas únicas (excluyendo 0 que es el fondo)
    labels = np.unique(L)
    labels = labels[labels > 0]
    
    if len(labels) == 0:
        return []
    
    stats = []
    
    for label in labels:
        mask = (L == label)
        region_props = {}
        
        # Obtener coordenadas de píxeles en la región
        rows, cols = np.where(mask)
        
        # Area
        if 'area' in properties or 'equivdiameter' in properties or 'extent' in properties or 'circularity' in properties:
            area = len(rows)
            region_props['Area'] = area
        
        # Centroid
        if any(prop in properties for prop in ['centroid', 'majoraxislength', 'minoraxislength', 'orientation', 'eccentricity']):
            cx = np.mean(cols)
            cy = np.mean(rows)
            region_props['Centroid'] = [cx, cy]
        
        # BoundingBox
        if 'boundingbox' in properties or 'extent' in properties:
            x_min = np.min(cols) - 0.5
            y_min = np.min(rows) - 0.5
            width = np.max(cols) - np.min(cols) + 1
            height = np.max(rows) - np.min(rows) + 1
            region_props['BoundingBox'] = [x_min, y_min, width, height]
        
        # Perimeter
        if 'perimeter' in properties or 'circularity' in properties:
            perimeter = _calculate_perimeter_chain8(mask)
            region_props['Perimeter'] = perimeter
        
        # Propiedades de elipse (momentos de segundo orden)
        if any(prop in properties for prop in ['majoraxislength', 'minoraxislength', 'orientation', 'eccentricity']):
            maj, min_axis, ori, ecc = _calculate_ellipse_properties_v2(rows, cols, cx, cy)
            if 'majoraxislength' in properties:
                region_props['MajorAxisLength'] = maj
            if 'minoraxislength' in properties:
                region_props['MinorAxisLength'] = min_axis
            if 'orientation' in properties:
                region_props['Orientation'] = ori
            if 'eccentricity' in properties:
                region_props['Eccentricity'] = ecc
        
        # EquivDiameter
        if 'equivdiameter' in properties:
            equiv_diameter = np.sqrt(4 * area / np.pi)
            region_props['EquivDiameter'] = equiv_diameter
        
        # Extent
        if 'extent' in properties:
            if 'BoundingBox' not in region_props:
                width = np.max(cols) - np.min(cols) + 1
                height = np.max(rows) - np.min(rows) + 1
            else:
                width = region_props['BoundingBox'][2]
                height = region_props['BoundingBox'][3]
            
            if width > 0 and height > 0:
                extent = area / (width * height)
            else:
                extent = 0
            region_props['Extent'] = extent
        
        # Circularity
        if 'circularity' in properties:
            if 'Perimeter' not in region_props:
                perimeter = _calculate_perimeter_chain8(mask)
            else:
                perimeter = region_props['Perimeter']
            
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter ** 2)
            else:
                circularity = 0
            region_props['Circularity'] = circularity
        
        # ConvexHull y ConvexArea
        if 'convexhull' in properties or 'convexarea' in properties:
            points = np.column_stack([cols, rows])  # [x, y]
            convex_hull = _convex_hull_andrew(points)
            
            if 'convexhull' in properties:
                region_props['ConvexHull'] = convex_hull
            if 'convexarea' in properties:
                convex_area = _polygon_area_shoelace(convex_hull)
                region_props['ConvexArea'] = convex_area
        
        stats.append(region_props)
    
    return stats




# ====================================================================
#  Transformada de Hough y Detección de Círculos/Líneas
# ====================================================================

def hough(BW, Theta=None, RhoResolution=1):
    """
    Calcula la transformada de Hough para líneas.

    Parámetros
    ----------
    BW : ndarray
        Parámetro BW.
    Theta : objeto
        Parámetro Theta.
    RhoResolution : objeto
        Parámetro RhoResolution.

    Retorna
    -------
    out : objeto
        Resultado de hough.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = hough(BW, Theta, RhoResolution)
    """
    BW = np.asarray(BW)
    if Theta is None:
        theta = np.arange(-90, 90, dtype=float)  # -90:89 (180 muestras)
    else:
        theta = np.asarray(Theta, dtype=float).ravel()
    if not np.isscalar(RhoResolution) or RhoResolution <= 0:
        raise ValueError("RhoResolution debe ser escalar positivo")

    Hpix, Wpix = BW.shape[:2]

    # Rango máximo de rho (diagonal) con origen en (0,0): x∈[0,W-1], y∈[0,H-1]
    rhomax = int(np.ceil(np.hypot(Wpix - 1, Hpix - 1)))
    rho = np.arange(-rhomax, rhomax + RhoResolution, RhoResolution, dtype=float)

    # Precompute cos/sin en radianes
    th_rad = np.deg2rad(theta)
    ct = np.cos(th_rad)
    st = np.sin(th_rad)

    # Acumulador
    H = np.zeros((rho.size, theta.size), dtype=np.int32)

    rho_min = rho[0]
    inv_dr  = 1.0 / float(RhoResolution)

    # Bucles for explícitos (fila→i, col→j, ángulo→t)
    for i in range(Hpix):          # i = fila (y)
        for j in range(Wpix):      # j = columna (x)
            if BW[i, j] != 0:
                # Coordenadas con origen en (0,0) en la esquina superior izquierda
                y = float(i - 1)
                x = float(j - 1)
                for t in range(theta.size):
                    r = x * ct[t] + y * st[t]                     # rho(θ)
                    # Índice de bin en rho (desplazado a [0..len(rho)-1])
                    ri = int(np.rint((r - rho_min) * inv_dr))
                    # Clampeo de seguridad (por posibles redondeos en borde)
                    if 0 <= ri < rho.size:
                        H[ri, t] += 1

    return H, theta, rho


def houghpeaks(H, numpeaks, *, Threshold=None, NHoodSize=None):
    """
    Localiza picos en el espacio de Hough.

    Parámetros
    ----------
    H : ndarray
        Parámetro H.
    numpeaks : objeto
        Parámetro numpeaks.
     : tuple
        Argumentos variables para houghpeaks.
    Threshold : objeto
        Parámetro Threshold.
    NHoodSize : objeto
        Parámetro NHoodSize.

    Retorna
    -------
    out : objeto
        Resultado de houghpeaks.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = houghpeaks(H, numpeaks, *, Threshold, NHoodSize)
    """
    H = np.asarray(H, dtype=float)
    nr, nt = H.shape

    # Umbral por defecto
    if Threshold is None:
        # Si H está vacío o todo a 0, max será 0
        maxH = np.nanmax(H) if np.isfinite(H).any() else 0.0
        Threshold = 0.5 * maxH

    # NHoodSize por defecto: ceil(size/50)*2 + 1 (siempre impar)
    if NHoodSize is None:
        def odd_from(n):
            k = int(np.ceil(n / 50.0))
            return 2 * k + 1
        NHoodSize = (odd_from(nr), odd_from(nt))
    else:
        # Forzar a impares si vinieron pares
        rsz, csz = int(NHoodSize[0]), int(NHoodSize[1])
        if rsz % 2 == 0: rsz += 1
        if csz % 2 == 0: csz += 1
        NHoodSize = (rsz, csz)

    # Copia de trabajo del acumulador
    Hwork = H.copy()

    peaks = []
    hr = (NHoodSize[0] - 1) // 2
    hc = (NHoodSize[1] - 1) // 2

    for _ in range(int(numpeaks)):
        # Máximo global actual
        idx = np.nanargmax(Hwork) if np.isfinite(Hwork).any() else 0
        val = Hwork.flat[idx]

        # Parada si por debajo del umbral o si todo es 0/NaN
        if not np.isfinite(val) or val < Threshold:
            break

        r, c = np.unravel_index(idx, Hwork.shape)
        peaks.append([r, c])

        # Supresión de vecindad centrada en (r,c)
        r0 = max(0, r - hr); r1 = min(nr, r + hr + 1)
        c0 = max(0, c - hc); c1 = min(nt, c + hc + 1)
        Hwork[r0:r1, c0:c1] = 0.0  # suprimir

    if len(peaks) == 0:
        return np.zeros((0, 2), dtype=int)
    return np.array(peaks, dtype=int)
    
    
    
import numpy as np

def houghlines(BW, theta, rho, picos, FillGap=20, MinLength=40):
    """
    Extrae segmentos de línea a partir de picos de Hough.

    Parámetros
    ----------
    BW : ndarray
        Parámetro BW.
    theta : objeto
        Parámetro theta.
    rho : objeto
        Parámetro rho.
    picos : objeto
        Parámetro picos.
    FillGap : objeto
        Parámetro FillGap.
    MinLength : objeto
        Parámetro MinLength.

    Retorna
    -------
    out : objeto
        Resultado de houghlines.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = houghlines(BW, theta, rho, picos, FillGap, MinLength)
    """
    lineas = []
    altura, ancho = BW.shape
    tolerancia = 1.5
    
    # Obtener coordenadas de pixeles blancos
    filas, cols = np.where(BW == True)
    pixeles_borde = np.column_stack([cols, filas])  # [x, y]
    
    if len(pixeles_borde) == 0:
        return lineas
    
    # Procesar cada pico detectado
    for r_idx, c_idx in picos:
        theta_val = theta[c_idx]
        rho_val = rho[r_idx]
        
        # Convertir a radianes
        theta_rad = np.deg2rad(theta_val)
        cos_t = np.cos(theta_rad)
        sin_t = np.sin(theta_rad)
        
        # Encontrar pixeles cercanos a la linea: |x*cos + y*sin - rho| < tolerancia
        distancias = np.abs(pixeles_borde[:, 0] * cos_t + 
                           pixeles_borde[:, 1] * sin_t - rho_val)
        pixeles_linea = pixeles_borde[distancias < tolerancia]
        
        if len(pixeles_linea) == 0:
            continue
        
        # Proyectar pixeles sobre direccion de la linea
        direccion_x = -sin_t
        direccion_y = cos_t
        parametros_t = (pixeles_linea[:, 0] * direccion_x + 
                       pixeles_linea[:, 1] * direccion_y)
        
        # Ordenar pixeles por parametro t
        indices = np.argsort(parametros_t)
        pixeles_ordenados = pixeles_linea[indices]
        
        # Detectar segmentos por brechas (codigo inline)
        if len(pixeles_ordenados) == 0:
            continue
            
        segmentos = []
        segmento_actual = [pixeles_ordenados[0]]
        
        for i in range(1, len(pixeles_ordenados)):
            # Distancia entre pixeles consecutivos
            dist = np.sqrt((pixeles_ordenados[i][0] - pixeles_ordenados[i-1][0])**2 + 
                          (pixeles_ordenados[i][1] - pixeles_ordenados[i-1][1])**2)
            
            if dist <= FillGap:
                segmento_actual.append(pixeles_ordenados[i])
            else:
                if len(segmento_actual) > 1:
                    segmentos.append(np.array(segmento_actual))
                segmento_actual = [pixeles_ordenados[i]]
        
        # Agregar ultimo segmento
        if len(segmento_actual) > 1:
            segmentos.append(np.array(segmento_actual))
        
        # Filtrar por longitud minima
        for segmento in segmentos:
            if len(segmento) >= 2:
                punto1 = segmento[0]
                punto2 = segmento[-1]
                
                # Calcular longitud
                dist = np.sqrt((punto2[0] - punto1[0])**2 + 
                              (punto2[1] - punto1[1])**2)
                
                if dist >= MinLength:
                    linea = {
                        'point1': punto1.tolist(),
                        'point2': punto2.tolist(),
                        'theta': theta_val,
                        'rho': rho_val
                    }
                    lineas.append(linea)
    
    return lineas
    
    
def imfindcircles(BW, radius_range, Method='PhaseCode', ObjectPolarity='bright', Sensitivity=0.85, EdgeThreshold=None):
    """
    Encuentra círculos en IMAGEN BINARIA usando Transformada de Hough circular.
    Versión simplificada - SOLO NumPy, sin dependencias de scipy.
    
    Parámetros:
    -----------
    BW : ndarray (bool)
        Imagen binaria con bordes en blanco
    radius_range : tuple [Rmin, Rmax]
        Rango de radios a buscar en píxeles
    ObjectPolarity : str
        'bright' - bordes blancos (default)
        'dark' - bordes negros (invierte imagen)
    Sensitivity : float
        Sensibilidad [0,1]. Mayor valor = más círculos. Default: 0.85
    
    Retorna:
    --------
    centers : ndarray (N x 2) - Coordenadas [x, y]
    radii : ndarray (N,) - Radios
    metric : ndarray (N,) - Calidad [0,1]
    """
    
    # Convertir a binaria si no lo es
    if BW.dtype != bool:
        BW = BW.astype(bool)
    
    # Invertir si buscamos bordes oscuros
    if ObjectPolarity.lower() == 'dark':
        BW = ~BW
    
    print("Procesando imagen binaria (solo NumPy)...")
    
    # Obtener píxeles de borde (blancos)
    edge_y, edge_x = np.where(BW)
    num_pixels = len(edge_x)
    
    print(f"Píxeles de borde: {num_pixels}")
    
    if num_pixels == 0:
        return np.zeros((0, 2)), np.array([]), np.array([])
    
    # Parámetros de radios
    Rmin, Rmax = int(radius_range[0]), int(radius_range[1])
    M, N = BW.shape
    
    # Radios a evaluar
    radii_test = np.arange(Rmin, Rmax + 1)
    print(f"Evaluando {len(radii_test)} radios: {Rmin} a {Rmax}")
    
    # Acumulador 3D: [filas, columnas, radios]
    H = np.zeros((M, N, len(radii_test)), dtype=np.int32)
    
    # Votación: círculos alrededor de cada píxel de borde
    print("Votando en acumulador...")
    
    # Ángulos para círculos (cada 5 grados = 72 puntos)
    thetas = np.linspace(0, 2*np.pi, 72)
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    
    # Votar por cada píxel de borde
    for i in range(num_pixels):
        x = edge_x[i]
        y = edge_y[i]
        
        # Para cada radio
        for r_idx, r in enumerate(radii_test):
            # Votar en todos los posibles centros a distancia r
            for cos_theta, sin_theta in zip(cos_t, sin_t):
                cx = int(round(x + r * cos_theta))
                cy = int(round(y + r * sin_theta))
                
                # Votar si está dentro de límites
                if 0 <= cx < N and 0 <= cy < M:
                    H[cy, cx, r_idx] += 1
    
    print("Buscando picos...")
    
    # Normalizar acumulador [0, 1]
    H_max = np.max(H)
    if H_max == 0:
        return np.zeros((0, 2)), np.array([]), np.array([])
    
    H_norm = H.astype(np.float32) / H_max
    
    # Umbral basado en sensibilidad
    threshold = (1 - Sensitivity) * 0.5
    
    # Encontrar picos (máximos locales)
    centers_list = []
    radii_list = []
    metric_list = []
    
    nhood = 7  # Tamaño de vecindad para supresión no-máxima
    
    for r_idx, r in enumerate(radii_test):
        H_slice = H_norm[:, :, r_idx]
        
        # Buscar máximos locales
        for y in range(nhood, M - nhood):
            for x in range(nhood, N - nhood):
                val = H_slice[y, x]
                
                if val < threshold:
                    continue
                
                # Verificar si es máximo en vecindad
                vecindad = H_slice[y-nhood:y+nhood+1, x-nhood:x+nhood+1]
                
                if val >= np.max(vecindad):
                    centers_list.append([x, y])
                    radii_list.append(r)
                    metric_list.append(val)
    
    if len(centers_list) == 0:
        print("No se encontraron círculos")
        return np.zeros((0, 2)), np.array([]), np.array([])
    
    print(f"Picos encontrados: {len(centers_list)}")
    
    # Convertir a arrays
    centers = np.array(centers_list, dtype=np.float64)
    radii = np.array(radii_list, dtype=np.float64)
    metric = np.array(metric_list, dtype=np.float64)
    
    # Eliminar duplicados cercanos
    keep = []
    for i in range(len(centers)):
        duplicado = False
        for j in keep:
            dist = np.sqrt((centers[i,0] - centers[j,0])**2 + 
                          (centers[i,1] - centers[j,1])**2)
            rad_diff = abs(radii[i] - radii[j])
            
            # Si están muy cerca con radios similares, es duplicado
            if dist < 20 and rad_diff < 10:
                # Quedarse con el de mejor métrica
                if metric[i] > metric[j]:
                    keep.remove(j)
                    keep.append(i)
                duplicado = True
                break
        
        if not duplicado:
            keep.append(i)
    
    # Filtrar duplicados
    centers = centers[keep]
    radii = radii[keep]
    metric = metric[keep]
    
    # Ordenar por métrica (mejores primero)
    idx = np.argsort(metric)[::-1]
    
    print(f"Círculos únicos detectados: {len(centers)}")
    
    return centers[idx], radii[idx], metric[idx]
#-------------------------------------------------------------
def viscircles(centers, radii, ax=None, Color='blue', LineWidth=2, LineStyle='-', EnhanceVisibility=False):
    """
    Dibuja círculos en ejes de Matplotlib.
    Compatible con MATLAB viscircles.
    
    Parámetros:
    -----------
    centers : ndarray (N x 2)
        Coordenadas [x, y] de los centros
    radii : ndarray (N,) o list
        Radios de los círculos
    ax : matplotlib axes, opcional
        Ejes donde dibujar. Si None, usa plt.gca()
    Color : str o tuple, opcional
        Color de línea. Default: 'blue'
    LineWidth : float, opcional
        Grosor de línea. Default: 2
    LineStyle : str, opcional
        Estilo de línea ('-', '--', ':', '-.'). Default: '-'
    EnhanceVisibility : bool, opcional
        Si True, dibuja borde blanco adicional. Default: False
    
    Retorna:
    --------
    handles : list
        Lista de objetos Line2D creados
    
    Ejemplo:
    --------
    >>> centers = np.array([[100, 150], [200, 250]])
    >>> radii = np.array([50, 60])
    >>> viscircles(centers, radii, Color='red', LineWidth=3)
    """
    
    # Obtener ejes actuales si no se especifican
    if ax is None:
        ax = plt.gca()
    
    # Convertir a arrays si no lo son
    centers = np.atleast_2d(centers)
    radii = np.atleast_1d(radii)
    
    # Verificar dimensiones
    if centers.shape[1] != 2:
        raise ValueError("centers debe ser Nx2 (coordenadas x,y)")
    
    if len(radii) != len(centers):
        raise ValueError("radii debe tener la misma longitud que centers")
    
    # Ángulos para dibujar círculos
    theta = np.linspace(0, 2*np.pi, 100)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    handles = []
    
    # Dibujar cada círculo
    for i in range(len(centers)):
        cx, cy = centers[i]
        r = radii[i]
        
        # Coordenadas del círculo
        x = cx + r * cos_theta
        y = cy + r * sin_theta
        
        # Borde blanco para visibilidad (si está habilitado)
        if EnhanceVisibility:
            h_white = ax.plot(x, y, color='white', 
                            linewidth=LineWidth + 2,
                            linestyle=LineStyle,
                            zorder=1)[0]
        
        # Círculo principal
        h = ax.plot(x, y, color=Color, 
                   linewidth=LineWidth,
                   linestyle=LineStyle,
                   zorder=2)[0]
        
        handles.append(h)
    
    return handles
    


# ====================================================================
#  Transformada de Fourier
# ====================================================================

def fft(X, n: int | None = None, dim: int | None = None):
    """
    Función fft de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    X : objeto
        Parámetro X.
    n: int | None : objeto
        Parámetro n: int | None.
    dim: int | None : objeto
        Parámetro dim: int | None.

    Retorna
    -------
    out : objeto
        Resultado de fft.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = fft(X, n: int | None, dim: int | None)
    """
    X = np.asarray(X)
    if dim is None:
        dim = _first_nontrivial_dim(X)
    if n is not None:
        if not (isinstance(n, (int, np.integer)) and n >= 0):
            raise ValueError("fft: 'n' debe ser entero no negativo o None.")
    return np.fft.fft(X, n=n, axis=dim)


def ifft(X, n: int | None = None, dim: int | None = None):
    """
    Función ifft de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    X : objeto
        Parámetro X.
    n: int | None : objeto
        Parámetro n: int | None.
    dim: int | None : objeto
        Parámetro dim: int | None.

    Retorna
    -------
    out : objeto
        Resultado de ifft.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = ifft(X, n: int | None, dim: int | None)
    """
    X = np.asarray(X)
    if dim is None:
        dim = _first_nontrivial_dim(X)
    if n is not None:
        if not (isinstance(n, (int, np.integer)) and n >= 0):
            raise ValueError("ifft: 'n' debe ser entero no negativo o None.")
    return np.fft.ifft(X, n=n, axis=dim)


# ------------------------------------------------------------
# FFT / IFFT 2D (firmas MATLAB, sobre primeras 2 dimensiones)
# ------------------------------------------------------------
def fft2(X, M: int | None = None, N: int | None = None):
    """
    Función fft2 de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    X : objeto
        Parámetro X.
    M: int | None : objeto
        Parámetro M: int | None.
    N: int | None : objeto
        Parámetro N: int | None.

    Retorna
    -------
    out : objeto
        Resultado de fft2.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = fft2(X, M: int | None, N: int | None)
    """
    X = np.asarray(X)
    if X.ndim < 2:
        # MATLAB permite fft2 sobre vectores tratándolos como (M x 1) o (1 x N);
        # aquí exigimos al menos 2D para claridad; el usuario puede usar fft().
        X = np.atleast_2d(X)
    s = _matlab_fft2_shape(X, M, N)
    return np.fft.fft2(X, s=s, axes=(0, 1))


def ifft2(X, M: int | None = None, N: int | None = None):
    """
    Función ifft2 de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    X : objeto
        Parámetro X.
    M: int | None : objeto
        Parámetro M: int | None.
    N: int | None : objeto
        Parámetro N: int | None.

    Retorna
    -------
    out : objeto
        Resultado de ifft2.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = ifft2(X, M: int | None, N: int | None)
    """
    X = np.asarray(X)
    if X.ndim < 2:
        X = np.atleast_2d(X)
    s = _matlab_fft2_shape(X, M, N)
    return np.fft.ifft2(X, s=s, axes=(0, 1))


# ------------------------------------------------------------
# Centrados (idénticos a MATLAB para pares e impares)
# ------------------------------------------------------------
def fftshift(X, axes=None):
    """
    Función fftshift de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    X : objeto
        Parámetro X.
    axes : objeto
        Parámetro axes.

    Retorna
    -------
    out : objeto
        Resultado de fftshift.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = fftshift(X, axes)
    """
    X = np.asarray(X)
    if axes is None:
        axes = tuple(range(X.ndim))
    elif np.isscalar(axes):
        axes = (int(axes),)
    else:
        axes = tuple(int(ax) for ax in axes)

    Y = X
    for ax in axes:
        n = Y.shape[ax]
        if n > 1:
            Y = np.roll(Y, n // 2, axis=ax)  # +floor(n/2)
    return Y


def ifftshift(X, axes=None):
    """
    Función ifftshift de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    X : objeto
        Parámetro X.
    axes : objeto
        Parámetro axes.

    Retorna
    -------
    out : objeto
        Resultado de ifftshift.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = ifftshift(X, axes)
    """
    X = np.asarray(X)
    if axes is None:
        axes = tuple(range(X.ndim))
    elif np.isscalar(axes):
        axes = (int(axes),)
    else:
        axes = tuple(int(ax) for ax in axes)

    Y = X
    for ax in axes:
        n = Y.shape[ax]
        if n > 1:
            Y = np.roll(Y, (n + 1) // 2, axis=ax)  # +ceil(n/2)
    return Y



# ====================================================================
#  TRANSFORMADAS DE FOURIER
# ====================================================================

def dft(x):
    """
    Transformada Discreta de Fourier (DFT) 1-D.
    
    Calcula la DFT directa mediante la fórmula:
    F[k] = sum_{n=0}^{N-1} x[n] * exp(-j*2*pi*k*n/N)
    
    Parámetros
    ----------
    x : array_like
        Señal de entrada en el dominio del tiempo.
        
    Retorna
    -------
    np.ndarray
        Transformada de Fourier de la señal de entrada (dominio de la frecuencia).
        
    Notas
    -----
    Esta implementación utiliza multiplicación matricial directa y tiene
    complejidad O(N²). Para señales largas, FFT es más eficiente O(N log N).
    """
    x = np.asarray(x, dtype=complex).ravel()
    N = x.size
    n = np.arange(N)
    k = n.reshape(N, 1)
    W = np.exp(-1j * 2 * np.pi * k * n / N)
    return W @ x


def idft(X):
    """
    Transformada Inversa Discreta de Fourier (IDFT) 1-D.
    
    Calcula la IDFT mediante la fórmula:
    x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * exp(+j*2*pi*k*n/N)
    
    Parámetros
    ----------
    X : array_like
        Señal de entrada en el dominio de la frecuencia.
        
    Retorna
    -------
    np.ndarray
        Señal reconstruida en el dominio del tiempo.
        
    Notas
    -----
    La IDFT es esencialmente la DFT con exponencial conjugada y
    normalización por 1/N.
    """
    X = np.asarray(X, dtype=complex).ravel()
    N = X.size
    n = np.arange(N)
    k = n.reshape(N, 1)
    Wc = np.exp(+1j * 2 * np.pi * k * n / N)
    return (Wc @ X) / N


# ====================================================================
#  UTILIDADES ESPECTRALES
# ====================================================================

def dftshift(X, axis=-1):
    """
    Desplaza el componente DC (frecuencia cero) al centro del espectro.
    
    Realiza un desplazamiento circular de +floor(N/2) posiciones, moviendo
    las componentes de frecuencia negativa a la primera mitad del array.
    
    Parámetros
    ----------
    X : array_like
        Espectro de entrada (resultado de DFT).
    axis : int, opcional
        Eje sobre el cual realizar el desplazamiento. Por defecto -1.
        
    Retorna
    -------
    np.ndarray
        Espectro con DC centrado.
        
    Notas
    -----
    Equivalente a np.fft.fftshift pero implementado sin dependencia de fft.
    """
    X = np.asarray(X)
    axis = int(axis) % X.ndim
    n = X.shape[axis]
    s = n // 2
    return np.roll(X, s, axis=axis)


def idftshift(X, axis=-1):
    """
    Operación inversa de dftshift.
    
    Realiza un desplazamiento circular de +ceil(N/2) posiciones para
    deshacer el efecto de dftshift.
    
    Parámetros
    ----------
    X : array_like
        Espectro con DC centrado.
    axis : int, opcional
        Eje sobre el cual realizar el desplazamiento. Por defecto -1.
        
    Retorna
    -------
    np.ndarray
        Espectro en formato estándar de DFT.
        
    Notas
    -----
    Equivalente a np.fft.ifftshift pero implementado sin dependencia de fft.
    """
    X = np.asarray(X)
    axis = int(axis) % X.ndim
    n = X.shape[axis]
    s = (n + 1) // 2
    return np.roll(X, s, axis=axis)


def dftfreq(n, d):
    """
    Calcula el eje de frecuencias correspondiente a una DFT.
    
    Genera el vector de frecuencias discretas asociado a una DFT de longitud n
    con periodo de muestreo d.
    
    Parámetros
    ----------
    n : int
        Longitud de la DFT (número de muestras).
    d : float
        Periodo de muestreo en segundos [s].
        
    Retorna
    -------
    np.ndarray
        Vector de frecuencias en Hz. Las frecuencias negativas aparecen
        en la segunda mitad del array.
        
    Notas
    -----
    El rango de frecuencias va de -fs/2 a fs/2 donde fs = 1/d es la
    frecuencia de muestreo. Equivalente a np.fft.fftfreq.
    """
    k = np.arange(n)
    val = 1.0 / (n * d)
    out = k.astype(float)
    mask = k > (n // 2)
    out[mask] = out[mask] - n
    return out * val


# ====================================================================
#  DCT / IDCT (Transformada Discreta del Coseno)
# ====================================================================

def dct(x, n=None, dim=None):
    """
    Transformada Discreta del Coseno tipo II (DCT-II).
    Compatible con MATLAB dct().
    
    Parámetros
    ----------
    x : array_like
        Señal de entrada (real).
    n : int, opcional
        Longitud de salida (pad/trunca si difiere de len(x)).
    dim : int, opcional
        Dimensión a transformar (default: primera dim > 1).
        
    Retorna
    -------
    ndarray
        Coeficientes DCT.
        
    Ejemplo
    -------
    >>> x = np.array([1, 2, 3, 4])
    >>> C = dct(x)
    >>> x_rec = idct(C)
    """
    x = np.asarray(x, dtype=np.float64)
    
    if dim is None:
        dim = _first_nontrivial_dim(x)
    
    if n is not None:
        x = _pad_or_truncate(x, n, dim)
    
    # Mover dim al final
    x = np.moveaxis(x, dim, -1)
    N = x.shape[-1]
    
    if N == 0:
        return np.moveaxis(x, -1, dim)
    
    # Extensión par: [x, flip(x)]
    y = np.concatenate([x, x[..., ::-1]], axis=-1)
    
    # FFT y corrección de fase
    Y = fft(y, n=2*N, dim=-1)[..., :N]
    k = np.arange(N, dtype=np.float64)
    w = np.exp(-1j * np.pi * k / (2.0 * N))
    C = 0.5 * np.real(Y * w)
    
    # Normalización ortonormal
    alpha = np.sqrt(2.0 / N)
    C *= alpha
    C[..., 0] /= np.sqrt(2.0)
    
    return np.moveaxis(C, -1, dim)


def idct(C, n=None, dim=None):
    """
    Transformada Inversa Discreta del Coseno (IDCT).
    Compatible con MATLAB idct().
    
    Parámetros
    ----------
    C : array_like
        Coeficientes DCT (real).
    n : int, opcional
        Longitud de salida.
    dim : int, opcional
        Dimensión a transformar.
        
    Retorna
    -------
    ndarray
        Señal reconstruida.
        
    Ejemplo
    -------
    >>> C = dct(x)
    >>> x_rec = idct(C)
    """
    C = np.asarray(C, dtype=np.float64)
    
    if dim is None:
        dim = _first_nontrivial_dim(C)
    
    if n is not None:
        C = _pad_or_truncate(C, n, dim)
    
    C = np.moveaxis(C, dim, -1)
    N = C.shape[-1]
    
    if N == 0:
        return np.moveaxis(C, -1, dim)
    
    # Desnormalizar
    ctilde = C.copy()
    ctilde[..., 0] *= np.sqrt(2.0)
    ctilde /= np.sqrt(2.0 / N)
    
    # Construir espectro para IFFT
    k = np.arange(N, dtype=np.float64)
    Y = np.zeros(C.shape[:-1] + (2*N,), dtype=np.complex128)
    Y[..., :N] = 2.0 * ctilde * np.exp(1j * np.pi * k / (2.0 * N))
    Y[..., N] = 0.0
    if N > 1:
        Y[..., N+1:] = np.conj(Y[..., 1:N][..., ::-1])
    
    # IFFT
    x = np.real(ifft(Y, n=2*N, dim=-1)[..., :N])
    
    return np.moveaxis(x, -1, dim)


def dct2(X, m=None, n=None):
    """
    Transformada Discreta del Coseno 2D (DCT2).
    Compatible con MATLAB dct2().
    
    Parámetros
    ----------
    X : array_like
        Imagen de entrada (real).
    m : int, opcional
        Número de filas.
    n : int, opcional
        Número de columnas.
        
    Retorna
    -------
    ndarray
        Coeficientes DCT 2D.
        
    Ejemplo
    -------
    >>> img = np.random.rand(8, 8)
    >>> C = dct2(img)
    >>> img_rec = idct2(C)
    """
    X = np.asarray(X, dtype=np.float64)
    if X.ndim < 2:
        X = np.atleast_2d(X)
    
    if m is not None:
        X = _pad_or_truncate(X, m, axis=0)
    if n is not None:
        X = _pad_or_truncate(X, n, axis=1)
    
    # DCT separable
    C = dct(X, dim=0)
    C = dct(C, dim=1)
    return C


def idct2(C, m=None, n=None):
    """
    Transformada Inversa Discreta del Coseno 2D (IDCT2).
    Compatible con MATLAB idct2().
    
    Parámetros
    ----------
    C : array_like
        Coeficientes DCT 2D (real).
    m : int, opcional
        Número de filas.
    n : int, opcional
        Número de columnas.
        
    Retorna
    -------
    ndarray
        Imagen reconstruida.
        
    Ejemplo
    -------
    >>> C = dct2(img)
    >>> img_rec = idct2(C)
    """
    C = np.asarray(C, dtype=np.float64)
    if C.ndim < 2:
        C = np.atleast_2d(C)
    
    if m is not None:
        C = _pad_or_truncate(C, m, axis=0)
    if n is not None:
        C = _pad_or_truncate(C, n, axis=1)
    
    # IDCT separable
    X = idct(C, dim=1)
    X = idct(X, dim=0)
    return X


# ====================================================================
#  Función auxiliar ( necesaria)
# ====================================================================

def _pad_or_truncate(X, n, axis):
    """Pad con ceros o trunca X a longitud n sobre eje axis."""
    axis = axis % X.ndim
    cur = X.shape[axis]
    
    if n == cur:
        return X
    if n < cur:
        slices = [slice(None)] * X.ndim
        slices[axis] = slice(0, n)
        return X[tuple(slices)]
    
    pad_width = [(0, 0)] * X.ndim
    pad_width[axis] = (0, n - cur)
    return np.pad(X, pad_width, mode='constant', constant_values=0)




# ====================================================================
#  Restauración y Métricas de Calidad
# ====================================================================

def deconvwnr(I, psf, nsr):
    """
    Función deconvwnr de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    psf : ndarray
        Parámetro psf.
    nsr : objeto
        Parámetro nsr.

    Retorna
    -------
    out : objeto
        Resultado de deconvwnr.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = deconvwnr(I, psf, nsr)
    """
    
    # Validación y conversión de tipos
    I = np.asarray(I, dtype=np.float64)
    psf = np.asarray(psf, dtype=np.float64)
    
    if I.ndim != 2 or psf.ndim != 2:
        raise ValueError("La imagen y la PSF deben ser bidimensionales")
    if not np.isscalar(nsr) or nsr < 0:
        raise ValueError("NSR debe ser un escalar no negativo")
    
    # Obtener dimensiones originales
    M, N = I.shape
    P, Q = psf.shape
    
    # Calcular dimensiones del padding mínimo (convolución lineal)
    # Sección 1.6.2.1 página 21: L >= M+P-1, K >= N+Q-1
    L = M + P - 1
    K = N + Q - 1
    
    # Alineación de la PSF: centrar en el origen para eliminar rampa de fase
    # Sección 1.6.4 paso 4 página 23
    a = P // 2
    b = Q // 2
    psf_aligned = np.roll(psf, shift=(-a, -b), axis=(0, 1))
    
    # Transformadas de Fourier con padding implícito
    G = fft2(I, L, K)              # Espectro imagen degradada
    H = fft2(psf_aligned, L, K)    # Función de transferencia del sistema
    
    # Construcción del filtro de Wiener
    # Sección 1.7.2.1 página 29: W(u,v) = H*/(|H|² + NSR)
    H_conj = np.conj(H)
    H_mag2 = np.abs(H) ** 2
    W = H_conj / (H_mag2 + nsr)
    
    # Aplicar filtrado en frecuencia
    F_est = W * G
    
    # Transformada inversa al dominio espacial
    f_full = np.real(ifft2(F_est))
    
    # Recorte a dimensiones originales usando imcrop
    # Sección 1.6.4 paso 7 página 23: extraer región MxN desde posición (a,b)
    f_est = imcrop(f_full, x=b, y=a, w=N, h=M)
    
    return f_est

    #-------------------------------------------------------------

def immse(Iref, I):
    """
    Calcula el error cuadrático medio (MSE) entre dos imágenes.

    Parámetros
    ----------
    Iref : objeto
        Parámetro Iref.
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : float
        Resultado de immse.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = immse(Iref, I)
    """
    # Asegurarse de que Iref e I sean del mismo tamaño y en formato float
    I1 = np.array(Iref, dtype=float)
    I2 = np.array(I, dtype=float)
    
    # Calcular el número total de píxeles en una sola vez
    num_pixels = I1.shape[0] * I1.shape[1]
    
    # Calcular MSE por canal y luego promediar
    if I1.ndim == 3:  # Imagen en RGB
        mse_R = np.sum((I1[:, :, 0] - I2[:, :, 0]) ** 2) / num_pixels
        mse_G = np.sum((I1[:, :, 1] - I2[:, :, 1]) ** 2) / num_pixels
        mse_B = np.sum((I1[:, :, 2] - I2[:, :, 2]) ** 2) / num_pixels
        MSE = (mse_R + mse_G + mse_B) / 3
    else:  # Imagen en escala de grises
        MSE = np.sum((I1 - I2) ** 2) / num_pixels
    
    return MSE


def psnr(Iref, I):
    """
    Calcula PSNR y SNR entre dos imágenes.

    Parámetros
    ----------
    Iref : objeto
        Parámetro Iref.
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : tuple[float, float]
        Resultado de psnr.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = psnr(Iref, I)
    """
    # Convertir las imágenes a float
    I2 = np.array(I, dtype=float)
    
    # Calcular el MSE
    A = immse(Iref, I)
    
    # Calcular PSNR
    max_pixel_value = 255.0
    psnr = 10 * np.log10((max_pixel_value ** 2) / A) if A != 0 else float('inf')
    
    # Calcular SNR
    Mean_noise = np.mean(I2 ** 2)
    snr = 10 * np.log10(Mean_noise / A) if A != 0 else float('inf')
    
    return psnr, snr


def ssim(A, ref):
    """
    Calcula el índice de similitud estructural (SSIM).

    Parámetros
    ----------
    A : ndarray
        Parámetro A.
    ref : ndarray
        Parámetro ref.

    Retorna
    -------
    out : float
        Resultado de ssim.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = ssim(A, ref)
    """
    A   = np.asarray(A)
    ref = np.asarray(ref)
    if A.shape != ref.shape:
        raise ValueError("ssim: A y ref deben tener las mismas dimensiones")

    # --- Selección de canales ---
    if A.ndim == 2:
        chans = [(A, ref)]
    elif A.ndim == 3 and A.shape[2] in (1, 3):
        if A.shape[2] == 1:
            chans = [(A[..., 0], ref[..., 0])]
        else:
            chans = [(A[..., c], ref[..., c]) for c in range(3)]
    else:
        raise ValueError("ssim: se admite 2D (grises) o 3D con 1 o 3 canales (RGB)")

    # --- Ventana gaussiana 11x11 (σ=1.5) ---
    win_size = 11
    sigma = 1.5
    w = fspecial('gaussian', win_size, sigma)  # suma=1
    m = win_size // 2

    # --- Constantes SSIM ---
    K1, K2 = 0.01, 0.03

    vals = []
    for Ac, Rc in chans:
        # Conversión a float64
        Ac = Ac.astype(np.float64, copy=False)
        Rc = Rc.astype(np.float64, copy=False)

        # Dynamic range L (inferido)
        if np.issubdtype(Ac.dtype, np.integer) or np.issubdtype(Rc.dtype, np.integer):
            # use el mayor rango representable de ambos tipos
            maxA = np.iinfo(Ac.dtype).max if np.issubdtype(Ac.dtype, np.integer) else 255
            maxR = np.iinfo(Rc.dtype).max if np.issubdtype(Rc.dtype, np.integer) else 255
            L = float(max(maxA, maxR))
        else:
            mx = float(max(Ac.max(), Rc.max()))
            L = 1.0 if mx <= 1.0 + 1e-12 else 255.0

        C1 = (K1 * L) ** 2
        C2 = (K2 * L) ** 2

        # Medias locales
        muA = imfilter(Ac, w, salida='same', tipodepad='replicate')
        muR = imfilter(Rc, w, salida='same', tipodepad='replicate')

        muA2 = muA * muA
        muR2 = muR * muR
        muAR = muA * muR

        # Energías y productos
        A2 = Ac * Ac
        R2 = Rc * Rc
        AR = Ac * Rc

        # Varianzas/covarianza locales
        sigmaA2 = imfilter(A2, w, salida='same', tipodepad='replicate') - muA2
        sigmaR2 = imfilter(R2, w, salida='same', tipodepad='replicate') - muR2
        sigmaAR = imfilter(AR, w, salida='same', tipodepad='replicate') - muAR

        # SSIM (forma compacta; equivalente a l*c*s con C3=C2/2)
        num = (2.0 * muAR + C1) * (2.0 * sigmaAR + C2)
        den = (muA2 + muR2 + C1) * (sigmaA2 + sigmaR2 + C2)
        ssim_map = num / (den + 1e-15)

        # Promedio 'valid'
        if Ac.shape[0] > win_size and Ac.shape[1] > win_size:
            vals.append(float(np.mean(ssim_map[m:-m, m:-m])))
        else:
            vals.append(float(np.mean(ssim_map)))

    return float(np.mean(vals))





# ====================================================================
# 🎲 Generación de Ruido
# ====================================================================

def imnoise(imagen, tipo, parametro1=None, parametro2=None):
    """
    Agrega diferentes tipos de ruido sintético a una imagen.

    Parámetros
    ----------
    imagen : ndarray
        Parámetro imagen.
    tipo : str
        Parámetro tipo.
    parametro1 : objeto
        Parámetro parametro1.
    parametro2 : objeto
        Parámetro parametro2.

    Retorna
    -------
    out : ndarray
        Resultado de imnoise.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = imnoise(imagen, tipo, parametro1, parametro2)
    """
    # Verificar argumentos mínimos
    if tipo is None:
        raise ValueError('Se requieren al menos dos argumentos: imagen y tipo de ruido')

    # Convertir tipo a minúsculas para comparación
    tipo = tipo.lower()

    # Validar tipo de ruido
    tipos_validos = ['gaussian', 'salt & pepper', 'speckle', 'poisson']
    if tipo not in tipos_validos:
        raise ValueError('Tipo de ruido no soportado. Use "salt & pepper", "gaussian", "speckle" o "poisson".')

    # Asignar valores por defecto según el tipo de ruido
    if tipo == 'gaussian':
        if parametro1 is None:
            parametro1 = 0  # Media por defecto
        if parametro2 is None:
            parametro2 = 0.01  # Varianza por defecto
    elif tipo == 'salt & pepper':
        if parametro1 is None:
            parametro1 = 0.05  # Densidad por defecto
    elif tipo == 'speckle':
        if parametro1 is None:
            parametro1 = 0.04  # Intensidad por defecto

    # Inicializar la imagen de salida
    In = imagen.astype(float)

    # Verificar si la imagen es en escala de grises o color (RGB)
    if len(imagen.shape) == 2:
        F, C = imagen.shape
        canales = 1
    elif len(imagen.shape) == 3:
        F, C, canales = imagen.shape
    else:
        raise ValueError('La imagen debe ser en escala de grises o RGB')

    # Aplicar el ruido según el tipo
    if tipo == 'salt & pepper':
        densidad = parametro1
        puntos = int(F * C * densidad)
        for ch in range(canales):
            coords = (np.random.randint(0, F, puntos), np.random.randint(0, C, puntos))
            if canales == 1:
                In[coords] = np.random.randint(0, 2, puntos) * 255
            else:
                In[coords[0], coords[1], ch] = np.random.randint(0, 2, puntos) * 255

    elif tipo == 'gaussian':
        media = parametro1
        varianza = parametro2
        ruido = media + np.sqrt(varianza) * np.random.randn(F, C, canales) if canales > 1 else media + np.sqrt(varianza) * np.random.randn(F, C)
        In += ruido

    elif tipo == 'speckle':
        intensidad = parametro1
        ruido = np.random.randn(F, C, canales) * intensidad if canales > 1 else np.random.randn(F, C) * intensidad
        In *= (1 + ruido)

    elif tipo == 'poisson':
        if canales == 1:
            In = np.random.poisson(In)
        else:
            for ch in range(canales):
                In[:, :, ch] = np.random.poisson(In[:, :, ch])

    # Limitar valores al rango [0, 255] y convertir a uint8
    In = np.clip(In, 0, 255).astype(np.uint8)
    
    return In





# ====================================================================
#  Utilidades Internas y Funciones Avanzadas
# ====================================================================

def non_overflowing_sum(a,b):
    """
    Función non_overflowing_sum de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    a : objeto
        Parámetro a.
    b : objeto
        Parámetro b.

    Retorna
    -------
    out : objeto
        Resultado de non_overflowing_sum.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = non_overflowing_sum(a, b)
    """
    c = np.uint16(a)+b
    c[np.where(c>255)] = 255
    c[np.where(c<0)] = 0
    return np.uint8(c)


def _slide_bool(A, B, op_any):
    """
    Función _slide_bool de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    A : ndarray
        Parámetro A.
    B : ndarray
        Parámetro B.
    op_any : objeto
        Parámetro op_any.

    Retorna
    -------
    out : objeto
        Resultado de _slide_bool.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _slide_bool(A, B, op_any)
    """
    A = A.astype(bool)
    B = B.astype(bool)
    m, n = B.shape
    rf = (m - 1) // 2
    cf = (n - 1) // 2

    M, N = A.shape
    out = np.zeros_like(A, dtype=bool)

    # Recorre sólo donde la ventana cabe completa (gracias al acolchado previo)
    for i in range(rf, M - rf):
        for j in range(cf, N - cf):
            win = A[i - rf:i + rf + 1, j - cf:j + cf + 1]
            if op_any:
                out[i, j] = np.any(win[B])
            else:
                out[i, j] = np.all(win[B])
    return out


def _non_maximum_suppression(magnitud, direccion):
    """
    Función _non_maximum_suppression de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    magnitud : objeto
        Parámetro magnitud.
    direccion : objeto
        Parámetro direccion.

    Retorna
    -------
    out : objeto
        Resultado de _non_maximum_suppression.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _non_maximum_suppression(magnitud, direccion)
    """
    M, N = magnitud.shape
    resultado = np.zeros((M, N), dtype=np.float64)
    
    # Normalizar direccion a [0, 180)
    direccion_norm = direccion % 180
    
    for i in range(1, M-1):
        for j in range(1, N-1):
            angulo = direccion_norm[i, j]
            mag = magnitud[i, j]
            
            # Cuantizar a 4 direcciones: 0, 45, 90, 135
            if (0 <= angulo < 22.5) or (157.5 <= angulo <= 180):
                v1, v2 = magnitud[i, j+1], magnitud[i, j-1]
            elif 22.5 <= angulo < 67.5:
                v1, v2 = magnitud[i-1, j+1], magnitud[i+1, j-1]
            elif 67.5 <= angulo < 112.5:
                v1, v2 = magnitud[i-1, j], magnitud[i+1, j]
            else:
                v1, v2 = magnitud[i-1, j-1], magnitud[i+1, j+1]
            
            if mag >= v1 and mag >= v2:
                resultado[i, j] = mag
    
    return resultado


def _hysteresis_threshold(imagen, T_low, T_high):
    """
    Función _hysteresis_threshold de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    imagen : ndarray
        Parámetro imagen.
    T_low : objeto
        Parámetro T_low.
    T_high : objeto
        Parámetro T_high.

    Retorna
    -------
    out : objeto
        Resultado de _hysteresis_threshold.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _hysteresis_threshold(imagen, T_low, T_high)
    """
    M, N = imagen.shape
    
    fuertes = imagen >= T_high
    debiles = (imagen >= T_low) & (imagen < T_high)
    
    BW = fuertes.copy()
    
    direcciones = [(-1,-1), (-1,0), (-1,1), 
                   (0,-1),          (0,1),
                   (1,-1),  (1,0),  (1,1)]
    
    cambio = True
    iteraciones = 0
    max_iter = M * N
    
    while cambio and iteraciones < max_iter:
        cambio = False
        iteraciones += 1
        
        for i in range(1, M-1):
            for j in range(1, N-1):
                if debiles[i, j] and not BW[i, j]:
                    for di, dj in direcciones:
                        if BW[i+di, j+dj]:
                            BW[i, j] = True
                            cambio = True
                            break
    
    return BW


def _detectar_cruces_cero(I):
    """
    Función _detectar_cruces_cero de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.

    Retorna
    -------
    out : objeto
        Resultado de _detectar_cruces_cero.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _detectar_cruces_cero(I)
    """
    M, N = I.shape
    BW = np.zeros((M, N), dtype=bool)
    
    for i in range(1, M-1):
        for j in range(1, N-1):
            vecindad = I[i-1:i+2, j-1:j+2]
            
            if np.any(vecindad > 0) and np.any(vecindad < 0):
                BW[i, j] = True
    
    return BW
import numpy as np

# ------------------------------------------------------------
# Utilidad: primera dimensión no trivial (MATLAB-compatible)
# ------------------------------------------------------------
def _first_nontrivial_dim(X: np.ndarray) -> int:
    """
    Función _first_nontrivial_dim de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    (sin parámetros)

    Retorna
    -------
    out : objeto
        Resultado de _first_nontrivial_dim.

    Ejemplo
    -------
    >>> out = _first_nontrivial_dim()
    """
    for k, n in enumerate(X.shape):
        if n > 1:
            return k
    return 0


# ------------------------------------------------------------
# FFT / IFFT 1D (firmas MATLAB)
# ------------------------------------------------------------
def _matlab_fft2_shape(X: np.ndarray, M: int | None, N: int | None) -> tuple | None:
    """
    Función _matlab_fft2_shape de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    (sin parámetros)

    Retorna
    -------
    out : objeto
        Resultado de _matlab_fft2_shape.

    Ejemplo
    -------
    >>> out = _matlab_fft2_shape()
    """
    if M is None and N is None:
        return None
    if M is not None and (not isinstance(M, (int, np.integer)) or M < 0):
        raise ValueError("fft2/ifft2: 'M' debe ser entero no negativo o None.")
    if N is not None and (not isinstance(N, (int, np.integer)) or N < 0):
        raise ValueError("fft2/ifft2: 'N' debe ser entero no negativo o None.")
    M_eff = X.shape[0] if M is None else int(M)
    N_eff = X.shape[1] if N is None else int(N)
    return (M_eff, N_eff)


def _calculate_perimeter_chain8(mask):
    """
    Función _calculate_perimeter_chain8 de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    mask : objeto
        Parámetro mask.

    Retorna
    -------
    out : objeto
        Resultado de _calculate_perimeter_chain8.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _calculate_perimeter_chain8(mask)
    """
    M, N = mask.shape
    
    # Encontrar punto inicial (primer píxel de borde)
    start_point = None
    for r in range(M):
        for c in range(N):
            if mask[r, c]:
                # Verificar si es píxel de borde
                is_border = (r == 0 or not mask[r-1, c] or 
                           r == M-1 or not mask[r+1, c] or
                           c == 0 or not mask[r, c-1] or 
                           c == N-1 or not mask[r, c+1])
                if is_border:
                    start_point = (r, c)
                    break
        if start_point:
            break
    
    if not start_point:
        return 0
    
    # Direcciones 8-conectadas: E, NE, N, NW, W, SW, S, SE
    dr = np.array([0, -1, -1, -1, 0, 1, 1, 1])
    dc = np.array([1, 1, 0, -1, -1, -1, 0, 1])
    
    r, c = start_point
    r0, c0 = start_point
    
    # Encontrar dirección inicial de backtrack
    prev_dir = -1
    for j in range(8):
        rr, cc = r + dr[j], c + dc[j]
        if rr < 0 or rr >= M or cc < 0 or cc >= N or not mask[rr, cc]:
            prev_dir = j
            break
    
    if prev_dir < 0:
        return 0
    
    n_cardinal = 0
    n_diagonal = 0
    max_iter = 8 * M * N
    iteration = 0
    
    while True:
        iteration += 1
        if iteration > max_iter:
            break
        
        found = False
        # Buscar siguiente píxel en sentido horario desde prev_dir+1
        for k in range(1, 9):
            direction = (prev_dir + k) % 8
            rr, cc = r + dr[direction], c + dc[direction]
            
            if 0 <= rr < M and 0 <= cc < N and mask[rr, cc]:
                # Clasificar paso como cardinal o diagonal
                if abs(dr[direction]) + abs(dc[direction]) == 1:
                    n_cardinal += 1
                else:
                    n_diagonal += 1
                
                prev_dir = (direction + 4) % 8  # Dirección opuesta para backtrack
                r, c = rr, cc
                found = True
                break
        
        if not found:
            # Componente de un solo píxel
            n_cardinal = 4
            n_diagonal = 0
            break
        
        # Verificar si hemos regresado al punto inicial
        if iteration > 1 and r == r0 and c == c0:
            break
    
    return n_cardinal + np.sqrt(2) * n_diagonal


def _calculate_ellipse_properties_v2(rows, cols, cx, cy):
    """
    Función _calculate_ellipse_properties de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    rows : objeto
        Parámetro rows.
    cols : objeto
        Parámetro cols.
    cx : objeto
        Parámetro cx.
    cy : objeto
        Parámetro cy.

    Retorna
    -------
    out : objeto
        Resultado de _calculate_ellipse_properties.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _calculate_ellipse_properties(rows, cols, cx, cy)
    """
    if len(rows) < 3:
        return 0, 0, 0, 0
    
    # Coordenadas relativas al centroide
    x = cols - cx
    y = rows - cy
    
    # Momentos centrales normalizados con corrección
    uxx = np.mean(x**2) + 1/12
    uyy = np.mean(y**2) + 1/12
    uxy = np.mean(x * y)
    
    # Autovalores de la matriz de covarianza
    s = uxx + uyy
    delta = np.sqrt((uxx - uyy)**2 + 4 * uxy**2)
    lambda1 = 0.5 * (s + delta)  # mayor
    lambda2 = 0.5 * (s - delta)  # menor
    
    # Longitudes de ejes
    major_axis = 4 * np.sqrt(max(lambda1, 0))
    minor_axis = 4 * np.sqrt(max(lambda2, 0))
    
    # --- Cálculo de Orientación Estándar (Momentos Centrales) ---
    # Usando la fórmula estándar derivada de la matriz de covarianza de imagen 2D
    # theta = 0.5 * arctan2(2 * mu_11, mu_20 - mu_02)
    # Donde:
    # mu_11 = cov(x, y) = uxy
    # mu_20 = var(x) = uxx
    # mu_02 = var(y) = uyy
    
    # Nota: np.arctan2 devuelve valores en (-pi, pi]
    # Al multiplicar por 0.5, el rango es (-pi/2, pi/2] -> (-90, 90] grados
    
    numerator = 2 * uxy
    denominator = uxx - uyy
    
    # Calcular ángulo en radianes
    theta_rad = 0.5 * np.arctan2(numerator, denominator)
    
    # Convertir a grados
    orientation_deg = np.degrees(theta_rad)
    
    # Ajuste por convención:
    # En imágenes, el eje Y crece hacia abajo. 
    # La convención usual (e.g., MATLAB regionprops) es medir el ángulo 
    # entre el eje mayor de la elipse y el eje X horizontal, 
    # positivo en sentido antihorario (hacia Y negativo en pantalla).
    # Sin embargo, dado que Y "baja", una rotación visual "antihoraria" 
    # en coordenadas de pantalla suele corresponder a un ángulo negativo matemático.
    
    # Para consistencia con skimage/MATLAB:
    # Si la elipse está vertical (uyy > uxx), el ángulo tiende a +/- 90.
    # Si está horizontal (uxx > uyy), tiende a 0.
    
    # Mantendremos el valor directo pero invertido de signo para compensar el eje Y
    orientation = -orientation_deg

    # Asegurar rango [-90, 90] explícitamente y evitar valores grandes
    # Asegurar rango [-90, 90] explícitamente y evitar valores grandes
    if orientation <= -90:
        orientation += 180
    elif orientation > 90:
        orientation -= 180
        
    # Excentricidad
    a = major_axis / 2
    b = minor_axis / 2
    if a <= 0:
        eccentricity = 0
    else:
        eccentricity = np.sqrt(max(0, 1 - (b/a)**2))
        
    return major_axis, minor_axis, orientation, eccentricity


def _convex_hull_andrew(points):
    """
    Función _convex_hull_andrew de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    points : objeto
        Parámetro points.

    Retorna
    -------
    out : objeto
        Resultado de _convex_hull_andrew.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _convex_hull_andrew(points)
    """
    points = np.unique(points, axis=0)
    if len(points) <= 2:
        return points
    
    # Ordenar puntos por x, luego por y
    points = points[np.lexsort((points[:, 1], points[:, 0]))]
    
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # Construir casco inferior
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # Construir casco superior
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    # Combinar (eliminar puntos duplicados en las esquinas)
    return np.array(lower[:-1] + upper[:-1])


def _polygon_area_shoelace(vertices):
    """
    Función _polygon_area_shoelace de la librería de procesamiento de imágenes.

    Parámetros
    ----------
    vertices : objeto
        Parámetro vertices.

    Retorna
    -------
    out : objeto
        Resultado de _polygon_area_shoelace.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = _polygon_area_shoelace(vertices)
    """
    n = len(vertices)
    if n < 3:
        return 0
    
    x = vertices[:, 0]
    y = vertices[:, 1]
    
    # Fórmula de Shoelace
    area = 0.5 * abs(np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))
    return area
    

#-----------------------------------------------------------------------


def insertShape(I, shape, position, **kwargs):
    """
    Dibuja formas geométricas sobre una imagen.

    Parámetros
    ----------
    I : ndarray
        Parámetro I.
    shape : str
        Parámetro shape.
    position : objeto
        Parámetro position.
    kwargs : dict
        Parámetros opcionales para insertShape.

    Retorna
    -------
    out : objeto
        Resultado de insertShape.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = insertShape(I, shape, position, **kwargs)
    """
    
    # ============== Normalización de imagen (NumPy optimizado) ==============
    img = np.atleast_3d(I).astype(np.float32)
    
    # Convertir grayscale a RGB
    if img.shape[2] == 1:
        img = np.repeat(img, 3, axis=2)
    # Remover canal alpha si existe
    elif img.shape[2] == 4:
        img = img[..., :3]
    
    # Normalizar a rango [0, 255]
    if img.max() <= 1.0:
        img = img * 255.0
    
    img = np.clip(img, 0, 255).astype(np.uint8)
    H, W = img.shape[:2]
    
    # ============== Extracción de parámetros ==============
    lw = float(kwargs.get("LineWidth", 2))
    color = kwargs.get("ShapeColor", kwargs.get("Color", "yellow"))
    opacity = kwargs.get("Opacity", None)
    show_orient = bool(kwargs.get("ShowOrientation", False))
    shape_lower = str(shape).lower().strip()
    is_filled = shape_lower.startswith("filled-")
    
    # Opacity por defecto para formas rellenas
    if is_filled and opacity is None:
        opacity = 1.0
    alpha = float(opacity) if opacity is not None else 1.0
    
    # ============== Normalización de posiciones (NumPy) ==============
    pos = np.atleast_2d(position).astype(float)
    if pos.ndim == 1:
        pos = pos.reshape(1, -1)
    
    # ============== Configuración de figura ==============
    dpi = 100
    fig, ax = plt.subplots(figsize=(W/dpi, H/dpi), dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    ax.imshow(img, origin="upper", extent=[0, W, H, 0])
    ax.set_xlim([0, W])
    ax.set_ylim([H, 0])
    ax.axis("off")
    
    # ============== Funciones auxiliares ==============
    def yaw_to_mpl(yaw_deg):
        """Convierte yaw de MATLAB (horario) a Matplotlib (antihorario)"""
        return -float(yaw_deg)
    
    def add_orientation_line(xc, yc, width, yaw_deg):
        """Dibuja línea de orientación para rectángulos rotados"""
        theta = np.deg2rad(-yaw_deg)
        dx = (width / 2) * np.cos(theta)
        dy = (width / 2) * np.sin(theta)
        ax.plot([xc - dx, xc + dx], [yc - dy, yc + dy], 
                linewidth=lw, color=color)
    
    # ============== Dibujado por forma ==============
    
    if "rectangle" in shape_lower:
        for row in pos:
            if row.size == 4:  # Rectángulo alineado a ejes
                x, y, w, h = row
                patch = Rectangle((x, y), w, h, linewidth=lw, 
                                edgecolor=color,
                                facecolor=color if is_filled else "none",
                                alpha=alpha if is_filled else 1.0)
            elif row.size == 5:  # Rectángulo rotado
                xc, yc, w, h, yaw = row
                angle = yaw_to_mpl(yaw)
                patch = Rectangle((xc - w/2, yc - h/2), w, h, 
                                linewidth=lw, 
                                edgecolor=color,
                                facecolor=color if is_filled else "none",
                                alpha=alpha if is_filled else 1.0)
                # Aplicar rotación usando transforms de Matplotlib
                t = mtransforms.Affine2D().rotate_deg_around(xc, yc, angle)
                patch.set_transform(t + ax.transData)
                
                if show_orient and not is_filled:
                    add_orientation_line(xc, yc, w, yaw)
            else:
                plt.close(fig)
                raise ValueError("rectangle: usar [x y w h] o [xc yc w h yaw]")
            ax.add_patch(patch)
    
    elif "circle" in shape_lower:
        if pos.shape[1] != 3:
            plt.close(fig)
            raise ValueError("circle: usar [xc yc radius]")
        
        for xc, yc, r in pos:
            patch = Ellipse((xc, yc), 2*r, 2*r, angle=0,
                          linewidth=lw, edgecolor=color,
                          facecolor=color if is_filled else "none",
                          alpha=alpha if is_filled else 1.0)
            ax.add_patch(patch)
    
    elif "ellipse" in shape_lower:
        if pos.shape[1] != 5:
            plt.close(fig)
            raise ValueError("ellipse: usar [xc yc major minor yaw]")
        
        for xc, yc, major, minor, yaw in pos:
            angle = yaw_to_mpl(yaw)
            patch = Ellipse((xc, yc), major, minor, angle=angle,
                          linewidth=lw, edgecolor=color,
                          facecolor=color if is_filled else "none",
                          alpha=alpha if is_filled else 1.0)
            ax.add_patch(patch)
    
    elif shape_lower == "line":
        if pos.shape[1] != 4:
            plt.close(fig)
            raise ValueError("line: usar [x1 y1 x2 y2]")
        
        for x1, y1, x2, y2 in pos:
            ax.plot([x1, x2], [y1, y2], linewidth=lw, color=color)
    
    elif "polygon" in shape_lower:
        # Manejar diferentes formatos de polígonos
        if pos.ndim == 2 and pos.shape[0] == 1:
            # Vector único: [x1 y1 x2 y2 ... xN yN]
            vertices = pos.reshape(-1, 2)
            polygons = [vertices]
        else:
            # Múltiples polígonos
            polygons = [row.reshape(-1, 2) for row in pos]
        
        for verts in polygons:
            if verts.shape[0] < 3:
                plt.close(fig)
                raise ValueError("polygon: se necesitan al menos 3 vértices")
            
            patch = Polygon(verts, closed=True, linewidth=lw, 
                          edgecolor=color,
                          facecolor=color if is_filled else "none",
                          alpha=alpha if is_filled else 1.0)
            ax.add_patch(patch)
    
    else:
        plt.close(fig)
        raise ValueError(f"Forma no soportada: {shape}")
    
    # ============== Extracción de imagen (optimizado) ==============
    fig.canvas.draw()
    
    # Obtener buffer como array NumPy directamente
    buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    w, h = fig.canvas.get_width_height()
    RGB = buf.reshape(h, w, 4)[..., :3].copy()
    
    plt.close(fig)
    return RGB
    
    
    #-----------------------------------------------------------------

def invmoments(B):
    """
    Calcula momentos invariantes de Hu a partir de una máscara.

    Parámetros
    ----------
    B : ndarray
        Parámetro B.

    Retorna
    -------
    out : objeto
        Resultado de invmoments.

    Ejemplo
    -------
    >>> # uso básico
    >>> out = invmoments(B)
    """
    # Convertir a float64 y sanear NaN/Inf
    B = np.asarray(B, dtype=np.float64)
    if B.ndim != 2 or B.size == 0:
        return np.zeros(7, dtype=np.float64)
    # Reemplazar no finitos por 0
    np.nan_to_num(B, copy=False, nan=0.0, posinf=0.0, neginf=0.0)

    M, N = B.shape
    # Coordenadas 1-basadas (estilo MATLAB)
    x, y = np.meshgrid(np.arange(1, N+1, dtype=np.float64),
                       np.arange(1, M+1, dtype=np.float64))

    # Momentos regulares de orden 0 y 1
    m00 = B.sum()
    if m00 == 0.0:
        return np.zeros(7, dtype=np.float64)

    m10 = (x * B).sum()
    m01 = (y * B).sum()

    # Centroide
    xc = m10 / m00
    yc = m01 / m00

    # Coordenadas centradas
    x0 = x - xc
    y0 = y - yc

    # Momentos centrales (orden 2 y 3)
    mu20 = (x0**2 * B).sum()
    mu02 = (y0**2 * B).sum()
    mu11 = (x0 * y0 * B).sum()

    mu30 = (x0**3 * B).sum()
    mu03 = (y0**3 * B).sum()
    mu21 = (x0**2 * y0 * B).sum()
    mu12 = (x0 * y0**2 * B).sum()

    # Normalización por área: eta_pq = mu_pq / m00^(1+(p+q)/2)
    m00_2  = m00**2.0
    m00_25 = m00**2.5

    eta20 = mu20 / m00_2
    eta02 = mu02 / m00_2
    eta11 = mu11 / m00_2

    eta30 = mu30 / m00_25
    eta03 = mu03 / m00_25
    eta21 = mu21 / m00_25
    eta12 = mu12 / m00_25

    # Combinaciones auxiliares
    s30_12 = eta30 + eta12
    s21_03 = eta21 + eta03
    d30_12 = eta30 - 3.0*eta12
    d21_03 = 3.0*eta21 - eta03
    d20_02 = eta20 - eta02

    # 7 momentos de Hu
    hu = np.empty(7, dtype=np.float64)
    hu[0] = eta20 + eta02
    hu[1] = d20_02**2 + 4.0*eta11**2
    hu[2] = d30_12**2 + d21_03**2
    hu[3] = s30_12**2 + s21_03**2
    hu[4] = d30_12*s30_12*(s30_12**2 - 3.0*s21_03**2) + d21_03*s21_03*(3.0*s30_12**2 - s21_03**2)
    hu[5] = d20_02*(s30_12**2 - s21_03**2) + 4.0*eta11*s30_12*s21_03
    hu[6] = d21_03*s30_12*(s30_12**2 - 3.0*s21_03**2) - d30_12*s21_03*(3.0*s30_12**2 - s21_03**2)

    return hu
#--------------------------------------------------------------------------------
    
def roipoly(I_or_m, c_or_n=None, r_or_c=None, r=None, return_coords=False):
    """
    Especifica región de interés (ROI) poligonal.
    Compatible con sintaxis MATLAB roipoly.

    Sintaxis
    --------
    BW = roipoly(I, c, r)
        Crea máscara del polígono con vértices (c, r) sobre imagen I.
        
    BW = roipoly(m, n, c, r)
        Crea máscara de tamaño m×n con polígono de vértices (c, r).

    BW = roipoly(I)
        Modo interactivo: muestra la imagen I y permite seleccionar la ROI
        con clics del ratón. Clic izquierdo: vértice; clic derecho o Enter:
        terminar el polígono.

    [BW, xi, yi] = roipoly(I, c, r, return_coords=True)
        Retorna también las coordenadas del polígono cerrado.

    Parámetros
    ----------
    I : ndarray
        Imagen de entrada (2D o 3D). Se usa solo para obtener dimensiones.
    m : int
        Número de filas de la máscara (alternativa a I).
    n : int
        Número de columnas de la máscara (alternativa a I).
    c : array-like
        Coordenadas X (columnas) de los vértices del polígono.
    r : array-like
        Coordenadas Y (filas) de los vértices del polígono.
    return_coords : bool, opcional
        Si True, retorna (BW, xi, yi). Por defecto False.

    Retorna
    -------
    BW : ndarray (bool)
        Máscara binaria con True dentro del polígono, False fuera.
    xi : ndarray (solo si return_coords=True)
        Coordenadas X del polígono cerrado.
    yi : ndarray (solo si return_coords=True)
        Coordenadas Y del polígono cerrado.

    Notas
    -----
    - El polígono se cierra automáticamente si no está cerrado.
    - Coordenadas c son columnas (X), r son filas (Y).
    - Convención 0-based en Python: píxeles en [0..cols-1], [0..rows-1].
    """
    # -----------------------------
    # 1) Sintaxis: roipoly(m, n, c, r)
    # -----------------------------
    if isinstance(I_or_m, (int, np.integer)):
        if c_or_n is None or r_or_c is None or r is None:
            raise ValueError("roipoly(m, n, c, r) requiere 4 argumentos")

        rows = int(I_or_m)
        cols = int(c_or_n)
        c_coords = np.asarray(r_or_c, dtype=float)
        r_coords = np.asarray(r, dtype=float)

    # -----------------------------
    # 2) Sintaxis: roipoly(I, c, r)  o  roipoly(I) interactivo
    # -----------------------------
    elif isinstance(I_or_m, np.ndarray):
        I = I_or_m
        if I.ndim == 2:
            rows, cols = I.shape
        elif I.ndim == 3:
            rows, cols = I.shape[:2]
        else:
            raise ValueError("I debe ser imagen 2D o 3D")

        # 2a) Modo interactivo: roipoly(I)
        if c_or_n is None and r_or_c is None:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            # Si la imagen es color, mostrarla tal cual; si es 2D, usar gray.
            if I.ndim == 2:
                ax.imshow(I, cmap="gray")
            else:
                ax.imshow(I)
            ax.set_title(
                "Seleccione ROI poligonal:\n"
                "clic izq. = vértice, clic der. o Enter = terminar."
            )
            ax.axis("image")
            ax.axis("off")

            puntos = plt.ginput(n=-1, timeout=0)
            plt.close(fig)

            if len(puntos) < 3:
                raise ValueError(
                    "Se requieren al menos 3 puntos para definir un polígono."
                )

            c_coords = np.array([p[0] for p in puntos], dtype=float)
            r_coords = np.array([p[1] for p in puntos], dtype=float)

        # 2b) Modo clásico: roipoly(I, c, r)
        else:
            if c_or_n is None or r_or_c is None:
                raise ValueError("roipoly(I, c, r) requiere 3 argumentos")

            c_coords = np.asarray(c_or_n, dtype=float)
            r_coords = np.asarray(r_or_c, dtype=float)

    else:
        raise TypeError("Primer argumento debe ser imagen (ndarray) o entero (m)")

    # -----------------------------
    # 3) Validaciones comunes
    # -----------------------------
    if len(c_coords) != len(r_coords):
        raise ValueError("c y r deben tener la misma longitud")

    if len(c_coords) < 3:
        raise ValueError("Se necesitan al menos 3 vértices para un polígono")

    # Cerrar polígono automáticamente si no está cerrado
    if c_coords[0] != c_coords[-1] or r_coords[0] != r_coords[-1]:
        c_coords = np.append(c_coords, c_coords[0])
        r_coords = np.append(r_coords, r_coords[0])

    # -----------------------------
    # 4) Construcción de la máscara
    # -----------------------------
    vertices = np.column_stack((c_coords, r_coords))
    poly = Path(vertices)

    # Coordenadas de píxeles (0..rows-1, 0..cols-1)
    Y, X = np.mgrid[0:rows, 0:cols]
    puntos = np.column_stack((X.ravel(), Y.ravel()))

    BW = poly.contains_points(puntos)
    BW = BW.reshape(rows, cols)

    if return_coords:
        return BW, c_coords, r_coords
    else:
        return BW


def roifilt2(h_or_I, I_or_BW, BW_or_fun, fun=None):
    """
    Filtra región de interés (ROI) en imagen.
    Compatible con sintaxis MATLAB roifilt2.

    Sintaxis
    --------
    J = roifilt2(h, I, BW)
        Aplica filtro lineal h solo en la región definida por BW.
        
    J = roifilt2(I, BW, fun)
        Aplica función fun solo en la región definida por BW.

    Parámetros
    ----------
    h : ndarray (2D)
        Kernel de filtro lineal (solo para sintaxis 1).
    I : ndarray (2D)
        Imagen de entrada en escala de grises.
    BW : ndarray (bool)
        Máscara binaria (True=ROI, False=fuera de ROI).
        Debe tener el mismo tamaño que I.
    fun : callable
        Función a aplicar en la ROI (solo para sintaxis 2).
        Debe aceptar un array y retornar array del mismo tamaño.

    Retorna
    -------
    J : ndarray
        Imagen de salida:
        - J[BW] contiene valores filtrados/procesados.
        - J[~BW] contiene valores originales de I.
    """
    if fun is not None:
        # Para evitar ambigüedad con la firma; se soportan solo 3 args.
        raise ValueError("roifilt2 acepta máximo 3 argumentos (h, I, BW) o (I, BW, fun)")

    # ---------------------------------------------------------
    # Detección de sintaxis:
    #   - roifilt2(h, I, BW)       → use_filter = True
    #   - roifilt2(I, BW, fun)     → use_filter = False
    # ---------------------------------------------------------
    if isinstance(h_or_I, np.ndarray):
        # Primer argumento es ndarray: puede ser h o puede ser I
        if not isinstance(I_or_BW, np.ndarray):
            raise TypeError("El segundo argumento debe ser ndarray (I o BW).")

        if isinstance(BW_or_fun, np.ndarray):
            # Sintaxis 1: roifilt2(h, I, BW)
            h = np.asarray(h_or_I, dtype=float)
            I = np.asarray(I_or_BW)
            BW = np.asarray(BW_or_fun, dtype=bool)
            use_filter = True
        elif callable(BW_or_fun):
            # Sintaxis 2: roifilt2(I, BW, fun)
            I = np.asarray(h_or_I)
            BW = np.asarray(I_or_BW, dtype=bool)
            fun = BW_or_fun
            use_filter = False
        else:
            raise TypeError("Tercer argumento debe ser ndarray (BW) o función callable.")
    else:
        raise TypeError("El primer argumento debe ser ndarray (h o I).")

    # ---------------------------------------------------------
    # Validaciones de forma
    # ---------------------------------------------------------
    if I.ndim != 2:
        raise ValueError("I debe ser imagen 2D (escala de grises).")

    if I.shape != BW.shape:
        raise ValueError("I y BW deben tener el mismo tamaño.")

    # ---------------------------------------------------------
    # Procesamiento
    # ---------------------------------------------------------
    if use_filter:
        # Sintaxis 1: filtro lineal en ROI
        from ip_functions import imfilter  # import local para evitar ciclos

        I_filtered = imfilter(I, h)

        J = I.copy()
        J[BW] = I_filtered[BW]

    else:
        # Sintaxis 2: función arbitraria en ROI
        I_processed = fun(I)

        if not isinstance(I_processed, np.ndarray):
            I_processed = np.asarray(I_processed)

        if I_processed.shape != I.shape:
            raise ValueError("La función debe retornar array del mismo tamaño que I.")

        J = I.copy()
        J[BW] = I_processed[BW]

    return J
    
    
#-----------------------------------------------
#     Transformada de Radon 
#-----------------------------------------------


import numpy as np

def radon(I, theta=None, method='linear', extrapval=0.0, normalize=False):
    """
    Transformada de Radon (MATLAB-like) usando SOLO NumPy + interp2 (ya implementada por el usuario).

    Sintaxis tipo MATLAB
    --------------------
    R       = radon(I)
    R       = radon(I, theta)
    [R, xp] = radon(I, theta)

    Extensión (en esta librería)
    ----------------------------
    [R, xp] = radon(I, theta, method='linear', extrapval=0.0, normalize=False)

    Parámetros
    ----------
    I : ndarray (H×W)
        Imagen 2D (grises).
    theta : None o array (grados)
        Si None: 0:179 (MATLAB-like).
    method : str
        Interpolación para el muestreo por rotación: 'nearest' | 'linear' | 'cubic'
        Se aceptan alias MATLAB típicos ('bilinear','bicubic','spline',...) y se mapean.
    extrapval : float
        Valor fuera de la imagen.
    normalize : bool
        Si True aplica mat2gray(I) antes de procesar (MATLAB no lo hace por defecto).

    Retorna
    -------
    R : ndarray (Nr×M)
        Sinograma. Cada columna corresponde a un ángulo.
    xp : ndarray (Nr,)
        Coordenada radial asociada a filas de R (espaciado 1 píxel).
    """
    I = np.asarray(I)
    if I.ndim != 2:
        raise ValueError("radon: I debe ser una imagen 2D (H×W).")

    # theta por defecto: 0..179 (MATLAB-like)
    if theta is None:
        theta = np.arange(180, dtype=float)
    theta = np.asarray(theta, dtype=float).ravel()

    # Normalización opcional (NO es el comportamiento por defecto de MATLAB)
    if normalize:
        I = mat2gray(I)

    I = I.astype(float)
    H, W = I.shape

    # Tamaño radial para imitar MATLAB (dependiente de la diagonal)
    Nr = int(2 * np.ceil(np.sqrt(H * H + W * W) / 2.0) + 3)

    # xp centrado (espaciado 1 píxel)
    c = (Nr - 1.0) / 2.0
    xp = np.arange(Nr, dtype=float) - c

    # Colocar I centrada en un canvas cuadrado Nr×Nr
    Ip = np.full((Nr, Nr), float(extrapval), dtype=float)
    y0 = int(np.floor((Nr - H) / 2.0))
    x0 = int(np.floor((Nr - W) / 2.0))
    Ip[y0:y0 + H, x0:x0 + W] = I

    # Malla de salida (una sola construcción)
    Yp, Xp = np.meshgrid(np.arange(Nr, dtype=float),
                         np.arange(Nr, dtype=float),
                         indexing='ij')
    Xr = Xp - c
    Yr = Yp - c

    # Mapeo de nombres MATLAB -> los tres permitidos por interp2 del usuario
    interp_in = (method if method is not None else 'linear')
    interp_in = str(interp_in).lower().strip()
    if interp_in in ['bilinear']:
        interp_in = 'linear'
    if interp_in in ['bicubic', 'spline', 'pchip', 'v5cubic']:
        interp_in = 'cubic'
    if interp_in not in ['nearest', 'linear', 'cubic']:
        raise ValueError("radon: method debe ser 'nearest', 'linear' o 'cubic' (o alias MATLAB).")

    # Salida (Nr × nTheta)
    R = np.zeros((Nr, theta.size), dtype=float)

    for k, th in enumerate(theta):
        a = np.deg2rad(th)
        ca = np.cos(a)
        sa = np.sin(a)

        # Rotación inversa (muestreo): (x',y') -> (x,y) en el canvas Ip
        Xin = ( Xr * ca + Yr * sa) + c
        Yin = (-Xr * sa + Yr * ca) + c

        # interp2 del usuario trabaja en 1-based (MATLAB)
        Xq = Xin + 1.0
        Yq = Yin + 1.0

        Irot = interp2(Ip, Xq, Yq, method=interp_in, extrapval=extrapval)

        # Proyección: suma sobre filas (y), produce función de x' (columnas)
        R[:, k] = np.sum(Irot, axis=0)

    if theta.size == 1:
        return R[:, 0], xp
    return R, xp


def iradon(R, theta=None, interp='linear', filt='Ram-Lak', frequency_scaling=1.0, output_size=None, return_filter=False):
    """
    iradon (MATLAB-like) por Retroproyección Filtrada (FBP), SOLO NumPy.

    Restricciones (según solicitud)
    -------------------------------
    Interpolación (SOLO):
        'nearest' | 'linear' | 'cubic'
    Filtro (SOLO):
        'Ram-Lak' | 'None'

    Ajuste clave (para NO obtener la imagen invertida)
    --------------------------------------------------
    En imágenes, el índice de fila aumenta hacia abajo (sistema "imagen").
    En la geometría de Radon/FBP, es más natural trabajar con y positivo hacia arriba (cartesiano).
    Para alinear la convención y evitar reconstrucciones "al revés", se define:

        Y_cart = cI - Y_img

    y luego se usa:
        t = X*cos(theta) + Y_cart*sin(theta)

    De este modo, la reconstrucción queda consistente con la radon() anterior sin aplicar flips post-proceso.
    """
    R = np.asarray(R)
    if R.ndim == 1:
        R = R.reshape(-1, 1)
    if R.ndim != 2:
        raise ValueError("iradon: R debe ser vector (Nr,) o matriz (Nr, M).")

    Nr, M = R.shape

    # --- theta MATLAB-like ---
    if theta is None or (isinstance(theta, (list, tuple, np.ndarray)) and np.asarray(theta).size == 0):
        # Distribución uniforme en [0,180) con M proyecciones (típico en MATLAB)
        theta_vec = np.arange(M, dtype=float) * (180.0 / M)
    else:
        theta_arr = np.asarray(theta, dtype=float).ravel()
        if theta_arr.size == 1:
            # Paso angular constante
            theta_vec = np.arange(M, dtype=float) * float(theta_arr[0])
        else:
            if theta_arr.size != M:
                raise ValueError("iradon: len(theta) debe coincidir con columnas de R.")
            theta_vec = theta_arr

    # --- output_size (aproximación MATLAB-like) ---
    if output_size is None:
        output_size = int(2 * np.floor(Nr / (2.0 * np.sqrt(2.0))))
        output_size = max(output_size, 1)
    N = int(output_size)

    # --- interp: SOLO nearest/linear/cubic ---
    interp_in = str(interp if interp is not None else 'linear').lower().strip()
    if interp_in not in ['nearest', 'linear', 'cubic']:
        raise ValueError("iradon: interp debe ser 'nearest', 'linear' o 'cubic'.")

    # --- filtro: SOLO Ram-Lak o None ---
    filt_in = str(filt if filt is not None else 'Ram-Lak').lower().strip()
    if filt_in not in ['ram-lak', 'ramlak', 'ramp', 'none']:
        raise ValueError("iradon: filt debe ser 'Ram-Lak' o 'None'.")

    fs = float(frequency_scaling)
    if not (0.0 < fs <= 1.0):
        raise ValueError("iradon: frequency_scaling debe estar en (0,1].")

    Rf = R.astype(float)

    # ------------------------------------------------------------
    # 1) Filtrado 1D (por columnas) con Ram-Lak (rampa)
    # ------------------------------------------------------------
    if filt_in == 'none':
        Rfilt = Rf
        H = None
    else:
        nfft = int(2 ** np.ceil(np.log2(max(64, 2 * Nr))))  # potencia de 2
        Rp = np.zeros((nfft, M), dtype=float)
        Rp[:Nr, :] = Rf

        f = np.fft.fftfreq(nfft)     # [-0.5, 0.5)
        fa = np.abs(f)               # rampa |f|
        cutoff = 0.5 * fs
        H = fa.copy()
        H[fa > cutoff] = 0.0

        F = np.fft.fft(Rp, axis=0)
        F *= H[:, None]
        rpf = np.fft.ifft(F, axis=0).real
        Rfilt = rpf[:Nr, :]

    # ------------------------------------------------------------
    # 2) Retroproyección (malla completa) + interpolación 1D
    # ------------------------------------------------------------
    cI = (N - 1.0) / 2.0

    # Coordenadas de imagen (índices) -> coordenadas centradas
    Yi, Xi = np.meshgrid(np.arange(N, dtype=float),
                         np.arange(N, dtype=float),
                         indexing='ij')
    X = Xi - cI

    # Ajuste clave para evitar inversión: y positivo hacia arriba (cartesiano)
    Y = cI - Yi

    # Centro radial coherente con xp de radon(): xp = arange(Nr) - (Nr-1)/2
    cR = (Nr - 1.0) / 2.0

    def _interp1(p, u, kind):
        """
        Interpolación 1D didáctica (nearest/linear/cubic Keys) sobre un vector p.
        Fuera del soporte se rellena con 0 (comportamiento típico de FBP).
        """
        p = np.asarray(p, dtype=float)

        if kind == 'nearest':
            ui = np.rint(u).astype(int)
            out = np.zeros(u.shape, dtype=float)
            ok = (ui >= 0) & (ui < p.size)
            out[ok] = p[ui[ok]]
            return out

        if kind == 'linear':
            u0 = np.floor(u).astype(int)
            u1 = u0 + 1
            w = u - u0
            out = np.zeros(u.shape, dtype=float)
            ok = (u0 >= 0) & (u1 < p.size)
            if np.any(ok):
                out[ok] = (1.0 - w[ok]) * p[u0[ok]] + w[ok] * p[u1[ok]]
            return out

        # kind == 'cubic' (Keys, a=-0.5)
        a = -0.5
        u0 = np.floor(u).astype(int)
        t = u - u0

        def w_cubic(tt):
            tt = np.abs(tt)
            w = np.zeros_like(tt, dtype=float)
            m1 = (tt <= 1)
            m2 = (tt > 1) & (tt < 2)
            w[m1] = (a + 2) * tt[m1]**3 - (a + 3) * tt[m1]**2 + 1
            w[m2] = a * tt[m2]**3 - 5*a * tt[m2]**2 + 8*a * tt[m2] - 4*a
            return w

        uidx = [u0 - 1, u0, u0 + 1, u0 + 2]
        wts  = [w_cubic(t + 1), w_cubic(t), w_cubic(t - 1), w_cubic(t - 2)]

        out = np.zeros(u.shape, dtype=float)
        ok = (uidx[0] >= 0) & (uidx[3] < p.size)
        if np.any(ok):
            acc = np.zeros(u.shape, dtype=float)
            for ui, wi in zip(uidx, wts):
                acc[ok] += wi[ok] * p[ui[ok]]
            out[ok] = acc[ok]
        return out

    img = np.zeros((N, N), dtype=float)

    for k, th in enumerate(theta_vec):
        a = np.deg2rad(th)
        ca = np.cos(a)
        sa = np.sin(a)

        # Coordenada detector (rho): t = x cos + y sin (con y cartesiano hacia arriba)
        t = X * ca + Y * sa

        # Convertir a índice radial flotante (0-based)
        u = t + cR

        img += _interp1(Rfilt[:, k], u, interp_in)

    # Escala típica FBP (factor estándar usado en prácticas para coincidir con MATLAB)
    img *= (np.pi / (2.0 * len(theta_vec)))

    if return_filter:
        return img, H
    return img

#-----------------------------------------------
#     Interpolacion
#-----------------------------------------------



def interp2(V, Xq, Yq, method='linear', extrapval=0.0):
    """
    interp2 tipo MATLAB (grid implícito):
        Vq = interp2(V, Xq, Yq, method, extrapval)

    - Xq: coordenadas x (columnas) en 1-based (MATLAB)
    - Yq: coordenadas y (filas)    en 1-based (MATLAB)
    - method: 'nearest' | 'linear' | 'cubic'
    - extrapval: valor fuera de la imagen
    - Soporta V 2D (H,W) y 3D (H,W,C) canal a canal
    """
    V = np.asarray(V, dtype=float)
    Xq = np.asarray(Xq, dtype=float)
    Yq = np.asarray(Yq, dtype=float)

    # MATLAB (1-based) -> Python (0-based)
    x = Xq - 1.0
    y = Yq - 1.0

    m = method.lower()
    if m == 'bilinear':
        m = 'linear'
    if m == 'bicubic':
        m = 'cubic'

    if m == 'nearest':
        return _interp2_nearest(V, x, y, extrapval)
    if m == 'linear':
        return _interp2_bilinear(V, x, y, extrapval)
    if m == 'cubic':
        return _interp2_bicubic(V, x, y, extrapval)

    raise ValueError("method debe ser 'nearest', 'linear'/'bilinear' o 'cubic'/'bicubic'.")


def _interp2_nearest(V, x, y, extrapval):
    H, W = V.shape[:2]
    xi = np.rint(x).astype(int)
    yi = np.rint(y).astype(int)

    valid = (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H)

    if V.ndim == 2:
        out = np.full(x.shape, extrapval, dtype=float)
        out[valid] = V[yi[valid], xi[valid]]
        return out

    C = V.shape[2]
    out = np.full((*x.shape, C), extrapval, dtype=float)
    out[valid, :] = V[yi[valid], xi[valid], :]
    return out


def _interp2_bilinear(V, x, y, extrapval):
    H, W = V.shape[:2]

    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1

    valid = (x0 >= 0) & (x1 < W) & (y0 >= 0) & (y1 < H)

    wx = x - x0
    wy = y - y0

    if V.ndim == 2:
        out = np.full(x.shape, extrapval, dtype=float)
        if not np.any(valid):
            return out

        I00 = V[y0[valid], x0[valid]]
        I10 = V[y0[valid], x1[valid]]
        I01 = V[y1[valid], x0[valid]]
        I11 = V[y1[valid], x1[valid]]

        wxv = wx[valid]
        wyv = wy[valid]

        out[valid] = (1-wxv)*(1-wyv)*I00 + (wxv)*(1-wyv)*I10 + (1-wxv)*(wyv)*I01 + (wxv)*(wyv)*I11
        return out

    C = V.shape[2]
    out = np.full((*x.shape, C), extrapval, dtype=float)
    if not np.any(valid):
        return out

    I00 = V[y0[valid], x0[valid], :]
    I10 = V[y0[valid], x1[valid], :]
    I01 = V[y1[valid], x0[valid], :]
    I11 = V[y1[valid], x1[valid], :]

    wxv = wx[valid][:, None]
    wyv = wy[valid][:, None]

    out[valid, :] = (1-wxv)*(1-wyv)*I00 + (wxv)*(1-wyv)*I10 + (1-wxv)*(wyv)*I01 + (wxv)*(wyv)*I11
    return out


def _cubic_w(t, a=-0.5):
    t = np.abs(t)
    w = np.zeros_like(t, dtype=float)

    m1 = (t <= 1)
    m2 = (t > 1) & (t < 2)

    w[m1] = (a+2)*t[m1]**3 - (a+3)*t[m1]**2 + 1
    w[m2] = a*t[m2]**3 - 5*a*t[m2]**2 + 8*a*t[m2] - 4*a
    return w


def _interp2_bicubic(V, x, y, extrapval):
    """
    Bicúbica separable (4x4). Didáctica: clara, no optimizada.
    """
    H, W = V.shape[:2]

    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)

    # Para bicúbica se requieren vecinos x0-1..x0+2 y y0-1..y0+2
    valid = (x0-1 >= 0) & (x0+2 < W) & (y0-1 >= 0) & (y0+2 < H)

    if V.ndim == 2:
        out = np.full(x.shape, extrapval, dtype=float)
        if not np.any(valid):
            return out

        dx = x - x0
        dy = y - y0

        acc = np.zeros_like(x, dtype=float)

        for j in range(-1, 3):
            wy = _cubic_w(dy - j)
            yj = y0 + j
            for i in range(-1, 3):
                wx = _cubic_w(dx - i)
                xi = x0 + i
                acc += (wx * wy) * V[yj, xi]

        out[valid] = acc[valid]
        return out

    C = V.shape[2]
    out = np.full((*x.shape, C), extrapval, dtype=float)
    if not np.any(valid):
        return out

    dx = x - x0
    dy = y - y0

    acc = np.zeros((*x.shape, C), dtype=float)

    for j in range(-1, 3):
        wy = _cubic_w(dy - j)
        yj = y0 + j
        for i in range(-1, 3):
            wx = _cubic_w(dx - i)
            xi = x0 + i
            w = (wx * wy)[..., None]
            acc += w * V[yj, xi, :]

    out[valid, :] = acc[valid, :]
    return out




def phantom(n: int = 256) -> np.ndarray:
    """
    Genera la imagen del fantasma de Shepp-Logan utilizando NumPy.
    
    El fantasma de Shepp-Logan es una imagen de prueba estándar utilizada en
    investigación de imágenes médicas, particularmente en tomografía computarizada
    (TC) y resonancia magnética (RM). Consiste en 10 elipses con diferentes
    intensidades que simulan una sección transversal simplificada de una cabeza
    humana.
    
    Parámetros
    ----------
    n : int, opcional
        Tamaño de la imagen cuadrada de salida (n x n píxeles). Por defecto 256.
        
    Retorna
    -------
    np.ndarray
        Array 2D de forma (n, n) que contiene la imagen del fantasma con valores
        de intensidad en punto flotante. La imagen está normalizada al rango
        definido por las intensidades de las elipses.
        
    Notas
    -----
    El fantasma se construye en un sistema de coordenadas normalizado
    [-1, 1] x [-1, 1] donde el origen (0, 0) corresponde al centro de la imagen.
    Cada elipse se define por su intensidad, longitudes de semi-ejes, posición
    del centro y ángulo de rotación. Las intensidades son aditivas donde las
    elipses se superponen.
    
    Referencias
    ----------
    Shepp, L. A., & Logan, B. F. (1974). The Fourier reconstruction of a head
    section. IEEE Transactions on Nuclear Science, 21(3), 21-43.
    
    Ejemplos
    --------
    >>> import matplotlib.pyplot as plt
    >>> img = phantom(256)
    >>> plt.imshow(img, cmap='gray')
    >>> plt.show()
    """
    x = np.linspace(-1.0, 1.0, n)
    y = np.linspace(-1.0, 1.0, n)
    X, Y = np.meshgrid(x, -y)
    
    I = np.zeros((n, n), dtype=float)
    
    ellipses = [
        [1.0,    0.69,   0.92,    0.0,      0.0,     0.0],
        [-0.98,  0.6624, 0.874,   0.0,     -0.0184,  0.0],
        [-0.02,  0.11,   0.31,    0.22,     0.0,    -18.0],
        [-0.02,  0.16,   0.41,   -0.22,     0.0,     18.0],
        [0.01,   0.21,   0.25,    0.0,      0.35,    0.0],
        [0.01,   0.046,  0.046,   0.0,      0.1,     0.0],
        [0.01,   0.046,  0.046,   0.0,     -0.1,     0.0],
        [0.01,   0.046,  0.023,  -0.08,    -0.605,   0.0],
        [0.01,   0.023,  0.023,   0.0,     -0.606,   0.0],
        [0.01,   0.023,  0.046,   0.06,    -0.605,   0.0],
    ]
    
    for amp, A, B, x0, y0, theta_deg in ellipses:
        theta = np.radians(theta_deg)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        x_translated = X - x0
        y_translated = Y - y0
        
        x_rot = x_translated * cos_theta + y_translated * sin_theta
        y_rot = -x_translated * sin_theta + y_translated * cos_theta
        
        mask = (x_rot / A) ** 2 + (y_rot / B) ** 2 <= 1.0
        
        I[mask] += amp
    
    return I