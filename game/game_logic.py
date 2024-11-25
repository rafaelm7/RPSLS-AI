from typing import Tuple
from .constants import Jogada, REGRAS_VITORIA

class LogicaJogo:
    @staticmethod
    def determinar_vencedor(jogada_jogador: Jogada, jogada_ia: Jogada) -> Tuple[str, str]:
        """Determina o vencedor e retorna (resultado, descrição)."""
        if jogada_jogador == jogada_ia:
            return "EMPATE", "Empate!"
            
        if jogada_ia in REGRAS_VITORIA[jogada_jogador]:
            return "VITORIA", f"{jogada_jogador.value} vence {jogada_ia.value}!"
            
        return "DERROTA", f"{jogada_ia.value} vence {jogada_jogador.value}!"