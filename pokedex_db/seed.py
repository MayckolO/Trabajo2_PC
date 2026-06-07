# seed.py
from sqlmodel import Session, select
from models import (
    Batalla, Entrenador, Participacion,
    Pokemon, PokemonTipo, Region, Tipo,
)

def poblado(session: Session) -> bool:
    return session.exec(select(Region)).first() is not None


def poblar(session: Session) -> None:
    if poblado(session):
        print("Ya hay datos..")
        return

    kanto  = Region(nombre="Kanto",  generacion=1, descripcion="La región original.")
    johto  = Region(nombre="Johto",  generacion=2, descripcion="Tierra de tradiciones.")
    hoenn  = Region(nombre="Hoenn",  generacion=3, descripcion="Rica en agua y tierra.")
    sinnoh = Region(nombre="Sinnoh", generacion=4, descripcion="Hogar del dios Pokémon.")
    unova  = Region(nombre="Unova",  generacion=5, descripcion="Región industrial.")
    session.add_all([kanto, johto, hoenn, sinnoh, unova])
    session.commit()
    for r in [kanto, johto, hoenn, sinnoh, unova]:
        session.refresh(r)

    fuego    = Tipo(nombre="Fuego",    color_hex="#F08030")
    agua     = Tipo(nombre="Agua",     color_hex="#6890F0")
    electrico = Tipo(nombre="Eléctrico", color_hex="#F8D030")
    planta   = Tipo(nombre="Planta",   color_hex="#78C850")
    normal   = Tipo(nombre="Normal",   color_hex="#A8A878")
    psiquico = Tipo(nombre="Psíquico", color_hex="#F85888")
    dragon   = Tipo(nombre="Dragón",   color_hex="#7038F8")
    hielo    = Tipo(nombre="Hielo",    color_hex="#98D8D8")
    siniestro = Tipo(nombre="Siniestro", color_hex="#705848")
    session.add_all([fuego, agua, electrico, planta, normal,
                     psiquico, dragon, hielo, siniestro])
    session.commit()
    for t in [fuego, agua, electrico, planta, normal,
              psiquico, dragon, hielo, siniestro]:
        session.refresh(t)

    ash    = Entrenador(nombre="Ash",    edad=10, insignias=8, es_campeon=True,  region_id=kanto.id)
    misty  = Entrenador(nombre="Misty",  edad=12, insignias=5, es_campeon=False, region_id=kanto.id)
    brock  = Entrenador(nombre="Brock",  edad=15, insignias=8, es_campeon=False, region_id=kanto.id)
    gary   = Entrenador(nombre="Gary",   edad=10, insignias=8, es_campeon=True,  region_id=kanto.id)
    may    = Entrenador(nombre="May",    edad=10, insignias=4, es_campeon=False, region_id=hoenn.id)
    dawn   = Entrenador(nombre="Dawn",   edad=10, insignias=3, es_campeon=False, region_id=sinnoh.id)
    serena = Entrenador(nombre="Serena", edad=10, insignias=6, es_campeon=True,  region_id=johto.id)
    ethan  = Entrenador(nombre="Ethan",  edad=13, insignias=8, es_campeon=True,  region_id=johto.id)
    iris   = Entrenador(nombre="Iris",   edad=12, insignias=7, es_campeon=False, region_id=unova.id)
    session.add_all([ash, misty, brock, gary, may, dawn, serena, ethan, iris])
    session.commit()
    for e in [ash, misty, brock, gary, may, dawn, serena, ethan, iris]:
        session.refresh(e)

    datos_pokemon = [
        ("Pikachu",          85, 210, False, "Pika",      ash),
        ("Charizard",        90, 320, False, None,        ash),
        ("Snorlax",          75, 500, True,  "Gordo",     ash),
        ("Bulbasaur",        15, 105, False, None,        ash),
        ("Staryu",           55, 180, False, None,        misty),
        ("Starmie",          80, 230, True,  "Estrella",  misty),
        ("Psyduck",          18, 115, False, None,        misty),
        ("Onix",             60, 290, False, None,        brock),
        ("Geodude",          12, 120, False, None,        brock),
        ("Blastoise",        88, 340, False, None,        gary),
        ("Eevee",            20, 130, True,  "Evee",      gary),
        ("Nidoking",         78, 280, False, None,        gary),
        ("Blaziken",         92, 310, False, None,        may),
        ("Beautifly",        35, 150, False, None,        may),
        ("Piplup",           10, 100, False, None,        dawn),
        ("Lucario",          82, 270, False, None,        dawn),
        ("Ampharos",         70, 245, False, None,        serena),
        ("Espeon",           65, 220, True,  "Espis",     serena),
        ("Typhlosion",       95, 350, False, None,        ethan),
        ("Feraligatr",       88, 330, False, None,        ethan),
        ("Dragonite",        88, 360, False, None,        iris),
        ("Axew",             14, 108, False, None,        iris),
    ]
    poke_objs: list[Pokemon] = []
    for nombre, nivel, pv, shiny, apodo, entrenador in datos_pokemon:
        p = Pokemon(
            nombre=nombre, nivel=nivel, puntos_vida=pv,
            es_shiny=shiny, apodo=apodo, entrenador_id=entrenador.id,
        )
        session.add(p)
        poke_objs.append(p)
    session.commit()
    for p in poke_objs:
        session.refresh(p)
    pk = {p.nombre: p for p in poke_objs}

    asignaciones = [
        (pk["Pikachu"],   electrico),
        (pk["Charizard"], fuego),   (pk["Charizard"], dragon),
        (pk["Snorlax"],   normal),
        (pk["Bulbasaur"], planta),
        (pk["Staryu"],    agua),
        (pk["Starmie"],   agua),    (pk["Starmie"],   psiquico),
        (pk["Psyduck"],   agua),    (pk["Psyduck"],   psiquico),
        (pk["Onix"],      normal),
        (pk["Geodude"],   normal),
        (pk["Blastoise"], agua),
        (pk["Eevee"],     normal),
        (pk["Nidoking"],  normal),  (pk["Nidoking"],  dragon),
        (pk["Blaziken"],  fuego),
        (pk["Beautifly"], planta),
        (pk["Piplup"],    agua),
        (pk["Lucario"],   psiquico),
        (pk["Ampharos"],  electrico),
        (pk["Espeon"],    psiquico),
        (pk["Typhlosion"],fuego),
        (pk["Feraligatr"],agua),
        (pk["Dragonite"], dragon),  (pk["Dragonite"], hielo),
        (pk["Axew"],      dragon),
    ]
    for pokemon, tipo in asignaciones:
        session.add(PokemonTipo(pokemon_id=pokemon.id, tipo_id=tipo.id))
    session.commit()

    batallas_data = [
        ("2026-01-10", "Gimnasio de Plateópolis", 3, ash),
        ("2026-01-15", "Liga Pokémon de Kanto",   5, gary),
        ("2026-02-01", "Ciudad Carmín",            3, misty),
        ("2026-02-20", "Cueva Zafiro",             4, may),
        ("2026-03-05", "Monte Corona",             2, None),
        ("2026-03-18", "Ciudad Nuvema",            3, ethan),
        ("2026-04-10", "Pueblo Raíz",              4, None),
    ]
    batalla_objs: list[Batalla] = []
    for fecha, lugar, rondas, ganador in batallas_data:
        b = Batalla(
            fecha=fecha, lugar=lugar, rondas=rondas,
            ganador_id=ganador.id if ganador else None,
        )
        session.add(b)
        batalla_objs.append(b)
    session.commit()
    for b in batalla_objs:
        session.refresh(b)

    partic = [
        (batalla_objs[0], ash,    "victoria", misty,  "derrota"),
        (batalla_objs[1], gary,   "victoria", ash,    "derrota"),
        (batalla_objs[2], misty,  "victoria", brock,  "derrota"),
        (batalla_objs[3], may,    "victoria", dawn,   "derrota"),
        (batalla_objs[4], serena, "empate",   ethan,  "empate"),
        (batalla_objs[5], ethan,  "victoria", iris,   "derrota"),
        (batalla_objs[6], ash,    "empate",   gary,   "empate"),
    ]
    for batalla, e1, r1, e2, r2 in partic:
        session.add(Participacion(entrenador_id=e1.id, batalla_id=batalla.id, resultado=r1))
        session.add(Participacion(entrenador_id=e2.id, batalla_id=batalla.id, resultado=r2))
    session.commit()
    print("Base de datos poblada exitosamente!")