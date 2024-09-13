import reflex as rx
from suma_resta.suma_resta import OperState
from rxconfig import config

#import suma_resta

class State(rx.State):
    @staticmethod
    def res():
        var = OperState.suma_numbers

@rx.page(route="/play",title="Juego")
def play() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.icon(tag="check", size=48), ),
        rx.vstack(
        rx.heading(
            f"Comprueba si acertaste al resultado",size="8",align="center"
        ),spacing="19", justify="center", align="center")
            , background_color="hsla(0, 100%, 50%, 0.1)",#"var(--accent-2)",
            border_radius="15px",
            width="95%",
            margin="24px",
            padding="25px",
            aling="center",
            justify="center",
        ),rx.box(
            rx.vstack(rx.text("El resultado es: ",size="5",),
        rx.text(f"{OperState.suma_numbers}",size="9",weight="bold")
        ,align="center"
        ,spacing="3"
        ,),
        rx.vstack(rx.link("Volver a jugar!", size="4",href="/",)
        ,spacing="3",
        justify="center",
        align="center"
        ),#,align="center",spacing="8"),
            background_color="var(--plum-3)",
        border_radius="15px",
        width="95%",
        margin="24px",
        padding="24px",
        aling="center",justify="center",)