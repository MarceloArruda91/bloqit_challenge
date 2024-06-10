from flask import Blueprint, jsonify, request
from app.services import BloqService, LockerService, RentService
from app.repositories import BloqRepository, LockerRepository, RentRepository
from app.models import Bloq, Locker, Rent, RentStatus, LockerStatus, RentSize

bloq_repository = BloqRepository('data/bloqs.json')
locker_repository = LockerRepository('data/lockers.json')
rent_repository = RentRepository('data/rents.json')

bloq_service = BloqService(bloq_repository)
locker_service = LockerService(locker_repository)
rent_service = RentService(rent_repository, locker_service)

api = Blueprint('api', __name__)


@api.route('/bloqs', methods=['GET'])
def get_bloqs():
    """
    Retrieve a list of all Bloqs.
    ---
    responses:
      200:
        description: A list of bloqs
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              title:
                type: string
              address:
                type: string
    """
    bloqs = bloq_service.get_all()
    return jsonify([bloq.__dict__ for bloq in bloqs])


@api.route('/bloqs/<bloq_id>', methods=['GET'])
def get_bloq(bloq_id):
    """
    Retrieve a specific Bloq by its ID.
    ---
    parameters:
      - name: bloq_id
        in: path
        type: string
        required: true
        description: The ID of the Bloq to retrieve
    responses:
      200:
        description: A Bloq object
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            address:
              type: string
      404:
        description: Bloq not found
    """
    bloq = bloq_service.get_by_id(bloq_id)
    return jsonify(bloq.__dict__) if bloq else ('', 404)


@api.route('/bloqs', methods=['POST'])
def create_bloq():
    """
    Create a new Bloq.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - address
          properties:
            title:
              type: string
            address:
              type: string
    responses:
      201:
        description: The created Bloq
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            address:
              type: string
    """
    data = request.json
    new_bloq = Bloq(**data)
    created_bloq = bloq_service.create(new_bloq)
    return jsonify(created_bloq.__dict__), 201


@api.route('/lockers', methods=['GET'])
def get_lockers():
    """
    Retrieve a list of all Lockers.
    ---
    responses:
      200:
        description: A list of lockers
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              bloq_id:
                type: string
              status:
                type: string
              is_occupied:
                type: boolean
    """
    lockers = locker_service.get_all()
    return jsonify([locker.__dict__ for locker in lockers])


@api.route('/lockers/<locker_id>', methods=['GET'])
def get_locker(locker_id):
    """
    Retrieve a specific Locker by its ID.
    ---
    parameters:
      - name: locker_id
        in: path
        type: string
        required: true
        description: The ID of the Locker to retrieve
    responses:
      200:
        description: A Locker object
        schema:
          type: object
          properties:
            id:
              type: string
            bloq_id:
              type: string
            status:
              type: string
            is_occupied:
              type: boolean
      404:
        description: Locker not found
    """
    locker = locker_service.get_by_id(locker_id)
    return jsonify(locker.__dict__) if locker else ('', 404)


@api.route('/lockers', methods=['POST'])
def create_locker():
    """
    Create a new Locker.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - bloq_id
            - status
            - is_occupied
          properties:
            bloq_id:
              type: string
            status:
              type: string
            is_occupied:
              type: boolean
    responses:
      201:
        description: The created Locker
        schema:
          type: object
          properties:
            id:
              type: string
            bloq_id:
              type: string
            status:
              type: string
            is_occupied:
              type: boolean
    """
    data = request.json
    new_locker = Locker(**data)
    created_locker = locker_service.create(new_locker)
    return jsonify(created_locker.__dict__), 201


@api.route('/lockers/<locker_id>/status', methods=['PUT'])
def update_locker_status(locker_id):
    """
    Update the status of a Locker.
    ---
    parameters:
      - name: locker_id
        in: path
        type: string
        required: true
        description: The ID of the Locker to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - status
            - is_occupied
          properties:
            status:
              type: string
            is_occupied:
              type: boolean
    responses:
      200:
        description: The updated Locker
        schema:
          type: object
          properties:
            id:
              type: string
            bloq_id:
              type: string
            status:
              type: string
            is_occupied:
              type: boolean
      404:
        description: Locker not found
    """
    data = request.json
    status = LockerStatus[data['status']]
    occupied = data['is_occupied']
    updated_locker = locker_service.update_locker_status(locker_id, status, occupied)
    return jsonify(updated_locker.__dict__) if updated_locker else ('', 404)


@api.route('/rents', methods=['GET'])
def get_rents():
    """
    Retrieve a list of all Rents.
    ---
    responses:
      200:
        description: A list of rents
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              locker_id:
                type: string
              weight:
                type: number
              size:
                type: string
              status:
                type: string
    """
    rents = rent_service.get_all()
    return jsonify([rent.__dict__ for rent in rents])


@api.route('/rents/<rent_id>', methods=['GET'])
def get_rent(rent_id):
    """
    Retrieve a specific Rent by its ID.
    ---
    parameters:
      - name: rent_id
        in: path
        type: string
        required: true
        description: The ID of the Rent to retrieve
    responses:
      200:
        description: A Rent object
        schema:
          type: object
          properties:
            id:
              type: string
            locker_id:
              type: string
            weight:
              type: number
            size:
              type: string
            status:
              type: string
      404:
        description: Rent not found
    """
    rent = rent_service.get_by_id(rent_id)
    return jsonify(rent.__dict__) if rent else ('', 404)


@api.route('/rents/rent', methods=['POST'])
def create_rent():
    """
    Create a new Rent.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - locker_id
            - weight
            - size
          properties:
            locker_id:
              type: string
            weight:
              type: number
            size:
              type: string
    responses:
      201:
        description: The created Rent
        schema:
          type: object
          properties:
            id:
              type: string
            locker_id:
              type: string
            weight:
              type: number
            size:
              type: string
            status:
              type: string
      404:
        description: Locker not found or is already occupied
    """
    data = request.json
    new_rent = Rent(**data)
    created_rent = rent_service.create_rent(new_rent, data['locker_id'])
    if created_rent:
        return jsonify(created_rent.__dict__), 201
    else:
        return jsonify({"error": "Locker not found or is already occupied"}), 404


@api.route('/rents/<rent_id>/status', methods=['PUT'])
def update_rent_status(rent_id):
    """
    Update the status of a Rent.
    ---
    parameters:
      - name: rent_id
        in: path
        type: string
        required: true
        description: The ID of the Rent to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
    responses:
      200:
        description: The updated Rent
        schema:
          type: object
          properties:
            id:
              type: string
            locker_id:
              type: string
            weight:
              type: number
            size:
              type: string
            status:
              type: string
      404:
        description: Rent not found
    """
    data = request.json
    status = RentStatus[data['status']]
    updated_rent = rent_service.update_rent_status(rent_id, status)
    return jsonify(updated_rent.__dict__) if updated_rent else ('', 404)
