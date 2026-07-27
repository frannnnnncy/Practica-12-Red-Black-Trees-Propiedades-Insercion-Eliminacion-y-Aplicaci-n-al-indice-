# ── Actividad 1: Estructura base y verificadores ────────────────────────
from enum import Enum, auto


class Color(Enum):
    ROJO = auto()
    NEGRO = auto()


class NodoRBT:
    def __init__(self, votante=None, color=Color.ROJO):
        self.votante = votante  # (dni, nombre, facultad, habilitado)
        self.izquierdo = None
        self.derecho = None
        self.padre = None
        self.color = color

    def __repr__(self):
        c = 'R' if self.color == Color.ROJO else 'N'
        dni = self.votante[0] if self.votante else 'NIL'
        return f'[{dni}:{c}]'


# Nodo NIL centinela compartido — todas las hojas apuntan a esta instancia
NIL = NodoRBT(votante=None, color=Color.NEGRO)
NIL.izquierdo = NIL.derecho = NIL.padre = NIL


def verificar_p2(raiz):
    """P2: la raiz es NEGRO."""
    return raiz is NIL or raiz.color == Color.NEGRO


def verificar_p4(nodo):
    """P4: ningun nodo ROJO tiene hijo ROJO (recorrido completo)."""
    if nodo is NIL:
        return True
    if nodo.color == Color.ROJO:
        if nodo.izquierdo.color == Color.ROJO:
            return False
        if nodo.derecho.color == Color.ROJO:
            return False
    return verificar_p4(nodo.izquierdo) and verificar_p4(nodo.derecho)


def altura_negra(nodo):
    """P5: retorna black-height si es consistente, -1 si la viola."""
    if nodo is NIL:
        return 0
    bh_izq = altura_negra(nodo.izquierdo)
    bh_der = altura_negra(nodo.derecho)
    if bh_izq == -1 or bh_der == -1 or bh_izq != bh_der:
        return -1
    return bh_izq + (1 if nodo.color == Color.NEGRO else 0)


def verificar_todas(raiz):
    ok_p2 = verificar_p2(raiz)
    ok_p4 = verificar_p4(raiz)
    ok_p5 = altura_negra(raiz) != -1
    return ok_p2 and ok_p4 and ok_p5


def es_bst_valido(nodo, minimo=None, maximo=None):
    """Verificacion adicional: el arbol tambien debe cumplir la invariante BST sobre el DNI."""
    if nodo is NIL:
        return True
    dni = nodo.votante[0]
    if minimo is not None and not (dni > minimo):
        return False
    if maximo is not None and not (dni < maximo):
        return False
    return (es_bst_valido(nodo.izquierdo, minimo, dni) and
            es_bst_valido(nodo.derecho, dni, maximo))


