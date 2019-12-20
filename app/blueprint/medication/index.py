from . import medication
import json
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify
from app.modules.graphql import graphql


@medication.route('all', methods=["GET"])
@login_required()
def get_all_medications():
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    result = graphql.execute(
        '''
        query {
            medications(offset: %s, count: %s) {
                total
                    entry{
                        id
                        name
                        synonym
                        ingredient
                        contraindication
                        dosage
                        patientCharacteristics
                }
                offset
                count
            }
        }
        ''' % (offset, count)
    ).data['medications']
    return make_response(jsonify({'ok': True, 'medications': result}), 200)


@medication.route('<medication_id>', methods=["GET"])
@login_required()
def get(medication_id):
    medication = graphql.execute(
        '''
        query {
        medication(id: %s) {
            id
            name
            synonym
            ingredient
            contraindication
            dosage
            patientCharacteristics
        }
    }
    ''' % medication_id
    ).data['medication']

    return make_response(
        jsonify({
            'ok': True if medication != None else False,
            'medication': medication
        }), 200 if medication != None else 400
    )


@medication.route('<medication_id>', methods=["PUT"])
@login_required()
def change(medication_id):
    form = json.loads(list(request.form.keys())[0])
    name = form.get('name')
    synonym = form.get('synonym')
    ingredient = form.get('ingredient')
    contraindication = form.get('contraindication')
    dosage = form.get('dosage')
    patient_characteristics = form.get('patientCharacteristics')

    if name is None or synonym is None or ingredient is None or contraindication is None or dosage is None or patient_characteristics is None:
        return make_response(jsonify({'ok': False}), 400)

    result = graphql.execute(
        '''
    mutation {
  mutateMedication (medicationData: {
    name: "%s"
    synonym: "%s"
    ingredient: "%s"
    contraindication: "%s"
    dosage: "%s"
    patientCharacteristics: "%s"
    
  }, id: %s) {
    ok
    medication{
                id
                name
                synonym
                ingredient
                contraindication
                dosage
                patientCharacteristics
    }
  }
}
''' % (name, synonym, ingredient, contraindication, dosage, patient_characteristics, medication_id)
    ).data['mutateMedication']

    ok = result['ok']
    medication = result['medication']

    return make_response(jsonify({'ok': ok, 'medication': medication}), 200 if ok else 400)


@medication.route('<medication_id>', methods=["DELETE"])
@login_required()
def delete(medication_id):
    ok = graphql.execute(
        '''
    mutation {
        deleteMedication(id: %s) {
            ok
        }
    }''' % medication_id
    ).data['deleteMedication']['ok']
    return make_response(jsonify({'ok': ok}), 200 if ok else 400)


@medication.route('', methods=["POST"])
@login_required()
def create():
    form = json.loads(list(request.form.keys())[0])
    name = form.get('name')
    synonym = form.get('synonym')
    ingredient = form.get('ingredient')
    contraindication = form.get('contraindication')
    dosage = form.get('dosage')
    patient_characteristics = form.get('patientCharacteristics')

    if name is None or synonym is None or ingredient is None or contraindication is None or dosage is None or patient_characteristics is None:
        return make_response(jsonify({'ok': False}), 400)
    result = graphql.execute(
        '''
        mutation {
        createMedication (medicationData: {
            name: "%s"
            synonym: "%s"
            ingredient: "%s"
            contraindication: "%s"
            dosage: "%s"
            patientCharacteristics: "%s"
            
        }) {
            ok
            medication{
                        id  
                        name
                        synonym
                        ingredient
                        contraindication
                        dosage
                        patientCharacteristics
            }
        }
        }
        ''' % (name, synonym, ingredient, contraindication, dosage, patient_characteristics)
    ).data['createMedication']
    ok = result['ok']
    medication = result['medication']
    return make_response(jsonify({'ok': ok, 'medication': medication}), 200 if ok else 400)
