# decoradores.py
from functools import wraps

def aumentar_velocidad(incremento: float = 1.5):
    def decorator(cls):
        original_init = cls.__init__

        @wraps(cls.__init__)
        def new_init(self, especie, nivelEnergia, velocidad, ubicacion, *args, **kwargs):
            # Llamamos al init original pero con la velocidad aumentada
            velocidad_aumentada = velocidad * incremento
            original_init(self, especie, nivelEnergia, velocidad_aumentada, ubicacion, *args, **kwargs)
            print(f"Velocidad aumentada de {velocidad} a {velocidad_aumentada}")

        cls.__init__ = new_init
        return cls

    return decorator