from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from weather import Weather, Unit
import logging

latitude = 0
longitude = 0
GETLOC, LATITUDE, LONGITUDE = range(3)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warning(f'Update {update} caused error {error}')

def setup(bot, update):
	update.message.reply_text(
	"""In order to get weather data, we will need your location.
	Type /skip to manually enter your latitude and longitude, or
	type next to automatically get your location.
	Type /stop at any time to stop setup.""")
	return GETLOC

def getLoc(bot, update):
	user = update.message.from_user
	user_location = update.message.location
	latitude = user_location.latitude
	longitude = user_location.longitude
	print(update.message.location)
	logger.info("Location: {latitude}, {longitude}")
	update.message.reply_text("Great! Now we can give you weather data!")
	return ConversationHandler.END

def skipLoc(bot, update):
	user = update.message.from_user
	update.message.reply_text("Manual entry selected. Type in your latitude or type /stop to exit setup.")
	return LATITUDE

def getLat(bot, update):
	global latitude
	latitude = float(update.message.text)
	update.message.reply_text("Type in your longitude or type /stop to exit setup.")	
	return LONGITUDE

def getLong(bot, update):
	global longitude
	longitude = float(update.message.text)
	update.message.reply_text("Great! Now we can give you weather data!")
	return ConversationHandler.END

def stop(bot, update):
	user = update.message.from_user
	logger.info(f"User {user.first_name} stopped setup.")
	update.message.reply_text("Setup canceled.", reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END

def getWeather(bot, update):
	global latitude
	global longitude
	weather_data = today(latitude, longitude)
	update.message.reply_text(f"Today, it is {weather_data[3:5]} {weather_data[0:1]}, {weather_data[7:10]}, and it will be {weather_data[0]} with a high of {weather_data[2]} and a low of {weather_data[3]}")

def today(latitude, longitude):
	weather = Weather(unit=Unit.FAHRENHEIT)	
	location = weather.lookup_by_latlng(latitude, longitude)
	forecast = location.forecast
	return [forecast[0].text, forecast[0].date, forecast[0].high, forecast[0].low]
def main():
	token = "682545666:AAHbQh6Fc61uWaWmt44cXMP1OUDnSYzpHes"

	updater = Updater(token)
	dp = updater.dispatcher

	conversation_handler = ConversationHandler(
		entry_points=[CommandHandler('setup', setup)],
		states={
			GETLOC: [MessageHandler(Filters.location, getLoc),
				 CommandHandler('skip', skipLoc)],
			LATITUDE: [MessageHandler(Filters.text, getLat)],
			LONGITUDE: [MessageHandler(Filters.text, getLong)]
		},
		fallbacks=[CommandHandler('stop', stop)]
	)
	dp.add_handler(CommandHandler('weather', getWeather))
	dp.add_handler(conversation_handler)
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()


if __name__ == "__main__":
	main()
