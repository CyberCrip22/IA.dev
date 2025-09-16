import sqlite3
import random

conn = sqlite3.connect("database.db")

conhecimento = {
    "oi": "Olá!",
    "como vai?": "Estou bem, e você?",
    "qual seu nome?": "Sou Pyton, seu assistente curioso!"
}

while True:
    entrada = input("Você: ").lower().strip()
    
    if entrada == 'sair':
        print("Até logo!")
        break
    
   
    
    respostas_automaticas = [
    "Hmm, {entrada}... interessante!",
    "Nunca pensei por esse lado: {entrada}. Boa!",
    "Sabe, {entrada} me faz lembrar algo importante.",
    "{entrada}? Isso combina com você.",
    "Curioso... você disse '{entrada}'. O que isso significa pra você?"
]
    
else:
   
    resposta_gerada = random.choice(respostas_automaticas).format(entrada=entrada)
    
conhecimento[entrada] = resposta_gerada
    
print(f"Bot: {resposta_gerada}")


with open('conhecimento.json', 'w') as f:
    json.dump(conhecimento, f)


try:
    with open('conhecimento.json', 'r') as f:
        conhecimento = json.load(f)
except FileNotFoundError:
    conhecimento = {}  

   



