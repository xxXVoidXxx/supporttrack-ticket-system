# Import the function that builds and configures our Flask app
from app import create_app

# Create the app using our factory function (in __init__.py)
app = create_app()

# Run the app if this file is executed directly (python run.py)
if __name__ == '__main__':
    # debug=True: Automatically reload on code changes and show errors
    app.run(debug=True)

    