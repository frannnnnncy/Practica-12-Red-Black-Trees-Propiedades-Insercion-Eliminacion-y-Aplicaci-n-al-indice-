// ── rbt.cpp — Clase ArbolElectoral en C++17 (insercion + eliminacion) ──
#include "rbt.hpp"

class ArbolElectoral {
    NodoRBT* NIL;
    NodoRBT* raiz;
    std::vector<NodoRBT*> todos; // para liberar memoria al final

    void rotIzq(NodoRBT* x) {
        NodoRBT* y = x->derecho;
        x->derecho = y->izquierdo;
        if (y->izquierdo != NIL) y->izquierdo->padre = x;
        y->padre = x->padre;
        if (x->padre == NIL) raiz = y;
        else if (x == x->padre->izquierdo) x->padre->izquierdo = y;
        else x->padre->derecho = y;
        y->izquierdo = x; x->padre = y;
    }

    void rotDer(NodoRBT* y) {
        NodoRBT* x = y->izquierdo;
        y->izquierdo = x->derecho;
        if (x->derecho != NIL) x->derecho->padre = y;
        x->padre = y->padre;
        if (y->padre == NIL) raiz = x;
        else if (y == y->padre->derecho) y->padre->derecho = x;
        else y->padre->izquierdo = x;
        x->derecho = y; y->padre = x;
    }

    void fixInsertar(NodoRBT* z) {
        while (z->padre->color == Color::ROJO) {
            if (z->padre == z->padre->padre->izquierdo) {
                NodoRBT* tio = z->padre->padre->derecho;
                if (tio->color == Color::ROJO) {
                    z->padre->color = tio->color = Color::NEGRO;
                    z->padre->padre->color = Color::ROJO; z = z->padre->padre;
                } else {
                    if (z == z->padre->derecho) { z = z->padre; rotIzq(z); }
                    z->padre->color = Color::NEGRO;
                    z->padre->padre->color = Color::ROJO;
                    rotDer(z->padre->padre);
                }
            } else { // simetrico
                NodoRBT* tio = z->padre->padre->izquierdo;
                if (tio->color == Color::ROJO) {
                    z->padre->color = tio->color = Color::NEGRO;
                    z->padre->padre->color = Color::ROJO; z = z->padre->padre;
                } else {
                    if (z == z->padre->izquierdo) { z = z->padre; rotDer(z); }
                    z->padre->color = Color::NEGRO;
                    z->padre->padre->color = Color::ROJO;
                    rotIzq(z->padre->padre);
                }
            }
        }
        raiz->color = Color::NEGRO;
    }

    // ---------------------------------------------------------------
    // EXTENSION: eliminacion completa (transplant + 4 sub-casos del
    // hermano w, simetricos a los 6 casos de doble-negro)
    // ---------------------------------------------------------------
    void transplant(NodoRBT* u, NodoRBT* v) {
        if (u->padre == NIL) raiz = v;
        else if (u == u->padre->izquierdo) u->padre->izquierdo = v;
        else u->padre->derecho = v;
        v->padre = u->padre;
    }

    NodoRBT* minimo(NodoRBT* n) const {
        while (n->izquierdo != NIL) n = n->izquierdo;
        return n;
    }

    void fixEliminar(NodoRBT* x) {
        while (x != raiz && x->color == Color::NEGRO) {
            if (x == x->padre->izquierdo) {
                NodoRBT* w = x->padre->derecho;
                if (w->color == Color::ROJO) { // Caso 1
                    w->color = Color::NEGRO; x->padre->color = Color::ROJO;
                    rotIzq(x->padre); w = x->padre->derecho;
                }
                if (w->izquierdo->color == Color::NEGRO && w->derecho->color == Color::NEGRO) {
                    w->color = Color::ROJO; x = x->padre; // Caso 2
                } else {
                    if (w->derecho->color == Color::NEGRO) { // Caso 3
                        w->izquierdo->color = Color::NEGRO; w->color = Color::ROJO;
                        rotDer(w); w = x->padre->derecho;
                    }
                    w->color = x->padre->color; // Caso 4
                    x->padre->color = Color::NEGRO;
                    w->derecho->color = Color::NEGRO;
                    rotIzq(x->padre); x = raiz;
                }
            } else { // simetrico
                NodoRBT* w = x->padre->izquierdo;
                if (w->color == Color::ROJO) {
                    w->color = Color::NEGRO; x->padre->color = Color::ROJO;
                    rotDer(x->padre); w = x->padre->izquierdo;
                }
                if (w->derecho->color == Color::NEGRO && w->izquierdo->color == Color::NEGRO) {
                    w->color = Color::ROJO; x = x->padre;
                } else {
                    if (w->izquierdo->color == Color::NEGRO) {
                        w->derecho->color = Color::NEGRO; w->color = Color::ROJO;
                        rotIzq(w); w = x->padre->izquierdo;
                    }
                    w->color = x->padre->color;
                    x->padre->color = Color::NEGRO;
                    w->izquierdo->color = Color::NEGRO;
                    rotDer(x->padre); x = raiz;
                }
            }
        }
        x->color = Color::NEGRO;
    }

public:
    ArbolElectoral() {
        NIL = new NodoRBT(); NIL->color = Color::NEGRO;
        NIL->izquierdo = NIL->derecho = NIL->padre = NIL;
        raiz = NIL; todos.push_back(NIL);
    }
    ~ArbolElectoral() { for (auto* n : todos) delete n; }

