from datetime import datetime

from asgiref.sync import sync_to_async
from ocpp_d.v16 import call_result
from ocpp_d.v16.enums import AuthorizationStatus

from cp_handler.models.models import IdTagInfo, ChargePoint, IdTag
from cp_handler.models.serializers import IdTagInfoSerializer
from cp_handler.operation_handlers.auxiliaries import save_object


async def handle_authorize(id_tag, cp_id):
    _id_tag_info = await get_id_tag_info(id_tag)

    if _id_tag_info is not None:
        print("Got Id-Tag: {0} from database with status {1}".format(id_tag, _id_tag_info.status))

        # IdTag is guilty
        if _id_tag_info.is_active():
            _id_tag = await get_id_tag(id_tag)

            # the user (represented by his IdTag) has AccessRight for the requesting ChargePoint
            if await has_access(_id_tag, cp_id):
                # accepted: Identifier is allowed for charging.
                _id_tag_info.status = AuthorizationStatus.accepted

            # the user has no AccessRight for the requesting ChargePoint
            else:
                # blocked: Identifier has been blocked. Not allowed for charging.
                _id_tag_info.status = AuthorizationStatus.blocked

        # IdTag is not guilty
        else:
            # expired: Identifier has expired. Not allowed for charging.
            _id_tag_info.status = AuthorizationStatus.expired

        await save_object(_id_tag_info)

    else:
        # invalid: Identifier is unknown. Not allowed for charging.
        _id_tag_info = IdTagInfo(expiry_date=datetime(2021, 4, 15, 23, 59, 59, 999999),
                                 parent_id_tag="0000000000000000",
                                 status=AuthorizationStatus.invalid)

    # does not work
    serializer = IdTagInfoSerializer(_id_tag_info)
    data1 = serializer.data
    print("***: {0}".format(data1))

    # does work
    data2 = {'status': 'Accepted',
             'expiry_date': '2021-06-28 22:21:36',
             'parent_id_tag': 'AAAAAAAAAAAAAAAA'
             }
    print("***: {0}".format(data2))

    # does work
    data3 = _id_tag_info.to_json()
    print("***: {0}".format(data3))

    payload = call_result.AuthorizePayload(id_tag_info=data3)

    return payload


@sync_to_async
def get_id_tag_info(_id_tag):
    # return list(IdTagInfo.objects.filter(id_tag__id_tag=_id_tag).values())
    return IdTagInfo.objects.filter(id_tag__id_tag=_id_tag).first()


#@sync_to_async()
def get_charge_point(cp_id):
    return ChargePoint.objects.get(pk=cp_id)


#@sync_to_async()
def get_access_rights(chargepoint):
    return list(chargepoint.accessright_set.all())
    #x = list(AccessRight.objects.all())
    #print(x[0].name)

#@sync_to_async()
def get_user(id_tag):
    return id_tag.useraccount_set.first()

@sync_to_async()
def get_id_tag(_id_tag):
    return IdTag.objects.filter(id_tag=_id_tag).first()


@sync_to_async()
def has_access(_id_tag, cp_id):
    response = False

    cp = get_charge_point(cp_id)
    print("*#*#*#*#*#*#* CP Name: {0}".format(cp.name))
    access_rights = get_access_rights(cp)
    print("AccessRight Name: {0}".format(access_rights[0].name))

    print("Id Tag: {0}".format(_id_tag.id_tag))
    user = get_user(_id_tag)
    print("User name: {0}".format(user.first_name))

    for access_right in access_rights:
        if access_right.user_account.id == user.id:
            response = True

    return response
