#8/Nov/2025 2:30am Colombia

import numpy as np
import random
import matplotlib as mpl
from matplotlib import pyplot as plt, image as mpimg, transforms as mtransforms
from matplotlib.patches import Rectangle, Ellipse, Polygon
from matplotlib.lines import Line2D




def imshow(I, *args):
    """
    Muestra una imagen. Sintaxis compatible con MATLAB.
    
    Sintaxis:
        imshow(I)              # Auto-escala
        imshow(I, [])          # Auto-escala explícita
        imshow(I, [low, high]) # Rango manual
        imshow(RGB)            # Imagen RGB
        imshow(BW)             # Binaria
        imshow(I, 'jet')       # Con colormap
    """
    
    if not isinstance(I, np.ndarray):
        I = np.array(I)
    
    # Parsear argumentos
    display_range = None
    cmap = None
    for arg in args:
        if isinstance(arg, str):
            cmap = arg
        elif isinstance(arg, (list, tuple, np.ndarray)):
            if len(arg) == 0:
                display_range = 'auto'
            elif len(arg) == 2:
                display_range = arg
    
    # CASO 1: RGB (M×N×3)
    if I.ndim == 3 and I.shape[2] in [3, 4]:
        if I.dtype == np.uint8:
            I_display = I.astype(np.float32) / 255.0
        elif I.dtype in [np.float32, np.float64]:
            I_display = I / 255.0 if I.max() > 1.0 else I
        else:
            I_display = I
        plt.imshow(np.clip(I_display, 0, 1))
        plt.axis('off')
        plt.show()
        return
    
    # CASO 2: Grises o Binaria (M×N)
    if I.ndim == 2:
        es_binaria = (I.dtype == bool) or (np.array_equal(I, I.astype(bool)))
        if cmap is None:
            cmap = 'gray'
        
        # Determinar vmin, vmax
        if display_range is None:
            if es_binaria:
                vmin, vmax = 0, 1
            elif I.dtype == np.uint8:
                vmin, vmax = 0, 255
            elif I.dtype in [np.float32, np.float64]:
                vmin, vmax = (0.0, 1.0) if I.max() <= 1.0 else (I.min(), I.max())
            else:
                vmin, vmax = I.min(), I.max()
        elif display_range == 'auto':
            vmin, vmax = I.min(), I.max()
        else:
            vmin, vmax = display_range[0], display_range[1]
        
        plt.imshow(I, cmap=cmap, vmin=vmin, vmax=vmax)
        plt.axis('off')
        plt.show()
        return
    
    raise ValueError(f"Dimensiones {I.shape} no soportadas")


def imread(filename):
    """
    Lee una imagen desde disco (similar a MATLAB imread).
    Devuelve un ndarray numpy:
    - Escala de grises: matriz MxN
    - Color RGB: matriz MxNx3
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
    - filename define el formato por la extensión (png, jpg, tif, bmp).
    - cmap es opcional (para imágenes en gris).
    """
    if I.dtype != np.uint8:
        I = np.clip(I, 0, 255).astype(np.uint8)
    plt.imsave(filename, I, cmap=cmap if cmap else None)

