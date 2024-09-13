import asyncio

import reflex as rx
import random

#from suma_resta.play import play

class OperState(rx.State):
    salir: bool = False
    running: bool = False
    val_len_num: bool = False
    number: int = 0
    suma_numbers: int = 0
    numbers_seen: list = []
    total: int = 0
    totalseg: int = 0
    len_num_seen: int
    text = "Ver Resultado"
    _n_tasks: int = 0

    def handle_reset(self):
        self.reset()

    @rx.background
    async def update(self):
        async with self:
            # The latest state values are always available inside the context
            if self._n_tasks > 0:
                # only allow 1 concurrent task
                return
            # State mutation is only allowed inside context block
            self._n_tasks += 1
        while True:
            async with self:
                self.number = random.randrange(-20,20,1)
                self.numbers_seen.append(self.number)
                self.suma_numbers +=  self.number
                if len(self.numbers_seen) > 0:
                    len_num_seen = len(self.numbers_seen)
                else:
                    len_num_seen = 0
                if len_num_seen == int(self.total):
                    self.salir = True
                    self.totalseg = 0
                    self.total = 0
                    self.running = False
                else:
                    self.salir
                if not self.running:
                    self._n_tasks -= 1
                    return
            await asyncio.sleep(int(self.totalseg))

    def toggle_running(self):
        self.running = not self.running
        if self.running:
            return OperState.update

    def totalnumeros(self, val):
        if val:
            self.total = val
            self.val_len_num = True
        else:
            self.total = OperState.total

    def totalsegs(self, val):
        if val:
            self.totalseg = val
        else:
            self.totalseg = OperState.totalseg

    def input_on_key_down(self,event):
        if event == "Backspace":
            self.total = ""

    @rx.var(cache=True)
    def page_number(self) -> int:
        if len(self.numbers_seen) > 0:
            return len(self.numbers_seen)
        else:
            return 0

    def ver_sumas(self):
        if self.text == "Ver Resultado":
            self.text = "El resultado es: ",f"{self.suma_numbers}"
        else:
            self.text ="Ver Resultado"

def index():
    return (
       # rx.script("document.documentElement.lang='es'"),
        rx.box(
            rx.flex(
                rx.icon(tag="calculator", size=48),),
        rx.vstack(
        rx.heading(
            f"Bienvenido al juego de suma y resta"
            ,size="8",align="center"
            ),spacing="19", justify="center", align="center"
        )
    , background_color="hsla(0, 100%, 50%, 0.1)",
    border_radius = "15px",
    width = "95%",
    margin = "24px",
    padding = "25px",
    aling = "center",
    justify = "center",
    ),rx.box(
        rx.cond(~OperState.salir & OperState.totalseg==0,
          rx.vstack(
              rx.vstack(rx.text(
            "Ingrese el total de Numeros:",size="5"),
            rx.input(
             on_change=OperState.totalnumeros,size="3",on_key_down=OperState.input_on_key_down,
            ),align="center",spacing="3"),
            rx.vstack(rx.text(
                "Ingrese el intervalo de tiempo en segundos entre Numeros:",size="5"),
            rx.input(
             on_change=OperState.totalsegs,size="3",
            ),align="center",spacing="3")
            ,justify="center",
            align="center",spacing="5",
          ),rx.text()
        ),
        rx.cond(~OperState.salir,
        rx.hstack(
            rx.cond(OperState.totalseg==0,rx.text(),rx.text(
                f"Total Numeros: ",
                rx.badge(
                    OperState.total,
                    variant="soft",
                    color_scheme="blue",size="3",
                ),size="5"
            )),
            rx.cond(OperState.totalseg==0,rx.text(),rx.text(
                f"Segundos entre Numeros: ",
                rx.badge(
                    OperState.totalseg,
                    variant="soft",
                    color_scheme="blue",size="3",
                ),size="5",
            )),
            justify="center",
            align="center"
        ),
         rx.text()
        ),
        rx.cond(OperState.totalseg==0,
                rx.text(),
                rx.vstack(
                rx.cond(OperState.totalseg>0,
                            rx.vstack(
                                rx.button("Iniciar Secuencia", on_click=OperState.toggle_running)
                                ,margin_top="3em",spacing="5"),
                            rx.text("",
                                size="9",)
                        ),
                        rx.cond(OperState.page_number>0,
                            rx.text(f"Secuencia de Numeros: ",
                            rx.text(
                                OperState.number,
                                size="9",weight="bold",align="center"
                            ),
                        ),rx.text())
                ,spacing="5",
                justify="center",
                align="center")
        ),
        rx.cond(OperState.salir & OperState.page_number>0,
            rx.vstack
            (
              rx.text(f"Fin de la Secuencia de Numeros: ", size="4",),
                    rx.text(
                        OperState.number,
                        size="9", weight="bold", align="center"),
                rx.link("Validar el resultado!", size="4", href="/play/", on_click=OperState.ver_sumas),
                    justify="center",
                    align="center"
            ),rx.vstack()
        )
        , background_color="var(--plum-3)",
        border_radius="45px",
        width="95%",
        margin="24px",
        padding="25px",
        aling="center",
        justify="center",
    )
)


app = rx.App(style={"breakpoints": ["520px", "768px", "1024px", "1280px", "1640px"]})


app.add_page(index, on_load=OperState.handle_reset)