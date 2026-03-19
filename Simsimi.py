import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import json
import random
import datetime
import os

class SimSimiAprendiz:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 SimSimi - Eu aprendo com VOCÊ!")
        self.root.geometry("700x800")
        self.root.configure(bg='#2b2b2b')
        
        # Arquivo de conhecimento
        self.arquivo_conhecimento = 'meu_conhecimento.json'
        self.conhecimento = self.carregar_conhecimento()
        
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
        """Mensagem inicial explicando como funciona"""
        self.adicionar_mensagem("sistema", "=" * 50)
        self.adicionar_mensagem("sistema", "🤖 Olá! Sou SimSimi, um chatbot que APRENDE com VOCÊ!")
        self.adicionar_mensagem("sistema", "")
        self.adicionar_mensagem("sistema", "📚 COMO FUNCIONA:")
        self.adicionar_mensagem("sistema", "• Quando eu NÃO sei responder, você pode ME ENSINAR")
        self.adicionar_mensagem("sistema", "• Depois que você me ensina, eu sempre lembrarei!")
        self.adicionar_mensagem("sistema", "• Quanto mais você conversa, mais inteligente eu fico")
        self.adicionar_mensagem("sistema", "")
        self.adicionar_mensagem("sistema", "💡 Vamos começar! Me faça uma pergunta...")
        self.adicionar_mensagem("sistema", "=" * 50)
    
    def carregar_conhecimento(self):
        """Carrega o conhecimento do arquivo"""
        try:
            with open(self.arquivo_conhecimento, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Conhecimento inicial
            return {
                "oi": "Olá! Como posso te ajudar hoje?",
                "tudo bem": "Tudo ótimo! E você?",
                "qual seu nome": "Meu nome é SimSimi! Fui criado para aprender com você!",
                "obrigado": "Por nada! Estou aqui para aprender com você!",
                "tchau": "Até mais! Continue me ensinando coisas novas!"
            }
    
    def salvar_conhecimento(self):
        """Salva o conhecimento no arquivo"""
        with open(self.arquivo_conhecimento, 'w', encoding='utf-8') as f:
            json.dump(self.conhecimento, f, indent=4, ensure_ascii=False)
        self.atualizar_status()
        self.adicionar_mensagem("sistema", "💾 Conhecimento salvo com sucesso!")
    
    def atualizar_status(self):
        """Atualiza a barra de status"""
        self.status_label.config(
            text=f"📝 Modo: {'APRENDIZADO' if self.modo_aprendizado else 'Conversa'} | Conhecimentos: {len(self.conhecimento)}"
        )
    
    def adicionar_mensagem(self, tipo, mensagem):
        """Adiciona mensagem ao chat"""
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
        """Processa mensagem enviada"""
        mensagem = self.entrada_var.get().strip()
        
        if not mensagem:
            return
        
        self.entrada_var.set("")
        self.adicionar_mensagem("user", mensagem)
        
        # Processar a mensagem
        self.processar_mensagem(mensagem.lower())
    
    def processar_mensagem(self, mensagem):
        """Processa a mensagem do usuário"""
        
        # Se estiver em modo de aprendizado
        if self.modo_aprendizado and self.ultima_pergunta:
            # Usuário está ensinando uma resposta
            self.conhecimento[self.ultima_pergunta] = mensagem
            self.salvar_conhecimento()
            
            self.adicionar_mensagem("aprendizado", f"Aprendi! Agora quando alguém perguntar '{self.ultima_pergunta}', eu responderei: '{mensagem}'")
            self.adicionar_mensagem("bot", "Obrigado por me ensinar! 😊")
            
            # Sair do modo aprendizado
            self.modo_aprendizado = False
            self.ultima_pergunta = None
            self.atualizar_status()
            return
        
        # Verificar se é um comando especial
        if mensagem.startswith('/'):
            self.processar_comando(mensagem)
            return
        
        # Verificar se já sabe a resposta
        if mensagem in self.conhecimento:
            resposta = self.conhecimento[mensagem]
            self.adicionar_mensagem("bot", resposta)
        else:
            # Não sabe a resposta - entra em modo de aprendizado
            self.modo_aprendizado = True
            self.ultima_pergunta = mensagem
            self.atualizar_status()
            
            self.adicionar_mensagem("aprendizado", f"Eu não sei responder '{mensagem}' ainda...")
            self.adicionar_mensagem("aprendizado", "Me ensine! O que eu deveria responder quando alguém perguntar isso?")
            self.adicionar_mensagem("bot", "Digite a resposta que você quer que eu aprenda:")
    
    def processar_comando(self, comando):
        """Processa comandos especiais"""
        if comando == '/ensinar':
            self.modo_aprendizado = True
            self.ultima_pergunta = None
            self.atualizar_status()
            self.adicionar_mensagem("aprendizado", "Modo de ensino ativado!")
            self.adicionar_mensagem("bot", "Qual pergunta você quer me ensinar?")
        
        elif comando == '/sair':
            if messagebox.askyesno("Sair", "Deseja realmente sair?"):
                self.salvar_conhecimento()
                self.root.quit()
        
        elif comando == '/ajuda':
            self.mostrar_ajuda()
    
    def limpar_chat(self):
        """Limpa a área de chat"""
        self.chat_area.delete(1.0, tk.END)
        self.adicionar_mensagem("sistema", "🧹 Chat limpo!")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas detalhadas"""
        total = len(self.conhecimento)
        
        # Contar respostas por tamanho
        curtas = sum(1 for r in self.conhecimento.values() if len(r) < 20)
        medias = sum(1 for r in self.conhecimento.values() if 20 <= len(r) < 50)
        longas = sum(1 for r in self.conhecimento.values() if len(r) >= 50)
        
        stats = f"""
📊 ESTATÍSTICAS DETALHADAS:
━━━━━━━━━━━━━━━━━━━━━
📚 Total de conhecimentos: {total}
📝 Respostas curtas (<20): {curtas}
📄 Respostas médias (20-50): {medias}
📖 Respostas longas (>50): {longas}

💾 Arquivo: {self.arquivo_conhecimento}
        """
        
        self.adicionar_mensagem("sistema", stats)
    
    def ver_conhecimentos(self):
        """Mostra lista de conhecimentos"""
        if not self.conhecimento:
            self.adicionar_mensagem("sistema", "Ainda não aprendi nada! Me ensine alguma coisa!")
            return
        
        self.adicionar_mensagem("sistema", "📚 O QUE EU SEI:")
        for i, (pergunta, resposta) in enumerate(list(self.conhecimento.items())[:10], 1):
            self.adicionar_mensagem("sistema", f"{i}. '{pergunta}' → '{resposta[:30]}...'")
        
        if len(self.conhecimento) > 10:
            self.adicionar_mensagem("sistema", f"... e mais {len(self.conhecimento) - 10} conhecimentos!")
    
    def mostrar_ajuda(self):
        """Mostra ajuda"""
        ajuda = """
📚 GUIA DE USO:
━━━━━━━━━━━━━━
💬 CONVERSA NORMAL:
  • Faça perguntas normalmente
  • Se eu não souber, você me ensina

📖 COMO ENSINAR:
  • Quando eu não souber, digite a resposta
  • Eu aprenderei automaticamente!

🎮 COMANDOS:
  • /ensinar - Ativar modo de ensino manual
  • /ajuda - Mostrar esta ajuda
  • /sair - Fechar o programa

💡 DICAS:
  • Quanto mais você ensina, mais inteligente eu fico!
  • Meus conhecimentos são salvos automaticamente
  • Use frases curtas e objetivas para melhor aprendizado
        """
        
        self.adicionar_mensagem("sistema", ajuda)

# Executar
if __name__ == "__main__":
    root = tk.Tk()
    app = SimSimiAprendiz(root)
    root.mainloop()