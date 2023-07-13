import math
import matplotlib.pyplot as plt
import io
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Fonction de résolution d'une équation du premier degré
def resoudre_equation_premier_degre(a, b):
    if a == 0:
        return "L'équation n'est pas valide (division par zéro)"
    else:
        solution = -b / a
        return f"La solution de l'équation est : x = {solution}"

# Fonction de résolution d'une équation du second degré
def resoudre_equation_second_degre(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return "L'équation n'a pas de solution réelle"
    elif discriminant == 0:
        solution = -b / (2*a)
        return f"L'équation a une solution double : x = {solution}"
    else:
        solution_1 = (-b + math.sqrt(discriminant)) / (2*a)
        solution_2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"L'équation a deux solutions : x1 = {solution_1}, x2 = {solution_2}"

# Gestionnaire de commande pour la commande /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenue dans l'univers des chiffres ! Choisissez le type d'équation que vous souhaitez résoudre :")

# Gestionnaire de commande pour la commande /equation1
def equation1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Vous avez choisi une équation du premier degré. Veuillez entrer les coefficients a et b.")

# Gestionnaire de commande pour la commande /equation2
def equation2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Vous avez choisi une équation du second degré. Veuillez entrer les coefficients a, b et c.")

# Gestionnaire de message pour la saisie des valeurs d'une équation du premier degré
def handle_equation1(update, context):
    try:
        values = list(map(float, update.message.text.split()))
        if len(values) == 2:
            a, b = values
            solution = resoudre_equation_premier_degre(a, b)
            context.bot.send_message(chat_id=update.effective_chat.id, text=solution)
        else:
            raise ValueError
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Erreur : Veuillez entrer les coefficients a et b.")

# Gestionnaire de message pour la saisie des valeurs d'une équation du second degré
def handle_equation2(update, context):
    try:
        values = list(map(float, update.message.text.split()))
        if len(values) == 3:
            a, b, c = values
            solution = resoudre_equation_second_degre(a, b, c)
            context.bot.send_message(chat_id=update.effective_chat.id, text=solution)
            # Tracer la courbe de l'équation
            x = range(-10, 11)
            y = [a*x**2 + b*x + c for x in x]
            plt.plot(x, y)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Courbe de l\'équation du second degré')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer)
            plt.close()
        else:
            raise ValueError
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Erreur : Veuillez entrer les coefficients a, b et c.")

# Configuration du bot Telegram
def main():
    updater = Updater(token='VOTRE_JETON_D_ACCES', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Ajout des gestionnaires de commande
    start_handler = CommandHandler('start', start)
    equation1_handler = CommandHandler('equation1', equation1)
    equation2_handler = CommandHandler('equation2', equation2)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(equation1_handler)
    dispatcher.add_handler(equation2_handler)

    # Ajout des gestionnaires de message
    equation1_message_handler = MessageHandler(Filters.text & (~Filters.command), handle_equation1)
    equation2_message_handler = MessageHandler(Filters.text & (~Filters.command), handle_equation2)
    dispatcher.add_handler(equation1_message_handler)
    dispatcher.add_handler(equation2_message_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
