from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from .constants import Jogada, EMOJIS_JOGADAS
from .game_logic import LogicaJogo
from .ai_player import JogadorIA

class EstadoJogo:
    def __init__(self):
        self.resetar()
        
    def resetar(self):
        self.jogador_ia = JogadorIA()
        self.logica_jogo = LogicaJogo()
        self.pontuacao = {"VITORIA": 0, "DERROTA": 0, "EMPATE": 0}
        self.historico = []
        
    def obter_analise_ia(self):
        if not self.jogador_ia.historico_oponente:
            return {
                "padroes": {},
                "estrategia": "Escolha aleatória (dados insuficientes)",
                "jogadas_analisadas": 0,
                "taxa_exploracao": round(self.jogador_ia.fator_exploracao * 100, 1)
            }
            
        frequencias = {
            jogada.value: self.jogador_ia.frequencia_jogadas[jogada]
            for jogada in Jogada
            if self.jogador_ia.frequencia_jogadas[jogada] > 0
        }
        
        mais_comum = max(frequencias.items(), key=lambda x: x[1])[0] if frequencias else None
        
        return {
            "padroes": frequencias,
            "estrategia": (
                f"Contra-atacando jogada mais frequente: {mais_comum}" 
                if mais_comum else "Construindo dados de padrões"
            ),
            "jogadas_analisadas": len(self.jogador_ia.historico_oponente),
            "taxa_exploracao": round(self.jogador_ia.fator_exploracao * 100, 1)
        }

estado_jogo = EstadoJogo()

class ManipuladorJogo(SimpleHTTPRequestHandler):
    def do_GET(self):
        caminho = urlparse(self.path)
        
        if caminho.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('game/templates/index.html', 'rb') as f:
                self.wfile.write(f.read())
                
        elif caminho.path == '/jogar':
            query = parse_qs(caminho.query)
            jogada = query.get('jogada', [None])[0]
            
            if jogada and jogada in [j.value for j in Jogada]:
                jogada_jogador = Jogada(jogada)
                jogada_ia = estado_jogo.jogador_ia.fazer_jogada()
                resultado, descricao = estado_jogo.logica_jogo.determinar_vencedor(
                    jogada_jogador, jogada_ia
                )
                
                estado_jogo.pontuacao[resultado] += 1
                estado_jogo.historico.insert(0, {
                    'jogada_jogador': jogada_jogador.value,
                    'jogada_ia': jogada_ia.value,
                    'resultado': resultado
                })
                
                estado_jogo.jogador_ia.aprender_do_jogo(
                    jogada_jogador, jogada_ia, resultado
                )
                
                resposta = {
                    'jogada_jogador': jogada_jogador.value,
                    'jogada_ia': jogada_ia.value,
                    'resultado': resultado,
                    'descricao': descricao,
                    'pontuacao': estado_jogo.pontuacao,
                    'historico': estado_jogo.historico[:10],
                    'analise_ia': estado_jogo.obter_analise_ia(),
                    'emojis': {
                        'jogador': EMOJIS_JOGADAS[jogada_jogador],
                        'ia': EMOJIS_JOGADAS[jogada_ia]
                    }
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(resposta).encode())
                
        elif caminho.path == '/resetar':
            estado_jogo.resetar()
            
            resposta = {
                'pontuacao': estado_jogo.pontuacao,
                'historico': [],
                'analise_ia': estado_jogo.obter_analise_ia()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resposta).encode())