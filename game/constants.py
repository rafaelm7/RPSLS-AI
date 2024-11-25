from enum import Enum

class Jogada(Enum):
    PEDRA = "PEDRA"
    PAPEL = "PAPEL"
    TESOURA = "TESOURA"
    LAGARTO = "LAGARTO"
    SPOCK = "SPOCK"

# Define as combinações vencedoras como um dicionário
REGRAS_VITORIA = {
    Jogada.PEDRA: [Jogada.TESOURA, Jogada.LAGARTO],    # Pedra esmaga Tesoura e Lagarto
    Jogada.PAPEL: [Jogada.PEDRA, Jogada.SPOCK],        # Papel cobre Pedra e refuta Spock
    Jogada.TESOURA: [Jogada.PAPEL, Jogada.LAGARTO],    # Tesoura corta Papel e decapita Lagarto
    Jogada.LAGARTO: [Jogada.PAPEL, Jogada.SPOCK],      # Lagarto come Papel e envenena Spock
    Jogada.SPOCK: [Jogada.PEDRA, Jogada.TESOURA]       # Spock vaporiza Pedra e quebra Tesoura
}

EMOJIS_JOGADAS = {
    Jogada.PEDRA: "🪨",
    Jogada.PAPEL: "📄",
    Jogada.TESOURA: "✂️",
    Jogada.LAGARTO: "🦎",
    Jogada.SPOCK: "🖖"
}