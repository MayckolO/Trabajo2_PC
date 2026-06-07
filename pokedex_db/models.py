from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class PokemonTipo(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    tipo_id: int = Field(foreign_key="tipo.id",    primary_key=True)
    
class Participacion(SQLModel, table=True):
    entrenador_id: int = Field(foreign_key="entrenador.id", primary_key=True)
    batalla_id: int = Field(foreign_key="batalla.id",    primary_key=True)
    resultado: str

class Region(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    generacion: int
    description: Optional[str] = None
    
    entrenadores: list["Entrenador"] = Relationship(back_populates="region")
  
class Entrenador(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    edad: int = Field(ge=10)
    insignias: int = Field(ge=0, le=8)
    es_campeon: Optional[bool] = None
    region_id: int | None = Field(default=None, foreign_key="region.id")
    
    region:   Optional[Region]  = Relationship(back_populates="entrenadores")
    pokemons: list["Pokemon"]   = Relationship(back_populates="entrenador")
    batallas: list["Batalla"]   = Relationship(back_populates="participantes", link_model=Participacion)
    
class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    nivel: int = Field(ge=1, le=100)
    puntos_vida: int = Field(gt=0)
    es_shiny: Optional[bool] = False
    apodo: Optional[str] = None
    entrenador_id: int = Field(foreign_key="entrenador.id")
    
    entrenador: Optional[Entrenador] = Relationship(back_populates="pokemons")
    tipos: list["Tipo"] = Relationship(back_populates="pokemons", link_model=PokemonTipo)

class Tipo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    color_hex: Optional[str] = None
    
    pokemons: list[Pokemon] = Relationship(back_populates="tipos", link_model=PokemonTipo)
    
class Batalla(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha: str
    lugar: str
    rondas: int = Field(gt=0)
    ganador_id: Optional[int] = Field(default=None, foreign_key="entrenador.id")
    
    participantes: list[Entrenador] = Relationship(back_populates="batallas", link_model=Participacion)