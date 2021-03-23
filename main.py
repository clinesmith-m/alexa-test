import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO


class LaunchRequestHandler(AbstractRequestHandler):
	# Handler to launch the skill
	def can_handle(self, handler_input):
		return ask_utils.is_request_type("LaunchRequest")(handler_input)

	def handle(self, handler_input):
		speak_output = "Welcome to CaptureBirthdayIntent. Modify this string to change what Alexa says"
		#reprompt_text = "Prompt the user for more dialogue here."
		return (
			handler_input.response_builder
				.speak(speak_output)
				#.ask(reprompt_text)
				.response
		)


class CaptureBirthdayIntentHandler(AbstractRquestHandler):
	def can_handle(self, handler_input):
		return ask_utils.is_intent_name("CaptureBirthdayIntent")(handler_input)

	def handle(self, handler_input):
		slots = handler_input.request_envelope.request.intent.slots
		month = slots["month"].value
		year = slots["year"].value
		day = slots["day"].value
		speak_output = "Thanks, I will remember that you were born %s %s %s"\
                            % (month, day, year)

		return (
			handler_input.response_builder
				.speak(speak_output)
				# .ask("Add a reprompt if you want to keep the session open for the user")
				.response
			)

class CaptureBirthdayIntentHandler(AbstractRquestHandler):
	def can_handle(self, handler_input):
		return ask_utils.is_intent_name("CaptureBirthdayIntent")(handler_input)

	def handle(self, handler_input):
		slots = handler_input.request_envelope.request.intent.slots
		month = slots["month"].value
		year = slots["year"].value
		day = slots["day"].value
		speak_output = "Change this string to modify what Alexa says"

		return (
			handler_input.response_builder
				.speak(speak_output)
				# .ask("Add a reprompt if you want to keep the session open for the user")
				.response
			)

# PLEASE DO NOT REMOVE OR MODIFY THIS COMMENT.
# easyA uses it as a marker when adding intents to this file


class HelpIntentHandler(AbstractRequestHandler):
	# Handles the default Amazon Help intent
	def can_handle(self, handler_input):
		return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

	def handle(self, handler_input):
		speak_output = "You can say hello to me!"
		reprompt_text = "How can I help?"
		return (
			handler_input.response_builder
				.speak(speak_output)
				.ask(reprompt_text)
				.response
		)


class CancelOrStopIntentHandler(AbstractRequestHandler):
	# Handles both the Cancel and Stop default intents
	def can_handle(self, handler_input):
		return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
			ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

	def handle(self, handler_input):
		speak_output = "Goodbye"

		return (
			handler_input.response_builder
				.speak(speak_output)
				.response
		)


class SessionEndedRequestHandler(AbstractRequestHandler):
	# Handles the session end
	def can_handle(self, handler_input):
	return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

	def handle(self, handler_input):

		# Any clean-up logic goes here

			return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
	# The intent reflector is used for testing and debugging the interaction model
	# It will simply repeat the intent the user said.
	# You can create custom handlersfor your intents by defining them above,
	# then also adding them to the request handler chain below.
	# The creator of easyA will point out said request handler
	# chain through its own comment once he figures out what/where it is
	def can_handle(self, handler_input):
		return ask_utils.is_request_type("IntentRequest")(handler_input)

	def handle(self, handler_input):
		intent_name = ask_utils.get_intent_name(handler_input)
		speak_output = "You just triggered" + intent_name + "."

		return (
			handler_input.response_builder
				.speak(speak_output)
				#.ask("Add a reprompt if you want to keep the session open for the user")
				.response
		)


class CatchAllExceptionHandler(AbstractExceptionHandler):
	# Generic error handling to capture any syntax or routing errors. If you receive an error
	# stating the request handler chain is not found, you have not implemented a handler
	# for the intent being invoked or included it in the skill builder below, per Amazon's github
	# It also means that easyA messed up, so please let the me know by opening an issue
	# describing your bug at github.com/clinemith-m/easya
	def can_handle(self, handler_input, exception):
		return True

	def handle(self, handler_input, exception):
		logger.error(exception, exc_info=True)

		speak_output = "Sorry, I had trouble doing what you asked. Please try again."
		return (
			handler_input.response_builder
				.speak(speak_output)
				.ask(speak_output)
				.response
		)


# YOU SHOULD NEVER HAVE TO MESS WITH THE BELOW CODE. IF THERE IS A PROBLEM PLEASE
# PLEASE NOTIFY ME BY OPENING AN ISSUE AT github.com/clinesmith-m/easya
# For the curious, though, per Amazon:
# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
# User intents are added here
sb.add_request_handler(CaptureBirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())# make sure this goes last

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

