import sqlite3
import telebot
from math import sin, cos, sqrt, atan2, radians

# Define your Telegram bot token
bot_token = 'Metti qua il tuo token'

# Connect to the SQLite database
con = sqlite3.connect("fontanelle.db")

# Create empty lists to store data from the database
nome_via = []
circoscrizioni = []
denominazioni = []
coord_x = []
coord_y = []

# Fetch data from the font table in the database
n_via = con.execute("SELECT Identificativo FROM font").fetchall()
circ = con.execute("SELECT Indirizzo FROM font").fetchall()
denom = con.execute("SELECT Tipologia FROM font").fetchall()
x = con.execute("SELECT Lat FROM font").fetchall()
y = con.execute("SELECT Long FROM font").fetchall()

# Populate the lists with data from the database
for i in range(len(n_via)):
    nome_via.append(n_via[i][0])
    circoscrizioni.append(circ[i][0])
    denominazioni.append(denom[i][0])
    coord_x.append(x[i][0])
    coord_y.append(y[i][0])

# Calculate the distance between two sets of coordinates
def distanza(lat1, lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371  # Radius of the Earth in kilometers
    return (c * r * 1000)

# Create a Telegram bot instance
bot = telebot.TeleBot(bot_token)

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Benvenuto su Fontanelle Comuni di dell'ovest veronese! La prego di mandarmi la sua posizione.")

# Handle the user's location message
@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_lat = message.location.latitude
    user_lon = message.location.longitude
    # Calculate the distance from the user's location to each fountain
    distances = []
    for i in range(len(coord_x)):
        distance = distanza(user_lat, user_lon, coord_x[i], coord_y[i])
        distances.append(distance)
      
    #bot.reply_to(message, distances)
    
    # Find the index of the nearest fountain
    nearest_index = distances.index(min(distances))

    # Retrieve the details of the nearest fountain
    nome = nome_via[nearest_index]
    circoscrizione = circoscrizioni[nearest_index]
    denominazione = denominazioni[nearest_index]

    # Send the information about the nearest fountain to the user
    response = f"Fontanella più vicina:\nNome: {nome}\nIndirizzo: {circoscrizione}\nTipo: {denominazione}"
    bot.reply_to(message, response)
    

# Start the bot
bot.polling()