    void insertar(Votante v) {
        NodoRBT* z = new NodoRBT();
        z->votante = v; z->izquierdo = z->derecho = z->padre = NIL;
        todos.push_back(z);
        NodoRBT *y = NIL, *x = raiz;
        while (x != NIL) {
            y = x;
            x = (v.dni < x->votante.dni) ? x->izquierdo : x->derecho;
        }
        z->padre = y;
        if (y == NIL) raiz = z;
        else if (v.dni < y->votante.dni) y->izquierdo = z;
        else y->derecho = z;
        fixInsertar(z);
    }

    NodoRBT* buscar(const std::string& dni) const {
        NodoRBT* x = raiz;
        while (x != NIL && x->votante.dni != dni)
            x = (dni < x->votante.dni) ? x->izquierdo : x->derecho;
        return x == NIL ? nullptr : x;
    }

    void eliminar(const std::string& dni) {
        NodoRBT* z = buscar(dni);
        if (!z) throw std::runtime_error("DNI no encontrado: " + dni);
        NodoRBT* y = z;
        Color yColorOriginal = y->color;
        NodoRBT* x;
        if (z->izquierdo == NIL) {
            x = z->derecho;
            transplant(z, z->derecho);
        } else if (z->derecho == NIL) {
            x = z->izquierdo;
            transplant(z, z->izquierdo);
        } else {
            y = minimo(z->derecho);
            yColorOriginal = y->color;
            x = y->derecho;
            if (y->padre == z) {
                x->padre = y;
            } else {
                transplant(y, y->derecho);
                y->derecho = z->derecho;
                y->derecho->padre = y;
            }
            transplant(z, y);
            y->izquierdo = z->izquierdo;
            y->izquierdo->padre = y;
            y->color = z->color;
        }
        if (yColorOriginal == Color::NEGRO) fixEliminar(x);
    }

    bool esRBTValido() const {
        return raiz->color == Color::NEGRO && p4(raiz) && p5(raiz) != -1;
    }

    int alturaNegra() const { return p5(raiz); }

private:
    bool p4(NodoRBT* n) const {
        if (n == NIL) return true;
        if (n->color==Color::ROJO &&
            (n->izquierdo->color==Color::ROJO || n->derecho->color==Color::ROJO))
            return false;
        return p4(n->izquierdo) && p4(n->derecho);
    }
    int p5(NodoRBT* n) const {
        if (n == NIL) return 0;
        int bl = p5(n->izquierdo), br = p5(n->derecho);
        if (bl==-1 || br==-1 || bl!=br) return -1;
        return bl + (n->color==Color::NEGRO ? 1 : 0);
    }
};

int main() {
    ArbolElectoral padron;
    padron.insertar({"70512340","Mamani Quispe, J.","Ing. Sistemas",true});
    padron.insertar({"70512100","Huanca Apaza, M.", "Ing. Civil", true});
    padron.insertar({"70512700","Condori Flores, P.","Medicina", true});
    padron.insertar({"70512050","Ticona Lupaca, R.", "Contabilidad",false});
    padron.insertar({"70512900","Pari Choque, L.", "Agronomia", true});

    std::cout << "RBT valido tras insercion: " << padron.esRBTValido() << '\n';
    std::cout << "Altura negra tras insercion: " << padron.alturaNegra() << '\n';

    auto* v = padron.buscar("70512700");
    std::cout << "Buscar 70512700: " << (v ? v->votante.nombre : "no encontrado") << '\n';

    // Extension: eliminacion (Actividad 5, requerida por la rubrica de C++)
    padron.eliminar("70512050"); // Ticona pierde habilitacion -> se da de baja
    std::cout << "RBT valido tras eliminacion de 70512050: " << padron.esRBTValido() << '\n';
    std::cout << "Altura negra tras eliminacion: " << padron.alturaNegra() << '\n';

    auto* borrado = padron.buscar("70512050");
    std::cout << "Buscar 70512050 (deberia no existir): "
              << (borrado ? borrado->votante.nombre : "no encontrado") << '\n';

    // Eliminaciones adicionales para ejercitar mas casos del fix-up
    padron.eliminar("70512340");
    padron.eliminar("70512900");
    std::cout << "RBT valido tras 3 eliminaciones totales: " << padron.esRBTValido() << '\n';
    std::cout << "Altura negra final: " << padron.alturaNegra() << '\n';

    return 0;
}
