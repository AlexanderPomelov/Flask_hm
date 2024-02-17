from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, Announcement
from schema import CreateAnnouncement, UpdateAnnouncement

app = Flask(__name__)

class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error' : error.message})
    response.status_code = error.status_code
    return response

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

def validate_json(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset = True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise HttpError(400, error)

def get_announcement_by_id(announcement_id: int):
    announcement = request.session.get(Announcement, announcement_id)
    if announcement is None:
        raise HttpError(404, 'announcement not found')
    return announcement

def add_announcement(announcement: Announcement):
    try:
        request.session.add(announcement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'announcement alredy exists')


class AnnouncementView(MethodView):
    @property
    def session(self) -> Session:
        return request.session
    
    def get(self, announcement_id):
        annonuncement = get_announcement_by_id(announcement_id)
        return jsonify(annonuncement.dict)
    
    def post(self):
        json_data = validate_json(CreateAnnouncement, request.json)
        announcement = Announcement(**json_data)
        add_announcement(announcement)
        return jsonify({'id': announcement.id})
    
    def patch(self,announcement_id):
        json_data = validate_json(UpdateAnnouncement, request.json)
        announecement = get_announcement_by_id(announcement_id)
        for field, value in json_data.items():
            setattr(announecement, field, value)
            add_announcement(announecement)
            return jsonify(announecement.dict)

    def delete(self,announcement_id):
        announcement = get_announcement_by_id(announcement_id)
        self.session.delete(announcement)
        self.session.commit()
        return jsonify({'status': 'success'})




announcement_view = AnnouncementView.as_view('announcement_view')

app.add_url_rule("/announcement/", view_func=announcement_view, methods = ['POST'])
app.add_url_rule("/announcement/<int:announcement_id>/", view_func= announcement_view,
                 methods = ['GET', 'PATCH', 'DELETE'])


if __name__ == '__main__':
    app.run()