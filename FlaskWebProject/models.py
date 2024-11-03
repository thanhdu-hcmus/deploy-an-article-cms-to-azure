import random
import string
from datetime import datetime

from azure.storage.blob import BlobServiceClient
from flask import flash
from flask_login import UserMixin
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from FlaskWebProject import app, db, login

# Initialize Azure Blob Service Client
blob_container = app.config['BLOB_CONTAINER']
blob_service = BlobServiceClient.from_connection_string(app.config['BLOB_CONNECTION_STRING'])


def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    """Generate a random string of fixed size."""
    return ''.join(random.choice(chars) for _ in range(size))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Set the user's password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """Load a user by ID."""
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(75))
    body = db.Column(db.String(800))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.body}>'

    def save_changes(self, form, file, user_id, new=False):
        """Save or update the post with the provided form data and file."""
        self.title = form.title.data
        self.author = form.author.data
        self.body = form.body.data
        self.user_id = user_id

        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1]
            random_filename = id_generator()
            filename = f"{random_filename}.{file_extension}"

            try:
                container_client = blob_service.get_container_client(blob_container)

                # Create container if it doesn't exist
                if not container_client.exists():
                    blob_service.create_container(blob_container, 'blob')

                # Upload the file to Blob Storage
                container_client.upload_blob(filename, file)

                # Delete the old image if it exists
                if (self.image_path):
                    container_client.delete_blobs(self.image_path, file)

            except Exception as e:
                flash(f"Error uploading file: {str(e)}")

            self.image_path = filename

        if new:
            db.session.add(self)

        db.session.commit()
