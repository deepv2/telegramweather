from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, JobQueue, Job
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from weather import Weather, Unit
from datetime import time
import logging

# Initial global variables
latitude = 0
longitude = 0
LATITUDE, LONGITUDE, TIMER = range(3)

# Debugging logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warning(f'Update {update} caused error {error}')

# Help message so users know how to use bot
def _help(bot, update):
	update.message.reply_text(
	"""
	Type /location to manually input the latitude and longitude of your location.
	Type /time to set a time to notify you daily of the weather (weather must be setup with /location beforehand).
	Type /reset to clear all timers.
	Type /weather to get the weather for today.
	Type /forecast to get a 5-day forecast.
	"""
	)

# Conversation stopper
def stop(bot, update):
	user = update.message.from_user
	logger.info(f"User {user.first_name} stopped action.")
	update.message.reply_text("Setup canceled.", reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END

# Location setters
def location(bot, update):
	update.message.reply_text("Type in your latitude or type /stop to exit setup.")
	return LATITUDE

def getLat(bot, update):
	global latitude
	try: # Prevent non-number inputs
		latitude = float((update.message.text).strip())
	except:
		update.message.reply_text("Error: latitude cannot be analyzed (maybe input was not a number?)")
		return ConversationHandler.END
	update.message.reply_text("Type in your longitude or type /stop to exit setup.")	
	return LONGITUDE

def getLong(bot, update):
	global longitude
	try: # Prevent non-number inputs
		longitude = float((update.message.text).strip())
	except:
		update.message.reply_text("Error: latitude cannot be analyzed (maybe input was not a number?)")
		return ConversationHandler.END
	update.message.reply_text("Great! Now we can give you weather data!")
	return ConversationHandler.END

# Today's weather getter methods
def getWeather(bot, update):
	global latitude
	global longitude
	if latitude is 0 or longitude is 0:
		update.message.reply_text("Please set your location first with /location.")	
	else:
		weather_data = today(latitude, longitude)
		update.message.reply_text(f"Today, it is {weather_data[1][3:6]} {weather_data[1][0:2]}, {weather_data[1][7:11]}, and it will be {weather_data[0].lower()} with a high of {weather_data[2]}F and a low of {weather_data[3]}F.")

def today(latitude, longitude):
	weather = Weather(unit=Unit.FAHRENHEIT)	
	location = weather.lookup_by_latlng(latitude, longitude)
	forecast = location.forecast
	return [forecast[0].text, forecast[0].date, forecast[0].high, forecast[0].low]

# Daily weather timer methods
def setTime(bot, update):
	global latitude
	global longitude
	if latitude is 0 or longitude is 0:
		update.message.reply_text("Please set your location first with /location.")	
		return ConversationHandler.END
	update.message.reply_text("Type the time at which you would like a daily reminder of the weather (24-hour format, {hour}:{minute})(type /stop to stop):")
	return TIMER

def callback_weather(bot, job):
	weather_data = today(latitude, longitude)
	text = f"Today, it is {weather_data[1][3:6]} {weather_data[1][0:2]}, {weather_data[1][7:11]}, and it will be {weather_data[0].lower()} with a high of {weather_data[2]}F and a low of {weather_data[3]}F."
	bot.send_message(chat_id=job.context, text=text)

def callback_timer(bot, update, job_queue):
	time_elements = update.message.text.replace(" ", "").split(":")
	try: # check to see if input is actually an int within 24-hour time ranges
		time_elements[0] = int(time_elements[0])
		time_elements[1] = int(time_elements[1])
		t = time(time_elements[0], time_elements[1])
		bot.send_message(chat_id=update.message.chat_id, text=f"Setting daily weather notification for {t}.")
		job_queue.run_daily(callback_weather, t, days=(0,1,2,3,4,5,6), context=update.message.chat_id)
	except:
		update.message.reply_text("Please enter a valid time. Format: {Hour}:{Minutes}")

def resetTimer(bot, update, job_queue):
	joblist = job_queue.jobs()
	for job in joblist:
		job.schedule_removal()
	update.message.reply_text("All timers have been removed.")
	
# Forecast method
def forecast(bot, update):
	weather = Weather(unit=Unit.FAHRENHEIT)
	if latitude is 0 or longitude is 0:
		update.message.reply_text("Please set your location first with /location.")	
	else:
		location = weather.lookup_by_latlng(latitude, longitude)
		forecast = location.forecast
		update.message.reply_text(
		f""" 
		 {forecast[1].date[3:6]} {forecast[1].date[0:2]}, {forecast[1].date[7:11]}
		Condition: {forecast[1].text.lower()}
		High: {forecast[1].high}F
		Low: {forecast[1].high}F
	
		{forecast[2].date[3:6]} {forecast[2].date[0:2]}, {forecast[2].date[7:11]}
		Condition: {forecast[2].text.lower()}
		High: {forecast[2].high}F
		Low: {forecast[2].high}F
	
		{forecast[3].date[3:6]} {forecast[3].date[0:2]}, {forecast[3].date[7:11]}
		Condition: {forecast[3].text.lower()}
		High: {forecast[3].high}F
		Low: {forecast[3].high}F
	
		{forecast[4].date[3:6]} {forecast[4].date[0:2]}, {forecast[4].date[7:11]}
		Condition: {forecast[4].text.lower()}
		High: {forecast[4].high}F
		Low: {forecast[4].high}F
	
		{forecast[5].date[3:6]} {forecast[5].date[0:2]}, {forecast[5].date[7:11]}
		Condition: {forecast[5].text.lower()}
		High: {forecast[5].high}F
		Low: {forecast[5].high}F
	
		"""
		)
# Main function, where bot commands are processed
def main():
	token = "INSERT API KEY HERE!"

	updater = Updater(token)
	dp = updater.dispatcher

	location_setter = ConversationHandler(
		entry_points=[CommandHandler('location', location)],
		states={
			LATITUDE: [MessageHandler(Filters.text, getLat)],
			LONGITUDE: [MessageHandler(Filters.text, getLong)]
		},
		fallbacks=[CommandHandler('stop', stop)]
	)

	time_setter = ConversationHandler(
		entry_points=[CommandHandler('time', setTime)],
		states={
			TIMER: [MessageHandler(Filters.text, callback_timer, pass_job_queue=True)]
		},
		fallbacks=[CommandHandler('stop', stop)]
	)

	dp.add_handler(CommandHandler('weather', getWeather))
	dp.add_handler(CommandHandler('help', _help))
	dp.add_handler(CommandHandler('forecast', forecast))
	dp.add_handler(CommandHandler('reset', resetTimer, pass_job_queue=True))
	dp.add_handler(time_setter)
	dp.add_handler(location_setter)
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()
