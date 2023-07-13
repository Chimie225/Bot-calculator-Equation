from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import math
import matplotlib.pyplot as plt
import io

# Configuration du logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Fonction pour gérer la commande /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenue dans l'univers des chiffres. Veuillez choisir le type d'équation : 1 pour le premier degré, 2 pour le second degré.")

# Fonction pour résoudre l'équation du premier degré
def resoudre_equation_premier_degre(a, b):
    if a == 0:
        return "Ce n'est pas une équation du premier degré."

    x = -b / a
    explication = f"L'équation du premier degré est de la forme ax + b = 0.\n"
    explication += f"On isole x en déplaçant b de l'autre côté de l'équation :\n"
    explication += f"{a}x = {-b}\n"
    explication += f"x = {-b}/{a}\n"
    explication += f"x = {x}"

    # Génération de l'image de la démonstration
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, explication, fontsize=12, ha='center', va='center')
    ax.axis('off')

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    return explication, image_stream

# Fonction pour résoudre l'équation du second degré
def resoudre_equation_second_degre(a, b, c):
    if a == 0:
        return resoudre_equation_premier_degre(b, c)

    discriminant = b * b - 4 * a * c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        explication = f"L'équation du second degré est de la forme ax^2 + bx + c = 0.\n"
        explication += f"On utilise la formule du discriminant pour trouver les solutions réelles :\n"
        explication += f"Discriminant = b^2 - 4ac = {b}^2 - 4*{a}*{c} = {discriminant}\n"
        explication += f"Les solutions sont :\n"
        explication += f"x1 = (-b + √(discriminant)) / (2a) = (-{b} + √({discriminant})) / (2*{a}) = {x1}\n"
        explication += f"x2 = (-b - √(discriminant)) / (2a) = (-{b} - √({discriminant})) / (2*{a}) = {x2}"

        # Génération de l'image de la démonstration
        x_values = range(-10, 11)
        y_values = [a * x * x + b * x + c for x in x_values]

        fig, ax = plt.subplots()
        ax.plot(x_values, y_values)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Courbe de l\'équation du second degré')

        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        return explication, image_stream
    elif discriminant == 0:
        x = -b / (2 * a)
        explication = f"L'équation du second degré est de la forme ax^2 + bx + c = 0.\n"
        explication += f"On utilise la formule du discriminant pour trouver la solution double :\n"
        explication += f"Discriminant = b^2 - 4ac = {b}^2 - 4*{a}*{c} = {discriminant}\n"
        explication += f"La solution est :\n"
        explication += f"x = -b / (2a) = -{b} / (2*{a}) = {x}"

        # Génération de l'image de la démonstration
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, explication, fontsize=12, ha='center', va='center')
        ax.axis('off')

        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        return explication, image_stream
    else:
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-discriminant) / (2 * a)
        explication = f"L'équation du second degré est de la forme ax^2 + bx + c = 0.\n"
        explication += f"On utilise la formule du discriminant pour trouver les solutions complexes :\n"
        explication += f"Discriminant = b^2 - 4ac = {b}^2 - 4*{a}*{c} = {discriminant}\n"
        explication += f"Les solutions complexes sont :\n"
        explication += f"x1 = (-b + √(-discriminant)) / (2a) = (-{b} + √({-discriminant})) / (2*{a}) = {real_part} + {imaginary_part}i\n"
        explication += f"x2 = (-b - √(-discriminant)) / (2a) = (-{b} - √({-discriminant})) / (2*{a}) = {real_part} - {imaginary_part}i"

        # Génération de l'image de la démonstration
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, explication, fontsize=12, ha='center', va='center')
        ax.axis('off')

        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        return explication, image_stream

# Fonction pour gérer les messages texte
def handle_message(update, context):
    message = update.message.text

    if message == '1':
        context.user_data['degre'] = 1
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vous avez choisi le premier degré. Veuillez entrer les valeurs de a et b séparées par un espace.")
    elif message == '2':
        context.user_data['degre'] = 2
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vous avez choisi le second degré. Veuillez entrer les valeurs de a, b et c séparées par un espace.")
    else:
        degre = context.user_data.get('degre')

        if degre == 1:
            try:
                a, b = map(float, message.split())
                explication, image_stream = resoudre_equation_premier_degre(a, b)
                context.bot.send_message(chat_id=update.effective_chat.id, text=explication)
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_stream)
            except ValueError:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez entrer des valeurs numériques valides.")
        elif degre == 2:
            try:
                a, b, c = map(float, message.split())
                explication, image_stream = resoudre_equation_second_degre(a, b, c)
                context.bot.send_message(chat_id=update.effective_chat.id, text=explication)
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_stream)
            except ValueError:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez entrer des valeurs numériques valides.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez d'abord choisir le type d'équation (1 ou 2).")

# Fonction principale pour exécuter le bot
def main():
    # Créez l'updater et le dispatcher
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    # Ajoutez les gestionnaires de commandes et de messages
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    # Démarrez le bot
    updater.start_polling()
    logger.info("Bot started.")
    updater.idle()

if __name__ == '__main__':
    main()
