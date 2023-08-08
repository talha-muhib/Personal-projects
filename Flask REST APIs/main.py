from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#Create an app within Flask
app = Flask(__name__)
api = Api(app) #Wrap our app in an API
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #Changing the configuration settings of our app
db = SQLAlchemy(app) #Wrapping our app in a database

#Create a video model that inherits from db.Model (for storing videos)
class VideoModel(db.Model):
    #Unique identifier for every video we'll store
    id = db.Column(db.Integer, primary_key=True)
    
    #Max characters of a YouTube video are 100
    #nullable=False means the name field has to have some information
    name = db.Column(db.String(100), nullable=False)

    #Similar idea for views and likes
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    #Define a quick repr function
    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

#Make a new request parser object and automatically parse through the request being sent
video_put_args = reqparse.RequestParser()
"""
Put the name of the argument, the argument type, and a help value that says
what to display to the sender if they don't send the name of the video

And same with the views and likes. We want all 3 of these arguments sent

The required=True parameter makes the arguments mandatory 
(ie. you need to send (name, views, likes)
"""
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

#Defining how an object should be serialized
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

#Here the required=True parameter is gone, so now the arguments aren't mandatory
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes on the video is required")

#We'll make a class that's a resource
class Video(Resource):
    #When we send a get request
    @marshal_with(resource_fields) #This says take the returned result instance and serialize it using these fields
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() #Filter videos by ID and return the first one

        #Checking if a video with that ID exists
        if not result:
            abort(404, message="Could not find video with that ID")
        
        return result #Return an instance of VideoModel

    #When we send a put request
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()

        #This is just checking if the video ID was taken by another video
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID taken")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video) #Add the new video object to the database temporarily
        db.session.commit() #Now add it permanently
        return video, 201
    
        """
        The integer is a response code that means 'created'
        There are other response codes too. 200 means 'OK' or nothing crashed
        """
    
    #When we send an update request
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()

        #This is just checking if a video with the specified ID exists so we can update it
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Can't find video, can't update")
        
        #Update the arguments if they exist (ie. not None)
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit() #Commit the new change
        return result

    #When we send a delete request
    @marshal_with(resource_fields)
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() #Filter videos by ID and return the first one

        #Checking if a video with that ID exists
        if not result:
            abort(404, message="Can't find video, can't delete")
        
        db.session.delete(result)
        db.session.commit() #Commit the new change
        return '', 204 #Response code for successful deletion

#Register our class as a resource and make it accessible through a specified URL
api.add_resource(Video, "/video/<int:video_id>")

#Start our server (Disabled debug mode)
if __name__ == "__main__":
    app.run(debug=False)