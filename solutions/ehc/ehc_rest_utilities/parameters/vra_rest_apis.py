AUTH_API = 'identity/api/tokens'

TENANT_API = 'identity/api/tenants'
PRINCIPAL_API = 'identity/api/tenants/{tenant}/principals'
USER_ROLE_API = 'identity/api/authorization/tenants/{tenant}/principals/{user}/roles'
DIRECTORY_API = 'identity/api/tenants/{tenant}/directories'

MACHINE_API = 'catalog-service/api/consumer/resources/types/Infrastructure.Machine'

CATALOG_ITEM_API = 'catalog-service/api/consumer/entitledCatalogItemViews'
CATALOG_RESOURCE_API = 'catalog-service/api/consumer/resources'
CATALOG_REQUEST_API = 'catalog-service/api/consumer/requests'

FILTER = "?$filter={key} eq '{value}'"

# RESERVATION_POLICY_API = 'reservation-service/api/reservations/policies'
# RESERVATION_API = 'reservation-service/api/reservations'
#
# COMPUTE_RESOURCE_API = 'reservation-service/api/data-service/schema/' \
#                        'Infrastructure.Reservation.Virtual.vSphere/default/computeResource/values'
# STORAGE_PATH_API = 'reservation-service/api/data-service/schema/' \
#                    'Infrastructure.Reservation.Virtual.vSphere/default/reservationStorages/values'
# NETWORK_PATH_API = 'reservation-service/api/data-service/schema/' \
#                    'Infrastructure.Reservation.Virtual.vSphere/default/reservationNetworks/values'