def imcomplement(I):
    """
    Versión simple de imcomplement (similar a MATLAB).
    - bool     : invierte 0 ↔ 1
    - float    : devuelve 1 - I   (se asume [0,1])
    - uint8    : devuelve 255 - I
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


def imhist(r, ax=None, ver=True):
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
  
    
    
    
def imsplit(I):
    r=np.array(I[:,:,0])
    g=np.array(I[:,:,1])
    b=np.array(I[:,:,2])
    return r,g,b



def rgb2gray(RGB):
    r,g,b=imsplit(RGB)
    gris=np.uint8(0.299*np.double(r)+0.587*np.double(g)+0.114*np.double(b))
    return gris

def non_overflowing_sum(a,b):
    c = np.uint16(a)+b
    c[np.where(c>255)] = 255
    c[np.where(c<0)] = 0
    return np.uint8(c)


def graythresh(I):
    h=imhist(I,None,False)
    return otsuthresh(h)


def otsuthresh(h):
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


    
def im2bw(I, threshold):
    # Convierte la imagen I a binaria usando el umbral especificado
    return (I >= threshold * 255).astype(bool)



def adaptthresh(I, P=None, V=None):
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



def imbinarize(I, *args):
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




def immse(Iref, I):
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
    ssimval = ssim(A, ref)
    - Compatible con MATLAB (forma compacta, C1=(K1*L)^2, C2=(K2*L)^2, ventana 11x11 σ=1.5).
    - Soporta grises (H×W) y RGB (H×W×3). En RGB promedia el SSIM por canal.
    - L (dynamic range) se infiere:
        * enteros: L = 2^bits - 1
        * float:   L = 1 si max<=1; en otro caso L = 255
    - Bordes: padding 'replicate'; promedio en región 'valid' (quita 5 px por lado).
    Retorna:
        ssimval (float)
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



def imnoise(imagen, tipo, parametro1=None, parametro2=None):
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



def rgb2hsv(I):
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
  
  
def xyz2lab(myXYZ):
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





def xyz2rgb(XYZ):
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

    
    

def rgb2xyz(RGB):
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
    


def rgb2lab(RGB):
    F, C, L = np.shape(RGB)
    if L != 3:
        raise ValueError('rgb2lab: La imagen debe ser MxNx3')
    
    xyz = rgb2xyz(RGB)
    CIEL = xyz2lab(xyz)
    
    return CIEL
    
def lab2rgb(LAB):
    # Verificar si la entrada es una matriz MxNx3
    F, C, L = np.shape(LAB)
    if L != 3:
        raise ValueError('lab2rgb: La imagen debe ser MxNx3')
    
    # Paso 1: Convertir de LAB a XYZ
    xyz = lab2xyz(LAB)
    
    # Paso 2: Convertir de XYZ a RGB
    RGB = xyz2rgb(xyz)
    
    return RGB


def imrotate(I, grados):
    # Convertir los grados a radianes
    theta = -grados * np.pi / 180

    # Obtener las dimensiones de la imagen original
    if len(I.shape) == 2:
        # Imagen en escala de grises
        M, N = I.shape
        C = 1
    else:
        # Imagen RGB
        M, N, C = I.shape

    # Centro de la imagen original
    pc = np.array([N, M, 1]) / 2

    # Matriz de rotación inversa
    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0,              0,             1]
    ])
    
    R_inv = np.linalg.inv(R)

    # Calcular las nuevas dimensiones de la imagen rotada
    D = np.abs(R)
    z = np.array([N, M, 1])
    zp = np.dot(D, z)  # Nuevas dimensiones sin el término homogéneo

    # Dimensiones de la imagen rotada
    Np = int(np.ceil(zp[0]))  # Nueva anchura
    Mp = int(np.ceil(zp[1]))  # Nueva altura

    # Centro de la imagen rotada
    pc_p = np.array([Np, Mp, 1]) / 2

    # Inicializar la nueva imagen rotada
    if C == 1:
        I_rotada = np.zeros((Mp, Np), dtype=I.dtype)
    else:
        I_rotada = np.zeros((Mp, Np, C), dtype=I.dtype)

    # Ciclos for para recorrer la imagen rotada
    for xp in range(Np):
        for yp in range(Mp):

            # Coordenadas homogéneas del píxel en la imagen rotada
            p_p = np.array([xp, yp, 1])

            # Calcular la posición relativa respecto al centro de la imagen rotada
            p_p_rel = p_p - pc_p

            # Aplicar la matriz de rotación inversa a las coordenadas relativas
            p_rel = np.dot(R_inv, p_p_rel)

            # Ajustar las coordenadas al centro de la imagen original
            p = p_rel + pc

            # Redondear las coordenadas al píxel más cercano
            x = int(np.round(p[0]))
            y = int(np.round(p[1]))

            # Verificar si las coordenadas están dentro de los límites de la imagen original
            if 0 <= x < N and 0 <= y < M:
                # Asignar los valores de los píxeles de la imagen original a la imagen rotada
                if C == 1:
                    I_rotada[yp, xp] = I[y, x]
                else:
                    I_rotada[yp, xp, :] = I[y, x, :]

    return I_rotada



def imcrop(I, x, y, w, h):
    if I.ndim not in [2, 3]:
        raise ValueError("La imagen debe ser 2D (escala de grises) o 3D (color)")
    
    height, width = I.shape[:2]
    
    # Validar los límites del recorte
    if x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("Los parámetros de recorte están fuera de los límites de la imagen")
    
    if I.ndim == 2:  # Imagen en escala de grises
        return I[y:y+h, x:x+w]
    else:  # Imagen en color
        return I[y:y+h, x:x+w, :]





def imresize(I, S):
    # Leer tamaño de la imagen original
    if len(I.shape) == 2:
        # Imagen en escala de grises
        N, M = I.shape
        L = 1
    else:
        # Imagen RGB
        N, M, L = I.shape
    
    # Determinar los factores de escala
    if np.isscalar(S):
        Sx = Sy = S  # Factor de escala en x y en y
    elif len(S) == 2:
        # Compatibilidad con formato (nueva_altura, nuevo_ancho)
        if isinstance(S[0], int) and isinstance(S[1], int):
            # S es (nuevo_alto, nuevo_ancho) - calcular factores
            Sy = S[0] / N  # Factor para altura
            Sx = S[1] / M  # Factor para ancho
        else:
            # S es (factor_x, factor_y) - formato original
            Sx, Sy = S[0], S[1]
    else:
        raise ValueError("S debe ser escalar o tupla de 2 elementos")
    
    # Construir la matriz de escalamiento
    S_matrix = np.array([
        [Sx,  0,  0],
        [ 0, Sy,  0],
        [ 0,  0,  1]
    ])
    
    # Calcular el nuevo tamaño de la imagen
    z = np.array([N, M, 1])  # Dimensiones originales en formato homogéneo
    zp = np.dot(S_matrix, z)  # Nuevas dimensiones
    Np = int(np.ceil(zp[0]))  # Nueva altura
    Mp = int(np.ceil(zp[1]))  # Nuevo ancho
    
    # Crear la nueva imagen de salida
    if L == 1:
        Ip = np.zeros((Np, Mp), dtype=I.dtype)
    else:
        Ip = np.zeros((Np, Mp, L), dtype=I.dtype)
    
    # Método Inverso
    for yp in range(Np):
        for xp in range(Mp):
            # Coordenadas homogéneas del píxel en la imagen escalada
            pp = np.array([xp, yp, 1])
            
            # Calcular la posición en la imagen original
            S_inv = np.array([
                [1/Sx, 0, 0],
                [0, 1/Sy, 0],
                [0, 0, 1]
            ])  # Matriz inversa de escalamiento
            
            p = np.dot(S_inv, pp)  # Coordenadas originales
            
            # Redondear las coordenadas al píxel más cercano
            x = int(np.round(p[0]))
            y = int(np.round(p[1]))
            
            # Verificar si las coordenadas están dentro de los límites de la imagen original
            if 0 <= x < M and 0 <= y < N:
                # Asignar los valores de los píxeles de la imagen original a la imagen escalada
                if L == 1:
                    Ip[yp, xp] = I[y, x]
                else:
                    Ip[yp, xp, :] = I[y, x, :]
    
    return Ip



def imtranslate(I, translation, mode='same'):
    # Obtiene las dimensiones de la imagen original
    if len(I.shape) == 2:
        # Imagen en escala de grises
        N, M = I.shape
        L = 1
    else:
        # Imagen RGB
        N, M, L = I.shape
    
    # Desplazamientos en x e y
    tx, ty = translation
    
    # Matriz de translación
    T = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    
    # Si el modo es 'full', se considera el tamaño extendido
    if mode == 'full':
        # Cálculo de nuevas dimensiones considerando el desplazamiento
        D = np.abs(T)
        z = np.array([M, N, 1])
        zp = np.dot(D, z)  # Nuevas dimensiones
        Mp = int(np.round(zp[0]))  # Nuevo ancho
        Np = int(np.round(zp[1]))  # Nueva altura
    elif mode == 'same':
        Mp, Np = M, N  # Mantiene las mismas dimensiones que la imagen original
    else:
        raise ValueError("El modo debe ser 'same' o 'full'")

    # Inicializa la nueva imagen con ceros
    if L == 1:
        Ip = np.zeros((Np, Mp), dtype=I.dtype)
    else:
        Ip = np.zeros((Np, Mp, L), dtype=I.dtype)

    # Recorrer cada píxel de la nueva imagen
    for yp in range(Np):
        for xp in range(Mp):
            # Calcula las coordenadas en la imagen original aplicando la inversa de T
            pp = np.array([xp, yp, 1])
            p = np.dot(np.linalg.inv(T), pp)
            
            x = int(np.round(p[0]))
            y = int(np.round(p[1]))

            # Verifica si las coordenadas están dentro de los límites de la imagen original
            if 0 <= x < M and 0 <= y < N:
                if L == 1:
                    Ip[yp, xp] = I[y, x]
                else:
                    Ip[yp, xp, :] = I[y, x, :]

    # Convierte la imagen resultante a tipo uint8 (si es necesario)
    return Ip


def fitgeotrans(puntos_iniciales, puntos_finales, transformation_type='projective'):
    # Número de puntos
    n = puntos_iniciales.shape[0]
    
    if transformation_type == 'affine':
        # Transformación afín
        num_params = 6
        A = np.zeros((2 * n, num_params))
        b = np.zeros(2 * n)
        
        for i in range(n):
            x, y = puntos_iniciales[i]
            x_prime, y_prime = puntos_finales[i]
            
            # Ecuación para x'
            A[2*i, :] = [x, y, 1, 0, 0, 0]
            b[2*i] = x_prime
            
            # Ecuación para y'
            A[2*i+1, :] = [0, 0, 0, x, y, 1]
            b[2*i+1] = y_prime
        
        # Resolver el sistema A * h = b
        h = np.linalg.lstsq(A, b, rcond=None)[0]
        
        # La matriz H tiene la forma [h1 h2 h3; h4 h5 h6; 0 0 1]
        H = np.array([[h[0], h[1], h[2]], 
                      [h[3], h[4], h[5]], 
                      [0, 0, 1]])

    elif transformation_type == 'projective':
        # Transformación proyectiva
        num_params = 8
        A = np.zeros((2 * n, num_params))
        b = np.zeros(2 * n)
        
        for i in range(n):
            x, y = puntos_iniciales[i]
            x_prime, y_prime = puntos_finales[i]
            
            # Ecuación para x'
            A[2*i, :] = [x, y, 1, 0, 0, 0, -x_prime * x, -x_prime * y]
            b[2*i] = x_prime
            
            # Ecuación para y'
            A[2*i+1, :] = [0, 0, 0, x, y, 1, -y_prime * x, -y_prime * y]
            b[2*i+1] = y_prime
        
        # Resolver el sistema A * h = b
        h = np.linalg.lstsq(A, b, rcond=None)[0]
        
        # La matriz H tiene la forma [h1 h2 h3; h4 h5 h6; h7 h8 1]
        H = np.array([[h[0], h[1], h[2]], 
                      [h[3], h[4], h[5]], 
                      [h[6], h[7], 1]])

    else:
        raise ValueError("Tipo de transformación no soportado. Use 'affine' o 'projective'.")
    
    return H




def imwarp(I, H):
    # Obtener las dimensiones de la imagen
    if len(I.shape) == 2:
        # Imagen en escala de grises
        N, M = I.shape
        L = 1
    else:
        # Imagen RGB
        N, M, L = I.shape

    # Esquinas de la imagen original (en coordenadas homogéneas)
    corners = np.array([
        [1, 1, 1],
        [M, 1, 1],
        [1, N, 1],
        [M, N, 1]
    ]).T  # Transpuesta para facilitar operaciones matriciales

    # Transformar las esquinas de la imagen
    transformed_corners = H @ corners
    transformed_corners /= transformed_corners[2, :]  # Normalizar

    # Calcular los límites de la nueva imagen
    x_min, y_min = np.min(transformed_corners[:2, :], axis=1)
    x_max, y_max = np.max(transformed_corners[:2, :], axis=1)

    # Calcular el nuevo tamaño de la imagen transformada
    Np = int(np.ceil(y_max - y_min + 1))
    Mp = int(np.ceil(x_max - x_min + 1))

    # Crear una imagen vacía para almacenar la imagen transformada
    if L == 1:
        imagen_transformada = np.zeros((Np, Mp), dtype=I.dtype)
    else:
        imagen_transformada = np.zeros((Np, Mp, L), dtype=I.dtype)

    # Calcular la matriz de transformación inversa
    H_inv = np.linalg.inv(H)

    # Recorrer la imagen transformada píxel por píxel
    for yp in range(Np):
        for xp in range(Mp):
            # Coordenadas ajustadas (en coordenadas homogéneas)
            p_p = np.array([xp + x_min - 1, yp + y_min - 1, 1])

            # Aplicar la transformación inversa
            p = H_inv @ p_p
            x_o = int(round(p[0] / p[2]))
            y_o = int(round(p[1] / p[2]))

            # Verificar si las coordenadas están dentro de los límites de la imagen original
            if 1 <= x_o <= M and 1 <= y_o <= N:
                if L == 1:
                    imagen_transformada[yp, xp] = I[y_o - 1, x_o - 1]  # Ajustar a 0-indexed
                else:
                    for c in range(L):  # Recorrer cada canal
                        imagen_transformada[yp, xp, c] = I[y_o - 1, x_o - 1, c]  # Ajustar a 0-indexed

    return imagen_transformada    
    



def imfilter(I, K, salida='same', tipodepad='symmetric', method='conv'):
    """
    Aplica un filtro a una imagen usando convolucion o correlacion.
    
    Parametros:
    I : ndarray
        Imagen de entrada
    K : ndarray
        Kernel del filtro
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
        Modos MATLAB: 'symmetric', 'replicate', 'circular', 'constant'
    method : str, opcional
        Metodo de filtrado ('conv' o 'corr', 'conv' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
    """
    # Verificar argumentos necesarios
    if K is None:
        raise ValueError('Es necesario el Kernel')
    
    # Mapeo de modos MATLAB a NumPy
    pad_mode_map = {
        'replicate': 'edge',      # MATLAB replicate = NumPy edge
        'symmetric': 'symmetric',  # Igual en ambos
        'circular': 'wrap',        # MATLAB circular = NumPy wrap
        'constant': 'constant'     # Igual en ambos
    }
    
    # Convertir modo de padding si es necesario
    if tipodepad in pad_mode_map:
        tipodepad_numpy = pad_mode_map[tipodepad]
    else:
        tipodepad_numpy = tipodepad  # Usar directamente si no esta en el mapeo
    
    # Convertir imagen a float para los calculos
    I = I.astype(float)
    
    # Parametros del Kernel
    Tx, Ty = K.shape
    Finix = (Tx - 1) // 2
    Ciniy = (Ty - 1) // 2
    
    # Ajustar el padding segun las dimensiones de la imagen
    if I.ndim == 3:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy), (0, 0))
    else:
        pad_width = ((Finix, Finix), (Ciniy, Ciniy))
    
    # Crear copia padded de la imagen (esta sera nuestra salida para 'full')
    If = np.pad(I, pad_width, mode=tipodepad_numpy)
    
    # Convertir a 3D si es necesario para procesamiento uniforme
    if If.ndim == 2:
        If = If[..., np.newaxis]
    
    # Preparar el kernel segun el metodo
    if method == 'conv':
        K = np.rot90(K, 2)
    
    # Obtener dimensiones
    M, N = If.shape[:2]
    L = If.shape[2] if If.ndim == 3 else 1
    
    # Copiar la imagen padded y solo modificar la region central
    If_temp = If.copy()
    
    # Aplicar el filtro solo en la region que cambia
    for i in range(Finix, M-Finix):
        for j in range(Ciniy, N-Ciniy):
            for canal in range(L):
                W = If[i-Finix:i+Finix+1, j-Ciniy:j+Ciniy+1, canal]
                If_temp[i, j, canal] = np.sum(W * K)
    
    If = If_temp
    
    # Ajustar el tamano segun el tipo de salida
    if salida == 'same':
        If = If[Finix:-Finix, Ciniy:-Ciniy]
    
    # Volver a 2D si era 2D originalmente
    if L == 1:
        If = If[..., 0]
    
    # Normalizar y convertir a uint8
    If = np.clip(If, 0, 255).astype(np.uint8)
    
    return If
    
    
    
    

def ordfilt2(I, Orden, K, salida='same', tipodepad='symmetric'):
    """
    Aplica un filtro de orden a una imagen usando una máscara K.
    
    Parámetros:
    I : ndarray
        Imagen de entrada
    Orden : int
        Orden del elemento a seleccionar (1 para mínimo, len(K) para máximo)
    K : ndarray
        Máscara binaria que define qué elementos considerar
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
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
    Aplica un filtro de mediana a una imagen usando una vecindad de tamaño especificado.
    
    Parámetros:
    I : ndarray
        Imagen de entrada
    FiltroTam : tuple, opcional
        Tamaño de la vecindad (por defecto (3, 3))
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
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
    Aplica un filtro de moda a una imagen usando una vecindad de tamaño especificado.
    
    Parámetros:
    I : ndarray
        Imagen de entrada
    FiltroTam : tuple, opcional
        Tamaño de la vecindad (por defecto (3, 3))
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
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
    Aplica un filtro de desviación estándar a una imagen usando una vecindad de tamaño especificado.
    
    Parámetros:
    I : ndarray
        Imagen de entrada
    FiltroTam : tuple, opcional
        Tamaño de la vecindad (por defecto (3, 3))
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
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
    Aplica un filtro de entropía a una imagen usando una vecindad de tamaño especificado.
    
    Parámetros:
    I : ndarray
        Imagen de entrada
    FiltroTam : tuple, opcional
        Tamaño de la vecindad (por defecto (3, 3))
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
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
    Aplica un filtro de rango a una imagen usando una vecindad de tamaño especificado.
    
    Parámetros:
    I : ndarray
        Imagen de entrada
    FiltroTam : tuple, opcional
        Tamaño de la vecindad (por defecto (3, 3))
    salida : str, opcional
        Tipo de salida ('same' o 'full', 'same' por defecto)
    tipodepad : str, opcional
        Tipo de padding ('symmetric' por defecto)
    
    Retorna:
    ndarray: Imagen filtrada
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
    tipo = tipo.lower()
    if tipo == 'average':
        T = 3 if T is None else T
        Tx, Ty = (T, T) if isinstance(T, int) else T
        return np.ones((Tx, Ty)) / (Tx * Ty)

    elif tipo == 'gaussian':
        T = 3 if T is None else T
        S = 0.5 if S is None else S
        Limite = (T - 1) / 2
        x, y = np.meshgrid(np.linspace(-Limite, Limite, T), np.linspace(-Limite, Limite, T))
        Z = (1 / (2 * np.pi * S ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * S ** 2))
        return Z / np.sum(Z)

    elif tipo == 'laplacian':
        A = 0.2 if T is None else T
        return (4 / (A + 1)) * np.array([[A / 4, (1 - A) / 4, A / 4],
                                         [(1 - A) / 4, -1, (1 - A) / 4],
                                         [A / 4, (1 - A) / 4, A / 4]])

    elif tipo == 'log':
        T = 5 if T is None else T
        S = 0.5 if S is None else S
        Limite = (T - 1) / 2
        x, y = np.meshgrid(np.linspace(-Limite, Limite, T), np.linspace(-Limite, Limite, T))
        gau = (1 / (2 * np.pi * S ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * S ** 2))
        gau /= np.sum(gau)
        f2 = (gau * (x ** 2 + y ** 2 - (2 * S ** 2))) / (S ** 4)
        return f2 - np.sum(f2) / (T ** 2)


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




def bwlabel(I, EE=4):
    """
    Etiqueta componentes conectados en imagen binaria.
    
    Parametros:
        I (ndarray bool 2D): Imagen binaria
        EE (int): Conectividad 4 u 8
    
    Retorna:
        Labels (ndarray int): Matriz de etiquetas
        Num (int): Numero de componentes
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
    Convierte etiquetas a imagen RGB pseudocoloreada.
    Compatible con MATLAB.
    
    Parámetros
    ----------
    L : ndarray
        Matriz de etiquetas (0=fondo, 1,2,3,...=regiones)
    colormap : str o ndarray, opcional
        'jet', 'hsv', etc. o array N×3 de colores RGB
    bgcolor : str o list, opcional
        'k','w','r','g','b' o [R,G,B]. Default: negro
    order : str, opcional
        'noshuffle' (secuencial) o 'shuffle' (aleatorio)
    
    Retorna
    -------
    RGB : ndarray (M×N×3)
        Imagen pseudocoloreada en [0,1]
    
    Ejemplos
    --------
    RGB = label2rgb(L)
    RGB = label2rgb(L, 'jet', 'w')
    RGB = label2rgb(L, 'jet', 'k', 'shuffle')
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

def strel(shape, size, angle=0):
    """
    Clon básico de strel de MATLAB usando solo NumPy.
    Genera un elemento estructurante (SE) booleano para operaciones
    morfológicas como dilatación y erosión.
    
    Parámetros
    ----------
    shape : str
        Tipo de elemento estructurante:
        - 'square'    : cuadrado lleno de unos.
        - 'rectangle' : rectángulo lleno de unos.
        - 'disk'      : aproximación discreta de un círculo.
        - 'diamond'   : rombo basado en la métrica L1.
        - 'line'      : línea de longitud dada en cierto ángulo.
        - 'octagon'   : aproximación discreta de un octágono.
    size : int o tuple
        - square/disk/diamond/octagon : entero (tamaño o radio).
        - rectangle : (alto, ancho).
        - line : longitud (entero).
    angle : float
        Solo para 'line'. Ángulo en grados (0° = horizontal).
    
    Retorna
    -------
    SE : ndarray bool
        Matriz binaria con True en la forma del SE.
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



def _slide_bool(A, B, op_any):
    """
    Núcleo deslizante sin acolchar ni recortar.
    Asume que A ya tiene el acolchado suficiente.
    Devuelve una imagen de la MISMA forma que A.
    - Si op_any=True: dilatación (any sobre máscara B)
    - Si op_any=False: erosión (all sobre máscara B)
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


def imdilate(Ibin, SE, pad=0):
    """
    Dilatación binaria.
    - pad == 0 o 1: acolcha externamente con ese valor y recorta al final (salida del tamaño de Ibin).
    - pad is None: NO acolcha NI recorta (asume que Ibin ya está acolchada); salida del tamaño de Ibin.
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
    Erosión binaria.
    - pad == 0 o 1: acolcha externamente con ese valor y recorta al final (salida del tamaño de Ibin).
    - pad is None: NO acolcha NI recorta (asume que Ibin ya está acolchada); salida del tamaño de Ibin.
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
    Apertura binaria (erosión -> dilatación) con acolchado consistente.
    - pad == 0 o 1: acolchado ÚNICO al principio; ambas fases sin acolchado interno; recorte ÚNICO al final.
    - pad is None: asume imagen ya acolchada y NO recorta al final.
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
    Cerramiento binario (dilatación -> erosión) con acolchado consistente.
    - pad == 0 o 1: acolchado ÚNICO al principio; ambas fases sin acolchado interno; recorte ÚNICO al final.
    - pad is None: asume imagen ya acolchada y NO recorta al final.
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


    
      

def mat2gray(I, limits=None):
    """Convierte imagen a escala de grises normalizada [0,1] compatible con MATLAB."""
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
def imgradient(I, method='sobel'):
    """
    Calcula la magnitud y direccion del gradiente de una imagen.
    100% compatible con MATLAB imgradient.
    
    Sintaxis MATLAB:
    ----------------
    [Gmag, Gdir] = imgradient(I)
    [Gmag, Gdir] = imgradient(I, method)
    
    Parametros:
    -----------
    I : ndarray
        Imagen en escala de grises
    method : str, opcional
        'sobel' (default), 'prewitt', 'roberts', 'central', 'intermediate'
    
    Retorna:
    --------
    Gmag : ndarray (float64)
        Magnitud del gradiente
    Gdir : ndarray (float64)
        Direccion del gradiente en grados [-180, 180]
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
    Detector de bordes 100% compatible con sintaxis MATLAB.
    
    Sintaxis MATLAB:
    ----------------
    BW = edge(I, method)
    BW = edge(I, method, thresh)
    BW = edge(I, method, thresh, sigma)
    BW = edge(I, method, thresh, direction)  % sobel/prewitt
    BW = edge(I, 'log', thresh, sigma, tsize)
    
    Parametros POSICIONALES:
    ------------------------
    I : ndarray
        Imagen en escala de grises (uint8 o float)
    method : str
        'canny', 'sobel', 'prewitt', 'roberts', 'log', 'zerocross'
        Default: 'canny'
    thresh : None, float [0,1], o [low, high]
        - None o []: calcula automaticamente
        - float: umbral normalizado [0,1] (MATLAB style)
        - [low, high]: dos umbrales normalizados para canny
        Default: None (automatico)
    sigma : float, opcional
        Desviacion estandar del filtro Gaussiano
        - Canny default: sqrt(2) ≈ 1.414 (MATLAB)
        - LoG default: 2.0
    direction : str, opcional
        'both', 'horizontal', 'vertical' (solo sobel/prewitt)
        Default: 'both'
    tsize : int, opcional
        Tamano del filtro (solo log/zerocross)
    
    Retorna:
    --------
    BW : ndarray (bool)
        Imagen binaria con bordes detectados
    
    Ejemplos MATLAB:
    ----------------
    >>> BW = edge(I, 'canny')                    # Auto
    >>> BW = edge(I, 'canny', 0.3)               # thresh=0.3
    >>> BW = edge(I, 'canny', [0.1, 0.3])        # [low, high]
    >>> BW = edge(I, 'canny', [], 2.0)           # sigma=2.0, thresh auto
    >>> BW = edge(I, 'canny', 0.2, 1.5)          # thresh=0.2, sigma=1.5
    >>> BW = edge(I, 'sobel', 0.1)               # thresh=0.1
    >>> BW = edge(I, 'sobel', 0.1, 'horizontal') # direccion
    >>> BW = edge(I, 'log', 0.002, 2)            # thresh, sigma
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

def _non_maximum_suppression(magnitud, direccion):
    """Supresion no maxima (funcion interna, no publica en MATLAB)."""
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
    """Umbralizacion con histeresis (funcion interna, no publica en MATLAB)."""
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
    """Detecta cruces por cero (funcion interna, no publica en MATLAB)."""
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
    Devuelve el primer eje cuya longitud sea > 1.
    Equivalente a la 'first non-singleton dimension' de MATLAB.
    Si todas son 1, retorna 0.
    """
    for k, n in enumerate(X.shape):
        if n > 1:
            return k
    return 0


# ------------------------------------------------------------
# FFT / IFFT 1D (firmas MATLAB)
# ------------------------------------------------------------
def fft(X, n: int | None = None, dim: int | None = None):
    """
    FFT 1-D compatible con MATLAB:
    - dim: eje de transformación; por defecto, primera dimensión no trivial.
    - n  : longitud objetivo sobre 'dim'. Si n > len -> zero-padding;
           si n < len -> truncamiento (idéntico a MATLAB).
    Restricciones: n debe ser entero positivo si se especifica.
    Algoritmo: FFT rápida (Cooley–Tukey radix mixto) vía NumPy.
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
    IFFT 1-D compatible con MATLAB:
    Misma semántica que fft() para (n, dim).
    Algoritmo: IFFT rápida consistente con FFT (Cooley–Tukey).
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
def _matlab_fft2_shape(X: np.ndarray, M: int | None, N: int | None) -> tuple | None:
    """
    Construye el tamaño objetivo (M,N) al estilo MATLAB:
    - Si ambos son None -> None (usa tamaño actual).
    - Si M es None -> usa X.shape[0]; si N es None -> usa X.shape[1].
    Valida que M,N sean enteros no negativos si se suministran.
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


def fft2(X, M: int | None = None, N: int | None = None):
    """
    FFT 2-D compatible con MATLAB (opera sobre filas, columnas = ejes 0 y 1).
    - M, N: tamaños objetivo por fila y columna (padding/truncamiento).
            None -> usa tamaño actual en ese eje (comportamiento MATLAB).
    Para arreglos con más de 2 dimensiones (p.ej. MxNxC), se aplica por 'páginas'
    a lo largo de las dimensiones restantes, igual que MATLAB.
    Algoritmo: FFT 2D Cooley–Tukey sobre ejes (0,1).
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
    IFFT 2-D compatible con MATLAB (inversa sobre ejes 0 y 1).
    - M, N: tamaños objetivo por fila y columna (padding/truncamiento).
    La salida conserva las dimensiones y se aplica por 'páginas' si hay más ejes.
    Algoritmo: IFFT 2D coherente con fft2 (Cooley–Tukey).
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
    Desplaza la DC al centro (idéntico a MATLAB):
    por cada eje: corrimiento +floor(n/2).
    - axes: None -> todos los ejes; int -> eje único; iterable -> ejes seleccionados.
    No altera magnitudes/fases, solo reordena cuadrantes (O(N)).
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
    Inverso de fftshift (idéntico a MATLAB):
    por cada eje: corrimiento +ceil(n/2) = (n+1)//2.
    - axes: None -> todos los ejes; int -> eje único; iterable -> ejes seleccionados.
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


def deconvwnr(I, psf, nsr):
    """
    Restauración de imagen mediante filtro de Wiener en el dominio de la frecuencia.  
    Implementa el filtro de Wiener óptimo para la restauración de imágenes degradadas
    por un sistema lineal invariante al desplazamiento con ruido aditivo gaussiano.
    
    Modelo de degradación:
        g(x,y) = h(x,y) * f(x,y) + η(x,y)
        G(u,v) = H(u,v)F(u,v) + N(u,v)
    
    Función de transferencia del filtro de Wiener:
        W(u,v) = H*(u,v) / (|H(u,v)|² + NSR)
    
    Parámetros:
    -----------
    I : ndarray de dimensiones MxN
        Imagen degradada observada g(x,y).
        
    psf : ndarray de dimensiones PxQ
        Point Spread Function h(x,y) del sistema de degradación.
        Debe estar normalizada (suma de elementos igual a 1).
        
    nsr : float, positivo
        Noise-to-Signal Ratio: NSR = σ²_n / σ²_f
        Controla el balance entre inversión y regularización.
        
    Retorna:
    --------
    f_est : ndarray de dimensiones MxN, dtype float64
        Imagen restaurada f̂(x,y) con dimensiones idénticas a la entrada.
        
    Compatibilidad:
    ---------------
    Sintaxis equivalente a MATLAB: J = deconvwnr(I, PSF, NSR)
    
    Referencias:
    ------------
    Sección 1.7 del documento (páginas 26-33)
    Gonzalez & Woods (2018). Digital Image Processing, 4th Edition.
    
    Ejemplos:
    ---------
    >>> # Restauración básica
    >>> psf = fspecial('gaussian', 5, 1.0)
    >>> J = deconvwnr(I, psf, 0.01)
    
    >>> # Estimar NSR desde varianzas
    >>> nsr = sigma_noise**2 / np.var(I.astype(float))
    >>> J = deconvwnr(I, psf, nsr)
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

def hough(BW, Theta=None, RhoResolution=1):
    """
    Transformada de Hough (líneas) en forma de Hesse, implementación sencilla con bucles for.

    Parámetros
    ----------
    BW : array_like
        Imagen binaria o numérica; todo píxel no nulo vota.
    Theta : array_like, opcional
        Vector de ángulos en grados. Por defecto, np.arange(-90, 90)  (i.e., -90:89).
    RhoResolution : int or float, opcional
        Resolución (paso) para el muestreo de rho en píxeles. Por defecto, 1.

    Retorna
    -------
    H : ndarray, shape (len(rho), len(theta))
        Acumulador en el espacio (rho, theta).
    theta : ndarray
        Vector de ángulos (grados) correspondiente a las columnas de H.
    rho : ndarray
        Vector de distancias (píxeles) correspondiente a las filas de H.

    Definición
    ----------
    rho = x*cos(theta) + y*sin(theta), con theta en grados,
    x = columna - 1, y = fila - 1 (origen en esquina sup-izq).
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
    Emulación sencilla de houghpeaks (MATLAB) para el acumulador de Hough.

    Parámetros
    ----------
    H : ndarray (nr x nt)
        Acumulador en el espacio (rho, theta).
    numpeaks : int
        Número máximo de picos a extraer.
    Threshold : float, opcional
        Umbral mínimo del acumulador para aceptar un pico (por defecto: 0.5*max(H)).
    NHoodSize : tuple(int,int), opcional
        Tamaño de la vecindad a suprimir alrededor de cada pico (filas, columnas).
        Debe ser impar en ambas dimensiones. Por defecto: ceil(size(H)/50)*2+1.

    Retorna
    -------
    P : ndarray (k x 2), dtype=int
        Coordenadas (row, col) de los picos encontrados en H (índices 0-based).
        En MATLAB serían (fila, columna) 1-based; aquí se deja 0-based por
        coherencia con Python. Si se requiere 1-based, sumar 1 al final.

    Notas
    -----
    - Estrategia: búsqueda iterativa del máximo global ≥ Threshold, registro del
      pico y supresión de una ventana NHoodSize centrada en el máximo.
    - La supresión se realiza por recorte (clamping) en los bordes del acumulador.
    - Si H contiene NaN/Inf, se ignoran al evaluar el valor máximo.
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
    Detecta segmentos de linea a partir de transformada de Hough.
    Compatible con MATLAB houghlines.
    
    Parametros:
    BW: imagen binaria
    theta: angulos (salida de hough)  
    rho: distancias (salida de hough)
    picos: picos detectados (salida de houghpeaks)
    FillGap: distancia maxima entre pixeles del mismo segmento
    MinLength: longitud minima del segmento
    
    Retorna lista de diccionarios con point1, point2, theta, rho
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
    
    
def viscircles(centers, radii, ax=None, Color='blue', LineWidth=2, 
               LineStyle='-', EnhanceVisibility=False):
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
    
def imfindcircles(BW, radius_range, Method='PhaseCode', ObjectPolarity='bright', 
                  Sensitivity=0.85, EdgeThreshold=None):
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
def regionprops(L, properties=None):
    """
    Calcula propiedades de regiones etiquetadas (clon de MATLAB regionprops).
    
    Parámetros:
    -----------
    L : ndarray
        Imagen etiquetada (cada región tiene un valor entero único)
    properties : list, str, opcional
        Lista de propiedades a calcular. Si es None, calcula ['Area', 'Centroid', 'BoundingBox']
        Propiedades disponibles:
        - 'Area': número de píxeles en la región
        - 'BoundingBox': [x_min, y_min, width, height] 
        - 'Centroid': [x_centroid, y_centroid]
        - 'Perimeter': perímetro usando cadena-8
        - 'MajorAxisLength': longitud del eje mayor de la elipse equivalente
        - 'MinorAxisLength': longitud del eje menor de la elipse equivalente
        - 'Orientation': orientación de la elipse equivalente en grados
        - 'Eccentricity': excentricidad de la elipse equivalente
        - 'EquivDiameter': diámetro del círculo con la misma área
        - 'Extent': relación entre área de la región y área del bounding box
        - 'Circularity': medida de qué tan circular es la región
        - 'ConvexHull': vértices del casco convexo
        - 'ConvexArea': área del casco convexo
    
    Retorna:
    --------
    list: Lista de diccionarios, uno por región, con las propiedades solicitadas
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
            maj, min_axis, ori, ecc = _calculate_ellipse_properties(rows, cols, cx, cy)
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


def _calculate_perimeter_chain8(mask):
    """
    Calcula el perímetro usando trazado de cadena-8 (Moore).
    Suma pasos cardinales (peso 1) y diagonales (peso sqrt(2)).
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


def _calculate_ellipse_properties(rows, cols, cx, cy):
    """
    Calcula propiedades de elipse equivalente usando momentos de segundo orden.
    Incluye corrección +1/12 en las diagonales como en MATLAB.
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
    
    # Orientación (convención de MATLAB)
    if uyy > uxx:
        theta = 0.5 * np.arctan2(2 * uxy, uyy - uxx)
        orientation = theta * 180 / np.pi
    else:
        theta = 0.5 * np.arctan2(2 * uxy, uyy - uxx)
        orientation = 90 + theta * 180 / np.pi
    
    # Normalizar a [-90, 90]
    while orientation > 90:
        orientation -= 180
    while orientation <= -90:
        orientation += 180
    
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
    Calcula el casco convexo usando el algoritmo de Andrew (cadena monótona).
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
    Calcula el área de un polígono usando la fórmula de Shoelace.
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
    insertShape(I, shape, position, Name=Value, ...)
    ------------------------------------------------
    Emula MATLAB insertShape para superponer formas en una imagen.
    Devuelve una imagen RGB con la forma pintada (no interactiva).

    Parámetros
    ----------
    I : np.ndarray
        Imagen (H×W), (H×W×3) o (H×W×4). Se normaliza a uint8 RGB.
    shape : str
        'rectangle', 'filled-rectangle',
        'circle', 'filled-circle',
        'ellipse', 'filled-ellipse',
        'polygon', 'filled-polygon',
        'line'
    position : array-like
        Formato (1 o N filas):
        - rectangle eje-alineado: [x y width height]
        - rectangle rotado:       [xctr yctr width height yaw]
        - circle:                  [xctr yctr radius]
        - ellipse:                 [xctr yctr major minor yaw]  (major/minor = diámetros)
        - polygon:                 [x1 y1 x2 y2 ... xN yN] (vector 1D) o matriz M×(2N)
        - line:                    [x1 y1 x2 y2]
    Name-Value (opcionales)
    -----------------------
    LineWidth : float   (por defecto 2)
    ShapeColor / Color : color de trazo (y relleno si es 'filled-*')
    Opacity : float 0..1  (por defecto 1.0 en formas rellenas)
    ShowOrientation : bool (rectangle rotado: dibuja eje mayor local)
    
    Returns
    -------
    RGB : np.ndarray uint8 (H×W×3)
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
    Calcula los 7 momentos invariantes de Hu (φ1..φ7) para una imagen 2D.
    Acepta binaria o en escala de grises con intensidades no negativas.

    Parámetros
    ----------
    B : np.ndarray
        Imagen 2D (bool, int o float). Se asume B >= 0 para la interpretación geométrica.

    Retorna
    -------
    hu : np.ndarray, shape (7,), dtype float64
        Vector con [φ1, φ2, ..., φ7]. Si m00==0 o entrada vacía → vector de ceros.
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
