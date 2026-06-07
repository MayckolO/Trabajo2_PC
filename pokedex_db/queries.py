# queries.py
from sqlalchemy import case, func
from sqlmodel import Session, select, text

from models import Entrenador, Participacion, Pokemon, PokemonTipo, Region, Tipo

def pokemon_alto_nivel(session: Session, umbral: int = 70) -> list[Pokemon]:
    """Retorna Pokémon con nivel >= umbral, de mayor a menor nivel."""
    stmt = (
        select(Pokemon)
        .where(Pokemon.nivel >= umbral)
        .order_by(Pokemon.nivel.desc())
    )
    return list(session.exec(stmt).all())

def campeones_por_region(session: Session, nombre_region: str) -> list[Entrenador]:
    """Retorna entrenadores campeones de la región indicada."""
    stmt = (
        select(Entrenador)
        .join(Region, Entrenador.region_id == Region.id)
        .where(Region.nombre == nombre_region)
        .where(Entrenador.es_campeon == True)
    )
    return list(session.exec(stmt).all())

def shiny_con_apodo(session: Session) -> list[tuple[str, str, int, str]]:
    """Retorna (nombre_pokemon, apodo, nivel, nombre_entrenador) para shiny con apodo."""
    stmt = (
        select(Pokemon.nombre, Pokemon.apodo, Pokemon.nivel, Entrenador.nombre)
        .join(Entrenador, Pokemon.entrenador_id == Entrenador.id)
        .where(Pokemon.es_shiny == True)
        .where(Pokemon.apodo != None)
    )
    return list(session.exec(stmt).all())

def promedio_nivel_por_entrenador(session: Session) -> list[tuple[str, float]]:
    """Retorna (nombre, promedio_nivel) de entrenadores con Pokémon, desc por promedio."""
    stmt = (
        select(
            Entrenador.nombre,
            func.round(func.avg(Pokemon.nivel), 2).label("avg_nivel"),
        )
        .join(Pokemon, Pokemon.entrenador_id == Entrenador.id)
        .group_by(Entrenador.id)
        .order_by(func.avg(Pokemon.nivel).desc())
    )
    return list(session.exec(stmt).all())


def conteo_pokemon_por_tipo(session: Session) -> list[tuple[str, int]]:
    """Retorna (nombre_tipo, cantidad) para tipos con al menos un Pokémon, desc."""
    stmt = (
        select(Tipo.nombre, func.count(PokemonTipo.pokemon_id).label("total"))
        .join(PokemonTipo, PokemonTipo.tipo_id == Tipo.id)
        .group_by(Tipo.id)
        .order_by(func.count(PokemonTipo.pokemon_id).desc())
    )
    return list(session.exec(stmt).all())


def estadisticas_batallas(session: Session) -> list[tuple[str, int, int, int]]:
    """Retorna (nombre, total_batallas, victorias, derrotas) desc por total."""
    stmt = (
        select(
            Entrenador.nombre,
            func.count(Participacion.batalla_id).label("total"),
            func.sum(
                case((Participacion.resultado == "victoria", 1), else_=0)
            ).label("victorias"),
            func.sum(
                case((Participacion.resultado == "derrota", 1), else_=0)
            ).label("derrotas"),
        )
        .join(Participacion, Participacion.entrenador_id == Entrenador.id)
        .group_by(Entrenador.id)
        .order_by(func.count(Participacion.batalla_id).desc())
    )
    return list(session.exec(stmt).all())


def region_mas_insignias(session: Session) -> tuple[str, float]:
    """Retorna (nombre_region, promedio_insignias) de la región con mayor promedio."""
    stmt = (
        select(
            Region.nombre,
            func.round(func.avg(Entrenador.insignias), 2).label("avg_ins"),
        )
        .join(Entrenador, Entrenador.region_id == Region.id)
        .group_by(Region.id)
        .order_by(func.avg(Entrenador.insignias).desc(), Region.nombre.asc())
        .limit(1)
    )
    return session.exec(stmt).first()