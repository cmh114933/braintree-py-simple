from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

import braintree

app = Flask('braintree_app', template_folder="templates")

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BT_MERCHANT_ID"),
        public_key=os.environ.get("BT_PUBLIC_KEY"),
        private_key=os.environ.get("BT_PRIVATE_KEY")
    )
)


@app.route("/")
def new():
    send_simple_message()
    client_token=gateway.client_token.generate()
    return render_template("payment.html", client_token=client_token)

@app.route("/checkout", methods=["POST"])
def checkout():
    print(request.form)
    result = gateway.transaction.sale({
        "amount": request.form["amount"],
        "payment_method_nonce": request.form["payment_method_nonce"],
        "options": {
            "submit_for_settlement": True
        }
    })
    return 'test'


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9807b835e0054889b168f2d57d1fada9.mailgun.org/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": "Excited User <mailgun@sandbox9807b835e0054889b168f2d57d1fada9.mailgun.org>",
              "to": ["cmh114933@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})



if __name__ == '__main__':
    app.run()
