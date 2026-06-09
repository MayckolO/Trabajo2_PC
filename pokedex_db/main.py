# main.py
import sys

sys.stdout.reconfigure(encoding="utf-8")

from database import create_db, get_session
from queries import (
    campeones_por_region,
    consulta_libre,
    conteo_pokemon_por_tipo,
    estadisticas_batallas,
    pokemon_alto_nivel,
    promedio_nivel_por_entrenador,
    region_mas_insignias,
    shiny_con_apodo,
)
from seed import poblar

def main() -> None:
    print("=" * 60)
    print("  Pokédex DB — EC2 Programación Científica con Python")
    print("=" * 60)

    print("\n[1] Recreando tablas...")
    create_db()
    
    print("\n[2] Poblando base de datos...")
    session = next(get_session())
    poblar(session)

    print("\n[Q1] Pokémon de alto nivel (nivel >= 70):")
    for p in pokemon_alto_nivel(session, umbral=70):
        apodo = f" ({p.apodo})" if p.apodo else ""
        print(f"  • {p.nombre}{apodo} — Nivel {p.nivel}")

    print("\n[Q2] Campeones de Kanto:")
    for e in campeones_por_region(session, "Kanto"):
        print(f"  • {e.nombre} — {e.insignias} insignias")

    print("\n[Q3] Pokémon shiny con apodo:")
    for nombre, apodo, nivel, entrenador in shiny_con_apodo(session):
        print(f"  • {nombre} '{apodo}' — Nv.{nivel} — Entrenador: {entrenador}")

    print("\n[Q4] Promedio de nivel por entrenador:")
    for nombre, promedio in promedio_nivel_por_entrenador(session):
        print(f"  • {nombre}: {promedio}")

    print("\n[Q5] Pokémon por tipo:")
    for tipo, cantidad in conteo_pokemon_por_tipo(session):
        print(f"  • {tipo}: {cantidad} Pokémon")

    print("\n[Q6] Estadísticas de batallas:")
    for nombre, total, victorias, derrotas in estadisticas_batallas(session):
        print(f"  • {nombre}: {total} batallas | {victorias}V - {derrotas}D")

    print("\n[Q7] Región con mayor promedio de insignias:")
    region, promedio = region_mas_insignias(session)
    print(f"  • {region} — promedio: {promedio} insignias")

    print("\n[Q8] Ranking de Pokémon por nivel dentro del equipo de cada entrenador:")
    for row in consulta_libre(session):
        shiny = " [shiny]" if row["es_shiny"] else ""
        print(
            f"  • [{row['ranking_en_equipo']}] {row['entrenador']}"
            f" — {row['pokemon']}{shiny} (Nv.{row['nivel']})"
        )

    print("\n" + "=" * 60)
    print("  ¡Todas las consultas ejecutadas exitosamente!")
    print("=" * 60)

if __name__ == "__main__":
    main()