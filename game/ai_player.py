import random
import numpy as np
from collections import defaultdict, Counter
from .constants import Jogada, REGRAS_VITORIA

class JogadorIA:
    def __init__(self):
        self.historico_jogadas = []
        self.historico_oponente = []
        self.frequencia_jogadas = defaultdict(int)
        self.matriz_transicao = {
            jogada: {outra_jogada: 0 for outra_jogada in Jogada}
            for jogada in Jogada
        }
        self.taxa_aprendizado = 0.1
        self.fator_exploracao = 0.2
        self.valores_q = {jogada: 0.0 for jogada in Jogada}
        
        self.tamanho_n_gram = 3
        self.padroes_n_gram = defaultdict(int)
        self.sequencia_oponente = []
        self.fator_decaimento = 0.95
        self.resultados = []
        
    def _atualizar_matriz_transicao(self):
        """Atualiza a matriz de transição com base no histórico de jogadas do oponente."""
        if len(self.historico_oponente) < 2:
            return
            
        ultima = self.historico_oponente[-2]
        atual = self.historico_oponente[-1]
        self.matriz_transicao[ultima][atual] += 1
        
    def _prever_proxima_jogada(self):
        """Prevê a próxima jogada do oponente usando a matriz de transição."""
        if not self.historico_oponente:
            return None
            
        ultima_jogada = self.historico_oponente[-1]
        transicoes = self.matriz_transicao[ultima_jogada]
        total = sum(transicoes.values())
        
        if total == 0:
            return None
            
        probabilidades = {
            jogada: count/total 
            for jogada, count in transicoes.items()
        }
        return max(probabilidades.items(), key=lambda x: x[1])[0]
        
    def _escolher_contra_jogada(self, jogada_prevista):
        """Escolhe a melhor jogada contra a jogada prevista do oponente."""
        if jogada_prevista is None:
            return random.choice(list(Jogada))
            
        jogadas_vencedoras = [
            jogada for jogada in Jogada
            if jogada_prevista in REGRAS_VITORIA[jogada]
        ]
        
        if jogadas_vencedoras:
            return random.choice(jogadas_vencedoras)
        return random.choice(list(Jogada))
        
    def _atualizar_padroes_n_gram(self):
        """Atualiza o reconhecimento de padrões n-gram"""
        if len(self.historico_oponente) >= self.tamanho_n_gram:
            padrao = tuple(self.historico_oponente[-self.tamanho_n_gram:])
            self.padroes_n_gram[padrao] += 1
            
    def _prever_por_n_grams(self):
        """Prevê próxima jogada baseada em padrões n-gram"""
        if len(self.historico_oponente) < self.tamanho_n_gram - 1:
            return None
            
        padrao_atual = tuple(self.historico_oponente[-(self.tamanho_n_gram-1):])
        contagem_max = 0
        jogada_prevista = None
        
        for padrao, contagem in self.padroes_n_gram.items():
            if padrao[:-1] == padrao_atual:
                if contagem > contagem_max:
                    contagem_max = contagem
                    jogada_prevista = padrao[-1]
                    
        return jogada_prevista

    def _ajustar_taxa_aprendizado(self):
        """Ajusta dinamicamente a taxa de aprendizado baseado no desempenho"""
        if not self.historico_jogadas:
            return
            
        jogos_recentes = self.historico_jogadas[-20:]
        resultados_recentes = self.resultados[-20:] if len(self.resultados) >= 20 else self.resultados
        
        if not resultados_recentes:
            return
            
        taxa_vitoria = sum(1 for resultado in resultados_recentes if resultado == "VITORIA") / len(resultados_recentes)
        
        if taxa_vitoria < 0.4:
            self.taxa_aprendizado = min(0.5, self.taxa_aprendizado * 1.1)
        elif taxa_vitoria > 0.6:
            self.taxa_aprendizado = max(0.1, self.taxa_aprendizado * 0.9)

    def _identificar_estrategia_oponente(self):
        """Identifica padrões na estratégia do oponente"""
        jogadas_recentes = self.historico_oponente[-10:]
        contagem_jogadas = Counter(jogadas_recentes)
        total_jogadas = len(jogadas_recentes)
        
        # Verifica tendência de jogadas
        for jogada, contagem in contagem_jogadas.items():
            if contagem/total_jogadas > 0.4:  # Oponente favorece esta jogada
                return self._obter_contra_jogada(jogada)
                
        # Verifica padrões alternados
        if len(jogadas_recentes) >= 4:
            if jogadas_recentes[-1] == jogadas_recentes[-3] and jogadas_recentes[-2] == jogadas_recentes[-4]:
                return self._obter_contra_jogada(jogadas_recentes[-3])
                
        return None

    def _obter_contra_jogada(self, jogada_oponente):
        """Retorna a jogada ideal para contra-atacar"""
        contra_jogadas = [
            jogada for jogada in Jogada 
            if jogada_oponente in REGRAS_VITORIA[jogada]
        ]
        return random.choice(contra_jogadas) if contra_jogadas else None

    def fazer_jogada(self) -> Jogada:
        """Processo de decisão aprimorado"""
        # Exploração estratégica
        if random.random() < self.fator_exploracao:
            return random.choice(list(Jogada))
            
        # Verificação de contra-estratégia
        contra_jogada = self._identificar_estrategia_oponente()
        if contra_jogada and random.random() > 0.2:
            return contra_jogada
            
        # Previsão por n-gram
        previsao_n_gram = self._prever_por_n_grams()
        if previsao_n_gram and random.random() > 0.3:
            return self._obter_contra_jogada(previsao_n_gram)
            
        # Previsão por matriz de transição
        previsao_transicao = self._prever_proxima_jogada()
        if previsao_transicao and random.random() > 0.4:
            return self._escolher_contra_jogada(previsao_transicao)
            
        # Decisão baseada em Q-learning
        return max(self.valores_q.items(), key=lambda x: x[1])[0]

    def aprender_do_jogo(self, jogada_jogador: Jogada, jogada_ia: Jogada, resultado: str):
        """Processo de aprendizado aprimorado"""
        self.historico_oponente.append(jogada_jogador)
        self.historico_jogadas.append(jogada_ia)
        self.resultados.append(resultado)
        self.frequencia_jogadas[jogada_jogador] += 1
        
        # Atualiza padrões n-gram
        self._atualizar_padroes_n_gram()
        
        # Atualiza matriz de transição
        self._atualizar_matriz_transicao()
        
        # Q-learning adaptativo
        recompensa = 1.0 if resultado == "VITORIA" else -1.0 if resultado == "DERROTA" else 0.0
        self.valores_q[jogada_ia] += self.taxa_aprendizado * (
            recompensa - self.valores_q[jogada_ia]
        )
        
        # Ajusta parâmetros de aprendizado
        self._ajustar_taxa_aprendizado()
        
        # Ajuste dinâmico da taxa de exploração
        self.fator_exploracao = max(
            0.1,
            self.fator_exploracao * (0.995 if resultado == "VITORIA" else 0.999)
        )