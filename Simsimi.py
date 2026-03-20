import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import json
import random
import datetime
import os
from rapidfuzz import process, fuzz

class SimSimiAprendiz:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 SimSimi - Eu aprendo com VOCÊ!")
        self.root.geometry("700x800")
        self.root.configure(bg='#2b2b2b')
        
        # Arquivo de conhecimento
        self.arquivo_conhecimento = 'meu_conhecimento.json'
        self.conhecimento = self.carregar_conhecimento()
        
        # Converte tudo para listas (para permitir múltiplas respostas)
        for chave in list(self.conhecimento.keys()):
            if not isinstance(self.conhecimento[chave], list):
                self.conhecimento[chave] = [self.conhecimento[chave]]
        
        # Modo de aprendizado
        self.modo_aprendizado = False
        self.ultima_pergunta = None
        
        self.configurar_interface()
        self.mensagem_boas_vindas()
    
    def configurar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="🤖 SimSimi - Eu aprendo com VOCÊ!",
            font=("Arial", 18, "bold"),
            bg='#2b2b2b',
            fg='#4fc3f7'
        )
        titulo.pack(pady=(0, 10))
        
        # Subtítulo explicativo
        subtitulo = tk.Label(
            main_frame,
            text="Me ensine! Quando eu não souber algo, você pode me ensinar a resposta",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#888888'
        )
        subtitulo.pack(pady=(0, 10))
        
        # Área do chat
        self.chat_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white',
            height=20
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configurar tags de cores
        self.chat_area.tag_config("user", foreground="#4fc3f7", font=("Arial", 11, "bold"))
        self.chat_area.tag_config("bot", foreground="#81c784", font=("Arial", 11, "bold"))
        self.chat_area.tag_config("aprendizado", foreground="#ffb74d", font=("Arial", 11, "italic"))
        self.chat_area.tag_config("sistema", foreground="#ff6b6b", font=("Arial", 10))
        self.chat_area.tag_config("hora", foreground="#888888", font=("Arial", 8))
        
        # Frame de status
        status_frame = tk.Frame(main_frame, bg='#333333', height=30)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="📝 Modo: Conversa | Conhecimentos: " + str(len(self.conhecimento)),
            bg='#333333',
            fg='#ffffff',
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Frame de entrada
        entrada_frame = tk.Frame(main_frame, bg='#2b2b2b')
        entrada_frame.pack(fill=tk.X)
        
        self.entrada_var = tk.StringVar()
        self.entrada = tk.Entry(
            entrada_frame,
            textvariable=self.entrada_var,
            font=("Arial", 12),
            bg='#3b3b3b',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.entrada.bind("<Return>", lambda e: self.enviar_mensagem())
        self.entrada.focus()
        
        self.btn_enviar = tk.Button(
            entrada_frame,
            text="Enviar 📤",
            font=("Arial", 11, "bold"),
            bg='#0d47a1',
            fg='white',
            relief=tk.FLAT,
            command=self.enviar_mensagem,
            cursor="hand2"
        )
        self.btn_enviar.pack(side=tk.RIGHT, padx=(5, 0), ipadx=15, ipady=5)
        
        # Frame de botões de controle
        controle_frame = tk.Frame(main_frame, bg='#2b2b2b')
        controle_frame.pack(fill=tk.X, pady=(10, 0))
        
        botoes = [
            ("🧹 Limpar Chat", self.limpar_chat),
            ("📊 Estatísticas", self.mostrar_estatisticas),
            ("📚 Ver Conhecimentos", self.ver_conhecimentos),
            ("💾 Salvar Agora", self.salvar_conhecimento),
            ("❓ Ajuda", self.mostrar_ajuda)
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(
                controle_frame,
                text=texto,
                font=("Arial", 9),
                bg='#404040',
                fg='white',
                relief=tk.FLAT,
                command=comando,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2, ipadx=5, ipady=2)
    
    def mensagem_boas_vindas(self):
        self.adicionar_mensagem("sistema", "=" * 50)
        self.adicionar_mensagem("sistema", "🤖 Olá! Sou SimSimi, um chatbot que APRENDE com VOCÊ!")
        self.adicionar_mensagem("sistema", "")
        self.adicionar_mensagem("sistema", "📚 COMO FUNCIONA:")
        self.adicionar_mensagem("sistema", "• Quando eu NÃO sei responder (ou não achar parecido), você pode ME ENSINAR")
        self.adicionar_mensagem("sistema", "• Posso ter várias respostas pra mesma pergunta (escolho uma aleatória)")
        self.adicionar_mensagem("sistema", "• Quanto mais você conversa e ensina merda, mais venenoso eu fico 😈")
        self.adicionar_mensagem("sistema", "")
        self.adicionar_mensagem("sistema", "💡 Vamos começar! Me xinga pra testar...")
        self.adicionar_mensagem("sistema", "=" * 50)
    
    def carregar_conhecimento(self):
        try:
            with open(self.arquivo_conhecimento, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "oi": ["Olá! Como posso te ajudar hoje?"],
                "tudo bem": ["Tudo ótimo! E você?", "Tô de boa, e tu?"],
                "qual seu nome": ["Meu nome é SimSimi! Fui criado para aprender com você!"],
                "obrigado": ["Por nada! Estou aqui para aprender com você!"],
                "tchau": ["Até mais! Continue me ensinando coisas novas!"]
            }
    
    def salvar_conhecimento(self):
        with open(self.arquivo_conhecimento, 'w', encoding='utf-8') as f:
            json.dump(self.conhecimento, f, indent=4, ensure_ascii=False)
        self.atualizar_status()
        self.adicionar_mensagem("sistema", "💾 Conhecimento salvo com sucesso!")
    
    def atualizar_status(self):
        self.status_label.config(
            text=f"📝 Modo: {'APRENDIZADO' if self.modo_aprendizado else 'Conversa'} | Conhecimentos: {len(self.conhecimento)}"
        )
    
    def adicionar_mensagem(self, tipo, mensagem):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.chat_area.insert(tk.END, f"[{hora}] ", "hora")
        
        if tipo == "user":
            self.chat_area.insert(tk.END, f"Você: ", "user")
            self.chat_area.insert(tk.END, f"{mensagem}\n\n")
        elif tipo == "bot":
            self.chat_area.insert(tk.END, f"SimSimi: ", "bot")
            self.chat_area.insert(tk.END, f"{mensagem}\n\n")
        elif tipo == "aprendizado":
            self.chat_area.insert(tk.END, f"📚 Aprendizado: ", "aprendizado")
            self.chat_area.insert(tk.END, f"{mensagem}\n\n")
        else:
            self.chat_area.insert(tk.END, f"{mensagem}\n", "sistema")
        
        self.chat_area.see(tk.END)
    
    def enviar_mensagem(self):
        mensagem = self.entrada_var.get().strip()
        
        if not mensagem:
            return
        
        self.entrada_var.set("")
        self.adicionar_mensagem("user", mensagem)
        
        self.processar_mensagem(mensagem.lower())
    
    def processar_mensagem(self, mensagem):
        if self.modo_aprendizado and self.ultima_pergunta:
            chave = self.ultima_pergunta
            if chave in self.conhecimento:
                self.conhecimento[chave].append(mensagem)
            else:
                self.conhecimento[chave] = [mensagem]
            
            self.salvar_conhecimento()
            
            self.adicionar_mensagem("aprendizado", 
                f"Aprendi mais uma resposta pra '{chave}'! Agora tenho {len(self.conhecimento[chave])} formas de responder isso.")
            self.adicionar_mensagem("bot", "Valeu pela aula, seu doente 😈")
            
            self.modo_aprendizado = False
            self.ultima_pergunta = None
            self.atualizar_status()
            return
        
        if mensagem.startswith('/'):
            self.processar_comando(mensagem)
            return
        
        THRESHOLD = 85  # Ajuste: 80 = mais solto, 90 = mais rigoroso
        
        if self.conhecimento:
            melhor = process.extractOne(
                mensagem,
                self.conhecimento.keys(),
                scorer=fuzz.WRatio
            )
            
            if melhor and melhor[1] >= THRESHOLD:
                pergunta_encontrada = melhor[0]
                score = melhor[1]
                respostas = self.conhecimento[pergunta_encontrada]
                resposta = random.choice(respostas)
                
                debug = f"({score:.0f}% match com '{pergunta_encontrada}')"
                self.adicionar_mensagem("bot", f"{resposta} {debug}")
                return
        
        # Não achou nada bom
        self.modo_aprendizado = True
        self.ultima_pergunta = mensagem
        self.atualizar_status()
        
        self.adicionar_mensagem("aprendizado", f"Não sei o que dizer pra '{mensagem}' (ou nada parecido o suficiente)...")
        self.adicionar_mensagem("aprendizado", "Me ensina aí o que eu devo responder quando falarem isso!")
        self.adicionar_mensagem("bot", "Joga a resposta que você quer que eu use:")
    
    def processar_comando(self, comando):
        if comando == '/ensinar':
            self.modo_aprendizado = True
            self.ultima_pergunta = None
            self.atualizar_status()
            self.adicionar_mensagem("aprendizado", "Modo ensino manual ativado!")
            self.adicionar_mensagem("bot", "Qual pergunta você quer me ensinar?")
        
        elif comando == '/sair':
            if messagebox.askyesno("Sair", "Deseja realmente sair?"):
                self.salvar_conhecimento()
                self.root.quit()
        
        elif comando == '/ajuda':
            self.mostrar_ajuda()
    
    def limpar_chat(self):
        self.chat_area.delete(1.0, tk.END)
        self.adicionar_mensagem("sistema", "🧹 Chat limpo!")
    
    def mostrar_estatisticas(self):
        total = len(self.conhecimento)
        respostas_totais = sum(len(resps) for resps in self.conhecimento.values())
        
        stats = f"""
📊 ESTATÍSTICAS ATUAIS:
━━━━━━━━━━━━━━━━━━━━━
Total de perguntas aprendidas: {total}
Total de respostas diferentes: {respostas_totais}
Média de respostas por pergunta: {respostas_totais / total if total > 0 else 0:.1f}

💾 Arquivo: {self.arquivo_conhecimento}
        """
        self.adicionar_mensagem("sistema", stats)
    
    def ver_conhecimentos(self):
        if not self.conhecimento:
            self.adicionar_mensagem("sistema", "Ainda não aprendi nada! Me ensine alguma coisa!")
            return
        
        self.adicionar_mensagem("sistema", "📚 ALGUNS DO QUE EU SEI (primeiros 10):")
        for i, (pergunta, respostas) in enumerate(list(self.conhecimento.items())[:10], 1):
            qtd = len(respostas)
            exemplo = respostas[0][:40] + "..." if len(respostas[0]) > 40 else respostas[0]
            self.adicionar_mensagem("sistema", f"{i}. '{pergunta}' → {qtd} respostas (ex: {exemplo})")
        
        if len(self.conhecimento) > 10:
            self.adicionar_mensagem("sistema", f"... e mais {len(self.conhecimento) - 10} perguntas!")
    
    def mostrar_ajuda(self):
        ajuda = """
📚 GUIA RÁPIDO:
━━━━━━━━━━━━━━
• Conversa normal: só fala
• Se eu não souber → me ensina a resposta
• Posso aprender várias respostas pra mesma frase (escolho aleatória)
• Quanto mais veneno você ensina, mais tóxico eu fico 😈

COMANDOS:
• /ensinar → ativa modo ensino manual
• /ajuda → esta mensagem
• /sair → fecha o programa

DICA: testa variações tipo "vai tomar no cu", "tomar no cu vai", "vai se foder" — com fuzzy eu pego parecido!
        """
        self.adicionar_mensagem("sistema", ajuda)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimSimiAprendiz(root)
    root.mainloop()
