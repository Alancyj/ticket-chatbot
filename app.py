from application import app

if __name__ == "__main__":

    app.config["DEBUG"] = True

    print("Starting Flask app...")

    app.run()