# ── Actividad 2 y 3: Clase ArbolElectoral — insercion y eliminacion ─────
class ArbolElectoral:
    def __init__(self):
        self.raiz = NIL

    def _rot_izq(self, x):
        y = x.derecho
        x.derecho = y.izquierdo
        if y.izquierdo is not NIL:
            y.izquierdo.padre = x
        y.padre = x.padre
        if x.padre is NIL:
            self.raiz = y
        elif x == x.padre.izquierdo:
            x.padre.izquierdo = y
        else:
            x.padre.derecho = y
        y.izquierdo = x
        x.padre = y

    def _rot_der(self, y):
        x = y.izquierdo
        y.izquierdo = x.derecho
        if x.derecho is not NIL:
            x.derecho.padre = y
        x.padre = y.padre
        if y.padre is NIL:
            self.raiz = x
        elif y == y.padre.derecho:
            y.padre.derecho = x
        else:
            y.padre.izquierdo = x
        x.derecho = y
        y.padre = x

    def insertar(self, votante):  # votante = (dni, nombre, facultad, habilitado)
        z = NodoRBT(votante=votante)
        z.izquierdo = z.derecho = z.padre = NIL
        y, x = NIL, self.raiz
        while x is not NIL:
            y = x
            x = x.izquierdo if votante[0] < x.votante[0] else x.derecho
        z.padre = y
        if y is NIL:
            self.raiz = z
        elif votante[0] < y.votante[0]:
            y.izquierdo = z
        else:
            y.derecho = z
        self._fix_insertar(z)

    def _fix_insertar(self, z):
        while z.padre.color == Color.ROJO:
            if z.padre == z.padre.padre.izquierdo:
                tio = z.padre.padre.derecho
                if tio.color == Color.ROJO:  # Caso 2
                    z.padre.color = tio.color = Color.NEGRO
                    z.padre.padre.color = Color.ROJO
                    z = z.padre.padre
                else:
                    if z == z.padre.derecho:  # Caso 3
                        z = z.padre
                        self._rot_izq(z)
                    z.padre.color = Color.NEGRO  # Caso 4
                    z.padre.padre.color = Color.ROJO
                    self._rot_der(z.padre.padre)
            else:  # simetrico
                tio = z.padre.padre.izquierdo
                if tio.color == Color.ROJO:
                    z.padre.color = tio.color = Color.NEGRO
                    z.padre.padre.color = Color.ROJO
                    z = z.padre.padre
                else:
                    if z == z.padre.izquierdo:
                        z = z.padre
                        self._rot_der(z)
                    z.padre.color = Color.NEGRO
                    z.padre.padre.color = Color.ROJO
                    self._rot_izq(z.padre.padre)
        self.raiz.color = Color.NEGRO

    def buscar(self, dni):
        x = self.raiz
        while x is not NIL and x.votante[0] != dni:
            x = x.izquierdo if dni < x.votante[0] else x.derecho
        return x if x is not NIL else None

    def _transplant(self, u, v):
        """Sustituye el subarbol con raiz u por el subarbol con raiz v."""
        if u.padre is NIL:
            self.raiz = v
        elif u == u.padre.izquierdo:
            u.padre.izquierdo = v
        else:
            u.padre.derecho = v
        v.padre = u.padre

    def _minimo(self, n):
        while n.izquierdo is not NIL:
            n = n.izquierdo
        return n

    def eliminar(self, dni):
        z = self.buscar(dni)
        if z is None:
            raise KeyError(f'DNI no encontrado: {dni}')
        y = z
        y_color_original = y.color
        if z.izquierdo is NIL:
            x = z.derecho
            self._transplant(z, z.derecho)
        elif z.derecho is NIL:
            x = z.izquierdo
            self._transplant(z, z.izquierdo)
        else:
            y = self._minimo(z.derecho)  # sucesor in-order
            y_color_original = y.color
            x = y.derecho
            if y.padre == z:
                x.padre = y
            else:
                self._transplant(y, y.derecho)
                y.derecho = z.derecho
                y.derecho.padre = y
            self._transplant(z, y)
            y.izquierdo = z.izquierdo
            y.izquierdo.padre = y
            y.color = z.color
        if y_color_original == Color.NEGRO:
            self._fix_eliminar(x)  # se perdio un nodo NEGRO

    def _fix_eliminar(self, x):
        while x != self.raiz and x.color == Color.NEGRO:
            if x == x.padre.izquierdo:
                w = x.padre.derecho  # hermano
                if w.color == Color.ROJO:  # Caso 1
                    w.color = Color.NEGRO
                    x.padre.color = Color.ROJO
                    self._rot_izq(x.padre)
                    w = x.padre.derecho
                if w.izquierdo.color == Color.NEGRO and w.derecho.color == Color.NEGRO:
                    w.color = Color.ROJO
                    x = x.padre  # Caso 2
                else:
                    if w.derecho.color == Color.NEGRO:  # Caso 3
                        w.izquierdo.color = Color.NEGRO
                        w.color = Color.ROJO
                        self._rot_der(w)
                        w = x.padre.derecho
                    w.color = x.padre.color  # Caso 4
                    x.padre.color = Color.NEGRO
                    w.derecho.color = Color.NEGRO
                    self._rot_izq(x.padre)
                    x = self.raiz
            else:  # simetrico
                w = x.padre.izquierdo
                if w.color == Color.ROJO:
                    w.color = Color.NEGRO
                    x.padre.color = Color.ROJO
                    self._rot_der(x.padre)
                    w = x.padre.izquierdo
                if w.derecho.color == Color.NEGRO and w.izquierdo.color == Color.NEGRO:
                    w.color = Color.ROJO
                    x = x.padre
                else:
                    if w.izquierdo.color == Color.NEGRO:
                        w.derecho.color = Color.NEGRO
                        w.color = Color.ROJO
                        self._rot_izq(w)
                        w = x.padre.izquierdo
                    w.color = x.padre.color
                    x.padre.color = Color.NEGRO
                    w.izquierdo.color = Color.NEGRO
                    self._rot_der(x.padre)
                    x = self.raiz
        x.color = Color.NEGRO


if __name__ == "__main__":
    # ── Prueba: padron de 5 facultades UNA-PUNO ─────────────────────────
    padron = ArbolElectoral()
    votantes = [
        ('70512340', 'Mamani Quispe, J.', 'Ing. Sistemas', True),
        ('70512100', 'Huanca Apaza, M.', 'Ing. Civil', True),
        ('70512700', 'Condori Flores, P.', 'Medicina', True),
        ('70512050', 'Ticona Lupaca, R.', 'Contabilidad', False),
        ('70512900', 'Pari Choque, L.', 'Agronomia', True),
    ]
    for v in votantes:
        padron.insertar(v)
    assert verificar_todas(padron.raiz), 'Propiedades RBT violadas tras insercion'
    assert es_bst_valido(padron.raiz), 'Invariante BST violada tras insercion'
    print('Insercion: 5 propiedades VERIFICADAS (P2, P4, P5 + invariante BST)')

    padron.eliminar('70512050')  # Ticona pierde habilitacion -> se da de baja
    assert verificar_todas(padron.raiz), 'Propiedades RBT violadas tras eliminacion'
    assert es_bst_valido(padron.raiz), 'Invariante BST violada tras eliminacion'
    print('Eliminacion: 5 propiedades VERIFICADAS (P2, P4, P5 + invariante BST)')

    encontrado = padron.buscar('70512700')
    print(f"Busqueda 70512700: {encontrado.votante[1]} ({encontrado.votante[2]})")

    bh = altura_negra(padron.raiz)
    print(f"Altura negra final del padron (5 facultades, 4 votantes activos): {bh}")
