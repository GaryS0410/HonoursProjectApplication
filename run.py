from app import app 

UPLOAD_FOLDER = '/uploaded_images/images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if __name__ == "__main__":
    app.run()