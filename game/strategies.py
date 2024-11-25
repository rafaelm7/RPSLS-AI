from abc import ABC, abstractmethod
import random
from typing import Optional, Dict, List
from collections import defaultdict
import numpy as np
from .constants import Jogada, REGRAS_VITORIA

class EstrategiaBase(ABC):
    @abstractmethod
    def escolher_jogada(self, historico_oponente: List[Jogada], historico_jogadas: List[Jogada]) -> Jogada:
        pass
        
    @abstractmethod
    def aprender(self, jogada_oponente: Jogada, jogada_ia: Jogada, resultado: str) -> None:
        pass

class EstrategiaAleatoria(EstrategiaBase):
    def escolher_jogada(self, historico_oponente: List[Jogada], historico_jogadas: List[Jogada]) -> Jogada:
        return random.choice(list(Jogada))
        
    def aprender(self, jogada_oponente: Jogada, jogada_ia: Jogada, resultado: str) -> None:
        pass

class EstrategiaMarkov(EstrategiaBase):
    def __init__(self):
        self.matriz_transicao = {
            jogada: defaultdict(int) for jogada in Jogada
        }
        self._historico_oponente = []
        self._historico_ia = []
        
    def escolher_jogada(self, historico_oponente: List[Jogada], historico_jogadas: List[Jogada]) -> Jogada:
        if not historico_oponente:
            return random.choice(list(Jogada))
            
        ultima_jogada = historico_oponente[-1]
        transicoes = self.matriz_transicao[ultima_jogada]
        
        if not transicoes:
            return random.choice(list(Jogada))
            
        jogada_prevista = max(transicoes.items(), key=lambda x: x[1])[0]
        return self._escolher_contra_jogada(jogada_prevista)
        
    def _escolher_contra_jogada(self, jogada_prevista: Jogada) -> Jogada:
        jogadas_vencedoras = [
            jogada for jogada in Jogada
            if jogada_prevista in REGRAS_VITORIA[jogada]
        ]
        return random.choice(jogadas_vencedoras) if jogadas_vencedoras else random.choice(list(Jogada))
        
    def aprender(self, jogada_oponente: Jogada, jogada_ia: Jogada, resultado: str) -> None:
        self._historico_oponente.append(jogada_oponente)
        self._historico_ia.append(jogada_ia)
        
        if len(self._historico_oponente) >= 2:
            ultima = self._historico_oponente[-2]
            atual = jogada_oponente
            self.matriz_transicao[ultima][atual] += 1

class EstrategiaQLearning(EstrategiaBase):
    def __init__(self, taxa_aprendizado: float = 0.1, fator_desconto: float = 0.9):
        self.taxa_aprendizado = taxa_aprendizado
        self.fator_desconto = fator_desconto
        self.valores_q = {
            (estado, acao): 0.0 
            for estado in Jogada 
            for acao in Jogada
        }
        
    def escolher_jogada(self, historico_oponente: List[Jogada], historico_jogadas: List[Jogada]) -> Jogada:
        if not historico_oponente:
            return random.choice(list(Jogada))
            
        estado_atual = historico_oponente[-1]
        return max(
            Jogada,
            key=lambda acao: self.valores_q[(estado_atual, acao)]
        )
        
    def aprender(self, jogada_oponente: Jogada, jogada_ia: Jogada, resultado: str) -> None:
        recompensa = 1.0 if resultado == "VITORIA" else -1.0 if resultado == "DERROTA" else 0.0
        
        if len(self._historico_oponente) >= 1:
            estado = self._historico_oponente[-1]
            novo_estado = jogada_oponente
            
            # Atualização Q-Learning
            valor_atual = self.valores_q[(estado, jogada_ia)]
            melhor_proximo = max(self.valores_q[(novo_estado, a)] for a in Jogada)
            
            self.valores_q[(estado, jogada_ia)] += self.taxa_aprendizado * (
                recompensa + self.fator_desconto * melhor_proximo - valor_atual
            )

class EstrategiaEnsemble(EstrategiaBase):
    def __init__(self):
        self.estrategias = [
            EstrategiaMarkov(),
            EstrategiaQLearning(),
            EstrategiaAleatoria()
        ]
        self.pesos = [0.4, 0.4, 0.2]  # Pesos iniciais para cada estratégia
        
    def escolher_jogada(self, historico_oponente: List[Jogada], historico_jogadas: List[Jogada]) -> Jogada:
        if random.random() < 0.1:  # 10% de exploração
            return random.choice(list(Jogada))
            
        # Votação ponderada
        votos = defaultdict(float)
        for estrategia, peso in zip(self.estrategias, self.pesos):
            jogada = estrategia.escolher_jogada(historico_oponente, historico_jogadas)
            votos[jogada] += peso
            
        return max(votos.items(), key=lambda x: x[1])[0]
        
    def aprender(self, jogada_oponente: Jogada, jogada_ia: Jogada, resultado: str) -> None:
        for estrategia in self.estrategias:
            estrategia.aprender(jogada_oponente, jogada_ia, resultado) 