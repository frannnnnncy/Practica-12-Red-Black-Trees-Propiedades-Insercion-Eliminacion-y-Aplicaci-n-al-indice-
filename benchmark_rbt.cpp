// ── benchmark_rbt.cpp — Carga mixta realista ────────────────────────────
#include <iostream>
#include <string>
#include <map>
#include <chrono>
#include <random>
#include <vector>
#include <algorithm>

struct Votante {
    std::string dni, nombre, facultad;
    bool habilitado;
};

using Clock = std::chrono::high_resolution_clock;

void simulacionCargaMixta(int n) {
    std::map<std::string, Votante> padron;
    std::mt19937 rng(42);
    std::vector<std::string> dnis;

    auto t0 = Clock::now();
    // Fase 1: matricula masiva (n altas)
    for (int i = 0; i < n; i++) {
        std::string dni = "70" + std::to_string(500000 + i);
        padron[dni] = {dni, "Estudiante_"+std::to_string(i), "Ing.Sistemas", true};
        dnis.push_back(dni);
    }
    auto t1 = Clock::now();

    // Fase 2: depuracion - 20% de bajas (deuda academica) intercaladas
    std::shuffle(dnis.begin(), dnis.end(), rng);
    int bajas = n / 5;
    for (int i = 0; i < bajas; i++) padron.erase(dnis[i]);
    auto t2 = Clock::now();

    // Fase 3: verificacion de elegibilidad - 50,000 consultas
    int encontrados = 0;
    for (int i = 0; i < 50000; i++) {
        std::string dni = dnis[rng() % dnis.size()];
        if (padron.count(dni)) encontrados++;
    }
    auto t3 = Clock::now();

    double ms_alta = std::chrono::duration<double,std::milli>(t1-t0).count();
    double ms_baja = std::chrono::duration<double,std::milli>(t2-t1).count();
    double ms_busq = std::chrono::duration<double,std::milli>(t3-t2).count();

    std::cout << "N=" << n
              << " | altas:" << ms_alta << "ms"
              << " | bajas:" << ms_baja << "ms (" << bajas << " registros)"
              << " | 50K consultas:" << ms_busq << "ms"
              << " | encontrados:" << encontrados
              << " | tamano final:" << padron.size() << '\n';
}

int main() {
    for (int n : {1000, 10000, 100000}) simulacionCargaMixta(n);
    return 0;
}
