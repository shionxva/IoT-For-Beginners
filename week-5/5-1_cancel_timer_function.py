
import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a request to the Timer Bot service.')

    try:
        req_body = req.get_json()
        # Mocking the LUIS prediction response structure
        prediction = req_body.get('prediction', {})
        top_intent = prediction.get('topIntent')
        entities = prediction.get('entities', {})

        if top_intent == 'CancelTimer':
            logging.info("INTENT RECOGNIZED: 'CancelTimer'. System is halting active timers.")
            return func.HttpResponse(
                json.dumps({
                    "message": "Your timer has been successfully cancelled.",
                    "status": "success",
                    "intent": "CancelTimer"
                }),
                mimetype="application/json",
                status_code=200
            )

        elif top_intent == 'SetTimer':
            duration = entities.get('duration', ['unknown'])[0]
            logging.info(f"Setting timer for {duration}.")
            return func.HttpResponse(f"Timer set for {duration}.", status_code=200)

        else:
            logging.warning(f"Unrecognized intent: {top_intent}")
            return func.HttpResponse("Intent not recognized.", status_code=400)

    except ValueError:
        return func.HttpResponse("Invalid JSON input.", status_code=400)
