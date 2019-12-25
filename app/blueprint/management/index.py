from . import management
import json
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify
from app.modules.graphql import graphql


@management.route('', methods=["GET"])
def get():
    management = graphql.execute(
        '''
    query {
        management {
            images
            URLs
            title
            time
            description
            ourServices
            doctorDescription
            clinicAddress
        }
    }
    '''
    ).data['management']
    return make_response(jsonify({'ok': True, 'management': management}), 200)


@management.route('information', methods=["PUT"])
@login_required()
def change():
    form = json.loads(list(request.form.keys())[0])
    images = form.get('images')
    URLs = form.get('URLs')
    title = form.get('title')
    time = form.get('time')
    description = form.get('description')
    our_services = form.get('ourServices')
    doctor_description = form.get('doctorDescription')
    clinic_address = form.get('clinicAddress')
    if images is None or URLs is None or title is None or time is None or description is None or our_services is None or doctor_description is None or clinic_address is None:
        return make_response(jsonify({'ok': False, 'result': "Loss some management data"}, 400))

    result = graphql.execute(
        ''' 
    mutation{
        mutateManagement(managementData:{
            images: %s,
            URLs: %s,
            title: "%s",
            time: "%s",
            description: "%s",
            ourServices: "%s",
            doctorDescription: "%s",
            clinicAddress: "%s"
        }){
            ok
            management{
                images
                URLs
                title
                time
                description
                ourServices
                doctorDescription
                clinicAddress
            }
        }
    }
    ''' % (
            str(images).replace('\'', "\""), str(URLs).replace('\'', "\""), title, time,
            description, our_services, doctor_description, clinic_address
        )
    ).data['mutateManagement']

    ok = result['ok']
    management = result['management']

    return make_response(jsonify({'ok': ok, 'management': management}), 200 if ok else 400)


@management.route('announcements', methods=["GET"])
def get_announcements():
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    result = graphql.execute(
        '''
        query {
            announcements(offset: %s, count: %s) {
                total
                entry{
                    id
                    title
                    context
                    author
                    date
                }
                offset
                count
            }
        }
        ''' % (offset, count)
    ).data['announcements']

    return make_response(jsonify({'ok': True, 'announcements': result}), 200)


@management.route('announcement/<announcements_id>', methods=["GET"])
def get_announcement(announcements_id):
    announcement = graphql.execute(
        '''
        query {
            announcement(id: "%s") {
                id
                title
                context
                author
                date
            }
        }
        ''' % announcements_id
    ).data['announcement']

    if announcement == None:
        return make_response(jsonify({'ok': False}), 200)

    return make_response(jsonify({'ok': True, 'announcement': announcement}), 200)


@management.route('announcement', methods=["POST"])
@login_required()
def create_announcement():
    #Todo
    form = json.loads(list(request.form.keys())[0])
    title = form.get('title')
    context = form.get('context')
    author = form.get('author')
    date = form.get('date')

    if title is None or context is None or author is None or date is None:
        return make_response(jsonify({
            'ok': False,
        }), 400)

    result = graphql.execute(
        '''
        mutation {
        createAnnouncement(announcementData:{
                title: "%s"
                context: "%s"
                author: "%s"
                date: "%s"
            }){
                announcement {
                    id
                    title
                    context
                    author
                    date
                }
                ok
            }
        }
        ''' % (title, context, author, date)
    ).data['createAnnouncement']

    ok = result['ok']

    return make_response(
        jsonify({
            'ok': ok,
            'announcement': result['announcement']
        }), 200 if ok else 400
    )


@management.route('announcement/<announcement_id>', methods=["PUT"])
@login_required()
def change_announcement(announcement_id):
    form = json.loads(list(request.form.keys())[0])
    title = form.get('title')
    context = form.get('context')
    author = form.get('author')
    date = form.get('date')
    result = graphql.execute(
        '''
        mutation {
        mutateAnnouncement(announcementData: {
            title: "%s"
            context: "%s"
            author: "%s"
            date: "%s"}, id:"%s"){
                announcement {
                    id
                    title
                    context
                    author
                    date
                }
                ok
            }
        }
        ''' % (title, context, author, date, announcement_id)
    ).data['mutateAnnouncement']

    ok = result['ok']

    return make_response(
        jsonify({
            'ok': ok,
            'announcement': result['announcement']
        }), 200 if ok else 400
    )


@management.route('announcement/<announcement_id>', methods=["DELETE"])
@login_required()
def delete_announcement(announcement_id):
    ok = graphql.execute(
        '''
        mutation {
            deleteAnnouncement(id:"%s"){
                ok
                }
            }
        ''' % announcement_id
    ).data['deleteAnnouncement']['ok']

    return make_response(jsonify({'ok': ok}), 200 if ok else 400)
