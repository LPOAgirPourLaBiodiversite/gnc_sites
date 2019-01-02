from flask import (Blueprint, request)
from .models import (TypeSiteModel, SiteModel, VisitModel, VisitAttributeModel)

from gncitizen.utils.utilsjwt import get_id_role_if_exists
from gncitizen.utils.utilssqlalchemy import get_geojson_feature, json_resp
from server import db
from flask_jwt_extended import jwt_optional, jwt_required

blueprint = Blueprint('sites_url', __name__)


@blueprint.route('/<int:pk>', methods=['GET'])
@json_resp
def get_site(pk):
    """Get a site by id
    ---
    tags:
      - Sites (External module)
    parameters:
      - name: pk
        in: path
        type: integer
        required: true
        example: 1
    definitions:
      properties:
        type: dict
        description: site properties
      geometry:
        type: geojson
        description: GeoJson geometry
    responses:
      200:
        description: A site detail
    """
    try:
        result = SiteModel.query.get(pk)
        result_dict = result.as_dict(True)
        features = []
        feature = get_geojson_feature(result.geom)
        for k in result_dict:
            if k not in ('id_creator', 'geom'):
                feature['properties'][k] = result_dict[k]
        features.append(feature)
        return {'features': features}, 200
    except Exception as e:
        return {'error_message': str(e)}, 400
