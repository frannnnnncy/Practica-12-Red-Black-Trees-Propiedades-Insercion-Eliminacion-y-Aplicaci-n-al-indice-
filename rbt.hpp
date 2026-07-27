#pragma once
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <iostream>

enum class Color { ROJO, NEGRO };

struct Votante {
    std::string dni, nombre, facultad;
    bool habilitado;
};

struct NodoRBT {
    Votante votante;
    Color color = Color::ROJO;
    NodoRBT* izquierdo = nullptr;
    NodoRBT* derecho = nullptr;
    NodoRBT* padre = nullptr;
};
