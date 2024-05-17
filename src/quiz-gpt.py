from rich.console import Console
from rich.prompt import Prompt
from openai import OpenAI
import json

console = Console()
chatgpt = OpenAI(
    api_key="GPT API KEY"
).chat


def esperar_enter():
    console.input(
        prompt="Pressione ENTER para continuar...",
        password=True
    )


def gerar_pergunta(topico):
    resposta = chatgpt.completions.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": f"""
                Você é um especialista muito experiente com conhecimento em diferentes
                assuntos e conceitos teóricos e práticos sobre {topico}.
                Você está trabalhando em um processo de contratação e seu trabalho agora é escrever perguntas
                para uma entrevista. Cada pergunta deve ter quatro respostas possíveis e uma delas
                deve ser correta. Escreva essas perguntas no seguinte formato:
                {{"enunciado": "pergunta", "opcoes": [
                    "Opção 1", "Opção 2", "Opção 3", "Opção 4"], "certa": "Opção 1"}}
            """
        }, {
            "role": "user",
            "content": f"Gere uma questão sobre {topico}"
        }]
    )

    conteudo = resposta.choices[0].message.content
    return json.loads(conteudo)


def gerar_quiz():
    pontos = 0
    continuar = ""

    topico = Prompt.ask("Qual é o tópico do quiz?")

    while continuar.lower() != "n":
        with console.status("Processando...", spinner="dots"):
            pergunta = gerar_pergunta(topico)

        opcoes = pergunta["opcoes"]

        console.clear()
        console.print(f"[bold]{pergunta["enunciado"]}")

        for i, opcao in enumerate(opcoes, start=1):
            console.print(f"{i}) {opcao}")

        resposta_indice = int(
            Prompt.ask(
                prompt="Opção ",
                choices=["1", "2", "3", "4"]
            )
        ) - 1

        resposta = opcoes[resposta_indice]
        resposta_certa = pergunta["certa"]

        console.clear()
        if resposta == resposta_certa:
            pontos += 1
            console.print(f"[green]Você acertou! Agora você tem {
                          pontos} pontos.")
        else:
            console.print(f"[red]Você errou! Você continua com {
                          pontos} pontos.")
            console.print(f"A resposta certa é [yellow]{
                          resposta_certa}[/yellow].")

        continuar = Prompt.ask(
            prompt="Deseja continuar? ",
            choices=["S", "n"],
            default="S"
        )


def main():
    console.clear()

    titulo = "[bold yellow]Quiz GPT[/bold yellow]"
    console.print(f"Bem vindo ao {titulo}")

    gerar_quiz()


main()
