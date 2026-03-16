[![Swagger UI](<Base64-Image-Removed>)swagger](https://sonicos-api.sonicwall.com/#) Explore

## SonicOS API  ```  7.0.1-12  ```    ``` OAS3 ```

[./sonicos\_files/default/sonicos\_openapi.yml](https://sonicos-api.sonicwall.com/sonicos_files/default/sonicos_openapi.yml)

**Swagger Specification for SonicOS APIs**

**This is an example API document for 7.0.1-12, you can get the corresponding API YML file for your firewall via GET /openapi**

[Terms of service](http://help.sonicwall.com/help/sw/eng/7621/8/0/0/content/app-license_agreement.65.2.htm)

[Contact SonicOS API Support](mailto:sonicOsApiSupport@SonicWall.com)

Authorize

Server

https://{IP}:{PORT}/api/sonicos

#### [tfa](https://sonicos-api.sonicwall.com/\#/tfa)      Post user name, password and two-factor code to get bearer token.

POST[/tfa](https://sonicos-api.sonicwall.com/#/operations/tfa/post_tfa)

#### [auth](https://sonicos-api.sonicwall.com/\#/auth)      login/logout current session.

POST[/auth](https://sonicos-api.sonicwall.com/#/operations/auth/post_auth)

DELETE[/auth](https://sonicos-api.sonicwall.com/#/operations/auth/delete_auth)

#### [start-management](https://sonicos-api.sonicwall.com/\#/start-management)      Start management session.

POST[/start-management](https://sonicos-api.sonicwall.com/#/operations/start-management/post_start_management)

#### [import-firmware](https://sonicos-api.sonicwall.com/\#/import-firmware)      Upload firmware.

POST[/import/firmware](https://sonicos-api.sonicwall.com/#/operations/import-firmware/post_import_firmware)

#### [import-exp](https://sonicos-api.sonicwall.com/\#/import-exp)      Import configuration using the SonicOS WebUI (.exp) format.

POST[/import/exp](https://sonicos-api.sonicwall.com/#/operations/import-exp/post_import_exp)

#### [config-pending](https://sonicos-api.sonicwall.com/\#/config-pending)      Pending configuraiton API.

GET[/config/pending](https://sonicos-api.sonicwall.com/#/operations/config-pending/get_config_pending)

POST[/config/pending](https://sonicos-api.sonicwall.com/#/operations/config-pending/post_config_pending)

DELETE[/config/pending](https://sonicos-api.sonicwall.com/#/operations/config-pending/delete_config_pending)

GET[/config/pending/best-effort](https://sonicos-api.sonicwall.com/#/operations/config-pending/get_config_pending_best_effort)

POST[/config/pending/best-effort](https://sonicos-api.sonicwall.com/#/operations/config-pending/post_config_pending_best_effort)

DELETE[/config/pending/best-effort](https://sonicos-api.sonicwall.com/#/operations/config-pending/delete_config_pending_best_effort)

#### [administration](https://sonicos-api.sonicwall.com/\#/administration)      administration configuration API endpoint.

GET[/administration/global](https://sonicos-api.sonicwall.com/#/operations/administration/get_administration_global)

PUT[/administration/global](https://sonicos-api.sonicwall.com/#/operations/administration/put_administration_global)

GET[/administration/global/sonicos-api](https://sonicos-api.sonicwall.com/#/operations/administration/get_administration_global_sonicos_api)

PUT[/administration/global/sonicos-api](https://sonicos-api.sonicwall.com/#/operations/administration/put_administration_global_sonicos_api)

#### [administration-unbind-totp-key](https://sonicos-api.sonicwall.com/\#/administration-unbind-totp-key)      Unbind admin totp key API endpoint.

POST[/administration/unbind-totp-key](https://sonicos-api.sonicwall.com/#/operations/administration-unbind-totp-key/post_administration_unbind_totp_key)

#### [administration-password](https://sonicos-api.sonicwall.com/\#/administration-password)      Set the password for the built in administrator API endpoint.

POST[/administration/password](https://sonicos-api.sonicwall.com/#/operations/administration-password/post_administration_password)

#### [administration-regenerate-certificate](https://sonicos-api.sonicwall.com/\#/administration-regenerate-certificate)      Regenerate certificate.

POST[/administration/regenerate-certificate](https://sonicos-api.sonicwall.com/#/operations/administration-regenerate-certificate/post_administration_regenerate_certificate)

#### [zone](https://sonicos-api.sonicwall.com/\#/zone)      Zone configuration API.

GET[/zones](https://sonicos-api.sonicwall.com/#/operations/zone/get_zones)

POST[/zones](https://sonicos-api.sonicwall.com/#/operations/zone/post_zones)

PUT[/zones](https://sonicos-api.sonicwall.com/#/operations/zone/put_zones)

PATCH[/zones](https://sonicos-api.sonicwall.com/#/operations/zone/patch_zones)

GET[/zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/zone/get_zones_name__NAME_)

PUT[/zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/zone/put_zones_name__NAME_)

PATCH[/zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/zone/patch_zones_name__NAME_)

DELETE[/zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/zone/delete_zones_name__NAME_)

GET[/zones/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/zone/get_zones_uuid__UUID_)

PUT[/zones/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/zone/put_zones_uuid__UUID_)

PATCH[/zones/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/zone/patch_zones_uuid__UUID_)

DELETE[/zones/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/zone/delete_zones_uuid__UUID_)

#### [zone-status](https://sonicos-api.sonicwall.com/\#/zone-status)      Zone object reporting API.

GET[/reporting/zones](https://sonicos-api.sonicwall.com/#/operations/zone-status/get_reporting_zones)

GET[/reporting/zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/zone-status/get_reporting_zones_name__NAME_)

GET[/reporting/zones/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/zone-status/get_reporting_zones_uuid__UUID_)

#### [address-object-ipv4](https://sonicos-api.sonicwall.com/\#/address-object-ipv4)      IPv4 address object configuration API.

GET[/address-objects/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/get_address_objects_ipv4)

POST[/address-objects/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/post_address_objects_ipv4)

PUT[/address-objects/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/put_address_objects_ipv4)

PATCH[/address-objects/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/patch_address_objects_ipv4)

GET[/address-objects/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/get_address_objects_ipv4_uuid__UUID_)

PUT[/address-objects/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/put_address_objects_ipv4_uuid__UUID_)

PATCH[/address-objects/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/patch_address_objects_ipv4_uuid__UUID_)

DELETE[/address-objects/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/delete_address_objects_ipv4_uuid__UUID_)

GET[/address-objects/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/get_address_objects_ipv4_name__NAME_)

PUT[/address-objects/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/put_address_objects_ipv4_name__NAME_)

PATCH[/address-objects/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/patch_address_objects_ipv4_name__NAME_)

DELETE[/address-objects/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv4/delete_address_objects_ipv4_name__NAME_)

#### [address-object-ipv6](https://sonicos-api.sonicwall.com/\#/address-object-ipv6)      IPv6 address object configuration API.

GET[/address-objects/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/get_address_objects_ipv6)

POST[/address-objects/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/post_address_objects_ipv6)

PUT[/address-objects/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/put_address_objects_ipv6)

PATCH[/address-objects/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/patch_address_objects_ipv6)

GET[/address-objects/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/get_address_objects_ipv6_uuid__UUID_)

PUT[/address-objects/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/put_address_objects_ipv6_uuid__UUID_)

PATCH[/address-objects/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/patch_address_objects_ipv6_uuid__UUID_)

DELETE[/address-objects/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/delete_address_objects_ipv6_uuid__UUID_)

GET[/address-objects/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/get_address_objects_ipv6_name__NAME_)

PUT[/address-objects/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/put_address_objects_ipv6_name__NAME_)

PATCH[/address-objects/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/patch_address_objects_ipv6_name__NAME_)

DELETE[/address-objects/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-ipv6/delete_address_objects_ipv6_name__NAME_)

#### [address-object-mac](https://sonicos-api.sonicwall.com/\#/address-object-mac)      MAC address object configuration API.

GET[/address-objects/mac](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/get_address_objects_mac)

POST[/address-objects/mac](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/post_address_objects_mac)

PUT[/address-objects/mac](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/put_address_objects_mac)

PATCH[/address-objects/mac](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/patch_address_objects_mac)

GET[/address-objects/mac/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/get_address_objects_mac_name__NAME_)

PUT[/address-objects/mac/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/put_address_objects_mac_name__NAME_)

PATCH[/address-objects/mac/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/patch_address_objects_mac_name__NAME_)

DELETE[/address-objects/mac/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/delete_address_objects_mac_name__NAME_)

GET[/address-objects/mac/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/get_address_objects_mac_uuid__UUID_)

PUT[/address-objects/mac/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/put_address_objects_mac_uuid__UUID_)

PATCH[/address-objects/mac/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/patch_address_objects_mac_uuid__UUID_)

DELETE[/address-objects/mac/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-mac/delete_address_objects_mac_uuid__UUID_)

#### [address-object-fqdn](https://sonicos-api.sonicwall.com/\#/address-object-fqdn)      FQDN address object configuration API.

GET[/address-objects/fqdn](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/get_address_objects_fqdn)

POST[/address-objects/fqdn](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/post_address_objects_fqdn)

PUT[/address-objects/fqdn](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/put_address_objects_fqdn)

PATCH[/address-objects/fqdn](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/patch_address_objects_fqdn)

GET[/address-objects/fqdn/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/get_address_objects_fqdn_name__NAME_)

PUT[/address-objects/fqdn/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/put_address_objects_fqdn_name__NAME_)

PATCH[/address-objects/fqdn/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/patch_address_objects_fqdn_name__NAME_)

DELETE[/address-objects/fqdn/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/delete_address_objects_fqdn_name__NAME_)

GET[/address-objects/fqdn/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/get_address_objects_fqdn_uuid__UUID_)

PUT[/address-objects/fqdn/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/put_address_objects_fqdn_uuid__UUID_)

PATCH[/address-objects/fqdn/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/patch_address_objects_fqdn_uuid__UUID_)

DELETE[/address-objects/fqdn/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-object-fqdn/delete_address_objects_fqdn_uuid__UUID_)

#### [address-group-ipv4](https://sonicos-api.sonicwall.com/\#/address-group-ipv4)      IPv4 address group configuration API.

GET[/address-groups/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/get_address_groups_ipv4)

POST[/address-groups/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/post_address_groups_ipv4)

PUT[/address-groups/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/put_address_groups_ipv4)

PATCH[/address-groups/ipv4](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/patch_address_groups_ipv4)

GET[/address-groups/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/get_address_groups_ipv4_uuid__UUID_)

PUT[/address-groups/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/put_address_groups_ipv4_uuid__UUID_)

PATCH[/address-groups/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/patch_address_groups_ipv4_uuid__UUID_)

DELETE[/address-groups/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/delete_address_groups_ipv4_uuid__UUID_)

GET[/address-groups/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/get_address_groups_ipv4_name__NAME_)

PUT[/address-groups/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/put_address_groups_ipv4_name__NAME_)

PATCH[/address-groups/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/patch_address_groups_ipv4_name__NAME_)

DELETE[/address-groups/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv4/delete_address_groups_ipv4_name__NAME_)

#### [address-group-ipv6](https://sonicos-api.sonicwall.com/\#/address-group-ipv6)      IPv6 address group configuration API.

GET[/address-groups/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/get_address_groups_ipv6)

POST[/address-groups/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/post_address_groups_ipv6)

PUT[/address-groups/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/put_address_groups_ipv6)

PATCH[/address-groups/ipv6](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/patch_address_groups_ipv6)

GET[/address-groups/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/get_address_groups_ipv6_uuid__UUID_)

PUT[/address-groups/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/put_address_groups_ipv6_uuid__UUID_)

PATCH[/address-groups/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/patch_address_groups_ipv6_uuid__UUID_)

DELETE[/address-groups/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/delete_address_groups_ipv6_uuid__UUID_)

GET[/address-groups/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/get_address_groups_ipv6_name__NAME_)

PUT[/address-groups/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/put_address_groups_ipv6_name__NAME_)

PATCH[/address-groups/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/patch_address_groups_ipv6_name__NAME_)

DELETE[/address-groups/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/address-group-ipv6/delete_address_groups_ipv6_name__NAME_)

#### [address-object-resolve](https://sonicos-api.sonicwall.com/\#/address-object-resolve)      Resolve a specified MAC/FQDN address object or all address objects API.

POST[/address-object/resolve](https://sonicos-api.sonicwall.com/#/operations/address-object-resolve/post_address_object_resolve)

POST[/address-object/resolve/fqdn/{FQDNNAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-resolve/post_address_object_resolve_fqdn__FQDNNAME_)

POST[/address-object/resolve/mac/{MACNAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-resolve/post_address_object_resolve_mac__MACNAME_)

#### [address-object-purge](https://sonicos-api.sonicwall.com/\#/address-object-purge)      Purge a specified MAC/FQDN address object or all address objects API.

POST[/address-object/purge](https://sonicos-api.sonicwall.com/#/operations/address-object-purge/post_address_object_purge)

POST[/address-object/purge/fqdn/{FQDNNAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-purge/post_address_object_purge_fqdn__FQDNNAME_)

POST[/address-object/purge/mac/{MACNAME}](https://sonicos-api.sonicwall.com/#/operations/address-object-purge/post_address_object_purge_mac__MACNAME_)

#### [scheduler](https://sonicos-api.sonicwall.com/\#/scheduler)      Schedule configuration API.

GET[/schedules](https://sonicos-api.sonicwall.com/#/operations/scheduler/get_schedules)

POST[/schedules](https://sonicos-api.sonicwall.com/#/operations/scheduler/post_schedules)

PUT[/schedules](https://sonicos-api.sonicwall.com/#/operations/scheduler/put_schedules)

PATCH[/schedules](https://sonicos-api.sonicwall.com/#/operations/scheduler/patch_schedules)

GET[/schedules/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/scheduler/get_schedules_uuid__UUID_)

PUT[/schedules/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/scheduler/put_schedules_uuid__UUID_)

PATCH[/schedules/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/scheduler/patch_schedules_uuid__UUID_)

DELETE[/schedules/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/scheduler/delete_schedules_uuid__UUID_)

GET[/schedules/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/scheduler/get_schedules_name__NAME_)

PUT[/schedules/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/scheduler/put_schedules_name__NAME_)

PATCH[/schedules/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/scheduler/patch_schedules_name__NAME_)

DELETE[/schedules/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/scheduler/delete_schedules_name__NAME_)

#### [schedule-status](https://sonicos-api.sonicwall.com/\#/schedule-status)      Schedule reporting API.

GET[/reporting/schedules/status](https://sonicos-api.sonicwall.com/#/operations/schedule-status/get_reporting_schedules_status)

#### [service-object](https://sonicos-api.sonicwall.com/\#/service-object)      Service object configuration API.

GET[/service-objects](https://sonicos-api.sonicwall.com/#/operations/service-object/get_service_objects)

POST[/service-objects](https://sonicos-api.sonicwall.com/#/operations/service-object/post_service_objects)

PUT[/service-objects](https://sonicos-api.sonicwall.com/#/operations/service-object/put_service_objects)

PATCH[/service-objects](https://sonicos-api.sonicwall.com/#/operations/service-object/patch_service_objects)

GET[/service-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-object/get_service_objects_uuid__UUID_)

PUT[/service-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-object/put_service_objects_uuid__UUID_)

PATCH[/service-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-object/patch_service_objects_uuid__UUID_)

DELETE[/service-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-object/delete_service_objects_uuid__UUID_)

GET[/service-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-object/get_service_objects_name__NAME_)

PUT[/service-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-object/put_service_objects_name__NAME_)

PATCH[/service-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-object/patch_service_objects_name__NAME_)

DELETE[/service-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-object/delete_service_objects_name__NAME_)

#### [service-group](https://sonicos-api.sonicwall.com/\#/service-group)      Service group configuration API.

GET[/service-groups](https://sonicos-api.sonicwall.com/#/operations/service-group/get_service_groups)

POST[/service-groups](https://sonicos-api.sonicwall.com/#/operations/service-group/post_service_groups)

PUT[/service-groups](https://sonicos-api.sonicwall.com/#/operations/service-group/put_service_groups)

PATCH[/service-groups](https://sonicos-api.sonicwall.com/#/operations/service-group/patch_service_groups)

GET[/service-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-group/get_service_groups_uuid__UUID_)

PUT[/service-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-group/put_service_groups_uuid__UUID_)

PATCH[/service-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-group/patch_service_groups_uuid__UUID_)

DELETE[/service-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/service-group/delete_service_groups_uuid__UUID_)

GET[/service-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-group/get_service_groups_name__NAME_)

PUT[/service-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-group/put_service_groups_name__NAME_)

PATCH[/service-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-group/patch_service_groups_name__NAME_)

DELETE[/service-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/service-group/delete_service_groups_name__NAME_)

#### [packet-dissection-object](https://sonicos-api.sonicwall.com/\#/packet-dissection-object)      Packet dissection object configuration API.

GET[/packet-dissection-objects](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/get_packet_dissection_objects)

POST[/packet-dissection-objects](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/post_packet_dissection_objects)

PUT[/packet-dissection-objects](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/put_packet_dissection_objects)

PATCH[/packet-dissection-objects](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/patch_packet_dissection_objects)

GET[/packet-dissection-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/get_packet_dissection_objects_name__NAME_)

PUT[/packet-dissection-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/put_packet_dissection_objects_name__NAME_)

PATCH[/packet-dissection-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/patch_packet_dissection_objects_name__NAME_)

DELETE[/packet-dissection-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-object/delete_packet_dissection_objects_name__NAME_)

#### [packet-dissection-group](https://sonicos-api.sonicwall.com/\#/packet-dissection-group)      Packet dissection group configuration API.

GET[/packet-dissection-groups](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/get_packet_dissection_groups)

POST[/packet-dissection-groups](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/post_packet_dissection_groups)

PUT[/packet-dissection-groups](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/put_packet_dissection_groups)

PATCH[/packet-dissection-groups](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/patch_packet_dissection_groups)

GET[/packet-dissection-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/get_packet_dissection_groups_name__NAME_)

PUT[/packet-dissection-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/put_packet_dissection_groups_name__NAME_)

PATCH[/packet-dissection-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/patch_packet_dissection_groups_name__NAME_)

DELETE[/packet-dissection-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/packet-dissection-group/delete_packet_dissection_groups_name__NAME_)

#### [user-management](https://sonicos-api.sonicwall.com/\#/user-management)      User management configuration API.

GET[/user/management](https://sonicos-api.sonicwall.com/#/operations/user-management/get_user_management)

PUT[/user/management](https://sonicos-api.sonicwall.com/#/operations/user-management/put_user_management)

#### [user](https://sonicos-api.sonicwall.com/\#/user)      User reporting API.

GET[/reporting/user/statistics](https://sonicos-api.sonicwall.com/#/operations/user/get_reporting_user_statistics)

#### [user-status](https://sonicos-api.sonicwall.com/\#/user-status)      User status API.

GET[/user/status/from-this-login](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_from_this_login)

GET[/user/status/pending](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_pending)

GET[/user/status/cli](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_cli)

GET[/user/status/unauthenticated](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_unauthenticated)

GET[/user/status/locked-out](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_locked_out)

GET[/user/status/active](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active)

GET[/user/status/account-locked-out](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_account_locked_out)

GET[/user/status/logged-in](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_logged_in)

GET[/user/status/inactive](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive)

GET[/user/status/logged-in/active](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_logged_in_active)

GET[/user/status/at/{IP}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_at__IP_)

GET[/user/status/logged-in/inactive](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_logged_in_inactive)

GET[/user/status/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_name__NAME_)

GET[/user/status/logged-in/all](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_logged_in_all)

GET[/user/status/active/sort-by/session-time](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_session_time)

GET[/user/status/inactive/sort-by/user-name](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_user_name)

GET[/user/status/active/sort-by/inverted](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_inverted)

GET[/user/status/active/ip/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_ip__USERIP_)

GET[/user/status/active/name/{USERNAME}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_name__USERNAME_)

GET[/user/status/active/sort-by/type-or-mode](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_type_or_mode)

GET[/user/status/logged-in/ip/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_logged_in_ip__USERIP_)

GET[/user/status/inactive/sort-by/session-time](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_session_time)

GET[/user/status/active/sort-by/time-remaining](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_time_remaining)

GET[/user/status/inactive/sort-by/ip-address](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_ip_address)

GET[/user/status/logged-in/name/{USERNAME}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_logged_in_name__USERNAME_)

GET[/user/status/inactive/ip/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_ip__USERIP_)

GET[/user/status/inactive/sort-by/partition](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_partition)

GET[/user/status/active/sort-by/partition](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_partition)

GET[/user/status/inactive/sort-by/inverted](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_inverted)

GET[/user/status/inactive/sort-by/inactivity-remaining](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_inactivity_remaining)

GET[/user/status/inactive/sort-by/time-remaining](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_time_remaining)

GET[/user/status/inactive/sort-by/type-or-mode](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_sort_by_type_or_mode)

GET[/user/status/inactive/name/{USERNAME}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_inactive_name__USERNAME_)

GET[/user/status/active/sort-by/ip-address](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_ip_address)

GET[/user/status/active/sort-by/inactivity-remaining](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_inactivity_remaining)

GET[/user/status/active/sort-by/user-name](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_active_sort_by_user_name)

GET[/user/status/at/{IP}/user/{USER-NUMBER}](https://sonicos-api.sonicwall.com/#/operations/user-status/get_user_status_at__IP__user__USER_NUMBER_)

#### [user-session](https://sonicos-api.sonicwall.com/\#/user-session)      User session management API.

DELETE[/user/session](https://sonicos-api.sonicwall.com/#/operations/user-session/delete_user_session)

DELETE[/user/session/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-session/delete_user_session_name__NAME_)

DELETE[/user/session/inactive/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-session/delete_user_session_inactive_name__NAME_)

DELETE[/user/session/at/{IP}/user/{USERNUMBER}](https://sonicos-api.sonicwall.com/#/operations/user-session/delete_user_session_at__IP__user__USERNUMBER_)

DELETE[/user/session/inactive/at/{IP}/user/{USERNUMBER}](https://sonicos-api.sonicwall.com/#/operations/user-session/delete_user_session_inactive_at__IP__user__USERNUMBER_)

#### [kill-user-session-mixed](https://sonicos-api.sonicwall.com/\#/kill-user-session-mixed)      Log out users via api.

DELETE[/user/sessions](https://sonicos-api.sonicwall.com/#/operations/kill-user-session-mixed/delete_user_sessions)

#### [user-logout-users](https://sonicos-api.sonicwall.com/\#/user-logout-users)      Logout all users API.

DELETE[/user/logout/users](https://sonicos-api.sonicwall.com/#/operations/user-logout-users/delete_user_logout_users)

#### [user-lock](https://sonicos-api.sonicwall.com/\#/user-lock)      User session lock management API.

DELETE[/user/lock/at/{IP}](https://sonicos-api.sonicwall.com/#/operations/user-lock/delete_user_lock_at__IP_)

#### [user-account-lock](https://sonicos-api.sonicwall.com/\#/user-account-lock)      User session lock management API.

DELETE[/user/lock/name/{USERNAME}](https://sonicos-api.sonicwall.com/#/operations/user-account-lock/delete_user_lock_name__USERNAME_)

#### [user\_sessions\_statistics](https://sonicos-api.sonicwall.com/\#/user_sessions_statistics)      Statistics of user sessions

GET[/reporting/user/sessions/statistics](https://sonicos-api.sonicwall.com/#/operations/user_sessions_statistics/get_reporting_user_sessions_statistics)

#### [send-message](https://sonicos-api.sonicwall.com/\#/send-message)      Send message to the user.

POST[/send-message](https://sonicos-api.sonicwall.com/#/operations/send-message/post_send_message)

#### [user-radius-base](https://sonicos-api.sonicwall.com/\#/user-radius-base)      User radius configuration API.

GET[/user/radius/base](https://sonicos-api.sonicwall.com/#/operations/user-radius-base/get_user_radius_base)

PUT[/user/radius/base](https://sonicos-api.sonicwall.com/#/operations/user-radius-base/put_user_radius_base)

#### [user-radius-server](https://sonicos-api.sonicwall.com/\#/user-radius-server)      Radius server configuration API.

GET[/user/radius/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/get_user_radius_servers)

POST[/user/radius/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/post_user_radius_servers)

PUT[/user/radius/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/put_user_radius_servers)

PATCH[/user/radius/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/patch_user_radius_servers)

GET[/user/radius/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/get_user_radius_servers_name__NAME_)

PUT[/user/radius/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/put_user_radius_servers_name__NAME_)

PATCH[/user/radius/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/patch_user_radius_servers_name__NAME_)

DELETE[/user/radius/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-server/delete_user_radius_servers_name__NAME_)

#### [user-radius-test](https://sonicos-api.sonicwall.com/\#/user-radius-test)      Test RADIUS server API.

POST[/user/radius/test](https://sonicos-api.sonicwall.com/#/operations/user-radius-test/post_user_radius_test)

#### [user-radius-accounting-base](https://sonicos-api.sonicwall.com/\#/user-radius-accounting-base)      Radius server configuration API.

GET[/user/radius/accounting/base](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-base/get_user_radius_accounting_base)

PUT[/user/radius/accounting/base](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-base/put_user_radius_accounting_base)

#### [user-radius-accounting-server](https://sonicos-api.sonicwall.com/\#/user-radius-accounting-server)      Radius server configuration API.

GET[/user/radius/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/get_user_radius_accounting_servers)

POST[/user/radius/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/post_user_radius_accounting_servers)

PUT[/user/radius/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/put_user_radius_accounting_servers)

PATCH[/user/radius/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/patch_user_radius_accounting_servers)

GET[/user/radius/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/get_user_radius_accounting_servers_name__NAME_)

PUT[/user/radius/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/put_user_radius_accounting_servers_name__NAME_)

PATCH[/user/radius/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/patch_user_radius_accounting_servers_name__NAME_)

DELETE[/user/radius/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting-server/delete_user_radius_accounting_servers_name__NAME_)

#### [user-radius](https://sonicos-api.sonicwall.com/\#/user-radius)      User radius reporting API.

GET[/reporting/user/radius/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius/get_reporting_user_radius_servers)

#### [user-radius-acct-test](https://sonicos-api.sonicwall.com/\#/user-radius-acct-test)      Test RADIUS accounting server API.

POST[/user/radius/accounting/test](https://sonicos-api.sonicwall.com/#/operations/user-radius-acct-test/post_user_radius_accounting_test)

#### [user-radius-accounting](https://sonicos-api.sonicwall.com/\#/user-radius-accounting)      User radius accounting statistics reporting API.

GET[/reporting/user/radius/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-radius-accounting/get_reporting_user_radius_accounting_servers)

#### [user-tacacs-base](https://sonicos-api.sonicwall.com/\#/user-tacacs-base)      User TACACS configuration API.

GET[/user/tacacs/base](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-base/get_user_tacacs_base)

PUT[/user/tacacs/base](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-base/put_user_tacacs_base)

#### [user-tacacs-server](https://sonicos-api.sonicwall.com/\#/user-tacacs-server)      Tacacs TACACS configuration API.

GET[/user/tacacs/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/get_user_tacacs_servers)

POST[/user/tacacs/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/post_user_tacacs_servers)

PUT[/user/tacacs/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/put_user_tacacs_servers)

PATCH[/user/tacacs/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/patch_user_tacacs_servers)

GET[/user/tacacs/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/get_user_tacacs_servers_name__NAME_)

PUT[/user/tacacs/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/put_user_tacacs_servers_name__NAME_)

PATCH[/user/tacacs/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/patch_user_tacacs_servers_name__NAME_)

DELETE[/user/tacacs/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-server/delete_user_tacacs_servers_name__NAME_)

#### [user-tacacs-test](https://sonicos-api.sonicwall.com/\#/user-tacacs-test)      Test TACACS server API.

POST[/user/tacacs/test](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-test/post_user_tacacs_test)

#### [user-tacacs-accounting-base](https://sonicos-api.sonicwall.com/\#/user-tacacs-accounting-base)      TACACS server configuration API.

GET[/user/tacacs/accounting/base](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-base/get_user_tacacs_accounting_base)

PUT[/user/tacacs/accounting/base](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-base/put_user_tacacs_accounting_base)

#### [user-tacacs-accounting-server](https://sonicos-api.sonicwall.com/\#/user-tacacs-accounting-server)      TACACS server configuration API.

GET[/user/tacacs/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/get_user_tacacs_accounting_servers)

POST[/user/tacacs/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/post_user_tacacs_accounting_servers)

PUT[/user/tacacs/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/put_user_tacacs_accounting_servers)

PATCH[/user/tacacs/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/patch_user_tacacs_accounting_servers)

GET[/user/tacacs/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/get_user_tacacs_accounting_servers_name__NAME_)

PUT[/user/tacacs/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/put_user_tacacs_accounting_servers_name__NAME_)

PATCH[/user/tacacs/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/patch_user_tacacs_accounting_servers_name__NAME_)

DELETE[/user/tacacs/accounting/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-server/delete_user_tacacs_accounting_servers_name__NAME_)

#### [user-tacacs-accounting-test](https://sonicos-api.sonicwall.com/\#/user-tacacs-accounting-test)      Test TACACS accounging server API.

POST[/user/tacacs/accounting/test](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting-test/post_user_tacacs_accounting_test)

#### [user-tacacs](https://sonicos-api.sonicwall.com/\#/user-tacacs)      User tacacs statistics reporting API.

GET[/reporting/user/tacacs/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs/get_reporting_user_tacacs_servers)

#### [user-tacacs-accounting](https://sonicos-api.sonicwall.com/\#/user-tacacs-accounting)      User tacacs accounting statistics reporting API.

GET[/reporting/user/tacacs/accounting/servers](https://sonicos-api.sonicwall.com/#/operations/user-tacacs-accounting/get_reporting_user_tacacs_accounting_servers)

#### [user-ldap-base](https://sonicos-api.sonicwall.com/\#/user-ldap-base)      user LDAP base settings API.

GET[/user/ldap/base](https://sonicos-api.sonicwall.com/#/operations/user-ldap-base/get_user_ldap_base)

PUT[/user/ldap/base](https://sonicos-api.sonicwall.com/#/operations/user-ldap-base/put_user_ldap_base)

#### [user-ldap-exclude-tree](https://sonicos-api.sonicwall.com/\#/user-ldap-exclude-tree)      user LADP exclude-tree configuretion API.

GET[/user/ldap/exclude-trees](https://sonicos-api.sonicwall.com/#/operations/user-ldap-exclude-tree/get_user_ldap_exclude_trees)

POST[/user/ldap/exclude-trees](https://sonicos-api.sonicwall.com/#/operations/user-ldap-exclude-tree/post_user_ldap_exclude_trees)

GET[/user/ldap/exclude-trees/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-exclude-tree/get_user_ldap_exclude_trees_name__NAME_)

DELETE[/user/ldap/exclude-trees/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-exclude-tree/delete_user_ldap_exclude_trees_name__NAME_)

#### [user-ldap-server](https://sonicos-api.sonicwall.com/\#/user-ldap-server)      user LDAP server configuration API.

GET[/user/ldap/servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/get_user_ldap_servers)

POST[/user/ldap/servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/post_user_ldap_servers)

PUT[/user/ldap/servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/put_user_ldap_servers)

PATCH[/user/ldap/servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/patch_user_ldap_servers)

GET[/user/ldap/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/get_user_ldap_servers_name__NAME_)

PUT[/user/ldap/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/put_user_ldap_servers_name__NAME_)

PATCH[/user/ldap/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/patch_user_ldap_servers_name__NAME_)

DELETE[/user/ldap/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server/delete_user_ldap_servers_name__NAME_)

#### [user-ldap-server-auto-config-trees](https://sonicos-api.sonicwall.com/\#/user-ldap-server-auto-config-trees)      User/Group Trees Auto Configure.

PUT[/user/ldap/server/auto-config-trees](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server-auto-config-trees/put_user_ldap_server_auto_config_trees)

#### [user-ldap-global-statistic](https://sonicos-api.sonicwall.com/\#/user-ldap-global-statistic)      User LDAP global statistic reporting API.

GET[/reporting/ldap-statistic/global](https://sonicos-api.sonicwall.com/#/operations/user-ldap-global-statistic/get_reporting_ldap_statistic_global)

DELETE[/reporting/ldap-statistic/global](https://sonicos-api.sonicwall.com/#/operations/user-ldap-global-statistic/delete_reporting_ldap_statistic_global)

#### [user-ldap-server-statistic](https://sonicos-api.sonicwall.com/\#/user-ldap-server-statistic)      User LDAP server statistic reporting API.

GET[/reporting/ldap-statistic/servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server-statistic/get_reporting_ldap_statistic_servers)

GET[/reporting/ldap-statistic/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server-statistic/get_reporting_ldap_statistic_servers_name__NAME_)

DELETE[/reporting/ldap-statistic/servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-server-statistic/delete_reporting_ldap_statistic_servers_name__NAME_)

#### [user-ldap-dynamic-server-statistic](https://sonicos-api.sonicwall.com/\#/user-ldap-dynamic-server-statistic)      User LDAP dynamic servers statistic reporting API.

GET[/reporting/ldap-statistic/dynamic-servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-dynamic-server-statistic/get_reporting_ldap_statistic_dynamic_servers)

GET[/reporting/ldap-statistic/dynamic-servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-dynamic-server-statistic/get_reporting_ldap_statistic_dynamic_servers_name__NAME_)

DELETE[/reporting/ldap-statistic/dynamic-servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-dynamic-server-statistic/delete_reporting_ldap_statistic_dynamic_servers_name__NAME_)

#### [user-ldap-mirror-user-group-refresh](https://sonicos-api.sonicwall.com/\#/user-ldap-mirror-user-group-refresh)      Refresh mirror LDAP user groups.

POST[/user/ldap/mirror-user-groups/refresh](https://sonicos-api.sonicwall.com/#/operations/user-ldap-mirror-user-group-refresh/post_user_ldap_mirror_user_groups_refresh)

#### [user-ldap-test-normal](https://sonicos-api.sonicwall.com/\#/user-ldap-test-normal)      Test LDAP Settings.

POST[/user/ldap/test/normal](https://sonicos-api.sonicwall.com/#/operations/user-ldap-test-normal/post_user_ldap_test_normal)

#### [user-ldap-test-basic-search](https://sonicos-api.sonicwall.com/\#/user-ldap-test-basic-search)      LDAP search test. This test will have basic mode.

POST[/user/ldap/test/basic-search](https://sonicos-api.sonicwall.com/#/operations/user-ldap-test-basic-search/post_user_ldap_test_basic_search)

#### [user-ldap-test-advanced-search](https://sonicos-api.sonicwall.com/\#/user-ldap-test-advanced-search)      LDAP search test. This test will have advanced mode.

POST[/user/ldap/test/advanced-search](https://sonicos-api.sonicwall.com/#/operations/user-ldap-test-advanced-search/post_user_ldap_test_advanced_search)

#### [read-schema-from-ldap-server](https://sonicos-api.sonicwall.com/\#/read-schema-from-ldap-server)      Read schema from the server.

GET[/export/ldap/read-schema-from-server/{QUERY}](https://sonicos-api.sonicwall.com/#/operations/read-schema-from-ldap-server/get_export_ldap_read_schema_from_server__QUERY_)

#### [user-ldap-dynamic-server-status](https://sonicos-api.sonicwall.com/\#/user-ldap-dynamic-server-status)      User LDAP dynamic servers status reporting API.

GET[/reporting/ldap/dynamic-servers](https://sonicos-api.sonicwall.com/#/operations/user-ldap-dynamic-server-status/get_reporting_ldap_dynamic_servers)

GET[/reporting/ldap/dynamic-servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-dynamic-server-status/get_reporting_ldap_dynamic_servers_name__NAME_)

DELETE[/reporting/ldap/dynamic-servers/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-ldap-dynamic-server-status/delete_reporting_ldap_dynamic_servers_name__NAME_)

#### [user-guest-base](https://sonicos-api.sonicwall.com/\#/user-guest-base)      User guest base settings API.

GET[/user/guest/base](https://sonicos-api.sonicwall.com/#/operations/user-guest-base/get_user_guest_base)

PUT[/user/guest/base](https://sonicos-api.sonicwall.com/#/operations/user-guest-base/put_user_guest_base)

#### [user-guest-profile](https://sonicos-api.sonicwall.com/\#/user-guest-profile)      Guest profile configuration API.

GET[/user/guest/profiles](https://sonicos-api.sonicwall.com/#/operations/user-guest-profile/get_user_guest_profiles)

POST[/user/guest/profiles](https://sonicos-api.sonicwall.com/#/operations/user-guest-profile/post_user_guest_profiles)

PUT[/user/guest/profiles](https://sonicos-api.sonicwall.com/#/operations/user-guest-profile/put_user_guest_profiles)

GET[/user/guest/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-profile/get_user_guest_profiles_name__NAME_)

PUT[/user/guest/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-profile/put_user_guest_profiles_name__NAME_)

DELETE[/user/guest/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-profile/delete_user_guest_profiles_name__NAME_)

#### [user-guest-user](https://sonicos-api.sonicwall.com/\#/user-guest-user)      Guest user configuration API.

GET[/user/guest/users](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/get_user_guest_users)

POST[/user/guest/users](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/post_user_guest_users)

PUT[/user/guest/users](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/put_user_guest_users)

GET[/user/guest/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/get_user_guest_users_uuid__UUID_)

PUT[/user/guest/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/put_user_guest_users_uuid__UUID_)

DELETE[/user/guest/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/delete_user_guest_users_uuid__UUID_)

GET[/user/guest/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/get_user_guest_users_name__NAME_)

PUT[/user/guest/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/put_user_guest_users_name__NAME_)

DELETE[/user/guest/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-user/delete_user_guest_users_name__NAME_)

#### [user-logout-guest](https://sonicos-api.sonicwall.com/\#/user-logout-guest)      User logout all guest management API.

DELETE[/user/logout/guests](https://sonicos-api.sonicwall.com/#/operations/user-logout-guest/delete_user_logout_guests)

DELETE[/user/logout/guests/at/{IP}](https://sonicos-api.sonicwall.com/#/operations/user-logout-guest/delete_user_logout_guests_at__IP_)

#### [user-guest-statistic](https://sonicos-api.sonicwall.com/\#/user-guest-statistic)      User guest statistic reporting API.

GET[/reporting/user/guest/statistic/ip/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/user-guest-statistic/get_reporting_user_guest_statistic_ip__USERIP_)

DELETE[/reporting/user/guest/statistic/ip/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/user-guest-statistic/delete_reporting_user_guest_statistic_ip__USERIP_)

#### [user-guest-statistic-by-name](https://sonicos-api.sonicwall.com/\#/user-guest-statistic-by-name)      User guest statistic reporting API.

GET[/reporting/user/guest/statistics](https://sonicos-api.sonicwall.com/#/operations/user-guest-statistic-by-name/get_reporting_user_guest_statistics)

GET[/reporting/user/guest/statistics/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-statistic-by-name/get_reporting_user_guest_statistics_name__NAME_)

#### [user-guest-status](https://sonicos-api.sonicwall.com/\#/user-guest-status)      User guest status reporting API.

GET[/reporting/user/guest/status](https://sonicos-api.sonicwall.com/#/operations/user-guest-status/get_reporting_user_guest_status)

GET[/reporting/user/guest/status/ip/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/user-guest-status/get_reporting_user_guest_status_ip__USERIP_)

#### [user-guest-detail](https://sonicos-api.sonicwall.com/\#/user-guest-detail)      User guest status reporting API.

GET[/reporting/user/guest/detail](https://sonicos-api.sonicwall.com/#/operations/user-guest-detail/get_reporting_user_guest_detail)

GET[/reporting/user/guest/detail/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-guest-detail/get_reporting_user_guest_detail_name__NAME_)

#### [user-guest-generate](https://sonicos-api.sonicwall.com/\#/user-guest-generate)      User guest users generate API.

POST[/user/guest/generate](https://sonicos-api.sonicwall.com/#/operations/user-guest-generate/post_user_guest_generate)

#### [export-user-guest](https://sonicos-api.sonicwall.com/\#/export-user-guest)      Export guest accounts configurations.

GET[/export/user/guest-accounts](https://sonicos-api.sonicwall.com/#/operations/export-user-guest/get_export_user_guest_accounts)

#### [user-local-base](https://sonicos-api.sonicwall.com/\#/user-local-base)      User local base settings API.

GET[/user/local/base](https://sonicos-api.sonicwall.com/#/operations/user-local-base/get_user_local_base)

PUT[/user/local/base](https://sonicos-api.sonicwall.com/#/operations/user-local-base/put_user_local_base)

#### [user-local-group](https://sonicos-api.sonicwall.com/\#/user-local-group)      User local configuration API.

GET[/user/local/groups](https://sonicos-api.sonicwall.com/#/operations/user-local-group/get_user_local_groups)

POST[/user/local/groups](https://sonicos-api.sonicwall.com/#/operations/user-local-group/post_user_local_groups)

PUT[/user/local/groups](https://sonicos-api.sonicwall.com/#/operations/user-local-group/put_user_local_groups)

PATCH[/user/local/groups](https://sonicos-api.sonicwall.com/#/operations/user-local-group/patch_user_local_groups)

GET[/user/local/groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/get_user_local_groups_uuid__UUID_)

PUT[/user/local/groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/put_user_local_groups_uuid__UUID_)

PATCH[/user/local/groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/patch_user_local_groups_uuid__UUID_)

DELETE[/user/local/groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/delete_user_local_groups_uuid__UUID_)

GET[/user/local/groups/name/{NAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/get_user_local_groups_name__NAME__domain__DNAME_)

PUT[/user/local/groups/name/{NAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/put_user_local_groups_name__NAME__domain__DNAME_)

PATCH[/user/local/groups/name/{NAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/patch_user_local_groups_name__NAME__domain__DNAME_)

DELETE[/user/local/groups/name/{NAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-group/delete_user_local_groups_name__NAME__domain__DNAME_)

#### [user-local-user](https://sonicos-api.sonicwall.com/\#/user-local-user)      User local configuration API.

GET[/user/local/users](https://sonicos-api.sonicwall.com/#/operations/user-local-user/get_user_local_users)

POST[/user/local/users](https://sonicos-api.sonicwall.com/#/operations/user-local-user/post_user_local_users)

PUT[/user/local/users](https://sonicos-api.sonicwall.com/#/operations/user-local-user/put_user_local_users)

PATCH[/user/local/users](https://sonicos-api.sonicwall.com/#/operations/user-local-user/patch_user_local_users)

GET[/user/local/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/get_user_local_users_uuid__UUID_)

PUT[/user/local/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/put_user_local_users_uuid__UUID_)

PATCH[/user/local/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/patch_user_local_users_uuid__UUID_)

DELETE[/user/local/users/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/delete_user_local_users_uuid__UUID_)

GET[/user/local/users/name/{UNAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/get_user_local_users_name__UNAME__domain__DNAME_)

PUT[/user/local/users/name/{UNAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/put_user_local_users_name__UNAME__domain__DNAME_)

PATCH[/user/local/users/name/{UNAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/patch_user_local_users_name__UNAME__domain__DNAME_)

DELETE[/user/local/users/name/{UNAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-user/delete_user_local_users_name__UNAME__domain__DNAME_)

#### [user-local-users-quota](https://sonicos-api.sonicwall.com/\#/user-local-users-quota)      Local users quota status API.

GET[/reporting/local/user/quota/users](https://sonicos-api.sonicwall.com/#/operations/user-local-users-quota/get_reporting_local_user_quota_users)

GET[/reporting/local/user/quota/users/name/{NAME}/domain/{DNAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-users-quota/get_reporting_local_user_quota_users_name__NAME__domain__DNAME_)

#### [user-local-unbind-totp-key](https://sonicos-api.sonicwall.com/\#/user-local-unbind-totp-key)      User unbind totp key API.

POST[/user/local/unbind-totp-key/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-local-unbind-totp-key/post_user_local_unbind_totp_key__NAME_)

POST[/user/local/unbind-totp-key/{NAME}/domain/{DOMAIN}](https://sonicos-api.sonicwall.com/#/operations/user-local-unbind-totp-key/post_user_local_unbind_totp_key__NAME__domain__DOMAIN_)

#### [user-sso-base](https://sonicos-api.sonicwall.com/\#/user-sso-base)      User SSO base settings API.

GET[/user/sso/base](https://sonicos-api.sonicwall.com/#/operations/user-sso-base/get_user_sso_base)

PUT[/user/sso/base](https://sonicos-api.sonicwall.com/#/operations/user-sso-base/put_user_sso_base)

#### [user-sso-agent](https://sonicos-api.sonicwall.com/\#/user-sso-agent)      User SSO agent API.

GET[/user/sso/agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/get_user_sso_agents)

POST[/user/sso/agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/post_user_sso_agents)

PUT[/user/sso/agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/put_user_sso_agents)

PATCH[/user/sso/agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/patch_user_sso_agents)

GET[/user/sso/agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/get_user_sso_agents_name__NAME_)

PUT[/user/sso/agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/put_user_sso_agents_name__NAME_)

PATCH[/user/sso/agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/patch_user_sso_agents_name__NAME_)

DELETE[/user/sso/agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent/delete_user_sso_agents_name__NAME_)

#### [user-sso-terminal-services-agent](https://sonicos-api.sonicwall.com/\#/user-sso-terminal-services-agent)      User SSO terminal services agent API.

GET[/user/sso/terminal-services-agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/get_user_sso_terminal_services_agents)

POST[/user/sso/terminal-services-agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/post_user_sso_terminal_services_agents)

PUT[/user/sso/terminal-services-agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/put_user_sso_terminal_services_agents)

PATCH[/user/sso/terminal-services-agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/patch_user_sso_terminal_services_agents)

GET[/user/sso/terminal-services-agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/get_user_sso_terminal_services_agents_name__NAME_)

PUT[/user/sso/terminal-services-agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/put_user_sso_terminal_services_agents_name__NAME_)

PATCH[/user/sso/terminal-services-agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/patch_user_sso_terminal_services_agents_name__NAME_)

DELETE[/user/sso/terminal-services-agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-services-agent/delete_user_sso_terminal_services_agents_name__NAME_)

#### [user-sso-radius-accounting-client](https://sonicos-api.sonicwall.com/\#/user-sso-radius-accounting-client)      User SSO RADIUS accounting client configuration API.

GET[/user/sso/radius-accounting-clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/get_user_sso_radius_accounting_clients)

POST[/user/sso/radius-accounting-clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/post_user_sso_radius_accounting_clients)

PUT[/user/sso/radius-accounting-clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/put_user_sso_radius_accounting_clients)

PATCH[/user/sso/radius-accounting-clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/patch_user_sso_radius_accounting_clients)

GET[/user/sso/radius-accounting-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/get_user_sso_radius_accounting_clients_name__NAME_)

PUT[/user/sso/radius-accounting-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/put_user_sso_radius_accounting_clients_name__NAME_)

PATCH[/user/sso/radius-accounting-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/patch_user_sso_radius_accounting_clients_name__NAME_)

DELETE[/user/sso/radius-accounting-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client/delete_user_sso_radius_accounting_clients_name__NAME_)

#### [user-sso-radius-user-name-exclusion](https://sonicos-api.sonicwall.com/\#/user-sso-radius-user-name-exclusion)      User SSO RADIUS user name exclusion API.

GET[/user/sso/radius-user-name-exclusions](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/get_user_sso_radius_user_name_exclusions)

POST[/user/sso/radius-user-name-exclusions](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/post_user_sso_radius_user_name_exclusions)

PUT[/user/sso/radius-user-name-exclusions](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/put_user_sso_radius_user_name_exclusions)

PATCH[/user/sso/radius-user-name-exclusions](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/patch_user_sso_radius_user_name_exclusions)

GET[/user/sso/radius-user-name-exclusions/name/{NAME}/type/{TYPE}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/get_user_sso_radius_user_name_exclusions_name__NAME__type__TYPE_)

PUT[/user/sso/radius-user-name-exclusions/name/{NAME}/type/{TYPE}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/put_user_sso_radius_user_name_exclusions_name__NAME__type__TYPE_)

PATCH[/user/sso/radius-user-name-exclusions/name/{NAME}/type/{TYPE}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/patch_user_sso_radius_user_name_exclusions_name__NAME__type__TYPE_)

DELETE[/user/sso/radius-user-name-exclusions/name/{NAME}/type/{TYPE}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-user-name-exclusion/delete_user_sso_radius_user_name_exclusions_name__NAME__type__TYPE_)

#### [user-sso-enforce-on-zone](https://sonicos-api.sonicwall.com/\#/user-sso-enforce-on-zone)      User SSO enforce on zone API.

GET[/user/sso/enforce-on-zones](https://sonicos-api.sonicwall.com/#/operations/user-sso-enforce-on-zone/get_user_sso_enforce_on_zones)

POST[/user/sso/enforce-on-zones](https://sonicos-api.sonicwall.com/#/operations/user-sso-enforce-on-zone/post_user_sso_enforce_on_zones)

PUT[/user/sso/enforce-on-zones](https://sonicos-api.sonicwall.com/#/operations/user-sso-enforce-on-zone/put_user_sso_enforce_on_zones)

GET[/user/sso/enforce-on-zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-enforce-on-zone/get_user_sso_enforce_on_zones_name__NAME_)

PUT[/user/sso/enforce-on-zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-enforce-on-zone/put_user_sso_enforce_on_zones_name__NAME_)

DELETE[/user/sso/enforce-on-zones/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-enforce-on-zone/delete_user_sso_enforce_on_zones_name__NAME_)

#### [user-sso-windows-service-user-name](https://sonicos-api.sonicwall.com/\#/user-sso-windows-service-user-name)      User SSO enforce on zone API.

GET[/user/sso/windows-service-user-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/get_user_sso_windows_service_user_names)

POST[/user/sso/windows-service-user-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/post_user_sso_windows_service_user_names)

PUT[/user/sso/windows-service-user-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/put_user_sso_windows_service_user_names)

PATCH[/user/sso/windows-service-user-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/patch_user_sso_windows_service_user_names)

GET[/user/sso/windows-service-user-names/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/get_user_sso_windows_service_user_names_name__NAME_)

PUT[/user/sso/windows-service-user-names/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/put_user_sso_windows_service_user_names_name__NAME_)

PATCH[/user/sso/windows-service-user-names/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/patch_user_sso_windows_service_user_names_name__NAME_)

DELETE[/user/sso/windows-service-user-names/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-windows-service-user-name/delete_user_sso_windows_service_user_names_name__NAME_)

#### [user-sso-security-service-bypass](https://sonicos-api.sonicwall.com/\#/user-sso-security-service-bypass)      User SSO security service bypass API.

GET[/user/sso/security-services-bypass](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/get_user_sso_security_services_bypass)

POST[/user/sso/security-services-bypass](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/post_user_sso_security_services_bypass)

PUT[/user/sso/security-services-bypass](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/put_user_sso_security_services_bypass)

GET[/user/sso/security-services-bypass/address/name/{ADDROBJNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/get_user_sso_security_services_bypass_address_name__ADDROBJNAME_)

PUT[/user/sso/security-services-bypass/address/name/{ADDROBJNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/put_user_sso_security_services_bypass_address_name__ADDROBJNAME_)

DELETE[/user/sso/security-services-bypass/address/name/{ADDROBJNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/delete_user_sso_security_services_bypass_address_name__ADDROBJNAME_)

GET[/user/sso/security-services-bypass/service/built-in/{BLTNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/get_user_sso_security_services_bypass_service_built_in__BLTNAME_)

PUT[/user/sso/security-services-bypass/service/built-in/{BLTNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/put_user_sso_security_services_bypass_service_built_in__BLTNAME_)

DELETE[/user/sso/security-services-bypass/service/built-in/{BLTNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/delete_user_sso_security_services_bypass_service_built_in__BLTNAME_)

GET[/user/sso/security-services-bypass/service/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/get_user_sso_security_services_bypass_service_group__GRPNAME_)

PUT[/user/sso/security-services-bypass/service/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/put_user_sso_security_services_bypass_service_group__GRPNAME_)

DELETE[/user/sso/security-services-bypass/service/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/delete_user_sso_security_services_bypass_service_group__GRPNAME_)

GET[/user/sso/security-services-bypass/address/group/{ADDRGRPNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/get_user_sso_security_services_bypass_address_group__ADDRGRPNAME_)

PUT[/user/sso/security-services-bypass/address/group/{ADDRGRPNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/put_user_sso_security_services_bypass_address_group__ADDRGRPNAME_)

DELETE[/user/sso/security-services-bypass/address/group/{ADDRGRPNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/delete_user_sso_security_services_bypass_address_group__ADDRGRPNAME_)

GET[/user/sso/security-services-bypass/service/name/{OBJNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/get_user_sso_security_services_bypass_service_name__OBJNAME_)

PUT[/user/sso/security-services-bypass/service/name/{OBJNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/put_user_sso_security_services_bypass_service_name__OBJNAME_)

DELETE[/user/sso/security-services-bypass/service/name/{OBJNAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-security-service-bypass/delete_user_sso_security_services_bypass_service_name__OBJNAME_)

#### [user-sso-global-statistic](https://sonicos-api.sonicwall.com/\#/user-sso-global-statistic)      User SSO reporting API.

GET[/reporting/sso-statistic/global](https://sonicos-api.sonicwall.com/#/operations/user-sso-global-statistic/get_reporting_sso_statistic_global)

DELETE[/reporting/sso-statistic/global](https://sonicos-api.sonicwall.com/#/operations/user-sso-global-statistic/delete_reporting_sso_statistic_global)

#### [user-sso-agent-statistic](https://sonicos-api.sonicwall.com/\#/user-sso-agent-statistic)      User SSO agent reporting API.

GET[/reporting/sso-statistic/agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent-statistic/get_reporting_sso_statistic_agents)

GET[/reporting/sso-statistic/agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent-statistic/get_reporting_sso_statistic_agents_name__NAME_)

DELETE[/reporting/sso-statistic/agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-agent-statistic/delete_reporting_sso_statistic_agents_name__NAME_)

#### [user-sso-terminal-service-agent-statistic](https://sonicos-api.sonicwall.com/\#/user-sso-terminal-service-agent-statistic)      User SSO agent reporting API.

GET[/reporting/sso-statistic/terminal-services-agents](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-service-agent-statistic/get_reporting_sso_statistic_terminal_services_agents)

GET[/reporting/sso-statistic/terminal-services-agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-service-agent-statistic/get_reporting_sso_statistic_terminal_services_agents_name__NAME_)

DELETE[/reporting/sso-statistic/terminal-services-agents/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-terminal-service-agent-statistic/delete_reporting_sso_statistic_terminal_services_agents_name__NAME_)

#### [user-sso-radius-accounting-client-statistic](https://sonicos-api.sonicwall.com/\#/user-sso-radius-accounting-client-statistic)      User SSO radius accounting client reporting API.

GET[/reporting/sso-statistic/radius-accounting-clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client-statistic/get_reporting_sso_statistic_radius_accounting_clients)

GET[/reporting/sso-statistic/radius-accounting-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client-statistic/get_reporting_sso_statistic_radius_accounting_clients_name__NAME_)

DELETE[/reporting/sso-statistic/radius-accounting-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-radius-accounting-client-statistic/delete_reporting_sso_statistic_radius_accounting_clients_name__NAME_)

#### [user-sso-3rd-party-api-client-statistic](https://sonicos-api.sonicwall.com/\#/user-sso-3rd-party-api-client-statistic)      User SSO third party api client reporting API.

GET[/reporting/sso-statistic/third-party-api-clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client-statistic/get_reporting_sso_statistic_third_party_api_clients)

GET[/reporting/sso-statistic/third-party-api-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client-statistic/get_reporting_sso_statistic_third_party_api_clients_name__NAME_)

DELETE[/reporting/sso-statistic/third-party-api-clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client-statistic/delete_reporting_sso_statistic_third_party_api_clients_name__NAME_)

#### [user-sso-status](https://sonicos-api.sonicwall.com/\#/user-sso-status)      User SSO status reporting API.

GET[/reporting/sso-status](https://sonicos-api.sonicwall.com/#/operations/user-sso-status/get_reporting_sso_status)

#### [user-sso-test](https://sonicos-api.sonicwall.com/\#/user-sso-test)      Test SSO agents API.

POST[/user/sso/test](https://sonicos-api.sonicwall.com/#/operations/user-sso-test/post_user_sso_test)

#### [user-sso-3rd-party-api-base](https://sonicos-api.sonicwall.com/\#/user-sso-3rd-party-api-base)      User SSO 3rd party api base setting API.

GET[/user/sso/third-party-api/base](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-base/get_user_sso_third_party_api_base)

PUT[/user/sso/third-party-api/base](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-base/put_user_sso_third_party_api_base)

#### [user-sso-3rd-party-api-client](https://sonicos-api.sonicwall.com/\#/user-sso-3rd-party-api-client)      User SSO 3rd party api client setting API.

GET[/user/sso/third-party-api/clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/get_user_sso_third_party_api_clients)

POST[/user/sso/third-party-api/clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/post_user_sso_third_party_api_clients)

PUT[/user/sso/third-party-api/clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/put_user_sso_third_party_api_clients)

PATCH[/user/sso/third-party-api/clients](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/patch_user_sso_third_party_api_clients)

GET[/user/sso/third-party-api/clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/get_user_sso_third_party_api_clients_name__NAME_)

PUT[/user/sso/third-party-api/clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/put_user_sso_third_party_api_clients_name__NAME_)

PATCH[/user/sso/third-party-api/clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/patch_user_sso_third_party_api_clients_name__NAME_)

DELETE[/user/sso/third-party-api/clients/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/user-sso-3rd-party-api-client/delete_user_sso_third_party_api_clients_name__NAME_)

#### [user-sso-capture-client-base](https://sonicos-api.sonicwall.com/\#/user-sso-capture-client-base)      User SSO capture client base setting API.

GET[/user/sso/capture-client/base](https://sonicos-api.sonicwall.com/#/operations/user-sso-capture-client-base/get_user_sso_capture_client_base)

PUT[/user/sso/capture-client/base](https://sonicos-api.sonicwall.com/#/operations/user-sso-capture-client-base/put_user_sso_capture_client_base)

#### [user-sso-consistent-domain-name](https://sonicos-api.sonicwall.com/\#/user-sso-consistent-domain-name)      User SSO Consistent domain name setting API.

GET[/user/sso/consistent-domain-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/get_user_sso_consistent_domain_names)

POST[/user/sso/consistent-domain-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/post_user_sso_consistent_domain_names)

PUT[/user/sso/consistent-domain-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/put_user_sso_consistent_domain_names)

PATCH[/user/sso/consistent-domain-names](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/patch_user_sso_consistent_domain_names)

GET[/user/sso/consistent-domain-names/dn/{DN}](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/get_user_sso_consistent_domain_names_dn__DN_)

PUT[/user/sso/consistent-domain-names/dn/{DN}](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/put_user_sso_consistent_domain_names_dn__DN_)

PATCH[/user/sso/consistent-domain-names/dn/{DN}](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/patch_user_sso_consistent_domain_names_dn__DN_)

DELETE[/user/sso/consistent-domain-names/dn/{DN}](https://sonicos-api.sonicwall.com/#/operations/user-sso-consistent-domain-name/delete_user_sso_consistent_domain_names_dn__DN_)

#### [user-partitioning-base](https://sonicos-api.sonicwall.com/\#/user-partitioning-base)      User partitioning base configuration API.

GET[/user/partitioning/base](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-base/get_user_partitioning_base)

PUT[/user/partitioning/base](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-base/put_user_partitioning_base)

#### [user-partitioning-partitions](https://sonicos-api.sonicwall.com/\#/user-partitioning-partitions)      User authentication partitions configuration API.

GET[/user/partitioning/partitions](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/get_user_partitioning_partitions)

POST[/user/partitioning/partitions](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/post_user_partitioning_partitions)

PUT[/user/partitioning/partitions](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/put_user_partitioning_partitions)

PATCH[/user/partitioning/partitions](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/patch_user_partitioning_partitions)

GET[/user/partitioning/partitions/name/{PNAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/get_user_partitioning_partitions_name__PNAME_)

PUT[/user/partitioning/partitions/name/{PNAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/put_user_partitioning_partitions_name__PNAME_)

PATCH[/user/partitioning/partitions/name/{PNAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/patch_user_partitioning_partitions_name__PNAME_)

DELETE[/user/partitioning/partitions/name/{PNAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-partitions/delete_user_partitioning_partitions_name__PNAME_)

#### [user-partitioning-policies](https://sonicos-api.sonicwall.com/\#/user-partitioning-policies)      User partition selection policies configuration API.

GET[/user/partitioning/policies](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/get_user_partitioning_policies)

POST[/user/partitioning/policies](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/post_user_partitioning_policies)

PUT[/user/partitioning/policies](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/put_user_partitioning_policies)

PATCH[/user/partitioning/policies](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/patch_user_partitioning_policies)

GET[/user/partitioning/policies/interface/{IF}/zone/{ZONENAME}/address-object/{AONAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/get_user_partitioning_policies_interface__IF__zone__ZONENAME__address_object__AONAME_)

PUT[/user/partitioning/policies/interface/{IF}/zone/{ZONENAME}/address-object/{AONAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/put_user_partitioning_policies_interface__IF__zone__ZONENAME__address_object__AONAME_)

PATCH[/user/partitioning/policies/interface/{IF}/zone/{ZONENAME}/address-object/{AONAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/patch_user_partitioning_policies_interface__IF__zone__ZONENAME__address_object__AONAME_)

DELETE[/user/partitioning/policies/interface/{IF}/zone/{ZONENAME}/address-object/{AONAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-policies/delete_user_partitioning_policies_interface__IF__zone__ZONENAME__address_object__AONAME_)

#### [user-partitioning-auto-assign](https://sonicos-api.sonicwall.com/\#/user-partitioning-auto-assign)      User authentication auto assign partition configuration API.

POST[/user/partitioning/auto-assign/partitions](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-auto-assign/post_user_partitioning_auto_assign_partitions)

POST[/user/partitioning/auto-assign/partitions/name/{PNAME}](https://sonicos-api.sonicwall.com/#/operations/user-partitioning-auto-assign/post_user_partitioning_auto_assign_partitions_name__PNAME_)

#### [user-auth-base](https://sonicos-api.sonicwall.com/\#/user-auth-base)      User authentication base settings API.

GET[/user/authentication/base](https://sonicos-api.sonicwall.com/#/operations/user-auth-base/get_user_authentication_base)

PUT[/user/authentication/base](https://sonicos-api.sonicwall.com/#/operations/user-auth-base/put_user_authentication_base)

#### [user-auth-methods](https://sonicos-api.sonicwall.com/\#/user-auth-methods)      User authentication method and single sign on method API.

GET[/user/authentication/methods](https://sonicos-api.sonicwall.com/#/operations/user-auth-methods/get_user_authentication_methods)

PUT[/user/authentication/methods](https://sonicos-api.sonicwall.com/#/operations/user-auth-methods/put_user_authentication_methods)

#### [user-auth-bypass](https://sonicos-api.sonicwall.com/\#/user-auth-bypass)      User authentication bypass url API.

GET[/user/authentication/rule-auth-bypass-http-urls](https://sonicos-api.sonicwall.com/#/operations/user-auth-bypass/get_user_authentication_rule_auth_bypass_http_urls)

POST[/user/authentication/rule-auth-bypass-http-urls](https://sonicos-api.sonicwall.com/#/operations/user-auth-bypass/post_user_authentication_rule_auth_bypass_http_urls)

#### [user-authentication-bypass-track-traffic](https://sonicos-api.sonicwall.com/\#/user-authentication-bypass-track-traffic)      User authentication bypass track traffic API.

POST[/user/authentication/bypass/track-traffic/{SOURCEIP}](https://sonicos-api.sonicwall.com/#/operations/user-authentication-bypass-track-traffic/post_user_authentication_bypass_track_traffic__SOURCEIP_)

#### [interface-ipv4](https://sonicos-api.sonicwall.com/\#/interface-ipv4)      Interface IPv4 configuration API.

GET[/interfaces/ipv4](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/get_interfaces_ipv4)

POST[/interfaces/ipv4](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/post_interfaces_ipv4)

PUT[/interfaces/ipv4](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/put_interfaces_ipv4)

PATCH[/interfaces/ipv4](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/patch_interfaces_ipv4)

GET[/interfaces/ipv4/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/get_interfaces_ipv4_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

PUT[/interfaces/ipv4/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/put_interfaces_ipv4_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

PATCH[/interfaces/ipv4/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/patch_interfaces_ipv4_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

DELETE[/interfaces/ipv4/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4/delete_interfaces_ipv4_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

#### [interface-vlan-ipv4](https://sonicos-api.sonicwall.com/\#/interface-vlan-ipv4)      Interfaces IPv4 vlan configuration API.

GET[/interfaces/vlan/ipv4](https://sonicos-api.sonicwall.com/#/operations/interface-vlan-ipv4/get_interfaces_vlan_ipv4)

GET[/interfaces/vlan/ipv4/parent/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/interface-vlan-ipv4/get_interfaces_vlan_ipv4_parent__IFNAME_)

#### [interfaces-display-traffic](https://sonicos-api.sonicwall.com/\#/interfaces-display-traffic)      Interfaces display all traffic configuration API.

GET[/interfaces/display-all-traffic](https://sonicos-api.sonicwall.com/#/operations/interfaces-display-traffic/get_interfaces_display_all_traffic)

PUT[/interfaces/display-all-traffic](https://sonicos-api.sonicwall.com/#/operations/interfaces-display-traffic/put_interfaces_display_all_traffic)

#### [tunnel-interface-4to6](https://sonicos-api.sonicwall.com/\#/tunnel-interface-4to6)      4to6 tunnel interface configuration API.

GET[/tunnel-interfaces/4to6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/get_tunnel_interfaces_4to6)

POST[/tunnel-interfaces/4to6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/post_tunnel_interfaces_4to6)

PUT[/tunnel-interfaces/4to6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/put_tunnel_interfaces_4to6)

PATCH[/tunnel-interfaces/4to6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/patch_tunnel_interfaces_4to6)

GET[/tunnel-interfaces/4to6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/get_tunnel_interfaces_4to6_name__TUNNELNAME_)

PUT[/tunnel-interfaces/4to6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/put_tunnel_interfaces_4to6_name__TUNNELNAME_)

PATCH[/tunnel-interfaces/4to6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/patch_tunnel_interfaces_4to6_name__TUNNELNAME_)

DELETE[/tunnel-interfaces/4to6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6/delete_tunnel_interfaces_4to6_name__TUNNELNAME_)

#### [tunnel-interface-4to6-mtu](https://sonicos-api.sonicwall.com/\#/tunnel-interface-4to6-mtu)      MAC interfaces reporting API.

GET[/reporting/tunnel-interfaces/4to6/status](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6-mtu/get_reporting_tunnel_interfaces_4to6_status)

GET[/reporting/tunnel-interfaces/4to6/status/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-4to6-mtu/get_reporting_tunnel_interfaces_4to6_status_name__NAME_)

#### [tunnel-interface-vpn](https://sonicos-api.sonicwall.com/\#/tunnel-interface-vpn)      VPN tunnel interface configuration API.

GET[/tunnel-interfaces/vpn](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/get_tunnel_interfaces_vpn)

POST[/tunnel-interfaces/vpn](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/post_tunnel_interfaces_vpn)

PUT[/tunnel-interfaces/vpn](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/put_tunnel_interfaces_vpn)

PATCH[/tunnel-interfaces/vpn](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/patch_tunnel_interfaces_vpn)

GET[/tunnel-interfaces/vpn/name/{VPNTUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/get_tunnel_interfaces_vpn_name__VPNTUNNELNAME_)

PUT[/tunnel-interfaces/vpn/name/{VPNTUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/put_tunnel_interfaces_vpn_name__VPNTUNNELNAME_)

PATCH[/tunnel-interfaces/vpn/name/{VPNTUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/patch_tunnel_interfaces_vpn_name__VPNTUNNELNAME_)

DELETE[/tunnel-interfaces/vpn/name/{VPNTUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn/delete_tunnel_interfaces_vpn_name__VPNTUNNELNAME_)

#### [tunnel-interface-vpn-status](https://sonicos-api.sonicwall.com/\#/tunnel-interface-vpn-status)      VPN tunnel interface reporting API.

GET[/reporting/tunnel-interfaces/vpn/status](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn-status/get_reporting_tunnel_interfaces_vpn_status)

GET[/reporting/tunnel-interfaces/vpn/status/name/{VPNTUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-vpn-status/get_reporting_tunnel_interfaces_vpn_status_name__VPNTUNNELNAME_)

#### [interface-statistics](https://sonicos-api.sonicwall.com/\#/interface-statistics)      Clear interfaces statistics API.

DELETE[/interfaces/statistics](https://sonicos-api.sonicwall.com/#/operations/interface-statistics/delete_interfaces_statistics)

#### [interface-ipv4-statistics](https://sonicos-api.sonicwall.com/\#/interface-ipv4-statistics)      IPv4 interfaces reporting API.

GET[/reporting/interfaces/ipv4/statistics/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4-statistics/get_reporting_interfaces_ipv4_statistics_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

DELETE[/reporting/interfaces/ipv4/statistics/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4-statistics/delete_reporting_interfaces_ipv4_statistics_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

GET[/reporting/interfaces/ipv4/statistics](https://sonicos-api.sonicwall.com/#/operations/interface-ipv4-statistics/get_reporting_interfaces_ipv4_statistics)

#### [interface-ipv6-statistics](https://sonicos-api.sonicwall.com/\#/interface-ipv6-statistics)      IPv6 interfaces reporting API.

GET[/reporting/interfaces/ipv6/statistics/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-statistics/get_reporting_interfaces_ipv6_statistics_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

DELETE[/reporting/interfaces/ipv6/statistics/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-statistics/delete_reporting_interfaces_ipv6_statistics_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

GET[/reporting/interfaces/ipv6/statistics](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-statistics/get_reporting_interfaces_ipv6_statistics)

#### [interface-status-ipv4](https://sonicos-api.sonicwall.com/\#/interface-status-ipv4)      IP interfaces reporting API.

GET[/reporting/interfaces/ipv4/status/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-status-ipv4/get_reporting_interfaces_ipv4_status_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

GET[/reporting/interfaces/ipv4/status](https://sonicos-api.sonicwall.com/#/operations/interface-status-ipv4/get_reporting_interfaces_ipv4_status)

#### [interface-ip-ipv4](https://sonicos-api.sonicwall.com/\#/interface-ip-ipv4)      IP interfaces reporting API.

GET[/reporting/interfaces/ipv4/ip/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ip-ipv4/get_reporting_interfaces_ipv4_ip_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

GET[/reporting/interfaces/ipv4/ip](https://sonicos-api.sonicwall.com/#/operations/interface-ip-ipv4/get_reporting_interfaces_ipv4_ip)

#### [interface-status-ipv6](https://sonicos-api.sonicwall.com/\#/interface-status-ipv6)      Interfaces status reporting API.

GET[/reporting/interfaces/ipv6/status/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-status-ipv6/get_reporting_interfaces_ipv6_status_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

GET[/reporting/interfaces/ipv6/status](https://sonicos-api.sonicwall.com/#/operations/interface-status-ipv6/get_reporting_interfaces_ipv6_status)

#### [interface-ip-ipv6](https://sonicos-api.sonicwall.com/\#/interface-ip-ipv6)      IP interfaces reporting API.

GET[/reporting/interfaces/ipv6/ip/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ip-ipv6/get_reporting_interfaces_ipv6_ip_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

GET[/reporting/interfaces/ipv6/ip](https://sonicos-api.sonicwall.com/#/operations/interface-ip-ipv6/get_reporting_interfaces_ipv6_ip)

#### [interface-mac](https://sonicos-api.sonicwall.com/\#/interface-mac)      MAC interfaces reporting API.

GET[/reporting/interfaces/mac](https://sonicos-api.sonicwall.com/#/operations/interface-mac/get_reporting_interfaces_mac)

GET[/reporting/interfaces/mac/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-mac/get_reporting_interfaces_mac_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

#### [interface-shutdown](https://sonicos-api.sonicwall.com/\#/interface-shutdown)      Interface shutdown API.

POST[/interface/shutdown/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/interface-shutdown/post_interface_shutdown__IFNAME_)

DELETE[/interface/shutdown/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/interface-shutdown/delete_interface_shutdown__IFNAME_)

#### [interface-renew-ipv4](https://sonicos-api.sonicwall.com/\#/interface-renew-ipv4)      Renew IPv4 Interface API.

POST[/renew/ipv4/name/{IPV4NAME}](https://sonicos-api.sonicwall.com/#/operations/interface-renew-ipv4/post_renew_ipv4_name__IPV4NAME_)

#### [interface-renew-ipv6](https://sonicos-api.sonicwall.com/\#/interface-renew-ipv6)      Renew IPv6 Interface API.

POST[/renew/ipv6/name/{IPV6NAME}](https://sonicos-api.sonicwall.com/#/operations/interface-renew-ipv6/post_renew_ipv6_name__IPV6NAME_)

#### [interface-release-ipv4](https://sonicos-api.sonicwall.com/\#/interface-release-ipv4)      Release Interface API.

POST[/release/ipv4/name/{IPV4NAME}](https://sonicos-api.sonicwall.com/#/operations/interface-release-ipv4/post_release_ipv4_name__IPV4NAME_)

#### [interface-release-ipv6](https://sonicos-api.sonicwall.com/\#/interface-release-ipv6)      Release Interface API.

POST[/release/ipv6/name/{IPV6NAME}](https://sonicos-api.sonicwall.com/#/operations/interface-release-ipv6/post_release_ipv6_name__IPV6NAME_)

#### [interface-connect](https://sonicos-api.sonicwall.com/\#/interface-connect)      Interface connect API.

POST[/connect/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/interface-connect/post_connect__IFNAME_)

#### [interface-disconnect](https://sonicos-api.sonicwall.com/\#/interface-disconnect)      Interface disconnect API.

POST[/disconnect/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/interface-disconnect/post_disconnect__IFNAME_)

#### [interface-ipv6-base](https://sonicos-api.sonicwall.com/\#/interface-ipv6-base)      Interface IPv6 configuration API.

GET[/interfaces/ipv6/base](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-base/get_interfaces_ipv6_base)

PUT[/interfaces/ipv6/base](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-base/put_interfaces_ipv6_base)

GET[/interfaces/ipv6/base/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-base/get_interfaces_ipv6_base_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

PUT[/interfaces/ipv6/base/name/{NAME}/vlan/{VLANID}/tunnel/{TUNNELID}](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-base/put_interfaces_ipv6_base_name__NAME__vlan__VLANID__tunnel__TUNNELID_)

#### [interface-ipv6-extra-ip](https://sonicos-api.sonicwall.com/\#/interface-ipv6-extra-ip)      Interface IPv6 extra IP configuration API.

GET[/interfaces/ipv6/extra-ip](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-extra-ip/get_interfaces_ipv6_extra_ip)

PUT[/interfaces/ipv6/extra-ip](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-extra-ip/put_interfaces_ipv6_extra_ip)

PATCH[/interfaces/ipv6/extra-ip](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-extra-ip/patch_interfaces_ipv6_extra_ip)

#### [interface-ipv6-prefixes](https://sonicos-api.sonicwall.com/\#/interface-ipv6-prefixes)      Interface IPv6 prefixes configuration API.

GET[/interfaces/ipv6/prefixes](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-prefixes/get_interfaces_ipv6_prefixes)

PUT[/interfaces/ipv6/prefixes](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-prefixes/put_interfaces_ipv6_prefixes)

PATCH[/interfaces/ipv6/prefixes](https://sonicos-api.sonicwall.com/#/operations/interface-ipv6-prefixes/patch_interfaces_ipv6_prefixes)

#### [tunnel-interface-ipv6](https://sonicos-api.sonicwall.com/\#/tunnel-interface-ipv6)      IPv6 tunnel interface configuration API.

GET[/tunnel-interfaces/ipv6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/get_tunnel_interfaces_ipv6)

POST[/tunnel-interfaces/ipv6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/post_tunnel_interfaces_ipv6)

PUT[/tunnel-interfaces/ipv6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/put_tunnel_interfaces_ipv6)

PATCH[/tunnel-interfaces/ipv6](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/patch_tunnel_interfaces_ipv6)

GET[/tunnel-interfaces/ipv6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/get_tunnel_interfaces_ipv6_name__TUNNELNAME_)

PUT[/tunnel-interfaces/ipv6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/put_tunnel_interfaces_ipv6_name__TUNNELNAME_)

PATCH[/tunnel-interfaces/ipv6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/patch_tunnel_interfaces_ipv6_name__TUNNELNAME_)

DELETE[/tunnel-interfaces/ipv6/name/{TUNNELNAME}](https://sonicos-api.sonicwall.com/#/operations/tunnel-interface-ipv6/delete_tunnel_interfaces_ipv6_name__TUNNELNAME_)

#### [bandwidth-object](https://sonicos-api.sonicwall.com/\#/bandwidth-object)      Bandwidth object configuration API.

GET[/bandwidth-objects](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/get_bandwidth_objects)

POST[/bandwidth-objects](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/post_bandwidth_objects)

PUT[/bandwidth-objects](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/put_bandwidth_objects)

PATCH[/bandwidth-objects](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/patch_bandwidth_objects)

GET[/bandwidth-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/get_bandwidth_objects_name__NAME_)

PUT[/bandwidth-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/put_bandwidth_objects_name__NAME_)

PATCH[/bandwidth-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/patch_bandwidth_objects_name__NAME_)

DELETE[/bandwidth-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/bandwidth-object/delete_bandwidth_objects_name__NAME_)

#### [dynamic-external-object](https://sonicos-api.sonicwall.com/\#/dynamic-external-object)      Dynamic external object configuration API.

GET[/dynamic-external-objects](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/get_dynamic_external_objects)

POST[/dynamic-external-objects](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/post_dynamic_external_objects)

PUT[/dynamic-external-objects](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/put_dynamic_external_objects)

PATCH[/dynamic-external-objects](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/patch_dynamic_external_objects)

GET[/dynamic-external-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/get_dynamic_external_objects_name__NAME_)

PUT[/dynamic-external-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/put_dynamic_external_objects_name__NAME_)

PATCH[/dynamic-external-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/patch_dynamic_external_objects_name__NAME_)

DELETE[/dynamic-external-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object/delete_dynamic_external_objects_name__NAME_)

#### [dynamic-external-object-statistics](https://sonicos-api.sonicwall.com/\#/dynamic-external-object-statistics)      Dynamic external object reporting API.

GET[/reporting/dynamic-external-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object-statistics/get_reporting_dynamic_external_objects_name__NAME_)

DELETE[/reporting/dynamic-external-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object-statistics/delete_reporting_dynamic_external_objects_name__NAME_)

#### [dynamic-external-object-download](https://sonicos-api.sonicwall.com/\#/dynamic-external-object-download)      Dynamic external object reporting API.

POST[/dynamic-external-object/download/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-external-object-download/post_dynamic_external_object_download_name__NAME_)

#### [email-object](https://sonicos-api.sonicwall.com/\#/email-object)      Email object configuration API.

GET[/email-objects](https://sonicos-api.sonicwall.com/#/operations/email-object/get_email_objects)

POST[/email-objects](https://sonicos-api.sonicwall.com/#/operations/email-object/post_email_objects)

PUT[/email-objects](https://sonicos-api.sonicwall.com/#/operations/email-object/put_email_objects)

PATCH[/email-objects](https://sonicos-api.sonicwall.com/#/operations/email-object/patch_email_objects)

GET[/email-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/email-object/get_email_objects_name__NAME_)

PUT[/email-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/email-object/put_email_objects_name__NAME_)

PATCH[/email-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/email-object/patch_email_objects_name__NAME_)

DELETE[/email-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/email-object/delete_email_objects_name__NAME_)

#### [email-object-status](https://sonicos-api.sonicwall.com/\#/email-object-status)      Email objects reporting API.

GET[/reporting/email-objects](https://sonicos-api.sonicwall.com/#/operations/email-object-status/get_reporting_email_objects)

#### [match-object](https://sonicos-api.sonicwall.com/\#/match-object)      Match object configuration API.

GET[/match-objects](https://sonicos-api.sonicwall.com/#/operations/match-object/get_match_objects)

POST[/match-objects](https://sonicos-api.sonicwall.com/#/operations/match-object/post_match_objects)

PUT[/match-objects](https://sonicos-api.sonicwall.com/#/operations/match-object/put_match_objects)

PATCH[/match-objects](https://sonicos-api.sonicwall.com/#/operations/match-object/patch_match_objects)

GET[/match-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/match-object/get_match_objects_name__NAME_)

PUT[/match-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/match-object/put_match_objects_name__NAME_)

PATCH[/match-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/match-object/patch_match_objects_name__NAME_)

DELETE[/match-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/match-object/delete_match_objects_name__NAME_)

#### [match-object-status](https://sonicos-api.sonicwall.com/\#/match-object-status)      Match objects reporting API.

GET[/reporting/match-objects](https://sonicos-api.sonicwall.com/#/operations/match-object-status/get_reporting_match_objects)

#### [action-object](https://sonicos-api.sonicwall.com/\#/action-object)      Action object configuration API.

GET[/action-objects](https://sonicos-api.sonicwall.com/#/operations/action-object/get_action_objects)

POST[/action-objects](https://sonicos-api.sonicwall.com/#/operations/action-object/post_action_objects)

PUT[/action-objects](https://sonicos-api.sonicwall.com/#/operations/action-object/put_action_objects)

PATCH[/action-objects](https://sonicos-api.sonicwall.com/#/operations/action-object/patch_action_objects)

GET[/action-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/action-object/get_action_objects_name__NAME_)

PUT[/action-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/action-object/put_action_objects_name__NAME_)

PATCH[/action-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/action-object/patch_action_objects_name__NAME_)

DELETE[/action-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/action-object/delete_action_objects_name__NAME_)

#### [action-object-default](https://sonicos-api.sonicwall.com/\#/action-object-default)      Default Action objects reporting API.

GET[/reporting/action-objects/default](https://sonicos-api.sonicwall.com/#/operations/action-object-default/get_reporting_action_objects_default)

#### [action-object-default-bandwidth-management](https://sonicos-api.sonicwall.com/\#/action-object-default-bandwidth-management)      Default bandwidth management Action objects reporting API.

GET[/reporting/action-objects/default-bandwidth-management](https://sonicos-api.sonicwall.com/#/operations/action-object-default-bandwidth-management/get_reporting_action_objects_default_bandwidth_management)

#### [action-object-status](https://sonicos-api.sonicwall.com/\#/action-object-status)      Action objects status reporting API.

GET[/reporting/action-objects/status](https://sonicos-api.sonicwall.com/#/operations/action-object-status/get_reporting_action_objects_status)

#### [action-object-bwm-usage](https://sonicos-api.sonicwall.com/\#/action-object-bwm-usage)      Action objects bandwidth management usage reporting API.

GET[/reporting/action-objects/bandwidth-usage](https://sonicos-api.sonicwall.com/#/operations/action-object-bwm-usage/get_reporting_action_objects_bandwidth_usage)

GET[/reporting/action-objects/bandwidth-usage/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/action-object-bwm-usage/get_reporting_action_objects_bandwidth_usage_name__NAME_)

#### [app-rule](https://sonicos-api.sonicwall.com/\#/app-rule)      App rules configuration API.

GET[/app-rules/base](https://sonicos-api.sonicwall.com/#/operations/app-rule/get_app_rules_base)

PUT[/app-rules/base](https://sonicos-api.sonicwall.com/#/operations/app-rule/put_app_rules_base)

#### [app-rule-policy](https://sonicos-api.sonicwall.com/\#/app-rule-policy)      App rules policy object configuration API.

GET[/app-rules/policies](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/get_app_rules_policies)

POST[/app-rules/policies](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/post_app_rules_policies)

PUT[/app-rules/policies](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/put_app_rules_policies)

PATCH[/app-rules/policies](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/patch_app_rules_policies)

GET[/app-rules/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/get_app_rules_policies_name__NAME_)

PUT[/app-rules/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/put_app_rules_policies_name__NAME_)

PATCH[/app-rules/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/patch_app_rules_policies_name__NAME_)

DELETE[/app-rules/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy/delete_app_rules_policies_name__NAME_)

#### [app-rule-policy-all](https://sonicos-api.sonicwall.com/\#/app-rule-policy-all)      Delete all app rules policy objects API.

DELETE[/app-rules/all-policies](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy-all/delete_app_rules_all_policies)

#### [app-rules](https://sonicos-api.sonicwall.com/\#/app-rules)      App rules reporting API.

GET[/reporting/app-rules](https://sonicos-api.sonicwall.com/#/operations/app-rules/get_reporting_app_rules)

#### [app-rule-policy-statistics](https://sonicos-api.sonicwall.com/\#/app-rule-policy-statistics)      App rules policy statistics reporting API.

GET[/reporting/app-rule/policy/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-rule-policy-statistics/get_reporting_app_rule_policy_name__NAME_)

#### [app-control](https://sonicos-api.sonicwall.com/\#/app-control)      App control configuration API.

GET[/app-control/base](https://sonicos-api.sonicwall.com/#/operations/app-control/get_app_control_base)

PUT[/app-control/base](https://sonicos-api.sonicwall.com/#/operations/app-control/put_app_control_base)

#### [app-control-category](https://sonicos-api.sonicwall.com/\#/app-control-category)      App control category object configuration API.

GET[/app-control/categories](https://sonicos-api.sonicwall.com/#/operations/app-control-category/get_app_control_categories)

POST[/app-control/categories](https://sonicos-api.sonicwall.com/#/operations/app-control-category/post_app_control_categories)

PUT[/app-control/categories](https://sonicos-api.sonicwall.com/#/operations/app-control-category/put_app_control_categories)

GET[/app-control/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-category/get_app_control_categories_name__NAME_)

PUT[/app-control/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-category/put_app_control_categories_name__NAME_)

GET[/app-control/categories/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/app-control-category/get_app_control_categories_id__ID_)

PUT[/app-control/categories/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/app-control-category/put_app_control_categories_id__ID_)

#### [app-control-application](https://sonicos-api.sonicwall.com/\#/app-control-application)      App control application object configuration API.

GET[/app-control/applications](https://sonicos-api.sonicwall.com/#/operations/app-control-application/get_app_control_applications)

POST[/app-control/applications](https://sonicos-api.sonicwall.com/#/operations/app-control-application/post_app_control_applications)

PUT[/app-control/applications](https://sonicos-api.sonicwall.com/#/operations/app-control-application/put_app_control_applications)

GET[/app-control/applications/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/app-control-application/get_app_control_applications_id__ID_)

PUT[/app-control/applications/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/app-control-application/put_app_control_applications_id__ID_)

GET[/app-control/applications/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-application/get_app_control_applications_name__NAME_)

PUT[/app-control/applications/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-application/put_app_control_applications_name__NAME_)

#### [app-control-signature](https://sonicos-api.sonicwall.com/\#/app-control-signature)      App control signature object configuration API.

GET[/app-control/signatures](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/get_app_control_signatures)

POST[/app-control/signatures](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/post_app_control_signatures)

PUT[/app-control/signatures](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/put_app_control_signatures)

GET[/app-control/signatures/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/get_app_control_signatures_name__NAME_)

PUT[/app-control/signatures/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/put_app_control_signatures_name__NAME_)

GET[/app-control/signatures/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/get_app_control_signatures_id__ID_)

PUT[/app-control/signatures/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/app-control-signature/put_app_control_signatures_id__ID_)

#### [app-control-exclusion-list](https://sonicos-api.sonicwall.com/\#/app-control-exclusion-list)      App control configuration API.

GET[/app-control/exclusion-list](https://sonicos-api.sonicwall.com/#/operations/app-control-exclusion-list/get_app_control_exclusion_list)

PUT[/app-control/exclusion-list](https://sonicos-api.sonicwall.com/#/operations/app-control-exclusion-list/put_app_control_exclusion_list)

#### [app-control-update-signatures](https://sonicos-api.sonicwall.com/\#/app-control-update-signatures)      App control update signatures action API.

POST[/app-control/update-signatures](https://sonicos-api.sonicwall.com/#/operations/app-control-update-signatures/post_app_control_update_signatures)

#### [app-control-reset](https://sonicos-api.sonicwall.com/\#/app-control-reset)      App control reset action API.

POST[/app-control/reset](https://sonicos-api.sonicwall.com/#/operations/app-control-reset/post_app_control_reset)

#### [app-control-status](https://sonicos-api.sonicwall.com/\#/app-control-status)      App control reporting API.

GET[/reporting/app-control](https://sonicos-api.sonicwall.com/#/operations/app-control-status/get_reporting_app_control)

#### [app-control-applications-list](https://sonicos-api.sonicwall.com/\#/app-control-applications-list)      App control applications list API.

GET[/app-control/applications-list/category/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-applications-list/get_app_control_applications_list_category_name__NAME_)

#### [app-control-signatures-list](https://sonicos-api.sonicwall.com/\#/app-control-signatures-list)      App control signatures list API.

GET[/app-control/signatures-list/category/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-signatures-list/get_app_control_signatures_list_category_name__NAME_)

GET[/app-control/signatures-list/category/name/{NAME}/application/name/{APPNAME}](https://sonicos-api.sonicwall.com/#/operations/app-control-signatures-list/get_app_control_signatures_list_category_name__NAME__application_name__APPNAME_)

#### [content-filter-uri-list-object](https://sonicos-api.sonicwall.com/\#/content-filter-uri-list-object)      Content filter URI list object configuration API.

GET[/content-filter/uri-list-objects](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/get_content_filter_uri_list_objects)

POST[/content-filter/uri-list-objects](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/post_content_filter_uri_list_objects)

PUT[/content-filter/uri-list-objects](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/put_content_filter_uri_list_objects)

PATCH[/content-filter/uri-list-objects](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/patch_content_filter_uri_list_objects)

GET[/content-filter/uri-list-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/get_content_filter_uri_list_objects_uuid__UUID_)

PUT[/content-filter/uri-list-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/put_content_filter_uri_list_objects_uuid__UUID_)

PATCH[/content-filter/uri-list-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/patch_content_filter_uri_list_objects_uuid__UUID_)

DELETE[/content-filter/uri-list-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/delete_content_filter_uri_list_objects_uuid__UUID_)

GET[/content-filter/uri-list-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/get_content_filter_uri_list_objects_name__NAME_)

PUT[/content-filter/uri-list-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/put_content_filter_uri_list_objects_name__NAME_)

PATCH[/content-filter/uri-list-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/patch_content_filter_uri_list_objects_name__NAME_)

DELETE[/content-filter/uri-list-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object/delete_content_filter_uri_list_objects_name__NAME_)

#### [content-filter-uri-list-group](https://sonicos-api.sonicwall.com/\#/content-filter-uri-list-group)      Content filter URI list group object configuration API.

GET[/content-filter/uri-list-groups](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/get_content_filter_uri_list_groups)

POST[/content-filter/uri-list-groups](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/post_content_filter_uri_list_groups)

PUT[/content-filter/uri-list-groups](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/put_content_filter_uri_list_groups)

PATCH[/content-filter/uri-list-groups](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/patch_content_filter_uri_list_groups)

GET[/content-filter/uri-list-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/get_content_filter_uri_list_groups_name__NAME_)

PUT[/content-filter/uri-list-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/put_content_filter_uri_list_groups_name__NAME_)

PATCH[/content-filter/uri-list-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/patch_content_filter_uri_list_groups_name__NAME_)

DELETE[/content-filter/uri-list-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/delete_content_filter_uri_list_groups_name__NAME_)

GET[/content-filter/uri-list-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/get_content_filter_uri_list_groups_uuid__UUID_)

PUT[/content-filter/uri-list-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/put_content_filter_uri_list_groups_uuid__UUID_)

PATCH[/content-filter/uri-list-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/patch_content_filter_uri_list_groups_uuid__UUID_)

DELETE[/content-filter/uri-list-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-group/delete_content_filter_uri_list_groups_uuid__UUID_)

#### [content-filter-action](https://sonicos-api.sonicwall.com/\#/content-filter-action)      Content filter action object configuration API.

GET[/content-filter/actions](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/get_content_filter_actions)

POST[/content-filter/actions](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/post_content_filter_actions)

PUT[/content-filter/actions](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/put_content_filter_actions)

PATCH[/content-filter/actions](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/patch_content_filter_actions)

GET[/content-filter/actions/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/get_content_filter_actions_name__NAME_)

PUT[/content-filter/actions/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/put_content_filter_actions_name__NAME_)

PATCH[/content-filter/actions/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/patch_content_filter_actions_name__NAME_)

DELETE[/content-filter/actions/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/delete_content_filter_actions_name__NAME_)

GET[/content-filter/actions/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/get_content_filter_actions_uuid__UUID_)

PUT[/content-filter/actions/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/put_content_filter_actions_uuid__UUID_)

PATCH[/content-filter/actions/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/patch_content_filter_actions_uuid__UUID_)

DELETE[/content-filter/actions/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-action/delete_content_filter_actions_uuid__UUID_)

#### [content-filter-profile](https://sonicos-api.sonicwall.com/\#/content-filter-profile)      Content filter profile object configuration API.

GET[/content-filter/profiles](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/get_content_filter_profiles)

POST[/content-filter/profiles](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/post_content_filter_profiles)

PUT[/content-filter/profiles](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/put_content_filter_profiles)

PATCH[/content-filter/profiles](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/patch_content_filter_profiles)

GET[/content-filter/profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/get_content_filter_profiles_uuid__UUID_)

PUT[/content-filter/profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/put_content_filter_profiles_uuid__UUID_)

PATCH[/content-filter/profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/patch_content_filter_profiles_uuid__UUID_)

DELETE[/content-filter/profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/delete_content_filter_profiles_uuid__UUID_)

GET[/content-filter/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/get_content_filter_profiles_name__NAME_)

PUT[/content-filter/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/put_content_filter_profiles_name__NAME_)

PATCH[/content-filter/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/patch_content_filter_profiles_name__NAME_)

DELETE[/content-filter/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-profile/delete_content_filter_profiles_name__NAME_)

#### [content-filter-uri-list-object-import-uris](https://sonicos-api.sonicwall.com/\#/content-filter-uri-list-object-import-uris)      Upload uri expressions action API.

PUT[/import/content-filter/uri-list-object/uris/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object-import-uris/put_import_content_filter_uri_list_object_uris_name__NAME_)

#### [content-filter-uri-list-object-import-keywords](https://sonicos-api.sonicwall.com/\#/content-filter-uri-list-object-import-keywords)      Upload keyword expressions action API.

PUT[/import/content-filter/uri-list-object/keywords/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object-import-keywords/put_import_content_filter_uri_list_object_keywords_name__NAME_)

#### [content-filter-uri-list-object-export-uris](https://sonicos-api.sonicwall.com/\#/content-filter-uri-list-object-export-uris)      Download uri expressions API.

GET[/export/content-filter/uri-list-object/uris/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object-export-uris/get_export_content_filter_uri_list_object_uris_name__NAME_)

#### [content-filter-uri-list-object-export-keywords](https://sonicos-api.sonicwall.com/\#/content-filter-uri-list-object-export-keywords)      Download keywords expressions action API.

GET[/export/content-filter/uri-list-object/keywords/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-uri-list-object-export-keywords/get_export_content_filter_uri_list_object_keywords_name__NAME_)

#### [content-filter-cfs](https://sonicos-api.sonicwall.com/\#/content-filter-cfs)      Content filter cfs configuration API.

GET[/content-filter/cfs/base](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs/get_content_filter_cfs_base)

PUT[/content-filter/cfs/base](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs/put_content_filter_cfs_base)

#### [content-filter-cfs-policies-statistics](https://sonicos-api.sonicwall.com/\#/content-filter-cfs-policies-statistics)      Content-filter CFS policies TCP statistics API.

GET[/reporting/content-filter/cfs/policies/statistics](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policies-statistics/get_reporting_content_filter_cfs_policies_statistics)

GET[/reporting/content-filter/cfs/policies/statistics/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policies-statistics/get_reporting_content_filter_cfs_policies_statistics_name__NAME_)

DELETE[/reporting/content-filter/cfs/policies/statistics/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policies-statistics/delete_reporting_content_filter_cfs_policies_statistics_name__NAME_)

#### [content-filter-cfs-policy](https://sonicos-api.sonicwall.com/\#/content-filter-cfs-policy)      Content filter cfs policy object configuration API.

GET[/content-filter/cfs/policies](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/get_content_filter_cfs_policies)

POST[/content-filter/cfs/policies](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/post_content_filter_cfs_policies)

PUT[/content-filter/cfs/policies](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/put_content_filter_cfs_policies)

PATCH[/content-filter/cfs/policies](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/patch_content_filter_cfs_policies)

GET[/content-filter/cfs/policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/get_content_filter_cfs_policies_uuid__UUID_)

PUT[/content-filter/cfs/policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/put_content_filter_cfs_policies_uuid__UUID_)

PATCH[/content-filter/cfs/policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/patch_content_filter_cfs_policies_uuid__UUID_)

DELETE[/content-filter/cfs/policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/delete_content_filter_cfs_policies_uuid__UUID_)

GET[/content-filter/cfs/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/get_content_filter_cfs_policies_name__NAME_)

PUT[/content-filter/cfs/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/put_content_filter_cfs_policies_name__NAME_)

PATCH[/content-filter/cfs/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/patch_content_filter_cfs_policies_name__NAME_)

DELETE[/content-filter/cfs/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-policy/delete_content_filter_cfs_policies_name__NAME_)

#### [content-filter-cfs-custom-category](https://sonicos-api.sonicwall.com/\#/content-filter-cfs-custom-category)      Content filter configuration API.

GET[/content-filter/cfs/custom-category/base](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category/get_content_filter_cfs_custom_category_base)

PUT[/content-filter/cfs/custom-category/base](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category/put_content_filter_cfs_custom_category_base)

#### [content-filter-cfs-custom-category-category-entry](https://sonicos-api.sonicwall.com/\#/content-filter-cfs-custom-category-category-entry)      Content filter cfs custom-category category-entry object configuration API.

GET[/content-filter/cfs/custom-category/category-entries](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/get_content_filter_cfs_custom_category_category_entries)

POST[/content-filter/cfs/custom-category/category-entries](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/post_content_filter_cfs_custom_category_category_entries)

PUT[/content-filter/cfs/custom-category/category-entries](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/put_content_filter_cfs_custom_category_category_entries)

PATCH[/content-filter/cfs/custom-category/category-entries](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/patch_content_filter_cfs_custom_category_category_entries)

GET[/content-filter/cfs/custom-category/category-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/get_content_filter_cfs_custom_category_category_entries_domain__NAME_)

PUT[/content-filter/cfs/custom-category/category-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/put_content_filter_cfs_custom_category_category_entries_domain__NAME_)

PATCH[/content-filter/cfs/custom-category/category-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/patch_content_filter_cfs_custom_category_category_entries_domain__NAME_)

DELETE[/content-filter/cfs/custom-category/category-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-category-entry/delete_content_filter_cfs_custom_category_category_entries_domain__NAME_)

#### [content-filter-cfs-custom-category-export](https://sonicos-api.sonicwall.com/\#/content-filter-cfs-custom-category-export)      Export content filter CFS custom category data to file.

GET[/export/content-filter/cfs/custom-category](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-export/get_export_content_filter_cfs_custom_category)

#### [content-filter-cfs-custom-category-import](https://sonicos-api.sonicwall.com/\#/content-filter-cfs-custom-category-import)      Import content filter CFS custom category data.

PUT[/import/content-filter/cfs/custom-category](https://sonicos-api.sonicwall.com/#/operations/content-filter-cfs-custom-category-import/put_import_content_filter_cfs_custom_category)

#### [cfs-get-latest-local-server-info](https://sonicos-api.sonicwall.com/\#/cfs-get-latest-local-server-info)      Get latest local server info.

POST[/content-filter/cfs/synchronize/local-server-info](https://sonicos-api.sonicwall.com/#/operations/cfs-get-latest-local-server-info/post_content_filter_cfs_synchronize_local_server_info)

#### [cfs-status](https://sonicos-api.sonicwall.com/\#/cfs-status)      CFS Status reporting API.

GET[/reporting/cfs/status](https://sonicos-api.sonicwall.com/#/operations/cfs-status/get_reporting_cfs_status)

#### [websense-status](https://sonicos-api.sonicwall.com/\#/websense-status)      Websense Status reporting API.

GET[/reporting/websense/status](https://sonicos-api.sonicwall.com/#/operations/websense-status/get_reporting_websense_status)

#### [content-filter-settings](https://sonicos-api.sonicwall.com/\#/content-filter-settings)      Content filter configuration API.

GET[/content-filter/settings](https://sonicos-api.sonicwall.com/#/operations/content-filter-settings/get_content_filter_settings)

PUT[/content-filter/settings](https://sonicos-api.sonicwall.com/#/operations/content-filter-settings/put_content_filter_settings)

#### [content-filter-websense](https://sonicos-api.sonicwall.com/\#/content-filter-websense)      Content filter configuration API.

GET[/content-filter/websense](https://sonicos-api.sonicwall.com/#/operations/content-filter-websense/get_content_filter_websense)

PUT[/content-filter/websense](https://sonicos-api.sonicwall.com/#/operations/content-filter-websense/put_content_filter_websense)

#### [endpoint-security-profile](https://sonicos-api.sonicwall.com/\#/endpoint-security-profile)      Endpoint Enforcement Profile configuration API.

GET[/endpoint-security/profiles](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-profile/get_endpoint_security_profiles)

POST[/endpoint-security/profiles](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-profile/post_endpoint_security_profiles)

PUT[/endpoint-security/profiles](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-profile/put_endpoint_security_profiles)

GET[/endpoint-security/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-profile/get_endpoint_security_profiles_name__NAME_)

PUT[/endpoint-security/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-profile/put_endpoint_security_profiles_name__NAME_)

DELETE[/endpoint-security/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-profile/delete_endpoint_security_profiles_name__NAME_)

#### [endpoint-security-policy](https://sonicos-api.sonicwall.com/\#/endpoint-security-policy)      Endpoint Enforcement Policy configuration API.

GET[/endpoint-security/policies](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-policy/get_endpoint_security_policies)

POST[/endpoint-security/policies](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-policy/post_endpoint_security_policies)

PUT[/endpoint-security/policies](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-policy/put_endpoint_security_policies)

GET[/endpoint-security/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-policy/get_endpoint_security_policies_name__NAME_)

PUT[/endpoint-security/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-policy/put_endpoint_security_policies_name__NAME_)

DELETE[/endpoint-security/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-policy/delete_endpoint_security_policies_name__NAME_)

#### [endpoint-security-settings](https://sonicos-api.sonicwall.com/\#/endpoint-security-settings)      Endpoint Security configuration API.

GET[/endpoint-security/settings](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-settings/get_endpoint_security_settings)

PUT[/endpoint-security/settings](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-settings/put_endpoint_security_settings)

#### [endpoint-security-status](https://sonicos-api.sonicwall.com/\#/endpoint-security-status)      Endpoint Security reporting API.

GET[/reporting/endpoint-security/status](https://sonicos-api.sonicwall.com/#/operations/endpoint-security-status/get_reporting_endpoint_security_status)

#### [custom-match](https://sonicos-api.sonicwall.com/\#/custom-match)      Custom match object configuration API.

GET[/custom-matches](https://sonicos-api.sonicwall.com/#/operations/custom-match/get_custom_matches)

POST[/custom-matches](https://sonicos-api.sonicwall.com/#/operations/custom-match/post_custom_matches)

PUT[/custom-matches](https://sonicos-api.sonicwall.com/#/operations/custom-match/put_custom_matches)

PATCH[/custom-matches](https://sonicos-api.sonicwall.com/#/operations/custom-match/patch_custom_matches)

GET[/custom-matches/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match/get_custom_matches_name__NAME_)

PUT[/custom-matches/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match/put_custom_matches_name__NAME_)

PATCH[/custom-matches/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match/patch_custom_matches_name__NAME_)

DELETE[/custom-matches/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match/delete_custom_matches_name__NAME_)

#### [custom-match-group](https://sonicos-api.sonicwall.com/\#/custom-match-group)      Custom match group settings.

GET[/custom-match-groups](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/get_custom_match_groups)

POST[/custom-match-groups](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/post_custom_match_groups)

PUT[/custom-match-groups](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/put_custom_match_groups)

GET[/custom-match-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/get_custom_match_groups_uuid__UUID_)

PUT[/custom-match-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/put_custom_match_groups_uuid__UUID_)

DELETE[/custom-match-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/delete_custom_match_groups_uuid__UUID_)

GET[/custom-match-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/get_custom_match_groups_name__NAME_)

PUT[/custom-match-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/put_custom_match_groups_name__NAME_)

DELETE[/custom-match-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/custom-match-group/delete_custom_match_groups_name__NAME_)

#### [custom-match-clone](https://sonicos-api.sonicwall.com/\#/custom-match-clone)      Clone custom match objects.

PUT[/clone/custom-matches](https://sonicos-api.sonicwall.com/#/operations/custom-match-clone/put_clone_custom_matches)

#### [custom-match-group-clone](https://sonicos-api.sonicwall.com/\#/custom-match-group-clone)      Clone custom match groups.

PUT[/clone/custom-match-groups](https://sonicos-api.sonicwall.com/#/operations/custom-match-group-clone/put_clone_custom_match_groups)

#### [reporting-profiles](https://sonicos-api.sonicwall.com/\#/reporting-profiles)      Reporting profile congifuration API.

GET[/reporting-profiles](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/get_reporting_profiles)

POST[/reporting-profiles](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/post_reporting_profiles)

PUT[/reporting-profiles](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/put_reporting_profiles)

PATCH[/reporting-profiles](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/patch_reporting_profiles)

GET[/reporting-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/get_reporting_profiles_name__NAME_)

PUT[/reporting-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/put_reporting_profiles_name__NAME_)

PATCH[/reporting-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/patch_reporting_profiles_name__NAME_)

DELETE[/reporting-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/delete_reporting_profiles_name__NAME_)

GET[/reporting-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/get_reporting_profiles_uuid__UUID_)

PUT[/reporting-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/put_reporting_profiles_uuid__UUID_)

PATCH[/reporting-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/patch_reporting_profiles_uuid__UUID_)

DELETE[/reporting-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/reporting-profiles/delete_reporting_profiles_uuid__UUID_)

#### [reporting-profile-clone](https://sonicos-api.sonicwall.com/\#/reporting-profile-clone)      Clone reporting profiles.

PUT[/clone/reporting-profiles](https://sonicos-api.sonicwall.com/#/operations/reporting-profile-clone/put_clone_reporting_profiles)

#### [dos-action-profile](https://sonicos-api.sonicwall.com/\#/dos-action-profile)      Dos action profile settings.

GET[/dos-action-profiles](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/get_dos_action_profiles)

POST[/dos-action-profiles](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/post_dos_action_profiles)

PUT[/dos-action-profiles](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/put_dos_action_profiles)

GET[/dos-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/get_dos_action_profiles_name__NAME_)

PUT[/dos-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/put_dos_action_profiles_name__NAME_)

DELETE[/dos-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/delete_dos_action_profiles_name__NAME_)

GET[/dos-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/get_dos_action_profiles_uuid__UUID_)

PUT[/dos-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/put_dos_action_profiles_uuid__UUID_)

DELETE[/dos-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile/delete_dos_action_profiles_uuid__UUID_)

#### [dos-action-profile-clone](https://sonicos-api.sonicwall.com/\#/dos-action-profile-clone)      Clone Dos action profiles.

PUT[/clone/dos-action-profiles](https://sonicos-api.sonicwall.com/#/operations/dos-action-profile-clone/put_clone_dos_action_profiles)

#### [security-action-profiles](https://sonicos-api.sonicwall.com/\#/security-action-profiles)      Security action profiles congifuration API.

GET[/security-action-profiles](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/get_security_action_profiles)

POST[/security-action-profiles](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/post_security_action_profiles)

PUT[/security-action-profiles](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/put_security_action_profiles)

PATCH[/security-action-profiles](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/patch_security_action_profiles)

GET[/security-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/get_security_action_profiles_uuid__UUID_)

PUT[/security-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/put_security_action_profiles_uuid__UUID_)

PATCH[/security-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/patch_security_action_profiles_uuid__UUID_)

DELETE[/security-action-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/delete_security_action_profiles_uuid__UUID_)

GET[/security-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/get_security_action_profiles_name__NAME_)

PUT[/security-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/put_security_action_profiles_name__NAME_)

PATCH[/security-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/patch_security_action_profiles_name__NAME_)

DELETE[/security-action-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/security-action-profiles/delete_security_action_profiles_name__NAME_)

#### [security-action-profile-clone](https://sonicos-api.sonicwall.com/\#/security-action-profile-clone)      Clone security action profiles.

PUT[/clone/security-action-profiles](https://sonicos-api.sonicwall.com/#/operations/security-action-profile-clone/put_clone_security_action_profiles)

#### [website-object](https://sonicos-api.sonicwall.com/\#/website-object)      Website object configuration API.

GET[/website-objects](https://sonicos-api.sonicwall.com/#/operations/website-object/get_website_objects)

POST[/website-objects](https://sonicos-api.sonicwall.com/#/operations/website-object/post_website_objects)

PUT[/website-objects](https://sonicos-api.sonicwall.com/#/operations/website-object/put_website_objects)

PATCH[/website-objects](https://sonicos-api.sonicwall.com/#/operations/website-object/patch_website_objects)

GET[/website-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-object/get_website_objects_uuid__UUID_)

PUT[/website-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-object/put_website_objects_uuid__UUID_)

PATCH[/website-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-object/patch_website_objects_uuid__UUID_)

DELETE[/website-objects/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-object/delete_website_objects_uuid__UUID_)

GET[/website-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-object/get_website_objects_name__NAME_)

PUT[/website-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-object/put_website_objects_name__NAME_)

PATCH[/website-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-object/patch_website_objects_name__NAME_)

DELETE[/website-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-object/delete_website_objects_name__NAME_)

#### [website-group](https://sonicos-api.sonicwall.com/\#/website-group)      Website group object configuration API.

GET[/website-groups](https://sonicos-api.sonicwall.com/#/operations/website-group/get_website_groups)

POST[/website-groups](https://sonicos-api.sonicwall.com/#/operations/website-group/post_website_groups)

PUT[/website-groups](https://sonicos-api.sonicwall.com/#/operations/website-group/put_website_groups)

PATCH[/website-groups](https://sonicos-api.sonicwall.com/#/operations/website-group/patch_website_groups)

GET[/website-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-group/get_website_groups_uuid__UUID_)

PUT[/website-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-group/put_website_groups_uuid__UUID_)

PATCH[/website-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-group/patch_website_groups_uuid__UUID_)

DELETE[/website-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/website-group/delete_website_groups_uuid__UUID_)

GET[/website-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-group/get_website_groups_name__NAME_)

PUT[/website-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-group/put_website_groups_name__NAME_)

PATCH[/website-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-group/patch_website_groups_name__NAME_)

DELETE[/website-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/website-group/delete_website_groups_name__NAME_)

#### [website-object-clone](https://sonicos-api.sonicwall.com/\#/website-object-clone)      Clone website objects.

PUT[/clone/website-objects](https://sonicos-api.sonicwall.com/#/operations/website-object-clone/put_clone_website_objects)

#### [website-group-clone](https://sonicos-api.sonicwall.com/\#/website-group-clone)      Clone website groups.

PUT[/clone/website-groups](https://sonicos-api.sonicwall.com/#/operations/website-group-clone/put_clone_website_groups)

#### [country-group](https://sonicos-api.sonicwall.com/\#/country-group)      Country group configuration API.

GET[/country-groups](https://sonicos-api.sonicwall.com/#/operations/country-group/get_country_groups)

POST[/country-groups](https://sonicos-api.sonicwall.com/#/operations/country-group/post_country_groups)

PUT[/country-groups](https://sonicos-api.sonicwall.com/#/operations/country-group/put_country_groups)

PATCH[/country-groups](https://sonicos-api.sonicwall.com/#/operations/country-group/patch_country_groups)

GET[/country-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/country-group/get_country_groups_name__NAME_)

PUT[/country-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/country-group/put_country_groups_name__NAME_)

PATCH[/country-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/country-group/patch_country_groups_name__NAME_)

DELETE[/country-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/country-group/delete_country_groups_name__NAME_)

GET[/country-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/country-group/get_country_groups_uuid__UUID_)

PUT[/country-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/country-group/put_country_groups_uuid__UUID_)

PATCH[/country-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/country-group/patch_country_groups_uuid__UUID_)

DELETE[/country-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/country-group/delete_country_groups_uuid__UUID_)

#### [web-category-object](https://sonicos-api.sonicwall.com/\#/web-category-object)      Web category object reporting API.

GET[/reporting/web-category-objects/status](https://sonicos-api.sonicwall.com/#/operations/web-category-object/get_reporting_web_category_objects_status)

#### [web-category-group](https://sonicos-api.sonicwall.com/\#/web-category-group)      Web category group object configuration API.

GET[/web-category-groups](https://sonicos-api.sonicwall.com/#/operations/web-category-group/get_web_category_groups)

POST[/web-category-groups](https://sonicos-api.sonicwall.com/#/operations/web-category-group/post_web_category_groups)

PUT[/web-category-groups](https://sonicos-api.sonicwall.com/#/operations/web-category-group/put_web_category_groups)

PATCH[/web-category-groups](https://sonicos-api.sonicwall.com/#/operations/web-category-group/patch_web_category_groups)

GET[/web-category-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/get_web_category_groups_name__NAME_)

PUT[/web-category-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/put_web_category_groups_name__NAME_)

PATCH[/web-category-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/patch_web_category_groups_name__NAME_)

DELETE[/web-category-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/delete_web_category_groups_name__NAME_)

GET[/web-category-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/get_web_category_groups_uuid__UUID_)

PUT[/web-category-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/put_web_category_groups_uuid__UUID_)

PATCH[/web-category-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/patch_web_category_groups_uuid__UUID_)

DELETE[/web-category-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/web-category-group/delete_web_category_groups_uuid__UUID_)

#### [threat-prevention-profile](https://sonicos-api.sonicwall.com/\#/threat-prevention-profile)      Threat prevention profile configuration API.

GET[/threat-prevention-profiles](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/get_threat_prevention_profiles)

POST[/threat-prevention-profiles](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/post_threat_prevention_profiles)

PUT[/threat-prevention-profiles](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/put_threat_prevention_profiles)

PATCH[/threat-prevention-profiles](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/patch_threat_prevention_profiles)

GET[/threat-prevention-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/get_threat_prevention_profiles_name__NAME_)

PUT[/threat-prevention-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/put_threat_prevention_profiles_name__NAME_)

PATCH[/threat-prevention-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/patch_threat_prevention_profiles_name__NAME_)

DELETE[/threat-prevention-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/delete_threat_prevention_profiles_name__NAME_)

GET[/threat-prevention-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/get_threat_prevention_profiles_uuid__UUID_)

PUT[/threat-prevention-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/put_threat_prevention_profiles_uuid__UUID_)

PATCH[/threat-prevention-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/patch_threat_prevention_profiles_uuid__UUID_)

DELETE[/threat-prevention-profiles/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/threat-prevention-profile/delete_threat_prevention_profiles_uuid__UUID_)

#### [policies-setting-base](https://sonicos-api.sonicwall.com/\#/policies-setting-base)      Policies base setting congifuration API.

GET[/policies-setting/base](https://sonicos-api.sonicwall.com/#/operations/policies-setting-base/get_policies_setting_base)

PUT[/policies-setting/base](https://sonicos-api.sonicwall.com/#/operations/policies-setting-base/put_policies_setting_base)

#### [policies-setting-enforcement](https://sonicos-api.sonicwall.com/\#/policies-setting-enforcement)      Security services enforcements mode API.

POST[/policies-setting/security-service-enforcement/policy](https://sonicos-api.sonicwall.com/#/operations/policies-setting-enforcement/post_policies_setting_security_service_enforcement_policy)

POST[/policies-setting/security-service-enforcement/global](https://sonicos-api.sonicwall.com/#/operations/policies-setting-enforcement/post_policies_setting_security_service_enforcement_global)

#### [policies-setting-clear-app-cache](https://sonicos-api.sonicwall.com/\#/policies-setting-clear-app-cache)      Clear APP cache API.

POST[/policies-setting/clear-app-cache](https://sonicos-api.sonicwall.com/#/operations/policies-setting-clear-app-cache/post_policies_setting_clear_app_cache)

#### [block-page](https://sonicos-api.sonicwall.com/\#/block-page)      Block page configuration API.

GET[/block-pages](https://sonicos-api.sonicwall.com/#/operations/block-page/get_block_pages)

POST[/block-pages](https://sonicos-api.sonicwall.com/#/operations/block-page/post_block_pages)

PUT[/block-pages](https://sonicos-api.sonicwall.com/#/operations/block-page/put_block_pages)

PATCH[/block-pages](https://sonicos-api.sonicwall.com/#/operations/block-page/patch_block_pages)

GET[/block-pages/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/block-page/get_block_pages_name__NAME_)

PUT[/block-pages/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/block-page/put_block_pages_name__NAME_)

PATCH[/block-pages/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/block-page/patch_block_pages_name__NAME_)

DELETE[/block-pages/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/block-page/delete_block_pages_name__NAME_)

#### [application-group](https://sonicos-api.sonicwall.com/\#/application-group)      Application group configuration API.

GET[/application-groups](https://sonicos-api.sonicwall.com/#/operations/application-group/get_application_groups)

POST[/application-groups](https://sonicos-api.sonicwall.com/#/operations/application-group/post_application_groups)

PUT[/application-groups](https://sonicos-api.sonicwall.com/#/operations/application-group/put_application_groups)

PATCH[/application-groups](https://sonicos-api.sonicwall.com/#/operations/application-group/patch_application_groups)

GET[/application-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/application-group/get_application_groups_name__NAME_)

PUT[/application-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/application-group/put_application_groups_name__NAME_)

PATCH[/application-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/application-group/patch_application_groups_name__NAME_)

DELETE[/application-groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/application-group/delete_application_groups_name__NAME_)

GET[/application-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/application-group/get_application_groups_uuid__UUID_)

PUT[/application-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/application-group/put_application_groups_uuid__UUID_)

PATCH[/application-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/application-group/patch_application_groups_uuid__UUID_)

DELETE[/application-groups/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/application-group/delete_application_groups_uuid__UUID_)

#### [security-policy-ipv4](https://sonicos-api.sonicwall.com/\#/security-policy-ipv4)      IPv4 security policy configuration API.

GET[/security-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4/get_security_policies_ipv4)

POST[/security-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4/post_security_policies_ipv4)

PUT[/security-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4/put_security_policies_ipv4)

GET[/security-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4/get_security_policies_ipv4_uuid__UUID_)

PUT[/security-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4/put_security_policies_ipv4_uuid__UUID_)

DELETE[/security-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4/delete_security_policies_ipv4_uuid__UUID_)

#### [security-policy-ipv6](https://sonicos-api.sonicwall.com/\#/security-policy-ipv6)      IPv6 security policy configuration API.

GET[/security-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6/get_security_policies_ipv6)

POST[/security-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6/post_security_policies_ipv6)

PUT[/security-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6/put_security_policies_ipv6)

GET[/security-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6/get_security_policies_ipv6_uuid__UUID_)

PUT[/security-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6/put_security_policies_ipv6_uuid__UUID_)

DELETE[/security-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6/delete_security_policies_ipv6_uuid__UUID_)

#### [security-policy-all-ipv4](https://sonicos-api.sonicwall.com/\#/security-policy-all-ipv4)      Delete all IPv4 security policies.

DELETE[/all-security-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/security-policy-all-ipv4/delete_all_security_policies_ipv4)

#### [security-policy-all-ipv6](https://sonicos-api.sonicwall.com/\#/security-policy-all-ipv6)      Delete all IPv6 security policies.

DELETE[/all-security-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/security-policy-all-ipv6/delete_all_security_policies_ipv6)

#### [security-policies-max-count](https://sonicos-api.sonicwall.com/\#/security-policies-max-count)      security policies max count configuration API.

GET[/security-policies/max-count](https://sonicos-api.sonicwall.com/#/operations/security-policies-max-count/get_security_policies_max_count)

PUT[/security-policies/max-count](https://sonicos-api.sonicwall.com/#/operations/security-policies-max-count/put_security_policies_max_count)

#### [security-policies-statistics](https://sonicos-api.sonicwall.com/\#/security-policies-statistics)      Firewall security policies statistics API.

GET[/reporting/security-policies/statistics](https://sonicos-api.sonicwall.com/#/operations/security-policies-statistics/get_reporting_security_policies_statistics)

#### [security-policy-ipv4-statistics](https://sonicos-api.sonicwall.com/\#/security-policy-ipv4-statistics)      IPv4 security policies reporting API.

GET[/reporting/security-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4-statistics/get_reporting_security_policies_ipv4)

GET[/reporting/security-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4-statistics/get_reporting_security_policies_ipv4_uuid__UUID_)

DELETE[/reporting/security-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4-statistics/delete_reporting_security_policies_ipv4_uuid__UUID_)

#### [security-policy-ipv6-statistics](https://sonicos-api.sonicwall.com/\#/security-policy-ipv6-statistics)      IPv6 security policies reporting API.

GET[/reporting/security-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6-statistics/get_reporting_security_policies_ipv6)

GET[/reporting/security-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6-statistics/get_reporting_security_policies_ipv6_uuid__UUID_)

DELETE[/reporting/security-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6-statistics/delete_reporting_security_policies_ipv6_uuid__UUID_)

#### [policy-section](https://sonicos-api.sonicwall.com/\#/policy-section)      Policy section configuration API.

GET[/policy/sections](https://sonicos-api.sonicwall.com/#/operations/policy-section/get_policy_sections)

POST[/policy/sections](https://sonicos-api.sonicwall.com/#/operations/policy-section/post_policy_sections)

PUT[/policy/sections](https://sonicos-api.sonicwall.com/#/operations/policy-section/put_policy_sections)

GET[/policy/sections/uuid/{UUID}/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/policy-section/get_policy_sections_uuid__UUID__name__NAME_)

PUT[/policy/sections/uuid/{UUID}/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/policy-section/put_policy_sections_uuid__UUID__name__NAME_)

DELETE[/policy/sections/uuid/{UUID}/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/policy-section/delete_policy_sections_uuid__UUID__name__NAME_)

#### [security-policy-ipv4-clone](https://sonicos-api.sonicwall.com/\#/security-policy-ipv4-clone)      Clone Ipv4 security policies.

PUT[/clone/security-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv4-clone/put_clone_security_policies_ipv4)

#### [security-policy-ipv6-clone](https://sonicos-api.sonicwall.com/\#/security-policy-ipv6-clone)      Clone Ipv6 security policies.

PUT[/clone/security-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/security-policy-ipv6-clone/put_clone_security_policies_ipv6)

#### [decryption-policy-server-statistics](https://sonicos-api.sonicwall.com/\#/decryption-policy-server-statistics)      Decryption policies reporting API.

GET[/reporting/decryption-policies/server](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server-statistics/get_reporting_decryption_policies_server)

GET[/reporting/decryption-policies/server/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server-statistics/get_reporting_decryption_policies_server_uuid__UUID_)

#### [decryption-policy-client-statistics](https://sonicos-api.sonicwall.com/\#/decryption-policy-client-statistics)      Decryption policies reporting API.

GET[/reporting/decryption-policies/client](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client-statistics/get_reporting_decryption_policies_client)

GET[/reporting/decryption-policies/client/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client-statistics/get_reporting_decryption_policies_client_uuid__UUID_)

#### [decryption-policy-ssh-statistics](https://sonicos-api.sonicwall.com/\#/decryption-policy-ssh-statistics)      Decryption policies reporting API.

GET[/reporting/decryption-policies/ssh](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh-statistics/get_reporting_decryption_policies_ssh)

GET[/reporting/decryption-policies/ssh/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh-statistics/get_reporting_decryption_policies_ssh_uuid__UUID_)

#### [decryption-policy-client](https://sonicos-api.sonicwall.com/\#/decryption-policy-client)      Client Decryption policy settings.

GET[/decryption-policies/client](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client/get_decryption_policies_client)

POST[/decryption-policies/client](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client/post_decryption_policies_client)

PUT[/decryption-policies/client](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client/put_decryption_policies_client)

GET[/decryption-policies/client/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client/get_decryption_policies_client_uuid__UUID_)

PUT[/decryption-policies/client/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client/put_decryption_policies_client_uuid__UUID_)

DELETE[/decryption-policies/client/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client/delete_decryption_policies_client_uuid__UUID_)

#### [decryption-policy-server](https://sonicos-api.sonicwall.com/\#/decryption-policy-server)      Server Decryption policy settings.

GET[/decryption-policies/server](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server/get_decryption_policies_server)

POST[/decryption-policies/server](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server/post_decryption_policies_server)

PUT[/decryption-policies/server](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server/put_decryption_policies_server)

GET[/decryption-policies/server/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server/get_decryption_policies_server_uuid__UUID_)

PUT[/decryption-policies/server/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server/put_decryption_policies_server_uuid__UUID_)

DELETE[/decryption-policies/server/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server/delete_decryption_policies_server_uuid__UUID_)

#### [decryption-policy-ssh](https://sonicos-api.sonicwall.com/\#/decryption-policy-ssh)      SSH Decryption policy settings.

GET[/decryption-policies/ssh](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh/get_decryption_policies_ssh)

POST[/decryption-policies/ssh](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh/post_decryption_policies_ssh)

PUT[/decryption-policies/ssh](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh/put_decryption_policies_ssh)

GET[/decryption-policies/ssh/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh/get_decryption_policies_ssh_uuid__UUID_)

PUT[/decryption-policies/ssh/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh/put_decryption_policies_ssh_uuid__UUID_)

DELETE[/decryption-policies/ssh/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh/delete_decryption_policies_ssh_uuid__UUID_)

#### [all-decryption-policies](https://sonicos-api.sonicwall.com/\#/all-decryption-policies)      Delete all decryption policies.

DELETE[/all-decryption-policies](https://sonicos-api.sonicwall.com/#/operations/all-decryption-policies/delete_all_decryption_policies)

DELETE[/all-decryption-policies/server](https://sonicos-api.sonicwall.com/#/operations/all-decryption-policies/delete_all_decryption_policies_server)

DELETE[/all-decryption-policies/ssh](https://sonicos-api.sonicwall.com/#/operations/all-decryption-policies/delete_all_decryption_policies_ssh)

DELETE[/all-decryption-policies/client](https://sonicos-api.sonicwall.com/#/operations/all-decryption-policies/delete_all_decryption_policies_client)

#### [reset-decryption-policy-status](https://sonicos-api.sonicwall.com/\#/reset-decryption-policy-status)      Reset decryption policy statistics.

POST[/reset/decryption-policies/statistics](https://sonicos-api.sonicwall.com/#/operations/reset-decryption-policy-status/post_reset_decryption_policies_statistics)

POST[/reset/decryption-policies/statistics/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/reset-decryption-policy-status/post_reset_decryption_policies_statistics_uuid__UUID_)

#### [decryption-policy-client-clone](https://sonicos-api.sonicwall.com/\#/decryption-policy-client-clone)      Clone client decryption policies.

PUT[/clone/decryption-policies/client](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-client-clone/put_clone_decryption_policies_client)

#### [decryption-policy-server-clone](https://sonicos-api.sonicwall.com/\#/decryption-policy-server-clone)      Clone server decryption policies.

PUT[/clone/decryption-policies/server](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-server-clone/put_clone_decryption_policies_server)

#### [decryption-policy-ssh-clone](https://sonicos-api.sonicwall.com/\#/decryption-policy-ssh-clone)      Clone ssh decryption policies.

PUT[/clone/decryption-policies/ssh](https://sonicos-api.sonicwall.com/#/operations/decryption-policy-ssh-clone/put_clone_decryption_policies_ssh)

#### [dos-policy](https://sonicos-api.sonicwall.com/\#/dos-policy)      DoS policy settings.

GET[/dos-policies](https://sonicos-api.sonicwall.com/#/operations/dos-policy/get_dos_policies)

POST[/dos-policies](https://sonicos-api.sonicwall.com/#/operations/dos-policy/post_dos_policies)

PUT[/dos-policies](https://sonicos-api.sonicwall.com/#/operations/dos-policy/put_dos_policies)

GET[/dos-policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-policy/get_dos_policies_uuid__UUID_)

PUT[/dos-policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-policy/put_dos_policies_uuid__UUID_)

DELETE[/dos-policies/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-policy/delete_dos_policies_uuid__UUID_)

#### [dos-policy-all](https://sonicos-api.sonicwall.com/\#/dos-policy-all)      Delete all DoS policies.

DELETE[/all-dos-policies](https://sonicos-api.sonicwall.com/#/operations/dos-policy-all/delete_all_dos_policies)

#### [dos-policies-counters](https://sonicos-api.sonicwall.com/\#/dos-policies-counters)      DOS policies counters reporting API.

GET[/reporting/dos-policies/counters](https://sonicos-api.sonicwall.com/#/operations/dos-policies-counters/get_reporting_dos_policies_counters)

GET[/reporting/dos-policies/counters/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-policies-counters/get_reporting_dos_policies_counters_uuid__UUID_)

#### [dos-policies-counter-status](https://sonicos-api.sonicwall.com/\#/dos-policies-counter-status)      DOS policies counter status reporting API.

GET[/reporting/dos-policies/counter-status](https://sonicos-api.sonicwall.com/#/operations/dos-policies-counter-status/get_reporting_dos_policies_counter_status)

#### [dos-policies-statistics](https://sonicos-api.sonicwall.com/\#/dos-policies-statistics)      DOS policies statistics reporting API.

GET[/reporting/dos-policies/statistics](https://sonicos-api.sonicwall.com/#/operations/dos-policies-statistics/get_reporting_dos_policies_statistics)

GET[/reporting/dos-policies/statistics/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-policies-statistics/get_reporting_dos_policies_statistics_uuid__UUID_)

DELETE[/reporting/dos-policies/statistics/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/dos-policies-statistics/delete_reporting_dos_policies_statistics_uuid__UUID_)

#### [dos-policy-clone](https://sonicos-api.sonicwall.com/\#/dos-policy-clone)      Clone Dos policies.

PUT[/clone/dos-policies](https://sonicos-api.sonicwall.com/#/operations/dos-policy-clone/put_clone_dos_policies)

#### [nat-policy-ipv4](https://sonicos-api.sonicwall.com/\#/nat-policy-ipv4)      IPv4 nat policy configuration API.

GET[/nat-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/get_nat_policies_ipv4)

POST[/nat-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/post_nat_policies_ipv4)

PUT[/nat-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/put_nat_policies_ipv4)

PATCH[/nat-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/patch_nat_policies_ipv4)

GET[/nat-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/get_nat_policies_ipv4_uuid__UUID_)

PUT[/nat-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/put_nat_policies_ipv4_uuid__UUID_)

PATCH[/nat-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/patch_nat_policies_ipv4_uuid__UUID_)

DELETE[/nat-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4/delete_nat_policies_ipv4_uuid__UUID_)

#### [nat-policy-ipv6](https://sonicos-api.sonicwall.com/\#/nat-policy-ipv6)      IPv6 nat policy configuration API.

GET[/nat-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/get_nat_policies_ipv6)

POST[/nat-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/post_nat_policies_ipv6)

PUT[/nat-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/put_nat_policies_ipv6)

PATCH[/nat-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/patch_nat_policies_ipv6)

GET[/nat-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/get_nat_policies_ipv6_uuid__UUID_)

PUT[/nat-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/put_nat_policies_ipv6_uuid__UUID_)

PATCH[/nat-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/patch_nat_policies_ipv6_uuid__UUID_)

DELETE[/nat-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6/delete_nat_policies_ipv6_uuid__UUID_)

#### [nat-policy-nat64](https://sonicos-api.sonicwall.com/\#/nat-policy-nat64)      NAT64 nat policy configuration API.

GET[/nat-policies/nat64](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/get_nat_policies_nat64)

POST[/nat-policies/nat64](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/post_nat_policies_nat64)

PUT[/nat-policies/nat64](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/put_nat_policies_nat64)

PATCH[/nat-policies/nat64](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/patch_nat_policies_nat64)

GET[/nat-policies/nat64/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/get_nat_policies_nat64_uuid__UUID_)

PUT[/nat-policies/nat64/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/put_nat_policies_nat64_uuid__UUID_)

PATCH[/nat-policies/nat64/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/patch_nat_policies_nat64_uuid__UUID_)

DELETE[/nat-policies/nat64/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64/delete_nat_policies_nat64_uuid__UUID_)

#### [all-nat-policies](https://sonicos-api.sonicwall.com/\#/all-nat-policies)      Delete all NAT policies.

DELETE[/all-nat-policies](https://sonicos-api.sonicwall.com/#/operations/all-nat-policies/delete_all_nat_policies)

DELETE[/all-nat-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/all-nat-policies/delete_all_nat_policies_ipv6)

DELETE[/all-nat-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/all-nat-policies/delete_all_nat_policies_ipv4)

DELETE[/all-nat-policies/nat64](https://sonicos-api.sonicwall.com/#/operations/all-nat-policies/delete_all_nat_policies_nat64)

#### [nat-policy-ipv4-statistics](https://sonicos-api.sonicwall.com/\#/nat-policy-ipv4-statistics)      IPv4 nat policies reporting API.

GET[/reporting/nat-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4-statistics/get_reporting_nat_policies_ipv4)

GET[/reporting/nat-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv4-statistics/get_reporting_nat_policies_ipv4_uuid__UUID_)

#### [nat-policy-ipv6-statistics](https://sonicos-api.sonicwall.com/\#/nat-policy-ipv6-statistics)      IPv6 nat policies reporting API.

GET[/reporting/nat-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6-statistics/get_reporting_nat_policies_ipv6)

GET[/reporting/nat-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-ipv6-statistics/get_reporting_nat_policies_ipv6_uuid__UUID_)

#### [nat-policy-nat64-statistics](https://sonicos-api.sonicwall.com/\#/nat-policy-nat64-statistics)      Nat64 nat policies reporting API.

GET[/reporting/nat-policies/nat64](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64-statistics/get_reporting_nat_policies_nat64)

GET[/reporting/nat-policies/nat64/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/nat-policy-nat64-statistics/get_reporting_nat_policies_nat64_uuid__UUID_)

#### [clear-nat-policy-statistics](https://sonicos-api.sonicwall.com/\#/clear-nat-policy-statistics)      Clear NAT policy statistics.

DELETE[/nat-policy/statistics](https://sonicos-api.sonicwall.com/#/operations/clear-nat-policy-statistics/delete_nat_policy_statistics)

#### [access-rule-ipv4](https://sonicos-api.sonicwall.com/\#/access-rule-ipv4)      IPv4 access rule configuration API.

GET[/access-rules/ipv4](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4/get_access_rules_ipv4)

POST[/access-rules/ipv4](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4/post_access_rules_ipv4)

PUT[/access-rules/ipv4](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4/put_access_rules_ipv4)

GET[/access-rules/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4/get_access_rules_ipv4_uuid__UUID_)

PUT[/access-rules/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4/put_access_rules_ipv4_uuid__UUID_)

DELETE[/access-rules/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4/delete_access_rules_ipv4_uuid__UUID_)

#### [access-rule-ipv6](https://sonicos-api.sonicwall.com/\#/access-rule-ipv6)      IPv6 access rule configuration API.

GET[/access-rules/ipv6](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6/get_access_rules_ipv6)

POST[/access-rules/ipv6](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6/post_access_rules_ipv6)

PUT[/access-rules/ipv6](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6/put_access_rules_ipv6)

GET[/access-rules/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6/get_access_rules_ipv6_uuid__UUID_)

PUT[/access-rules/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6/put_access_rules_ipv6_uuid__UUID_)

DELETE[/access-rules/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6/delete_access_rules_ipv6_uuid__UUID_)

#### [access-rule-all-ipv4](https://sonicos-api.sonicwall.com/\#/access-rule-all-ipv4)      Delete all IPv4 access rules.

DELETE[/all-access-rules/ipv4](https://sonicos-api.sonicwall.com/#/operations/access-rule-all-ipv4/delete_all_access_rules_ipv4)

#### [access-rule-all-ipv6](https://sonicos-api.sonicwall.com/\#/access-rule-all-ipv6)      Delete all IPv6 access rules.

DELETE[/all-access-rules/ipv6](https://sonicos-api.sonicwall.com/#/operations/access-rule-all-ipv6/delete_all_access_rules_ipv6)

#### [access-rules-max-count](https://sonicos-api.sonicwall.com/\#/access-rules-max-count)      Access rules max count configuration API.

GET[/access-rules/max-count](https://sonicos-api.sonicwall.com/#/operations/access-rules-max-count/get_access_rules_max_count)

PUT[/access-rules/max-count](https://sonicos-api.sonicwall.com/#/operations/access-rules-max-count/put_access_rules_max_count)

#### [access-rule-ipv4-statistics](https://sonicos-api.sonicwall.com/\#/access-rule-ipv4-statistics)      IPv4 access rules reporting API.

GET[/reporting/access-rules/ipv4](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-statistics/get_reporting_access_rules_ipv4)

GET[/reporting/access-rules/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-statistics/get_reporting_access_rules_ipv4_uuid__UUID_)

DELETE[/reporting/access-rules/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-statistics/delete_reporting_access_rules_ipv4_uuid__UUID_)

#### [access-rule-ipv6-statistics](https://sonicos-api.sonicwall.com/\#/access-rule-ipv6-statistics)      IPv6 access rules reporting API.

GET[/reporting/access-rules/ipv6](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-statistics/get_reporting_access_rules_ipv6)

GET[/reporting/access-rules/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-statistics/get_reporting_access_rules_ipv6_uuid__UUID_)

DELETE[/reporting/access-rules/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-statistics/delete_reporting_access_rules_ipv6_uuid__UUID_)

#### [access-rule-ipv4-connection-limits-src-connect](https://sonicos-api.sonicwall.com/\#/access-rule-ipv4-connection-limits-src-connect)      IPv4 access rules that enabled and on which source IP address connection limit is enabled reporting API.

GET[/reporting/connection-limits/ipv4/src-connect/from/{FROMZONE}/to/{TOZONE}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-connection-limits-src-connect/get_reporting_connection_limits_ipv4_src_connect_from__FROMZONE__to__TOZONE__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv4/src-connect/from/{FROMZONE}/to/{TOZONE}/source/{SRCADDR}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-connection-limits-src-connect/get_reporting_connection_limits_ipv4_src_connect_from__FROMZONE__to__TOZONE__source__SRCADDR__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv4/src-connect/from/{FROMZONE}/to/{TOZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-connection-limits-src-connect/get_reporting_connection_limits_ipv4_src_connect_from__FROMZONE__to__TOZONE_)

#### [access-rule-ipv4-connection-limits-dst-connect](https://sonicos-api.sonicwall.com/\#/access-rule-ipv4-connection-limits-dst-connect)      IPv4 access rules that enabled and on which destination IP address connection limit is enabled reporting API.

GET[/reporting/connection-limits/ipv4/dst-connect/from/{FROMZONE}/to/{TOZONE}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-connection-limits-dst-connect/get_reporting_connection_limits_ipv4_dst_connect_from__FROMZONE__to__TOZONE__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv4/dst-connect/from/{FROMZONE}/to/{TOZONE}/source/{SRCADDR}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-connection-limits-dst-connect/get_reporting_connection_limits_ipv4_dst_connect_from__FROMZONE__to__TOZONE__source__SRCADDR__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv4/dst-connect/from/{FROMZONE}/to/{TOZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv4-connection-limits-dst-connect/get_reporting_connection_limits_ipv4_dst_connect_from__FROMZONE__to__TOZONE_)

#### [access-rule-ipv6-connection-limits-src-connect](https://sonicos-api.sonicwall.com/\#/access-rule-ipv6-connection-limits-src-connect)      IPv6 access rules that enabled and on which source IP address connection limit is enabled reporting API.

GET[/reporting/connection-limits/ipv6/src-connect/from/{FROMZONE}/to/{TOZONE}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-connection-limits-src-connect/get_reporting_connection_limits_ipv6_src_connect_from__FROMZONE__to__TOZONE__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv6/src-connect/from/{FROMZONE}/to/{TOZONE}/source/{SRCADDR}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-connection-limits-src-connect/get_reporting_connection_limits_ipv6_src_connect_from__FROMZONE__to__TOZONE__source__SRCADDR__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv6/src-connect/from/{FROMZONE}/to/{TOZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-connection-limits-src-connect/get_reporting_connection_limits_ipv6_src_connect_from__FROMZONE__to__TOZONE_)

#### [access-rule-ipv6-connection-limits-dst-connect](https://sonicos-api.sonicwall.com/\#/access-rule-ipv6-connection-limits-dst-connect)      IPv6 access rules that enabled and on which destination IP address connection limit is enabled reporting API.

GET[/reporting/connection-limits/ipv6/dst-connect/from/{FROMZONE}/to/{TOZONE}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-connection-limits-dst-connect/get_reporting_connection_limits_ipv6_dst_connect_from__FROMZONE__to__TOZONE__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv6/dst-connect/from/{FROMZONE}/to/{TOZONE}/source/{SRCADDR}/destination/{DSTADDR}/service/{SVCNAME}/top/{TOPX}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-connection-limits-dst-connect/get_reporting_connection_limits_ipv6_dst_connect_from__FROMZONE__to__TOZONE__source__SRCADDR__destination__DSTADDR__service__SVCNAME__top__TOPX_)

GET[/reporting/connection-limits/ipv6/dst-connect/from/{FROMZONE}/to/{TOZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rule-ipv6-connection-limits-dst-connect/get_reporting_connection_limits_ipv6_dst_connect_from__FROMZONE__to__TOZONE_)

#### [access-rules-statistics](https://sonicos-api.sonicwall.com/\#/access-rules-statistics)      Clear firewall access rule statistics API.

DELETE[/access-rules/statistics](https://sonicos-api.sonicwall.com/#/operations/access-rules-statistics/delete_access_rules_statistics)

#### [access-rules-restore-defaults](https://sonicos-api.sonicwall.com/\#/access-rules-restore-defaults)      Restore firewall access rules to default settings API.

POST[/access-rules/restore-defaults](https://sonicos-api.sonicwall.com/#/operations/access-rules-restore-defaults/post_access_rules_restore_defaults)

POST[/access-rules/restore-defaults/from/{SRCZONE}/to/{DSTZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rules-restore-defaults/post_access_rules_restore_defaults_from__SRCZONE__to__DSTZONE_)

#### [clear\_policy\_lookup](https://sonicos-api.sonicwall.com/\#/clear_policy_lookup)      Reset the values to the default policy lookup settings.

POST[/clear/policy/lookup](https://sonicos-api.sonicwall.com/#/operations/clear_policy_lookup/post_clear_policy_lookup)

#### [access-rules-ipv4](https://sonicos-api.sonicwall.com/\#/access-rules-ipv4)      IPv4 access rules configuration API.

GET[/reporting/access-rules-ipv4/from/{SRCZONE}/to/{DSTZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rules-ipv4/get_reporting_access_rules_ipv4_from__SRCZONE__to__DSTZONE_)

#### [access-rules-ipv6](https://sonicos-api.sonicwall.com/\#/access-rules-ipv6)      IPv6 access rules configuration API.

GET[/reporting/access-rules-ipv6/from/{SRCZONE}/to/{DSTZONE}](https://sonicos-api.sonicwall.com/#/operations/access-rules-ipv6/get_reporting_access_rules_ipv6_from__SRCZONE__to__DSTZONE_)

#### [generate-shadow-list-access-rules](https://sonicos-api.sonicwall.com/\#/generate-shadow-list-access-rules)      Generate Shadow Rule List

POST[/shadow-rules-list/generate/access-rules](https://sonicos-api.sonicwall.com/#/operations/generate-shadow-list-access-rules/post_shadow_rules_list_generate_access_rules)

#### [generate-shadow-list-nat-policies](https://sonicos-api.sonicwall.com/\#/generate-shadow-list-nat-policies)      Generate Shadow Rule List

POST[/shadow-rules-list/generate/nat-policies](https://sonicos-api.sonicwall.com/#/operations/generate-shadow-list-nat-policies/post_shadow_rules_list_generate_nat_policies)

#### [generate-shadow-list-route-policies](https://sonicos-api.sonicwall.com/\#/generate-shadow-list-route-policies)      Generate Shadow Rule List

POST[/shadow-rules-list/generate/route-policies](https://sonicos-api.sonicwall.com/#/operations/generate-shadow-list-route-policies/post_shadow_rules_list_generate_route_policies)

#### [generate-shadow-list-decryption-policies](https://sonicos-api.sonicwall.com/\#/generate-shadow-list-decryption-policies)      Generate Shadow Rule List

POST[/shadow-rules-list/generate/decryption-policies](https://sonicos-api.sonicwall.com/#/operations/generate-shadow-list-decryption-policies/post_shadow_rules_list_generate_decryption_policies)

#### [generate-shadow-list-dos-policies](https://sonicos-api.sonicwall.com/\#/generate-shadow-list-dos-policies)      Generate Shadow Rule List

POST[/shadow-rules-list/generate/dos-policies](https://sonicos-api.sonicwall.com/#/operations/generate-shadow-list-dos-policies/post_shadow_rules_list_generate_dos_policies)

#### [routing](https://sonicos-api.sonicwall.com/\#/routing)      Routing configuration API.

GET[/routing](https://sonicos-api.sonicwall.com/#/operations/routing/get_routing)

PUT[/routing](https://sonicos-api.sonicwall.com/#/operations/routing/put_routing)

#### [route-policy-ipv4](https://sonicos-api.sonicwall.com/\#/route-policy-ipv4)      IPv4 route policy configuration API.

GET[/route-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/get_route_policies_ipv4)

POST[/route-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/post_route_policies_ipv4)

PUT[/route-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/put_route_policies_ipv4)

PATCH[/route-policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/patch_route_policies_ipv4)

GET[/route-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/get_route_policies_ipv4_uuid__UUID_)

PUT[/route-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/put_route_policies_ipv4_uuid__UUID_)

PATCH[/route-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/patch_route_policies_ipv4_uuid__UUID_)

DELETE[/route-policies/ipv4/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv4/delete_route_policies_ipv4_uuid__UUID_)

#### [route-policies-sdwan](https://sonicos-api.sonicwall.com/\#/route-policies-sdwan)      All SD-WAN route policies API.

DELETE[/route-policies-sdwan/all](https://sonicos-api.sonicwall.com/#/operations/route-policies-sdwan/delete_route_policies_sdwan_all)

#### [route-policies-ipv4](https://sonicos-api.sonicwall.com/\#/route-policies-ipv4)      All IPv4 route policies API.

DELETE[/route-policies-ipv4/all](https://sonicos-api.sonicwall.com/#/operations/route-policies-ipv4/delete_route_policies_ipv4_all)

#### [route-policies-ipv6](https://sonicos-api.sonicwall.com/\#/route-policies-ipv6)      All IPv6 route policies API.

DELETE[/route-policies-ipv6/all](https://sonicos-api.sonicwall.com/#/operations/route-policies-ipv6/delete_route_policies_ipv6_all)

#### [route-policy-ipv6](https://sonicos-api.sonicwall.com/\#/route-policy-ipv6)      IPv6 route policy configuration API.

GET[/route-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/get_route_policies_ipv6)

POST[/route-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/post_route_policies_ipv6)

PUT[/route-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/put_route_policies_ipv6)

PATCH[/route-policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/patch_route_policies_ipv6)

GET[/route-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/get_route_policies_ipv6_uuid__UUID_)

PUT[/route-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/put_route_policies_ipv6_uuid__UUID_)

PATCH[/route-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/patch_route_policies_ipv6_uuid__UUID_)

DELETE[/route-policies/ipv6/uuid/{UUID}](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6/delete_route_policies_ipv6_uuid__UUID_)

#### [route-policy-system](https://sonicos-api.sonicwall.com/\#/route-policy-system)      IPv4 Route policies system statistics reporting API.

GET[/reporting/route-policies/ipv4/system](https://sonicos-api.sonicwall.com/#/operations/route-policy-system/get_reporting_route_policies_ipv4_system)

#### [route-policy-dynamic](https://sonicos-api.sonicwall.com/\#/route-policy-dynamic)      IPv4 Route policies dynamic statistics reporting API.

GET[/reporting/route-policies/ipv4/dynamic](https://sonicos-api.sonicwall.com/#/operations/route-policy-dynamic/get_reporting_route_policies_ipv4_dynamic)

#### [route-policy-ipv6-system](https://sonicos-api.sonicwall.com/\#/route-policy-ipv6-system)      IPv6 Route policies system statistics reporting API.

GET[/reporting/route-policies/ipv6/system](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6-system/get_reporting_route_policies_ipv6_system)

#### [route-policy-ipv6-dynamic](https://sonicos-api.sonicwall.com/\#/route-policy-ipv6-dynamic)      IPv6 Route policies dynamic statistics reporting API.

GET[/reporting/route-policies/ipv6/dynamic](https://sonicos-api.sonicwall.com/#/operations/route-policy-ipv6-dynamic/get_reporting_route_policies_ipv6_dynamic)

#### [status-storage](https://sonicos-api.sonicwall.com/\#/status-storage)      Storage status API.

GET[/reporting/status/storage](https://sonicos-api.sonicwall.com/#/operations/status-storage/get_reporting_status_storage)

#### [status-system](https://sonicos-api.sonicwall.com/\#/status-system)      System status API.

GET[/reporting/status/system](https://sonicos-api.sonicwall.com/#/operations/status-system/get_reporting_status_system)

#### [status-security](https://sonicos-api.sonicwall.com/\#/status-security)      Security services status API.

GET[/reporting/status/security-services](https://sonicos-api.sonicwall.com/#/operations/status-security/get_reporting_status_security_services)

#### [status-interfaces](https://sonicos-api.sonicwall.com/\#/status-interfaces)      Network interfaces status API.

GET[/reporting/status/interfaces](https://sonicos-api.sonicwall.com/#/operations/status-interfaces/get_reporting_status_interfaces)

#### [restart](https://sonicos-api.sonicwall.com/\#/restart)      Appliance restart API.

GET[/restart](https://sonicos-api.sonicwall.com/#/operations/restart/get_restart)

POST[/restart](https://sonicos-api.sonicwall.com/#/operations/restart/post_restart)

DELETE[/restart](https://sonicos-api.sonicwall.com/#/operations/restart/delete_restart)

GET[/restart/at/{AT\_TIME}](https://sonicos-api.sonicwall.com/#/operations/restart/get_restart_at__AT_TIME_)

POST[/restart/at/{AT\_TIME}](https://sonicos-api.sonicwall.com/#/operations/restart/post_restart_at__AT_TIME_)

DELETE[/restart/at/{AT\_TIME}](https://sonicos-api.sonicwall.com/#/operations/restart/delete_restart_at__AT_TIME_)

GET[/restart/in/{IN\_TIME}/minutes](https://sonicos-api.sonicwall.com/#/operations/restart/get_restart_in__IN_TIME__minutes)

POST[/restart/in/{IN\_TIME}/minutes](https://sonicos-api.sonicwall.com/#/operations/restart/post_restart_in__IN_TIME__minutes)

DELETE[/restart/in/{IN\_TIME}/minutes](https://sonicos-api.sonicwall.com/#/operations/restart/delete_restart_in__IN_TIME__minutes)

GET[/restart/in/{IN\_TIME}/days](https://sonicos-api.sonicwall.com/#/operations/restart/get_restart_in__IN_TIME__days)

POST[/restart/in/{IN\_TIME}/days](https://sonicos-api.sonicwall.com/#/operations/restart/post_restart_in__IN_TIME__days)

DELETE[/restart/in/{IN\_TIME}/days](https://sonicos-api.sonicwall.com/#/operations/restart/delete_restart_in__IN_TIME__days)

GET[/restart/in/{IN\_TIME}/hours](https://sonicos-api.sonicwall.com/#/operations/restart/get_restart_in__IN_TIME__hours)

POST[/restart/in/{IN\_TIME}/hours](https://sonicos-api.sonicwall.com/#/operations/restart/post_restart_in__IN_TIME__hours)

DELETE[/restart/in/{IN\_TIME}/hours](https://sonicos-api.sonicwall.com/#/operations/restart/delete_restart_in__IN_TIME__hours)

#### [boot-current](https://sonicos-api.sonicwall.com/\#/boot-current)      Appliance boot current API.

POST[/boot/current](https://sonicos-api.sonicwall.com/#/operations/boot-current/post_boot_current)

POST[/boot/current/factory-default](https://sonicos-api.sonicwall.com/#/operations/boot-current/post_boot_current_factory_default)

#### [boot-uploaded](https://sonicos-api.sonicwall.com/\#/boot-uploaded)      Appliance boot uploaded API.

POST[/boot/uploaded](https://sonicos-api.sonicwall.com/#/operations/boot-uploaded/post_boot_uploaded)

POST[/boot/uploaded/factory-default](https://sonicos-api.sonicwall.com/#/operations/boot-uploaded/post_boot_uploaded_factory_default)

#### [local-backup-boot](https://sonicos-api.sonicwall.com/\#/local-backup-boot)      Appliance boot local backup API.

GET[/local-backup-boot/name/{PREFNAME}](https://sonicos-api.sonicwall.com/#/operations/local-backup-boot/get_local_backup_boot_name__PREFNAME_)

POST[/local-backup-boot/name/{PREFNAME}](https://sonicos-api.sonicwall.com/#/operations/local-backup-boot/post_local_backup_boot_name__PREFNAME_)

GET[/local-backup-boot/name/{PREFNAME}/delay/{DELAY\_TIME}](https://sonicos-api.sonicwall.com/#/operations/local-backup-boot/get_local_backup_boot_name__PREFNAME__delay__DELAY_TIME_)

POST[/local-backup-boot/name/{PREFNAME}/delay/{DELAY\_TIME}](https://sonicos-api.sonicwall.com/#/operations/local-backup-boot/post_local_backup_boot_name__PREFNAME__delay__DELAY_TIME_)

#### [cloud-backup-boot](https://sonicos-api.sonicwall.com/\#/cloud-backup-boot)      Appliance boot cloud backup API.

POST[/cloud-backup-boot/name/{PREFNAME2}](https://sonicos-api.sonicwall.com/#/operations/cloud-backup-boot/post_cloud_backup_boot_name__PREFNAME2_)

#### [config-mode](https://sonicos-api.sonicwall.com/\#/config-mode)      Preempt the other user, set self to config mode.

POST[/config-mode](https://sonicos-api.sonicwall.com/#/operations/config-mode/post_config_mode)

#### [non-config-mode](https://sonicos-api.sonicwall.com/\#/non-config-mode)      Release config mode, set self to non-config mode.

POST[/non-config-mode](https://sonicos-api.sonicwall.com/#/operations/non-config-mode/post_non_config_mode)

#### [sys-ext-storage-logs-enable](https://sonicos-api.sonicwall.com/\#/sys-ext-storage-logs-enable)      Enable log files on storage API.

POST[/storage/logfile/enable](https://sonicos-api.sonicwall.com/#/operations/sys-ext-storage-logs-enable/post_storage_logfile_enable)

#### [sys-ext-storage-logs-disable](https://sonicos-api.sonicwall.com/\#/sys-ext-storage-logs-disable)      Enable log files on storage API.

POST[/storage/logfile/disable](https://sonicos-api.sonicwall.com/#/operations/sys-ext-storage-logs-disable/post_storage_logfile_disable)

#### [sysfile-no-logs](https://sonicos-api.sonicwall.com/\#/sysfile-no-logs)      Delete logs files.

DELETE[/sysfile/log/{NAME}/dev/{DEVID}](https://sonicos-api.sonicwall.com/#/operations/sysfile-no-logs/delete_sysfile_log__NAME__dev__DEVID_)

#### [sysfile-list-logs](https://sonicos-api.sonicwall.com/\#/sysfile-list-logs)      List logs files.

GET[/reporting/sysfile/log](https://sonicos-api.sonicwall.com/#/operations/sysfile-list-logs/get_reporting_sysfile_log)

#### [sysfile-list-sysdata](https://sonicos-api.sonicwall.com/\#/sysfile-list-sysdata)      List system data files.

GET[/reporting/sysfile/sysdata](https://sonicos-api.sonicwall.com/#/operations/sysfile-list-sysdata/get_reporting_sysfile_sysdata)

#### [sysfile-list-diagdata](https://sonicos-api.sonicwall.com/\#/sysfile-list-diagdata)      List diagnostic data files.

GET[/reporting/sysfile/diagdata](https://sonicos-api.sonicwall.com/#/operations/sysfile-list-diagdata/get_reporting_sysfile_diagdata)

#### [sysfile-list-configbk](https://sonicos-api.sonicwall.com/\#/sysfile-list-configbk)      List configuration backup files.

GET[/reporting/sysfile/configbk](https://sonicos-api.sonicwall.com/#/operations/sysfile-list-configbk/get_reporting_sysfile_configbk)

#### [connection-cache-element](https://sonicos-api.sonicwall.com/\#/connection-cache-element)      delete connection cache element.

DELETE[/connection-cache-element/src-ip/{SRCIP}/src-port/{SRCPORT}/dst-ip/{DSTIP}/dst-port/{DSTPORT}/proto/{PROTOCAL}/srcIf/{SRCIFACE}/dstIf/{DSTIFACE}/dstNat/{NAT}](https://sonicos-api.sonicwall.com/#/operations/connection-cache-element/delete_connection_cache_element_src_ip__SRCIP__src_port__SRCPORT__dst_ip__DSTIP__dst_port__DSTPORT__proto__PROTOCAL__srcIf__SRCIFACE__dstIf__DSTIFACE__dstNat__NAT_)

#### [connection-caches](https://sonicos-api.sonicwall.com/\#/connection-caches)      delete all connection cache elements.

DELETE[/connection-caches](https://sonicos-api.sonicwall.com/#/operations/connection-caches/delete_connection_caches)

#### [sysfile-export-log](https://sonicos-api.sonicwall.com/\#/sysfile-export-log)      Export log in txt fromat API.

GET[/export/sysfile/log/txt/{NAME}/dev/{DEVID}](https://sonicos-api.sonicwall.com/#/operations/sysfile-export-log/get_export_sysfile_log_txt__NAME__dev__DEVID_)

#### [sysfile-export-sysdata](https://sonicos-api.sonicwall.com/\#/sysfile-export-sysdata)      Export system data in txt fromat API.

GET[/export/sysfile/sysdata/txt/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sysfile-export-sysdata/get_export_sysfile_sysdata_txt__NAME_)

#### [sysfile-export-diagdata](https://sonicos-api.sonicwall.com/\#/sysfile-export-diagdata)      Export diagdata in txt fromat API.

GET[/export/sysfile/diagdata/txt/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sysfile-export-diagdata/get_export_sysfile_diagdata_txt__NAME_)

#### [sysfile-storage](https://sonicos-api.sonicwall.com/\#/sysfile-storage)      Storage configuration API.

GET[/sysfile/storage](https://sonicos-api.sonicwall.com/#/operations/sysfile-storage/get_sysfile_storage)

PUT[/sysfile/storage](https://sonicos-api.sonicwall.com/#/operations/sysfile-storage/put_sysfile_storage)

#### [export-current-config-exp](https://sonicos-api.sonicwall.com/\#/export-current-config-exp)      Export current configuration using the SonicOS WebUI (.exp) format.

GET[/export/current-config/exp](https://sonicos-api.sonicwall.com/#/operations/export-current-config-exp/get_export_current_config_exp)

#### [export-current-config-cli](https://sonicos-api.sonicwall.com/\#/export-current-config-cli)      Export current configuration using the SonicOS E-CLI command format.

GET[/export/current-config/cli](https://sonicos-api.sonicwall.com/#/operations/export-current-config-cli/get_export_current_config_cli)

#### [export-firmware-current](https://sonicos-api.sonicwall.com/\#/export-firmware-current)      Export current firmware image off of the appliance.

GET[/export/firmware/current](https://sonicos-api.sonicwall.com/#/operations/export-firmware-current/get_export_firmware_current)

#### [export-firmware-uploaded](https://sonicos-api.sonicwall.com/\#/export-firmware-uploaded)      Export the latest uploaded firmware image.

GET[/export/firmware/uploaded](https://sonicos-api.sonicwall.com/#/operations/export-firmware-uploaded/get_export_firmware_uploaded)

#### [export-firmware-system-backup](https://sonicos-api.sonicwall.com/\#/export-firmware-system-backup)      Export the system backup firmware image.

GET[/export/firmware/system-backup](https://sonicos-api.sonicwall.com/#/operations/export-firmware-system-backup/get_export_firmware_system_backup)

#### [export-tech-support-report](https://sonicos-api.sonicwall.com/\#/export-tech-support-report)      Export the technical support report.

GET[/export/tech-support-report](https://sonicos-api.sonicwall.com/#/operations/export-tech-support-report/get_export_tech_support_report)

#### [export-ssoauth-log](https://sonicos-api.sonicwall.com/\#/export-ssoauth-log)      Export the SSO AUTH log.

GET[/export/ssoauth-log](https://sonicos-api.sonicwall.com/#/operations/export-ssoauth-log/get_export_ssoauth_log)

#### [export-and-reset-ssoauth-log](https://sonicos-api.sonicwall.com/\#/export-and-reset-ssoauth-log)      Export and reset the SSO AUTH log.

GET[/export-and-reset/ssoauth-log](https://sonicos-api.sonicwall.com/#/operations/export-and-reset-ssoauth-log/get_export_and_reset_ssoauth_log)

#### [export-swarm-report](https://sonicos-api.sonicwall.com/\#/export-swarm-report)      Export Swarm report

GET[/export/swarm-report/{QUERY}](https://sonicos-api.sonicwall.com/#/operations/export-swarm-report/get_export_swarm_report__QUERY_)

#### [export-trace-log](https://sonicos-api.sonicwall.com/\#/export-trace-log)      Export trace log.

GET[/export/trace-log/{QUERY}](https://sonicos-api.sonicwall.com/#/operations/export-trace-log/get_export_trace_log__QUERY_)

#### [export-core-dump](https://sonicos-api.sonicwall.com/\#/export-core-dump)      Export core dump.

GET[/export/core-dump/{QUERY}](https://sonicos-api.sonicwall.com/#/operations/export-core-dump/get_export_core_dump__QUERY_)

#### [export-address-objects-api](https://sonicos-api.sonicwall.com/\#/export-address-objects-api)      Export address objects.

GET[/export/address-objects](https://sonicos-api.sonicwall.com/#/operations/export-address-objects-api/get_export_address_objects)

#### [export-services-api](https://sonicos-api.sonicwall.com/\#/export-services-api)      Export services.

GET[/export/services](https://sonicos-api.sonicwall.com/#/operations/export-services-api/get_export_services)

#### [export-country-objects-api](https://sonicos-api.sonicwall.com/\#/export-country-objects-api)      Export country objects.

GET[/export/country-objects](https://sonicos-api.sonicwall.com/#/operations/export-country-objects-api/get_export_country_objects)

#### [export-applications-api](https://sonicos-api.sonicwall.com/\#/export-applications-api)      Export applications.

GET[/export/applications](https://sonicos-api.sonicwall.com/#/operations/export-applications-api/get_export_applications)

#### [export-web-categories-api](https://sonicos-api.sonicwall.com/\#/export-web-categories-api)      Export web categories.

GET[/export/web-categories](https://sonicos-api.sonicwall.com/#/operations/export-web-categories-api/get_export_web_categories)

#### [export-url-list-api](https://sonicos-api.sonicwall.com/\#/export-url-list-api)      Export url list.

GET[/export/url-list](https://sonicos-api.sonicwall.com/#/operations/export-url-list-api/get_export_url_list)

#### [export-custom-matches-api](https://sonicos-api.sonicwall.com/\#/export-custom-matches-api)      Export custom matches.

GET[/export/custom-matches](https://sonicos-api.sonicwall.com/#/operations/export-custom-matches-api/get_export_custom_matches)

#### [export-threat-prevention-profiles-api](https://sonicos-api.sonicwall.com/\#/export-threat-prevention-profiles-api)      Export threat prevention profiles.

GET[/export/threat-prevention-profiles](https://sonicos-api.sonicwall.com/#/operations/export-threat-prevention-profiles-api/get_export_threat_prevention_profiles)

#### [export-actions-api](https://sonicos-api.sonicwall.com/\#/export-actions-api)      Export actions.

GET[/export/actions](https://sonicos-api.sonicwall.com/#/operations/export-actions-api/get_export_actions)

#### [export-security-policies-api](https://sonicos-api.sonicwall.com/\#/export-security-policies-api)      Export security policies.

GET[/export/security-policies](https://sonicos-api.sonicwall.com/#/operations/export-security-policies-api/get_export_security_policies)

#### [export-nat-policies-api](https://sonicos-api.sonicwall.com/\#/export-nat-policies-api)      Export nat policies.

GET[/export/nat-policies](https://sonicos-api.sonicwall.com/#/operations/export-nat-policies-api/get_export_nat_policies)

#### [export-route-policies-api](https://sonicos-api.sonicwall.com/\#/export-route-policies-api)      Export route policies.

GET[/export/route-policies](https://sonicos-api.sonicwall.com/#/operations/export-route-policies-api/get_export_route_policies)

#### [export-decryption-policies-api](https://sonicos-api.sonicwall.com/\#/export-decryption-policies-api)      Export decryption policies.

GET[/export/decryption-policies](https://sonicos-api.sonicwall.com/#/operations/export-decryption-policies-api/get_export_decryption_policies)

#### [export-dos-policies-api](https://sonicos-api.sonicwall.com/\#/export-dos-policies-api)      Export dos policies.

GET[/export/dos-policies](https://sonicos-api.sonicwall.com/#/operations/export-dos-policies-api/get_export_dos_policies)

#### [export-access-rules-shadow-rule-list-api](https://sonicos-api.sonicwall.com/\#/export-access-rules-shadow-rule-list-api)      Export access rules shadow rule list.

GET[/export/shadow-rule-list/access-rules](https://sonicos-api.sonicwall.com/#/operations/export-access-rules-shadow-rule-list-api/get_export_shadow_rule_list_access_rules)

#### [export-nat-policies-shadow-rule-list-api](https://sonicos-api.sonicwall.com/\#/export-nat-policies-shadow-rule-list-api)      Export nat policies shadow rule list.

GET[/export/shadow-rule-list/nat-policies](https://sonicos-api.sonicwall.com/#/operations/export-nat-policies-shadow-rule-list-api/get_export_shadow_rule_list_nat_policies)

#### [export-route-policies-shadow-rule-list-api](https://sonicos-api.sonicwall.com/\#/export-route-policies-shadow-rule-list-api)      Export route policies shadow rule list.

GET[/export/shadow-rule-list/route-policies](https://sonicos-api.sonicwall.com/#/operations/export-route-policies-shadow-rule-list-api/get_export_shadow_rule_list_route_policies)

#### [export-decryption-policies-shadow-rule-list-api](https://sonicos-api.sonicwall.com/\#/export-decryption-policies-shadow-rule-list-api)      Export decryption policies shadow rule list.

GET[/export/shadow-rule-list/decryption-policies](https://sonicos-api.sonicwall.com/#/operations/export-decryption-policies-shadow-rule-list-api/get_export_shadow_rule_list_decryption_policies)

#### [export-dos-policies-shadow-rule-list-api](https://sonicos-api.sonicwall.com/\#/export-dos-policies-shadow-rule-list-api)      Export dos policies shadow rule list.

GET[/export/shadow-rule-list/dos-policies](https://sonicos-api.sonicwall.com/#/operations/export-dos-policies-shadow-rule-list-api/get_export_shadow_rule_list_dos_policies)

#### [export-cloud-backup-exp](https://sonicos-api.sonicwall.com/\#/export-cloud-backup-exp)      Export cloud backup exp.

GET[/export/cloud-backup/name/{EXPNAME}](https://sonicos-api.sonicwall.com/#/operations/export-cloud-backup-exp/get_export_cloud_backup_name__EXPNAME_)

#### [export-console-logs](https://sonicos-api.sonicwall.com/\#/export-console-logs)      Export console logs.

GET[/export/console/log](https://sonicos-api.sonicwall.com/#/operations/export-console-logs/get_export_console_log)

#### [export-safe-mode-logs](https://sonicos-api.sonicwall.com/\#/export-safe-mode-logs)      Export safe mode logs.

GET[/export/safemode/log](https://sonicos-api.sonicwall.com/#/operations/export-safe-mode-logs/get_export_safemode_log)

#### [import-exp-confirm](https://sonicos-api.sonicwall.com/\#/import-exp-confirm)      Confirm import configuration API.

POST[/confirm-import](https://sonicos-api.sonicwall.com/#/operations/import-exp-confirm/post_confirm_import)

#### [import-exp-abort](https://sonicos-api.sonicwall.com/\#/import-exp-abort)      Abort import configuration API.

POST[/abort-import](https://sonicos-api.sonicwall.com/#/operations/import-exp-abort/post_abort_import)

#### [firmware](https://sonicos-api.sonicwall.com/\#/firmware)      Firmware configuration API.

GET[/firmware/base](https://sonicos-api.sonicwall.com/#/operations/firmware/get_firmware_base)

PUT[/firmware/base](https://sonicos-api.sonicwall.com/#/operations/firmware/put_firmware_base)

#### [ftp](https://sonicos-api.sonicwall.com/\#/ftp)      ftp configuration API.

GET[/ftp/base](https://sonicos-api.sonicwall.com/#/operations/ftp/get_ftp_base)

PUT[/ftp/base](https://sonicos-api.sonicwall.com/#/operations/ftp/put_ftp_base)

#### [uploaded-firmware](https://sonicos-api.sonicwall.com/\#/uploaded-firmware)      Delete uploaded firmware.

DELETE[/upload-firmware](https://sonicos-api.sonicwall.com/#/operations/uploaded-firmware/delete_upload_firmware)

#### [local-backups](https://sonicos-api.sonicwall.com/\#/local-backups)      Delete the backup firmware and all configurations or boot local backup firmware with factory default configuration.

POST[/local-backups/version/{FWVER}](https://sonicos-api.sonicwall.com/#/operations/local-backups/post_local_backups_version__FWVER_)

DELETE[/local-backups/version/{FWVER}](https://sonicos-api.sonicwall.com/#/operations/local-backups/delete_local_backups_version__FWVER_)

#### [export-local-backup-firmware](https://sonicos-api.sonicwall.com/\#/export-local-backup-firmware)      Download the local backup firmware.

GET[/export/local-backup-firmware/version/{FWVER}](https://sonicos-api.sonicwall.com/#/operations/export-local-backup-firmware/get_export_local_backup_firmware_version__FWVER_)

#### [local-backup](https://sonicos-api.sonicwall.com/\#/local-backup)      Local backup.

POST[/local/backups](https://sonicos-api.sonicwall.com/#/operations/local-backup/post_local_backups)

DELETE[/local/backups](https://sonicos-api.sonicwall.com/#/operations/local-backup/delete_local_backups)

POST[/local/backups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/local-backup/post_local_backups_name__NAME_)

DELETE[/local/backups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/local-backup/delete_local_backups_name__NAME_)

#### [local-backup-retain](https://sonicos-api.sonicwall.com/\#/local-backup-retain)      Local backup setting.

PUT[/local-backup-retain](https://sonicos-api.sonicwall.com/#/operations/local-backup-retain/put_local_backup_retain)

#### [local-backup-comment](https://sonicos-api.sonicwall.com/\#/local-backup-comment)      Local backup setting.

PUT[/local-backup-comment](https://sonicos-api.sonicwall.com/#/operations/local-backup-comment/put_local_backup_comment)

#### [local-backup-gold](https://sonicos-api.sonicwall.com/\#/local-backup-gold)      Local backup setting.

PUT[/local-backup-gold](https://sonicos-api.sonicwall.com/#/operations/local-backup-gold/put_local_backup_gold)

#### [cloud-backup](https://sonicos-api.sonicwall.com/\#/cloud-backup)      Cloud backup.

POST[/cloud-backup](https://sonicos-api.sonicwall.com/#/operations/cloud-backup/post_cloud_backup)

DELETE[/cloud-backup](https://sonicos-api.sonicwall.com/#/operations/cloud-backup/delete_cloud_backup)

POST[/cloud-backup/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/cloud-backup/post_cloud_backup_name__NAME_)

DELETE[/cloud-backup/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/cloud-backup/delete_cloud_backup_name__NAME_)

#### [cloud-backup-retain](https://sonicos-api.sonicwall.com/\#/cloud-backup-retain)      cloud backup setting.

PUT[/cloud-backup-retain](https://sonicos-api.sonicwall.com/#/operations/cloud-backup-retain/put_cloud_backup_retain)

#### [cloud-backup-comment](https://sonicos-api.sonicwall.com/\#/cloud-backup-comment)      cloud backup setting.

PUT[/cloud-backup-comment](https://sonicos-api.sonicwall.com/#/operations/cloud-backup-comment/put_cloud_backup_comment)

#### [cloud-backup-gold](https://sonicos-api.sonicwall.com/\#/cloud-backup-gold)      cloud backup setting.

PUT[/cloud-backup-gold](https://sonicos-api.sonicwall.com/#/operations/cloud-backup-gold/put_cloud_backup_gold)

#### [delete-cloud-backups-fwVer](https://sonicos-api.sonicwall.com/\#/delete-cloud-backups-fwVer)      Delete all cloud backup configurations with specific firmware version.

DELETE[/cloud-backups/version/{FWVER}](https://sonicos-api.sonicwall.com/#/operations/delete-cloud-backups-fwVer/delete_cloud_backups_version__FWVER_)

#### [auto-upgrade](https://sonicos-api.sonicwall.com/\#/auto-upgrade)      Proceed auto-upgrade firmware.

POST[/auto-upgrade](https://sonicos-api.sonicwall.com/#/operations/auto-upgrade/post_auto_upgrade)

DELETE[/auto-upgrade](https://sonicos-api.sonicwall.com/#/operations/auto-upgrade/delete_auto_upgrade)

#### [firmware-update-status](https://sonicos-api.sonicwall.com/\#/firmware-update-status)      Firmware update status API.

GET[/reporting/firmware-update](https://sonicos-api.sonicwall.com/#/operations/firmware-update-status/get_reporting_firmware_update)

#### [firmware-download](https://sonicos-api.sonicwall.com/\#/firmware-download)      Download new firmware.

POST[/firmware/download](https://sonicos-api.sonicwall.com/#/operations/firmware-download/post_firmware_download)

#### [log-view-option](https://sonicos-api.sonicwall.com/\#/log-view-option)      Log syslog base settings API.

GET[/log/view/option](https://sonicos-api.sonicwall.com/#/operations/log-view-option/get_log_view_option)

PUT[/log/view/option](https://sonicos-api.sonicwall.com/#/operations/log-view-option/put_log_view_option)

#### [log-syslog](https://sonicos-api.sonicwall.com/\#/log-syslog)      Log syslog base settings API.

GET[/log/syslog/base](https://sonicos-api.sonicwall.com/#/operations/log-syslog/get_log_syslog_base)

PUT[/log/syslog/base](https://sonicos-api.sonicwall.com/#/operations/log-syslog/put_log_syslog_base)

#### [log-syslog-servers](https://sonicos-api.sonicwall.com/\#/log-syslog-servers)      Log syslog server settings API.

GET[/log/syslog/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/get_log_syslog_syslog_servers)

POST[/log/syslog/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/post_log_syslog_syslog_servers)

PUT[/log/syslog/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/put_log_syslog_syslog_servers)

PATCH[/log/syslog/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/patch_log_syslog_syslog_servers)

GET[/log/syslog/syslog-servers/server/{SRVNAME}/port/{PORTID}/profile/{PROID}](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/get_log_syslog_syslog_servers_server__SRVNAME__port__PORTID__profile__PROID_)

PUT[/log/syslog/syslog-servers/server/{SRVNAME}/port/{PORTID}/profile/{PROID}](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/put_log_syslog_syslog_servers_server__SRVNAME__port__PORTID__profile__PROID_)

PATCH[/log/syslog/syslog-servers/server/{SRVNAME}/port/{PORTID}/profile/{PROID}](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/patch_log_syslog_syslog_servers_server__SRVNAME__port__PORTID__profile__PROID_)

DELETE[/log/syslog/syslog-servers/server/{SRVNAME}/port/{PORTID}/profile/{PROID}](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers/delete_log_syslog_syslog_servers_server__SRVNAME__port__PORTID__profile__PROID_)

#### [log-syslog-servers-delete](https://sonicos-api.sonicwall.com/\#/log-syslog-servers-delete)      Delete all syslog servers API.

POST[/log/syslog/servers/delete](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers-delete/post_log_syslog_servers_delete)

#### [log-syslog-servers-enable](https://sonicos-api.sonicwall.com/\#/log-syslog-servers-enable)      Enable all syslog servers API.

POST[/log/syslog/servers/enable](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers-enable/post_log_syslog_servers_enable)

#### [log-syslog-servers-disable](https://sonicos-api.sonicwall.com/\#/log-syslog-servers-disable)      Disable all syslog servers API.

POST[/log/syslog/servers/disable](https://sonicos-api.sonicwall.com/#/operations/log-syslog-servers-disable/post_log_syslog_servers_disable)

#### [log-analyzer](https://sonicos-api.sonicwall.com/\#/log-analyzer)      Log analyzer base settings API.

GET[/log/analyzer/base](https://sonicos-api.sonicwall.com/#/operations/log-analyzer/get_log_analyzer_base)

PUT[/log/analyzer/base](https://sonicos-api.sonicwall.com/#/operations/log-analyzer/put_log_analyzer_base)

#### [log-analyzer-syslog-servers](https://sonicos-api.sonicwall.com/\#/log-analyzer-syslog-servers)      Log analyzer: syslog server settings API.

GET[/log/analyzer/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-analyzer-syslog-servers/get_log_analyzer_syslog_servers)

POST[/log/analyzer/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-analyzer-syslog-servers/post_log_analyzer_syslog_servers)

PUT[/log/analyzer/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-analyzer-syslog-servers/put_log_analyzer_syslog_servers)

PATCH[/log/analyzer/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-analyzer-syslog-servers/patch_log_analyzer_syslog_servers)

#### [log-viewpoint](https://sonicos-api.sonicwall.com/\#/log-viewpoint)      Log viewpoint base settings API.

GET[/log/viewpoint/base](https://sonicos-api.sonicwall.com/#/operations/log-viewpoint/get_log_viewpoint_base)

PUT[/log/viewpoint/base](https://sonicos-api.sonicwall.com/#/operations/log-viewpoint/put_log_viewpoint_base)

#### [log-viewpoint-syslog-servers](https://sonicos-api.sonicwall.com/\#/log-viewpoint-syslog-servers)      Log viewpoint: syslog server settings API.

GET[/log/viewpoint/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-viewpoint-syslog-servers/get_log_viewpoint_syslog_servers)

POST[/log/viewpoint/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-viewpoint-syslog-servers/post_log_viewpoint_syslog_servers)

PUT[/log/viewpoint/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-viewpoint-syslog-servers/put_log_viewpoint_syslog_servers)

PATCH[/log/viewpoint/syslog-servers](https://sonicos-api.sonicwall.com/#/operations/log-viewpoint-syslog-servers/patch_log_viewpoint_syslog_servers)

#### [log-name-resolution](https://sonicos-api.sonicwall.com/\#/log-name-resolution)      Log name resolution congifuration API.

GET[/log/name-resolution/base](https://sonicos-api.sonicwall.com/#/operations/log-name-resolution/get_log_name_resolution_base)

PUT[/log/name-resolution/base](https://sonicos-api.sonicwall.com/#/operations/log-name-resolution/put_log_name_resolution_base)

#### [name-resolution-reset-name-cache](https://sonicos-api.sonicwall.com/\#/name-resolution-reset-name-cache)      Log name resolution reset name cache API.

POST[/log/name-resolution/reset-name-cache](https://sonicos-api.sonicwall.com/#/operations/name-resolution-reset-name-cache/post_log_name_resolution_reset_name_cache)

#### [log-automation](https://sonicos-api.sonicwall.com/\#/log-automation)      Log automation congifuration API.

GET[/log/automation](https://sonicos-api.sonicwall.com/#/operations/log-automation/get_log_automation)

PUT[/log/automation](https://sonicos-api.sonicwall.com/#/operations/log-automation/put_log_automation)

#### [log-global-categories](https://sonicos-api.sonicwall.com/\#/log-global-categories)      Log global categories congifuration API.

GET[/log/global-categories](https://sonicos-api.sonicwall.com/#/operations/log-global-categories/get_log_global_categories)

PUT[/log/global-categories](https://sonicos-api.sonicwall.com/#/operations/log-global-categories/put_log_global_categories)

#### [log-categories](https://sonicos-api.sonicwall.com/\#/log-categories)      Log categories congifuration API.

GET[/log/categories](https://sonicos-api.sonicwall.com/#/operations/log-categories/get_log_categories)

PUT[/log/categories](https://sonicos-api.sonicwall.com/#/operations/log-categories/put_log_categories)

GET[/log/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/log-categories/get_log_categories_name__NAME_)

PUT[/log/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/log-categories/put_log_categories_name__NAME_)

#### [log-category-groups](https://sonicos-api.sonicwall.com/\#/log-category-groups)      Log groups congifuration API.

GET[/log/groups](https://sonicos-api.sonicwall.com/#/operations/log-category-groups/get_log_groups)

PUT[/log/groups](https://sonicos-api.sonicwall.com/#/operations/log-category-groups/put_log_groups)

GET[/log/groups/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/log-category-groups/get_log_groups_id__ID_)

PUT[/log/groups/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/log-category-groups/put_log_groups_id__ID_)

#### [log-category-events](https://sonicos-api.sonicwall.com/\#/log-category-events)      Log events congifuration API.

GET[/log/events](https://sonicos-api.sonicwall.com/#/operations/log-category-events/get_log_events)

PUT[/log/events](https://sonicos-api.sonicwall.com/#/operations/log-category-events/put_log_events)

GET[/log/events/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/log-category-events/get_log_events_id__ID_)

PUT[/log/events/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/log-category-events/put_log_events_id__ID_)

#### [log-display](https://sonicos-api.sonicwall.com/\#/log-display)      Log dispaly settings API.

GET[/log/display](https://sonicos-api.sonicwall.com/#/operations/log-display/get_log_display)

PUT[/log/display](https://sonicos-api.sonicwall.com/#/operations/log-display/put_log_display)

#### [log-aws](https://sonicos-api.sonicwall.com/\#/log-aws)      Log AWS settings API.

GET[/log/aws](https://sonicos-api.sonicwall.com/#/operations/log-aws/get_log_aws)

PUT[/log/aws](https://sonicos-api.sonicwall.com/#/operations/log-aws/put_log_aws)

#### [log-mail-server-test](https://sonicos-api.sonicwall.com/\#/log-mail-server-test)      Test mail server settings API.

POST[/log/mail-server/test](https://sonicos-api.sonicwall.com/#/operations/log-mail-server-test/post_log_mail_server_test)

#### [log-clear-log](https://sonicos-api.sonicwall.com/\#/log-clear-log)      Clear all log entries API.

POST[/log/clear](https://sonicos-api.sonicwall.com/#/operations/log-clear-log/post_log_clear)

#### [log-export-log](https://sonicos-api.sonicwall.com/\#/log-export-log)      Export log in csv or txt format API.

GET[/export/log/txt](https://sonicos-api.sonicwall.com/#/operations/log-export-log/get_export_log_txt)

GET[/export/log/csv](https://sonicos-api.sonicwall.com/#/operations/log-export-log/get_export_log_csv)

#### [log-email-log](https://sonicos-api.sonicwall.com/\#/log-email-log)      Send log to configured email address API.

POST[/log/email-log](https://sonicos-api.sonicwall.com/#/operations/log-email-log/post_log_email_log)

#### [log-save-template](https://sonicos-api.sonicwall.com/\#/log-save-template)      Log save template action API.

POST[/log/save-template/{DESCRIPTION}](https://sonicos-api.sonicwall.com/#/operations/log-save-template/post_log_save_template__DESCRIPTION_)

#### [log-import-template-default](https://sonicos-api.sonicwall.com/\#/log-import-template-default)      Log import default template API.

POST[/log/import-template/default](https://sonicos-api.sonicwall.com/#/operations/log-import-template-default/post_log_import_template_default)

#### [log-import-template-minimal](https://sonicos-api.sonicwall.com/\#/log-import-template-minimal)      Log import minimal template API.

POST[/log/import-template/minimal](https://sonicos-api.sonicwall.com/#/operations/log-import-template-minimal/post_log_import_template_minimal)

#### [log-import-template-analyzer-viewpoint-gms](https://sonicos-api.sonicwall.com/\#/log-import-template-analyzer-viewpoint-gms)      Log import template action API.

POST[/log/import-template/analyzer-viewpoint-gms](https://sonicos-api.sonicwall.com/#/operations/log-import-template-analyzer-viewpoint-gms/post_log_import_template_analyzer_viewpoint_gms)

#### [log-import-template-firewall-action](https://sonicos-api.sonicwall.com/\#/log-import-template-firewall-action)      Log import template action API.

POST[/log/import-template/firewall-action](https://sonicos-api.sonicwall.com/#/operations/log-import-template-firewall-action/post_log_import_template_firewall_action)

#### [log-import-template-custom](https://sonicos-api.sonicwall.com/\#/log-import-template-custom)      Log import template action API.

POST[/log/import-template/custom](https://sonicos-api.sonicwall.com/#/operations/log-import-template-custom/post_log_import_template_custom)

#### [log-reset-event-count-all](https://sonicos-api.sonicwall.com/\#/log-reset-event-count-all)      Log reset event count for all categories action API.

POST[/log/reset/event-count/all](https://sonicos-api.sonicwall.com/#/operations/log-reset-event-count-all/post_log_reset_event_count_all)

#### [log-reset-event-count-event-id](https://sonicos-api.sonicwall.com/\#/log-reset-event-count-event-id)      Log reset event count for specific event API.

POST[/log/reset/event-count/event-id/{EVENTID}](https://sonicos-api.sonicwall.com/#/operations/log-reset-event-count-event-id/post_log_reset_event_count_event_id__EVENTID_)

#### [log-reset-event-count](https://sonicos-api.sonicwall.com/\#/log-reset-event-count)      Log reset event count for specify category or group or event API.

POST[/log/reset/event-count/category/{CATNAME}](https://sonicos-api.sonicwall.com/#/operations/log-reset-event-count/post_log_reset_event_count_category__CATNAME_)

POST[/log/reset/event-count/category/{CATNAME}/group/{GRPNAME}/event/{EVENTNAME}](https://sonicos-api.sonicwall.com/#/operations/log-reset-event-count/post_log_reset_event_count_category__CATNAME__group__GRPNAME__event__EVENTNAME_)

#### [log-disable-event-id](https://sonicos-api.sonicwall.com/\#/log-disable-event-id)      Log reset event count for specific event API.

POST[/log/disable/event-id/{EVENTID}](https://sonicos-api.sonicwall.com/#/operations/log-disable-event-id/post_log_disable_event_id__EVENTID_)

#### [log-view-status](https://sonicos-api.sonicwall.com/\#/log-view-status)      Log view status reporting API.

GET[/reporting/log/view-status](https://sonicos-api.sonicwall.com/#/operations/log-view-status/get_reporting_log_view_status)

#### [log-view](https://sonicos-api.sonicwall.com/\#/log-view)      Log view reporting API.

GET[/reporting/log/view](https://sonicos-api.sonicwall.com/#/operations/log-view/get_reporting_log_view)

GET[/reporting/log/view/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/log-view/get_reporting_log_view_id__ID_)

#### [log-categories-statistics](https://sonicos-api.sonicwall.com/\#/log-categories-statistics)      Log categories reporting API.

GET[/reporting/log/categories](https://sonicos-api.sonicwall.com/#/operations/log-categories-statistics/get_reporting_log_categories)

GET[/reporting/log/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/log-categories-statistics/get_reporting_log_categories_name__NAME_)

#### [log-aws-status](https://sonicos-api.sonicwall.com/\#/log-aws-status)      Log AWS reporting API.

GET[/reporting/log/aws](https://sonicos-api.sonicwall.com/#/operations/log-aws-status/get_reporting_log_aws)

#### [export-sdwan-conn-log](https://sonicos-api.sonicwall.com/\#/export-sdwan-conn-log)      Export sdwan connection logs in csv or txt format API.

GET[/{INDEX}](https://sonicos-api.sonicwall.com/#/operations/export-sdwan-conn-log/get__INDEX_)

GET[/export/sdwan-conn-logs/{INDEX}](https://sonicos-api.sonicwall.com/#/operations/export-sdwan-conn-log/get_export_sdwan_conn_logs__INDEX_)

GET[/export/sdwan-conn-logs/csv](https://sonicos-api.sonicwall.com/#/operations/export-sdwan-conn-log/get_export_sdwan_conn_logs_csv)

GET[/export/sdwan-conn-logs/txt](https://sonicos-api.sonicwall.com/#/operations/export-sdwan-conn-log/get_export_sdwan_conn_logs_txt)

#### [log-reports-start](https://sonicos-api.sonicwall.com/\#/log-reports-start)      Log reports start data connection.

POST[/log/reports/start](https://sonicos-api.sonicwall.com/#/operations/log-reports-start/post_log_reports_start)

#### [log-reports-stop](https://sonicos-api.sonicwall.com/\#/log-reports-stop)      Log reports stop data connection.

POST[/log/reports/stop](https://sonicos-api.sonicwall.com/#/operations/log-reports-stop/post_log_reports_stop)

#### [log-reports-report-refresh](https://sonicos-api.sonicwall.com/\#/log-reports-report-refresh)      Log reports Refresh data.

POST[/log/reports/report-refresh](https://sonicos-api.sonicwall.com/#/operations/log-reports-report-refresh/post_log_reports_report_refresh)

#### [log-reports-report-reset](https://sonicos-api.sonicwall.com/\#/log-reports-report-reset)      Log reports reset data.

POST[/log/reports/report-reset](https://sonicos-api.sonicwall.com/#/operations/log-reports-report-reset/post_log_reports_report_reset)

#### [log-audit-view](https://sonicos-api.sonicwall.com/\#/log-audit-view)      Show audit records.

GET[/log/audit/view](https://sonicos-api.sonicwall.com/#/operations/log-audit-view/get_log_audit_view)

#### [time](https://sonicos-api.sonicwall.com/\#/time)      Time base settings API.

GET[/time/base](https://sonicos-api.sonicwall.com/#/operations/time/get_time_base)

PUT[/time/base](https://sonicos-api.sonicwall.com/#/operations/time/put_time_base)

#### [time-ntp-servers](https://sonicos-api.sonicwall.com/\#/time-ntp-servers)      Time NTP servers API.

GET[/time/ntp-servers](https://sonicos-api.sonicwall.com/#/operations/time-ntp-servers/get_time_ntp_servers)

POST[/time/ntp-servers](https://sonicos-api.sonicwall.com/#/operations/time-ntp-servers/post_time_ntp_servers)

PUT[/time/ntp-servers](https://sonicos-api.sonicwall.com/#/operations/time-ntp-servers/put_time_ntp_servers)

GET[/time/ntp-servers/name/{NTPNAME}](https://sonicos-api.sonicwall.com/#/operations/time-ntp-servers/get_time_ntp_servers_name__NTPNAME_)

PUT[/time/ntp-servers/name/{NTPNAME}](https://sonicos-api.sonicwall.com/#/operations/time-ntp-servers/put_time_ntp_servers_name__NTPNAME_)

DELETE[/time/ntp-servers/name/{NTPNAME}](https://sonicos-api.sonicwall.com/#/operations/time-ntp-servers/delete_time_ntp_servers_name__NTPNAME_)

#### [firewall](https://sonicos-api.sonicwall.com/\#/firewall)      Firewall configuration API.

GET[/firewall](https://sonicos-api.sonicwall.com/#/operations/firewall/get_firewall)

PUT[/firewall](https://sonicos-api.sonicwall.com/#/operations/firewall/put_firewall)

#### [firewall-status](https://sonicos-api.sonicwall.com/\#/firewall-status)      Firewall connection status reporting API.

GET[/reporting/firewall/connection-status](https://sonicos-api.sonicwall.com/#/operations/firewall-status/get_reporting_firewall_connection_status)

#### [firewall-deregister](https://sonicos-api.sonicwall.com/\#/firewall-deregister)      Deregistering the firewall.

POST[/deregister/firewall](https://sonicos-api.sonicwall.com/#/operations/firewall-deregister/post_deregister_firewall)

#### [diag-purge-coredump](https://sonicos-api.sonicwall.com/\#/diag-purge-coredump)      Purge all coredump files.

POST[/diag/purge/coredump](https://sonicos-api.sonicwall.com/#/operations/diag-purge-coredump/post_diag_purge_coredump)

#### [diag-acm-filter-reset](https://sonicos-api.sonicwall.com/\#/diag-acm-filter-reset)      Reset active connection monitor filter.

POST[/diag/acm-filter/reset](https://sonicos-api.sonicwall.com/#/operations/diag-acm-filter-reset/post_diag_acm_filter_reset)

#### [diag-acm-filter](https://sonicos-api.sonicwall.com/\#/diag-acm-filter)      Set Connection Monitor Filter.

PUT[/diag/acm-filter/apply](https://sonicos-api.sonicwall.com/#/operations/diag-acm-filter/put_diag_acm_filter_apply)

#### [packet-monitor](https://sonicos-api.sonicwall.com/\#/packet-monitor)      Packet monitor base settings API.

GET[/packet-monitor/base](https://sonicos-api.sonicwall.com/#/operations/packet-monitor/get_packet_monitor_base)

PUT[/packet-monitor/base](https://sonicos-api.sonicwall.com/#/operations/packet-monitor/put_packet_monitor_base)

#### [packet-monitor-log-to-ftp](https://sonicos-api.sonicwall.com/\#/packet-monitor-log-to-ftp)      Packet monitor log to FTP server API.

POST[/packet-monitor/log-to-ftp](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-log-to-ftp/post_packet_monitor_log_to_ftp)

#### [packet-monitor-monitor-all](https://sonicos-api.sonicwall.com/\#/packet-monitor-monitor-all)      Packet monitor monitor all API.

POST[/packet-monitor/monitor/all](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-monitor-all/post_packet_monitor_monitor_all)

#### [packet-monitor-monitor-default](https://sonicos-api.sonicwall.com/\#/packet-monitor-monitor-default)      Packet monitor monitor default API.

POST[/packet-monitor/monitor/default](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-monitor-default/post_packet_monitor_monitor_default)

#### [packet-monitor-start-capture](https://sonicos-api.sonicwall.com/\#/packet-monitor-start-capture)      Start packet capture API.

POST[/packet-monitor/start/capture](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-start-capture/post_packet_monitor_start_capture)

#### [packet-monitor-start-mirror](https://sonicos-api.sonicwall.com/\#/packet-monitor-start-mirror)      Start mirror API.

POST[/packet-monitor/start/mirror](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-start-mirror/post_packet_monitor_start_mirror)

#### [packet-monitor-stop-capture](https://sonicos-api.sonicwall.com/\#/packet-monitor-stop-capture)      Stop packet capture API.

POST[/packet-monitor/stop/capture](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-stop-capture/post_packet_monitor_stop_capture)

#### [packet-monitor-stop-mirror](https://sonicos-api.sonicwall.com/\#/packet-monitor-stop-mirror)      Stop mirror API.

POST[/packet-monitor/stop/mirror](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-stop-mirror/post_packet_monitor_stop_mirror)

#### [packet-monitor-capture](https://sonicos-api.sonicwall.com/\#/packet-monitor-capture)      Packet monitor clear capture API.

POST[/packet-monitor/capture](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-capture/post_packet_monitor_capture)

#### [export-captured-packets](https://sonicos-api.sonicwall.com/\#/export-captured-packets)      Export captured packets from the device.

GET[/export/captured-packets/libpcap](https://sonicos-api.sonicwall.com/#/operations/export-captured-packets/get_export_captured_packets_libpcap)

GET[/export/captured-packets/html](https://sonicos-api.sonicwall.com/#/operations/export-captured-packets/get_export_captured_packets_html)

GET[/export/captured-packets/text](https://sonicos-api.sonicwall.com/#/operations/export-captured-packets/get_export_captured_packets_text)

GET[/export/captured-packets/pcapng](https://sonicos-api.sonicwall.com/#/operations/export-captured-packets/get_export_captured_packets_pcapng)

GET[/export/captured-packets/app-data](https://sonicos-api.sonicwall.com/#/operations/export-captured-packets/get_export_captured_packets_app_data)

#### [packet-monitor-statistics](https://sonicos-api.sonicwall.com/\#/packet-monitor-statistics)      Packet monitor reporting API.

GET[/reporting/packet-monitor/statistics](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-statistics/get_reporting_packet_monitor_statistics)

#### [packet-monitor-trace-config](https://sonicos-api.sonicwall.com/\#/packet-monitor-trace-config)      Packet monitor reporting API.

GET[/reporting/packet-monitor/trace-config](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-trace-config/get_reporting_packet_monitor_trace_config)

#### [standby-trace](https://sonicos-api.sonicwall.com/\#/standby-trace)      Packet monitor standby trace settings API.

PUT[/packet-monitor/standby-trace](https://sonicos-api.sonicwall.com/#/operations/standby-trace/put_packet_monitor_standby_trace)

#### [packet-monitor-standby-default-trace](https://sonicos-api.sonicwall.com/\#/packet-monitor-standby-default-trace)      Default standby monitor API.

POST[/packet-monitor/standby-default-trace](https://sonicos-api.sonicwall.com/#/operations/packet-monitor-standby-default-trace/post_packet_monitor_standby_default_trace)

#### [tsr-options](https://sonicos-api.sonicwall.com/\#/tsr-options)      Tech support report options configuration API.

GET[/tech-support-report/options](https://sonicos-api.sonicwall.com/#/operations/tsr-options/get_tech_support_report_options)

PUT[/tech-support-report/options](https://sonicos-api.sonicwall.com/#/operations/tsr-options/put_tech_support_report_options)

#### [tsr-secure-send](https://sonicos-api.sonicwall.com/\#/tsr-secure-send)      Send tech support report to MySonicwall API.

POST[/tech-support-report/send](https://sonicos-api.sonicwall.com/#/operations/tsr-secure-send/post_tech_support_report_send)

#### [certificates-generate-signing-request](https://sonicos-api.sonicwall.com/\#/certificates-generate-signing-request)      Certificate signing request configuration API.

POST[/certificates/generate-signing-request](https://sonicos-api.sonicwall.com/#/operations/certificates-generate-signing-request/post_certificates_generate_signing_request)

#### [certificates-scep](https://sonicos-api.sonicwall.com/\#/certificates-scep)      Simple certificate enrollment protocol configuration API.

POST[/certificates/scep](https://sonicos-api.sonicwall.com/#/operations/certificates-scep/post_certificates_scep)

#### [certificates-no-enrollment](https://sonicos-api.sonicwall.com/\#/certificates-no-enrollment)      Stop enrollment for signing request API.

DELETE[/certificates/enrollment](https://sonicos-api.sonicwall.com/#/operations/certificates-no-enrollment/delete_certificates_enrollment)

#### [certificates-export-signing-request](https://sonicos-api.sonicwall.com/\#/certificates-export-signing-request)      Export certificate signing request.

GET[/export/certificates/signing-request/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/certificates-export-signing-request/get_export_certificates_signing_request_name__NAME_)

#### [certificates-export-cert-key-pair](https://sonicos-api.sonicwall.com/\#/certificates-export-cert-key-pair)      Export certificate signing request or certificate / key pair API.

GET[/export/certificates/cert-key-pair/name/{NAME}/password/{PASSWD}](https://sonicos-api.sonicwall.com/#/operations/certificates-export-cert-key-pair/get_export_certificates_cert_key_pair_name__NAME__password__PASSWD_)

#### [certificates-import-cert-key-pair](https://sonicos-api.sonicwall.com/\#/certificates-import-cert-key-pair)      Import certificate signing request or certificate / key pair API.

PUT[/import/certificates/cert-key-pair/name/{NAME}/password/{PASSWD}](https://sonicos-api.sonicwall.com/#/operations/certificates-import-cert-key-pair/put_import_certificates_cert_key_pair_name__NAME__password__PASSWD_)

#### [certificates-import-ca-cert](https://sonicos-api.sonicwall.com/\#/certificates-import-ca-cert)      Import CA certificate API.

PUT[/import/certificates/ca-cert](https://sonicos-api.sonicwall.com/#/operations/certificates-import-ca-cert/put_import_certificates_ca_cert)

#### [certificates-import-signed-cert](https://sonicos-api.sonicwall.com/\#/certificates-import-signed-cert)      Import CA signed certificate API.

PUT[/import/certificates/signed-cert/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/certificates-import-signed-cert/put_import_certificates_signed_cert_name__NAME_)

#### [certificates-import-crl](https://sonicos-api.sonicwall.com/\#/certificates-import-crl)      Import certificate revocation list or set the location to periodically download via HTTP.

POST[/certificates/import/crl/ca-name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl/post_certificates_import_crl_ca_name__NAME_)

POST[/certificates/import/crl/ca-name/{NAME}/invalidate-certificates](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl/post_certificates_import_crl_ca_name__NAME__invalidate_certificates)

POST[/certificates/import/crl/ca-name/{NAME}/disable-invalidate-certificates](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl/post_certificates_import_crl_ca_name__NAME__disable_invalidate_certificates)

#### [certificates-import-crl-periodically](https://sonicos-api.sonicwall.com/\#/certificates-import-crl-periodically)      Periodically auto-import certificate revocation list via HTTP.

POST[/certificates/import/crl-periodically/ca-name/{NAME}/url/{CRLURL}](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl-periodically/post_certificates_import_crl_periodically_ca_name__NAME__url__CRLURL_)

POST[/certificates/import/crl-periodically/ca-name/{NAME}/url/{CRLURL}/invalidate-certificates](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl-periodically/post_certificates_import_crl_periodically_ca_name__NAME__url__CRLURL__invalidate_certificates)

POST[/certificates/import/crl-periodically/ca-name/{NAME}/url/{CRLURL}/disable-invalidate-certificates](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl-periodically/post_certificates_import_crl_periodically_ca_name__NAME__url__CRLURL__disable_invalidate_certificates)

#### [certificates-import-crl-directly](https://sonicos-api.sonicwall.com/\#/certificates-import-crl-directly)      Import certificate revocation list directly by API.

PUT[/import/certificates/crl-directly/ca-name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl-directly/put_import_certificates_crl_directly_ca_name__NAME_)

PUT[/import/certificates/crl-directly/ca-name/{NAME}/disable-invalidate-certificates](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl-directly/put_import_certificates_crl_directly_ca_name__NAME__disable_invalidate_certificates)

PUT[/import/certificates/crl-directly/ca-name/{NAME}/invalidate-certificates](https://sonicos-api.sonicwall.com/#/operations/certificates-import-crl-directly/put_import_certificates_crl_directly_ca_name__NAME__invalidate_certificates)

#### [certificates-no-certificate](https://sonicos-api.sonicwall.com/\#/certificates-no-certificate)      Delete signing request or certificate / key pair API.

DELETE[/certificates/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/certificates-no-certificate/delete_certificates_name__NAME_)

#### [certificates-no-ca-certificate](https://sonicos-api.sonicwall.com/\#/certificates-no-ca-certificate)      Delete CA certificate API.

DELETE[/certificates/ca/{CAHASH}](https://sonicos-api.sonicwall.com/#/operations/certificates-no-ca-certificate/delete_certificates_ca__CAHASH_)

#### [certificate](https://sonicos-api.sonicwall.com/\#/certificate)      Certificate reporting API.

GET[/reporting/certificates](https://sonicos-api.sonicwall.com/#/operations/certificate/get_reporting_certificates)

GET[/reporting/certificates/imported](https://sonicos-api.sonicwall.com/#/operations/certificate/get_reporting_certificates_imported)

GET[/reporting/certificates/build-in/with-expired](https://sonicos-api.sonicwall.com/#/operations/certificate/get_reporting_certificates_build_in_with_expired)

GET[/reporting/certificates/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/certificate/get_reporting_certificates_name__NAME_)

#### [snmp](https://sonicos-api.sonicwall.com/\#/snmp)      SNMP configuration API.

GET[/snmp/base](https://sonicos-api.sonicwall.com/#/operations/snmp/get_snmp_base)

PUT[/snmp/base](https://sonicos-api.sonicwall.com/#/operations/snmp/put_snmp_base)

#### [snmp-view](https://sonicos-api.sonicwall.com/\#/snmp-view)      SNMP view OID lists configuration API.

GET[/snmp/views](https://sonicos-api.sonicwall.com/#/operations/snmp-view/get_snmp_views)

POST[/snmp/views](https://sonicos-api.sonicwall.com/#/operations/snmp-view/post_snmp_views)

#### [snmp-user](https://sonicos-api.sonicwall.com/\#/snmp-user)      SNMP users configuration API.

GET[/snmp/users](https://sonicos-api.sonicwall.com/#/operations/snmp-user/get_snmp_users)

POST[/snmp/users](https://sonicos-api.sonicwall.com/#/operations/snmp-user/post_snmp_users)

PUT[/snmp/users](https://sonicos-api.sonicwall.com/#/operations/snmp-user/put_snmp_users)

PATCH[/snmp/users](https://sonicos-api.sonicwall.com/#/operations/snmp-user/patch_snmp_users)

GET[/snmp/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-user/get_snmp_users_name__NAME_)

PUT[/snmp/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-user/put_snmp_users_name__NAME_)

PATCH[/snmp/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-user/patch_snmp_users_name__NAME_)

DELETE[/snmp/users/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-user/delete_snmp_users_name__NAME_)

#### [snmp-group](https://sonicos-api.sonicwall.com/\#/snmp-group)      SNMP groups configuration API.

GET[/snmp/groups](https://sonicos-api.sonicwall.com/#/operations/snmp-group/get_snmp_groups)

POST[/snmp/groups](https://sonicos-api.sonicwall.com/#/operations/snmp-group/post_snmp_groups)

PUT[/snmp/groups](https://sonicos-api.sonicwall.com/#/operations/snmp-group/put_snmp_groups)

PATCH[/snmp/groups](https://sonicos-api.sonicwall.com/#/operations/snmp-group/patch_snmp_groups)

GET[/snmp/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-group/get_snmp_groups_name__NAME_)

PUT[/snmp/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-group/put_snmp_groups_name__NAME_)

PATCH[/snmp/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-group/patch_snmp_groups_name__NAME_)

DELETE[/snmp/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-group/delete_snmp_groups_name__NAME_)

#### [snmp-access](https://sonicos-api.sonicwall.com/\#/snmp-access)      SNMP accesss configuration API.

GET[/snmp/accesses](https://sonicos-api.sonicwall.com/#/operations/snmp-access/get_snmp_accesses)

POST[/snmp/accesses](https://sonicos-api.sonicwall.com/#/operations/snmp-access/post_snmp_accesses)

PUT[/snmp/accesses](https://sonicos-api.sonicwall.com/#/operations/snmp-access/put_snmp_accesses)

PATCH[/snmp/accesses](https://sonicos-api.sonicwall.com/#/operations/snmp-access/patch_snmp_accesses)

GET[/snmp/accesses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-access/get_snmp_accesses_name__NAME_)

PUT[/snmp/accesses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-access/put_snmp_accesses_name__NAME_)

PATCH[/snmp/accesses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-access/patch_snmp_accesses_name__NAME_)

DELETE[/snmp/accesses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/snmp-access/delete_snmp_accesses_name__NAME_)

#### [license](https://sonicos-api.sonicwall.com/\#/license)      License configuration API.

GET[/license/base](https://sonicos-api.sonicwall.com/#/operations/license/get_license_base)

PUT[/license/base](https://sonicos-api.sonicwall.com/#/operations/license/put_license_base)

#### [license-register-code](https://sonicos-api.sonicwall.com/\#/license-register-code)      License register code config API.

GET[/license/registration-code](https://sonicos-api.sonicwall.com/#/operations/license-register-code/get_license_registration_code)

PUT[/license/registration-code](https://sonicos-api.sonicwall.com/#/operations/license-register-code/put_license_registration_code)

#### [license-synchronize](https://sonicos-api.sonicwall.com/\#/license-synchronize)      Synchronize licenses with www.mysonicwall.com action schema API.

POST[/license/synchronize](https://sonicos-api.sonicwall.com/#/operations/license-synchronize/post_license_synchronize)

#### [license-status](https://sonicos-api.sonicwall.com/\#/license-status)      License reporting API.

GET[/reporting/license](https://sonicos-api.sonicwall.com/#/operations/license-status/get_reporting_license)

GET[/reporting/license/security-services](https://sonicos-api.sonicwall.com/#/operations/license-status/get_reporting_license_security_services)

#### [ssh-server](https://sonicos-api.sonicwall.com/\#/ssh-server)      SSH server configuration API.

GET[/ssh/server/base](https://sonicos-api.sonicwall.com/#/operations/ssh-server/get_ssh_server_base)

PUT[/ssh/server/base](https://sonicos-api.sonicwall.com/#/operations/ssh-server/put_ssh_server_base)

#### [ssh-server-keygen](https://sonicos-api.sonicwall.com/\#/ssh-server-keygen)      Generate authentication keys for SSH API.

POST[/ssh/server/keygen](https://sonicos-api.sonicwall.com/#/operations/ssh-server-keygen/post_ssh_server_keygen)

#### [ssh-server-restart](https://sonicos-api.sonicwall.com/\#/ssh-server-restart)      Restart SSH server API.

POST[/ssh/server/restart](https://sonicos-api.sonicwall.com/#/operations/ssh-server-restart/post_ssh_server_restart)

#### [ssh-server-enable](https://sonicos-api.sonicwall.com/\#/ssh-server-enable)      Enable SSH server API.

POST[/ssh/server/enable](https://sonicos-api.sonicwall.com/#/operations/ssh-server-enable/post_ssh_server_enable)

#### [ssh-server-terminate](https://sonicos-api.sonicwall.com/\#/ssh-server-terminate)      Disable SSH access and terminate all SSH sessions API.

POST[/ssh/server/terminate](https://sonicos-api.sonicwall.com/#/operations/ssh-server-terminate/post_ssh_server_terminate)

#### [ssh-server-kill-session](https://sonicos-api.sonicwall.com/\#/ssh-server-kill-session)      Terminate specified SSH session API.

POST[/ssh/server/kill/sessions](https://sonicos-api.sonicwall.com/#/operations/ssh-server-kill-session/post_ssh_server_kill_sessions)

POST[/ssh/server/kill/sessions/ip/{IP}/port/{PORT}](https://sonicos-api.sonicwall.com/#/operations/ssh-server-kill-session/post_ssh_server_kill_sessions_ip__IP__port__PORT_)

#### [ssh-server-sessions](https://sonicos-api.sonicwall.com/\#/ssh-server-sessions)      SSH server sessions reporting API.

GET[/reporting/ssh/server/sessions](https://sonicos-api.sonicwall.com/#/operations/ssh-server-sessions/get_reporting_ssh_server_sessions)

#### [version](https://sonicos-api.sonicwall.com/\#/version)      Version configuration API.

GET[/version](https://sonicos-api.sonicwall.com/#/operations/version/get_version)

#### [fips](https://sonicos-api.sonicwall.com/\#/fips)      fips configuration API.

GET[/fips](https://sonicos-api.sonicwall.com/#/operations/fips/get_fips)

PUT[/fips](https://sonicos-api.sonicwall.com/#/operations/fips/put_fips)

#### [ndpp](https://sonicos-api.sonicwall.com/\#/ndpp)      ndpp configuration API.

GET[/ndpp](https://sonicos-api.sonicwall.com/#/operations/ndpp/get_ndpp)

PUT[/ndpp](https://sonicos-api.sonicwall.com/#/operations/ndpp/put_ndpp)

#### [log-audit](https://sonicos-api.sonicwall.com/\#/log-audit)      configuration auditing settings API.

GET[/log/audit/base](https://sonicos-api.sonicwall.com/#/operations/log-audit/get_log_audit_base)

PUT[/log/audit/base](https://sonicos-api.sonicwall.com/#/operations/log-audit/put_log_audit_base)

#### [log-export-audit](https://sonicos-api.sonicwall.com/\#/log-export-audit)      Export auditing records in csv or txt format API.

GET[/export/audit/csv](https://sonicos-api.sonicwall.com/#/operations/log-export-audit/get_export_audit_csv)

GET[/export/audit/txt](https://sonicos-api.sonicwall.com/#/operations/log-export-audit/get_export_audit_txt)

#### [log-email-audit](https://sonicos-api.sonicwall.com/\#/log-email-audit)      Send auditing records to configured email address API.

POST[/log/email-audit](https://sonicos-api.sonicwall.com/#/operations/log-email-audit/post_log_email_audit)

#### [arp-base](https://sonicos-api.sonicwall.com/\#/arp-base)      ARP base configuration API endpoint.

GET[/arp/base](https://sonicos-api.sonicwall.com/#/operations/arp-base/get_arp_base)

PUT[/arp/base](https://sonicos-api.sonicwall.com/#/operations/arp-base/put_arp_base)

#### [arp-entries](https://sonicos-api.sonicwall.com/\#/arp-entries)      ARP entries configuration API endpoint.

GET[/arp/entries](https://sonicos-api.sonicwall.com/#/operations/arp-entries/get_arp_entries)

POST[/arp/entries](https://sonicos-api.sonicwall.com/#/operations/arp-entries/post_arp_entries)

PUT[/arp/entries](https://sonicos-api.sonicwall.com/#/operations/arp-entries/put_arp_entries)

PATCH[/arp/entries](https://sonicos-api.sonicwall.com/#/operations/arp-entries/patch_arp_entries)

GET[/arp/entries/ip/{IP}/mac/{MAC}/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/arp-entries/get_arp_entries_ip__IP__mac__MAC__interface__INTERFACENAME_)

PUT[/arp/entries/ip/{IP}/mac/{MAC}/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/arp-entries/put_arp_entries_ip__IP__mac__MAC__interface__INTERFACENAME_)

PATCH[/arp/entries/ip/{IP}/mac/{MAC}/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/arp-entries/patch_arp_entries_ip__IP__mac__MAC__interface__INTERFACENAME_)

DELETE[/arp/entries/ip/{IP}/mac/{MAC}/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/arp-entries/delete_arp_entries_ip__IP__mac__MAC__interface__INTERFACENAME_)

#### [arp-caches](https://sonicos-api.sonicwall.com/\#/arp-caches)      ARP cache reporting API.

GET[/reporting/arp/caches](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches)

GET[/reporting/arp/caches/sort-by/mac-address](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_mac_address)

GET[/reporting/arp/caches/sort-by/vendor](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_vendor)

GET[/reporting/arp/caches/sort-by/inverted](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_inverted)

GET[/reporting/arp/caches/sort-by/timeout](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_timeout)

GET[/reporting/arp/caches/sort-by/interface](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_interface)

GET[/reporting/arp/caches/sort-by/ip-address](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_ip_address)

GET[/reporting/arp/caches/sort-by/type](https://sonicos-api.sonicwall.com/#/operations/arp-caches/get_reporting_arp_caches_sort_by_type)

#### [arp-cache](https://sonicos-api.sonicwall.com/\#/arp-cache)      ARP cache reporting API.

GET[/reporting/arp/cache/ip/{IP}/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/arp-cache/get_reporting_arp_cache_ip__IP__interface__INTERFACENAME_)

DELETE[/reporting/arp/cache/ip/{IP}/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/arp-cache/delete_reporting_arp_cache_ip__IP__interface__INTERFACENAME_)

#### [arp-statistics](https://sonicos-api.sonicwall.com/\#/arp-statistics)      ARP statistics reporting API.

GET[/reporting/arp/statistics](https://sonicos-api.sonicwall.com/#/operations/arp-statistics/get_reporting_arp_statistics)

#### [arp-entries-status](https://sonicos-api.sonicwall.com/\#/arp-entries-status)      ARP static entries status reporting API.

GET[/reporting/arp/entries/status](https://sonicos-api.sonicwall.com/#/operations/arp-entries-status/get_reporting_arp_entries_status)

#### [dns](https://sonicos-api.sonicwall.com/\#/dns)      DNS configuration API.

GET[/dns/base](https://sonicos-api.sonicwall.com/#/operations/dns/get_dns_base)

PUT[/dns/base](https://sonicos-api.sonicwall.com/#/operations/dns/put_dns_base)

#### [dns-split-entry](https://sonicos-api.sonicwall.com/\#/dns-split-entry)      DNS split DNS entry object configuration API.

GET[/dns/split-entries](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/get_dns_split_entries)

POST[/dns/split-entries](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/post_dns_split_entries)

PUT[/dns/split-entries](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/put_dns_split_entries)

PATCH[/dns/split-entries](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/patch_dns_split_entries)

GET[/dns/split-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/get_dns_split_entries_domain__NAME_)

PUT[/dns/split-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/put_dns_split_entries_domain__NAME_)

PATCH[/dns/split-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/patch_dns_split_entries_domain__NAME_)

DELETE[/dns/split-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-split-entry/delete_dns_split_entries_domain__NAME_)

#### [dns-cache](https://sonicos-api.sonicwall.com/\#/dns-cache)      DNS reporting API.

GET[/reporting/dns/cache](https://sonicos-api.sonicwall.com/#/operations/dns-cache/get_reporting_dns_cache)

GET[/reporting/dns/cache/interface-reverse](https://sonicos-api.sonicwall.com/#/operations/dns-cache/get_reporting_dns_cache_interface_reverse)

#### [dns-wan-ipv4](https://sonicos-api.sonicwall.com/\#/dns-wan-ipv4)      IPv4 WAN DNS reporting API.

GET[/reporting/dns/wan/ipv4](https://sonicos-api.sonicwall.com/#/operations/dns-wan-ipv4/get_reporting_dns_wan_ipv4)

#### [dns-wan-ipv6](https://sonicos-api.sonicwall.com/\#/dns-wan-ipv6)      IPv6 WAN DNS reporting API.

GET[/reporting/dns/wan/ipv6](https://sonicos-api.sonicwall.com/#/operations/dns-wan-ipv6/get_reporting_dns_wan_ipv6)

#### [dynamic-dns-profile-ipv4](https://sonicos-api.sonicwall.com/\#/dynamic-dns-profile-ipv4)      IPv4 Dynamic DNS profiles configuration API.

GET[/dynamic-dns/profiles/ipv4](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/get_dynamic_dns_profiles_ipv4)

POST[/dynamic-dns/profiles/ipv4](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/post_dynamic_dns_profiles_ipv4)

PUT[/dynamic-dns/profiles/ipv4](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/put_dynamic_dns_profiles_ipv4)

PATCH[/dynamic-dns/profiles/ipv4](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/patch_dynamic_dns_profiles_ipv4)

GET[/dynamic-dns/profiles/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/get_dynamic_dns_profiles_ipv4_name__NAME_)

PUT[/dynamic-dns/profiles/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/put_dynamic_dns_profiles_ipv4_name__NAME_)

PATCH[/dynamic-dns/profiles/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/patch_dynamic_dns_profiles_ipv4_name__NAME_)

DELETE[/dynamic-dns/profiles/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv4/delete_dynamic_dns_profiles_ipv4_name__NAME_)

#### [dynamic-dns-profile-ipv6](https://sonicos-api.sonicwall.com/\#/dynamic-dns-profile-ipv6)      IPv6 Dynamic DNS profiles configuration API.

GET[/dynamic-dns/profiles/ipv6](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/get_dynamic_dns_profiles_ipv6)

POST[/dynamic-dns/profiles/ipv6](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/post_dynamic_dns_profiles_ipv6)

PUT[/dynamic-dns/profiles/ipv6](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/put_dynamic_dns_profiles_ipv6)

PATCH[/dynamic-dns/profiles/ipv6](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/patch_dynamic_dns_profiles_ipv6)

GET[/dynamic-dns/profiles/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/get_dynamic_dns_profiles_ipv6_name__NAME_)

PUT[/dynamic-dns/profiles/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/put_dynamic_dns_profiles_ipv6_name__NAME_)

PATCH[/dynamic-dns/profiles/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/patch_dynamic_dns_profiles_ipv6_name__NAME_)

DELETE[/dynamic-dns/profiles/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-ipv6/delete_dynamic_dns_profiles_ipv6_name__NAME_)

#### [dynamic-dns-profile-status-ipv6](https://sonicos-api.sonicwall.com/\#/dynamic-dns-profile-status-ipv6)      IPv6 Dynamic DNS profiles status reporting API.

GET[/reporting/dynamic-dns/profiles/ipv6](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-status-ipv6/get_reporting_dynamic_dns_profiles_ipv6)

GET[/reporting/dynamic-dns/profiles/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-status-ipv6/get_reporting_dynamic_dns_profiles_ipv6_name__NAME_)

#### [dynamic-dns-profile-status-ipv4](https://sonicos-api.sonicwall.com/\#/dynamic-dns-profile-status-ipv4)      IPv4 Dynamic DNS profile reporting API.

GET[/reporting/dynamic-dns/profiles/ipv4](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-status-ipv4/get_reporting_dynamic_dns_profiles_ipv4)

GET[/reporting/dynamic-dns/profiles/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dynamic-dns-profile-status-ipv4/get_reporting_dynamic_dns_profiles_ipv4_name__NAME_)

#### [flb](https://sonicos-api.sonicwall.com/\#/flb)      Failover load balancing configuration API.

GET[/failover-lb/base](https://sonicos-api.sonicwall.com/#/operations/flb/get_failover_lb_base)

PUT[/failover-lb/base](https://sonicos-api.sonicwall.com/#/operations/flb/put_failover_lb_base)

#### [flb-group](https://sonicos-api.sonicwall.com/\#/flb-group)      Failover load balancing group object configuration API.

GET[/failover-lb/groups](https://sonicos-api.sonicwall.com/#/operations/flb-group/get_failover_lb_groups)

PUT[/failover-lb/groups](https://sonicos-api.sonicwall.com/#/operations/flb-group/put_failover_lb_groups)

GET[/failover-lb/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-group/get_failover_lb_groups_name__NAME_)

PUT[/failover-lb/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-group/put_failover_lb_groups_name__NAME_)

DELETE[/failover-lb/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-group/delete_failover_lb_groups_name__NAME_)

#### [flb-group-auto-adjust-ratio](https://sonicos-api.sonicwall.com/\#/flb-group-auto-adjust-ratio)      Automatically adjust all member ratios so total is 100% API.

PUT[/failover-lb/group-auto-adjust-ratio/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-group-auto-adjust-ratio/put_failover_lb_group_auto_adjust_ratio_name__NAME_)

#### [flb-group-member-percent](https://sonicos-api.sonicwall.com/\#/flb-group-member-percent)      Set the member usage percent for the interface API.

PUT[/failover-lb/group-member-percent/name/{NAME}/interface/{IFNAME}/{PERCENT}](https://sonicos-api.sonicwall.com/#/operations/flb-group-member-percent/put_failover_lb_group_member_percent_name__NAME__interface__IFNAME___PERCENT_)

#### [flb-statistics](https://sonicos-api.sonicwall.com/\#/flb-statistics)      Failover load balancing statistics reporting API.

GET[/reporting/failover-lb/statistics](https://sonicos-api.sonicwall.com/#/operations/flb-statistics/get_reporting_failover_lb_statistics)

GET[/reporting/failover-lb/statistics/group/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-statistics/get_reporting_failover_lb_statistics_group__NAME_)

#### [flb-responder](https://sonicos-api.sonicwall.com/\#/flb-responder)      Failover load balancing responder reporting API.

GET[/reporting/failover-lb/responder](https://sonicos-api.sonicwall.com/#/operations/flb-responder/get_reporting_failover_lb_responder)

#### [flb-status-group](https://sonicos-api.sonicwall.com/\#/flb-status-group)      Failover load balancing groups status reporting API.

GET[/reporting/failover-lb/status/groups](https://sonicos-api.sonicwall.com/#/operations/flb-status-group/get_reporting_failover_lb_status_groups)

GET[/reporting/failover-lb/status/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-status-group/get_reporting_failover_lb_status_groups_name__NAME_)

#### [flb-status-member](https://sonicos-api.sonicwall.com/\#/flb-status-member)      Failover load balancing members status reporting API.

GET[/reporting/failover-lb/status/members](https://sonicos-api.sonicwall.com/#/operations/flb-status-member/get_reporting_failover_lb_status_members)

GET[/reporting/failover-lb/status/members/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/flb-status-member/get_reporting_failover_lb_status_members_name__NAME_)

#### [flb-ipv4](https://sonicos-api.sonicwall.com/\#/flb-ipv4)      Failover load balancing ipv4 reporting API.

DELETE[/reporting/failover-lb/ipv4](https://sonicos-api.sonicwall.com/#/operations/flb-ipv4/delete_reporting_failover_lb_ipv4)

#### [flb-ipv6](https://sonicos-api.sonicwall.com/\#/flb-ipv6)      Failover load balancing ipv6 reporting API.

DELETE[/reporting/failover-lb/ipv6](https://sonicos-api.sonicwall.com/#/operations/flb-ipv6/delete_reporting_failover_lb_ipv6)

#### [dhcp-server-base](https://sonicos-api.sonicwall.com/\#/dhcp-server-base)      DHCP server IPv4 base configuration API endpoint.

GET[/dhcp-server/ipv4/base](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-base/get_dhcp_server_ipv4_base)

PUT[/dhcp-server/ipv4/base](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-base/put_dhcp_server_ipv4_base)

#### [dhcp-server-option-object](https://sonicos-api.sonicwall.com/\#/dhcp-server-option-object)      DHCP server IPv4 option object configuration API endpoint.

GET[/dhcp-server/ipv4/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/get_dhcp_server_ipv4_option_objects)

POST[/dhcp-server/ipv4/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/post_dhcp_server_ipv4_option_objects)

PUT[/dhcp-server/ipv4/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/put_dhcp_server_ipv4_option_objects)

PATCH[/dhcp-server/ipv4/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/patch_dhcp_server_ipv4_option_objects)

GET[/dhcp-server/ipv4/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/get_dhcp_server_ipv4_option_objects_name__NAME_)

PUT[/dhcp-server/ipv4/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/put_dhcp_server_ipv4_option_objects_name__NAME_)

PATCH[/dhcp-server/ipv4/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/patch_dhcp_server_ipv4_option_objects_name__NAME_)

DELETE[/dhcp-server/ipv4/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-object/delete_dhcp_server_ipv4_option_objects_name__NAME_)

#### [dhcp-server-option-group](https://sonicos-api.sonicwall.com/\#/dhcp-server-option-group)      DHCP server IPv4 option group configuration API endpoint.

GET[/dhcp-server/ipv4/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/get_dhcp_server_ipv4_option_groups)

POST[/dhcp-server/ipv4/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/post_dhcp_server_ipv4_option_groups)

PUT[/dhcp-server/ipv4/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/put_dhcp_server_ipv4_option_groups)

PATCH[/dhcp-server/ipv4/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/patch_dhcp_server_ipv4_option_groups)

GET[/dhcp-server/ipv4/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/get_dhcp_server_ipv4_option_groups_name__NAME_)

PUT[/dhcp-server/ipv4/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/put_dhcp_server_ipv4_option_groups_name__NAME_)

PATCH[/dhcp-server/ipv4/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/patch_dhcp_server_ipv4_option_groups_name__NAME_)

DELETE[/dhcp-server/ipv4/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-option-group/delete_dhcp_server_ipv4_option_groups_name__NAME_)

#### [dhcp-server-scope-dynamic](https://sonicos-api.sonicwall.com/\#/dhcp-server-scope-dynamic)      DHCP server IPv4 dynamic scopes configuration API endpoint.

GET[/dhcp-server/ipv4/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/get_dhcp_server_ipv4_scopes_dynamic)

POST[/dhcp-server/ipv4/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/post_dhcp_server_ipv4_scopes_dynamic)

PUT[/dhcp-server/ipv4/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/put_dhcp_server_ipv4_scopes_dynamic)

PATCH[/dhcp-server/ipv4/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/patch_dhcp_server_ipv4_scopes_dynamic)

GET[/dhcp-server/ipv4/scopes/dynamic/start/{STRATIP}/end/{ENDIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/get_dhcp_server_ipv4_scopes_dynamic_start__STRATIP__end__ENDIP_)

PUT[/dhcp-server/ipv4/scopes/dynamic/start/{STRATIP}/end/{ENDIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/put_dhcp_server_ipv4_scopes_dynamic_start__STRATIP__end__ENDIP_)

PATCH[/dhcp-server/ipv4/scopes/dynamic/start/{STRATIP}/end/{ENDIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/patch_dhcp_server_ipv4_scopes_dynamic_start__STRATIP__end__ENDIP_)

DELETE[/dhcp-server/ipv4/scopes/dynamic/start/{STRATIP}/end/{ENDIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-dynamic/delete_dhcp_server_ipv4_scopes_dynamic_start__STRATIP__end__ENDIP_)

#### [dhcp-server-scope-static](https://sonicos-api.sonicwall.com/\#/dhcp-server-scope-static)      DHCP server IPv4 static scopes configuration API endpoint.

GET[/dhcp-server/ipv4/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/get_dhcp_server_ipv4_scopes_static)

POST[/dhcp-server/ipv4/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/post_dhcp_server_ipv4_scopes_static)

PUT[/dhcp-server/ipv4/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/put_dhcp_server_ipv4_scopes_static)

PATCH[/dhcp-server/ipv4/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/patch_dhcp_server_ipv4_scopes_static)

GET[/dhcp-server/ipv4/scopes/static/ip/{IP}/mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/get_dhcp_server_ipv4_scopes_static_ip__IP__mac__MAC_)

PUT[/dhcp-server/ipv4/scopes/static/ip/{IP}/mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/put_dhcp_server_ipv4_scopes_static_ip__IP__mac__MAC_)

PATCH[/dhcp-server/ipv4/scopes/static/ip/{IP}/mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/patch_dhcp_server_ipv4_scopes_static_ip__IP__mac__MAC_)

DELETE[/dhcp-server/ipv4/scopes/static/ip/{IP}/mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-scope-static/delete_dhcp_server_ipv4_scopes_static_ip__IP__mac__MAC_)

#### [dhcp-server-ipv6-base](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-base)      DHCP server IPv6 base configuration API endpoint.

GET[/dhcp-server/ipv6/base](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-base/get_dhcp_server_ipv6_base)

PUT[/dhcp-server/ipv6/base](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-base/put_dhcp_server_ipv6_base)

#### [dhcp-server-ipv6-option-object](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-option-object)      DHCP server IPv6 option object configuration API endpoint.

GET[/dhcp-server/ipv6/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/get_dhcp_server_ipv6_option_objects)

POST[/dhcp-server/ipv6/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/post_dhcp_server_ipv6_option_objects)

PUT[/dhcp-server/ipv6/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/put_dhcp_server_ipv6_option_objects)

PATCH[/dhcp-server/ipv6/option/objects](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/patch_dhcp_server_ipv6_option_objects)

GET[/dhcp-server/ipv6/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/get_dhcp_server_ipv6_option_objects_name__NAME_)

PUT[/dhcp-server/ipv6/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/put_dhcp_server_ipv6_option_objects_name__NAME_)

PATCH[/dhcp-server/ipv6/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/patch_dhcp_server_ipv6_option_objects_name__NAME_)

DELETE[/dhcp-server/ipv6/option/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-object/delete_dhcp_server_ipv6_option_objects_name__NAME_)

#### [dhcp-server-ipv6-option-group](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-option-group)      DHCP server IPv6 option group configuration API endpoint.

GET[/dhcp-server/ipv6/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/get_dhcp_server_ipv6_option_groups)

POST[/dhcp-server/ipv6/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/post_dhcp_server_ipv6_option_groups)

PUT[/dhcp-server/ipv6/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/put_dhcp_server_ipv6_option_groups)

PATCH[/dhcp-server/ipv6/option/groups](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/patch_dhcp_server_ipv6_option_groups)

GET[/dhcp-server/ipv6/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/get_dhcp_server_ipv6_option_groups_name__NAME_)

PUT[/dhcp-server/ipv6/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/put_dhcp_server_ipv6_option_groups_name__NAME_)

PATCH[/dhcp-server/ipv6/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/patch_dhcp_server_ipv6_option_groups_name__NAME_)

DELETE[/dhcp-server/ipv6/option/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-option-group/delete_dhcp_server_ipv6_option_groups_name__NAME_)

#### [dhcp-server-ipv6-scope-dynamic](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-scope-dynamic)      DHCP server IPv6 dynamic scopes configuration API endpoint.

GET[/dhcp-server/ipv6/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/get_dhcp_server_ipv6_scopes_dynamic)

POST[/dhcp-server/ipv6/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/post_dhcp_server_ipv6_scopes_dynamic)

PUT[/dhcp-server/ipv6/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/put_dhcp_server_ipv6_scopes_dynamic)

PATCH[/dhcp-server/ipv6/scopes/dynamic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/patch_dhcp_server_ipv6_scopes_dynamic)

GET[/dhcp-server/ipv6/scopes/dynamic/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/get_dhcp_server_ipv6_scopes_dynamic_name__NAME_)

PUT[/dhcp-server/ipv6/scopes/dynamic/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/put_dhcp_server_ipv6_scopes_dynamic_name__NAME_)

PATCH[/dhcp-server/ipv6/scopes/dynamic/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/patch_dhcp_server_ipv6_scopes_dynamic_name__NAME_)

DELETE[/dhcp-server/ipv6/scopes/dynamic/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-dynamic/delete_dhcp_server_ipv6_scopes_dynamic_name__NAME_)

#### [dhcp-server-ipv6-scope-static](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-scope-static)      DHCP server IPv6 static scopes configuration API endpoint.

GET[/dhcp-server/ipv6/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/get_dhcp_server_ipv6_scopes_static)

POST[/dhcp-server/ipv6/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/post_dhcp_server_ipv6_scopes_static)

PUT[/dhcp-server/ipv6/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/put_dhcp_server_ipv6_scopes_static)

PATCH[/dhcp-server/ipv6/scopes/static](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/patch_dhcp_server_ipv6_scopes_static)

GET[/dhcp-server/ipv6/scopes/static/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/get_dhcp_server_ipv6_scopes_static_name__NAME_)

PUT[/dhcp-server/ipv6/scopes/static/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/put_dhcp_server_ipv6_scopes_static_name__NAME_)

PATCH[/dhcp-server/ipv6/scopes/static/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/patch_dhcp_server_ipv6_scopes_static_name__NAME_)

DELETE[/dhcp-server/ipv6/scopes/static/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-scope-static/delete_dhcp_server_ipv6_scopes_static_name__NAME_)

#### [dhcp-server-ipv4-leases](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv4-leases)      DHCP server IPv4 leases reporting API.

GET[/reporting/dhcp-server/ipv4/leases/status](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv4-leases/get_reporting_dhcp_server_ipv4_leases_status)

GET[/reporting/dhcp-server/ipv4/leases/status/ip/{LEASEIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv4-leases/get_reporting_dhcp_server_ipv4_leases_status_ip__LEASEIP_)

DELETE[/reporting/dhcp-server/ipv4/leases/status/ip/{LEASEIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv4-leases/delete_reporting_dhcp_server_ipv4_leases_status_ip__LEASEIP_)

#### [dhcp-server-ipv4-leases-statistic](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv4-leases-statistic)      DHCP server IPv4 leases statistic reporting API.

GET[/reporting/dhcp-server/ipv4/leases/statistic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv4-leases-statistic/get_reporting_dhcp_server_ipv4_leases_statistic)

#### [dhcp-server-ipv6-leases](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-leases)      DHCP server IPv6 leases reporting API.

GET[/reporting/dhcp-server/ipv6/leases/status](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-leases/get_reporting_dhcp_server_ipv6_leases_status)

GET[/reporting/dhcp-server/ipv6/leases/status/ip/{LEASEIPV6}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-leases/get_reporting_dhcp_server_ipv6_leases_status_ip__LEASEIPV6_)

DELETE[/reporting/dhcp-server/ipv6/leases/status/ip/{LEASEIPV6}](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-leases/delete_reporting_dhcp_server_ipv6_leases_status_ip__LEASEIPV6_)

#### [dhcp-server-ipv6-leases-statistic](https://sonicos-api.sonicwall.com/\#/dhcp-server-ipv6-leases-statistic)      DHCP server IPv6 leases statistic reporting API.

GET[/reporting/dhcp-server/ipv6/leases/statistic](https://sonicos-api.sonicwall.com/#/operations/dhcp-server-ipv6-leases-statistic/get_reporting_dhcp_server_ipv6_leases_statistic)

#### [dns-security-sinkhole](https://sonicos-api.sonicwall.com/\#/dns-security-sinkhole)      DNS security sinkhole configuration API.

GET[/dns-security/dns-sinkhole/base](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole/get_dns_security_dns_sinkhole_base)

PUT[/dns-security/dns-sinkhole/base](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole/put_dns_security_dns_sinkhole_base)

#### [dns-security-sinkhole-custom-malicious-entry](https://sonicos-api.sonicwall.com/\#/dns-security-sinkhole-custom-malicious-entry)      DNS security sinkhole custom malicious entries configuration API.

GET[/dns-security/dns-sinkhole/custom-malicious-entries](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole-custom-malicious-entry/get_dns_security_dns_sinkhole_custom_malicious_entries)

POST[/dns-security/dns-sinkhole/custom-malicious-entries](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole-custom-malicious-entry/post_dns_security_dns_sinkhole_custom_malicious_entries)

#### [dns-security-sinkhole-white-list-entry](https://sonicos-api.sonicwall.com/\#/dns-security-sinkhole-white-list-entry)      DNS security sinkhole white list entries configuration API.

GET[/dns-security/dns-sinkhole/white-list-entries](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole-white-list-entry/get_dns_security_dns_sinkhole_white_list_entries)

POST[/dns-security/dns-sinkhole/white-list-entries](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole-white-list-entry/post_dns_security_dns_sinkhole_white_list_entries)

#### [dns-security-tunnel](https://sonicos-api.sonicwall.com/\#/dns-security-tunnel)      DNS security tunnel configuration API.

GET[/dns-security/dns-tunnel/base](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel/get_dns_security_dns_tunnel_base)

PUT[/dns-security/dns-tunnel/base](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel/put_dns_security_dns_tunnel_base)

#### [dns-security-tunnel-white-list-entry](https://sonicos-api.sonicwall.com/\#/dns-security-tunnel-white-list-entry)      DNS security tunnel white list entries configuration API.

GET[/dns-security/dns-tunnel/white-list-entries](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel-white-list-entry/get_dns_security_dns_tunnel_white_list_entries)

POST[/dns-security/dns-tunnel/white-list-entries](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel-white-list-entry/post_dns_security_dns_tunnel_white_list_entries)

#### [dns-security-tunnel-block](https://sonicos-api.sonicwall.com/\#/dns-security-tunnel-block)      DNS security tunnel configuration API.

POST[/dns-security/dns-tunnel/block/{IP}](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel-block/post_dns_security_dns_tunnel_block__IP_)

DELETE[/dns-security/dns-tunnel/block/{IP}](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel-block/delete_dns_security_dns_tunnel_block__IP_)

#### [dns-security-sinkhole-statistics](https://sonicos-api.sonicwall.com/\#/dns-security-sinkhole-statistics)      DNS security DNS Sinkhole statistical reporting API.

GET[/reporting/dns-security/sinkhole-statistical](https://sonicos-api.sonicwall.com/#/operations/dns-security-sinkhole-statistics/get_reporting_dns_security_sinkhole_statistical)

#### [dns-security-tunnel-statistics](https://sonicos-api.sonicwall.com/\#/dns-security-tunnel-statistics)      DNS security tunnel clients reporting API.

GET[/reporting/dns-security/tunnel-clients](https://sonicos-api.sonicwall.com/#/operations/dns-security-tunnel-statistics/get_reporting_dns_security_tunnel_clients)

#### [iph](https://sonicos-api.sonicwall.com/\#/iph)      IP helper configuration API.

GET[/ip-helper/base](https://sonicos-api.sonicwall.com/#/operations/iph/get_ip_helper_base)

PUT[/ip-helper/base](https://sonicos-api.sonicwall.com/#/operations/iph/put_ip_helper_base)

#### [iph-policy](https://sonicos-api.sonicwall.com/\#/iph-policy)      IP helper configuration API.

GET[/ip-helper/policies](https://sonicos-api.sonicwall.com/#/operations/iph-policy/get_ip_helper_policies)

POST[/ip-helper/policies](https://sonicos-api.sonicwall.com/#/operations/iph-policy/post_ip_helper_policies)

PUT[/ip-helper/policies](https://sonicos-api.sonicwall.com/#/operations/iph-policy/put_ip_helper_policies)

PATCH[/ip-helper/policies](https://sonicos-api.sonicwall.com/#/operations/iph-policy/patch_ip_helper_policies)

GET[/ip-helper/policies/protocol/{PROTOCOL}/source](https://sonicos-api.sonicwall.com/#/operations/iph-policy/get_ip_helper_policies_protocol__PROTOCOL__source)

PUT[/ip-helper/policies/protocol/{PROTOCOL}/source](https://sonicos-api.sonicwall.com/#/operations/iph-policy/put_ip_helper_policies_protocol__PROTOCOL__source)

PATCH[/ip-helper/policies/protocol/{PROTOCOL}/source](https://sonicos-api.sonicwall.com/#/operations/iph-policy/patch_ip_helper_policies_protocol__PROTOCOL__source)

DELETE[/ip-helper/policies/protocol/{PROTOCOL}/source](https://sonicos-api.sonicwall.com/#/operations/iph-policy/delete_ip_helper_policies_protocol__PROTOCOL__source)

GET[/ip-helper/policies/protocol/{PROTOCOL}/source/zone/{ZONENAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/get_ip_helper_policies_protocol__PROTOCOL__source_zone__ZONENAME_)

PUT[/ip-helper/policies/protocol/{PROTOCOL}/source/zone/{ZONENAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/put_ip_helper_policies_protocol__PROTOCOL__source_zone__ZONENAME_)

PATCH[/ip-helper/policies/protocol/{PROTOCOL}/source/zone/{ZONENAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/patch_ip_helper_policies_protocol__PROTOCOL__source_zone__ZONENAME_)

DELETE[/ip-helper/policies/protocol/{PROTOCOL}/source/zone/{ZONENAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/delete_ip_helper_policies_protocol__PROTOCOL__source_zone__ZONENAME_)

GET[/ip-helper/policies/protocol/{PROTOCOL}/source/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/get_ip_helper_policies_protocol__PROTOCOL__source_interface__IFNAME_)

PUT[/ip-helper/policies/protocol/{PROTOCOL}/source/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/put_ip_helper_policies_protocol__PROTOCOL__source_interface__IFNAME_)

PATCH[/ip-helper/policies/protocol/{PROTOCOL}/source/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/patch_ip_helper_policies_protocol__PROTOCOL__source_interface__IFNAME_)

DELETE[/ip-helper/policies/protocol/{PROTOCOL}/source/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/delete_ip_helper_policies_protocol__PROTOCOL__source_interface__IFNAME_)

GET[/ip-helper/policies/protocol/{PROTOCOL}/source/group/{GROUPNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/get_ip_helper_policies_protocol__PROTOCOL__source_group__GROUPNAME_)

PUT[/ip-helper/policies/protocol/{PROTOCOL}/source/group/{GROUPNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/put_ip_helper_policies_protocol__PROTOCOL__source_group__GROUPNAME_)

PATCH[/ip-helper/policies/protocol/{PROTOCOL}/source/group/{GROUPNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/patch_ip_helper_policies_protocol__PROTOCOL__source_group__GROUPNAME_)

DELETE[/ip-helper/policies/protocol/{PROTOCOL}/source/group/{GROUPNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/delete_ip_helper_policies_protocol__PROTOCOL__source_group__GROUPNAME_)

GET[/ip-helper/policies/protocol/{PROTOCOL}/source/name/{NETWORKNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/get_ip_helper_policies_protocol__PROTOCOL__source_name__NETWORKNAME_)

PUT[/ip-helper/policies/protocol/{PROTOCOL}/source/name/{NETWORKNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/put_ip_helper_policies_protocol__PROTOCOL__source_name__NETWORKNAME_)

PATCH[/ip-helper/policies/protocol/{PROTOCOL}/source/name/{NETWORKNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/patch_ip_helper_policies_protocol__PROTOCOL__source_name__NETWORKNAME_)

DELETE[/ip-helper/policies/protocol/{PROTOCOL}/source/name/{NETWORKNAME}](https://sonicos-api.sonicwall.com/#/operations/iph-policy/delete_ip_helper_policies_protocol__PROTOCOL__source_name__NETWORKNAME_)

#### [iph-protocol](https://sonicos-api.sonicwall.com/\#/iph-protocol)      IP helper protocol object configuration API.

GET[/ip-helper/protocols](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/get_ip_helper_protocols)

POST[/ip-helper/protocols](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/post_ip_helper_protocols)

PUT[/ip-helper/protocols](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/put_ip_helper_protocols)

PATCH[/ip-helper/protocols](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/patch_ip_helper_protocols)

GET[/ip-helper/protocols/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/get_ip_helper_protocols_name__NAME_)

PUT[/ip-helper/protocols/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/put_ip_helper_protocols_name__NAME_)

PATCH[/ip-helper/protocols/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/patch_ip_helper_protocols_name__NAME_)

DELETE[/ip-helper/protocols/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/iph-protocol/delete_ip_helper_protocols_name__NAME_)

#### [iph-dhcp-relay-leases](https://sonicos-api.sonicwall.com/\#/iph-dhcp-relay-leases)      IP helper DHCP relay leases reporting API.

GET[/reporting/ip-helper/dhcp-relay-leases](https://sonicos-api.sonicwall.com/#/operations/iph-dhcp-relay-leases/get_reporting_ip_helper_dhcp_relay_leases)

#### [iph-dhcpv6-relay-leases](https://sonicos-api.sonicwall.com/\#/iph-dhcpv6-relay-leases)      IP helper IPv6 DHCP relay leases reporting API.

GET[/reporting/ip-helper/dhcpv6-relay-leases](https://sonicos-api.sonicwall.com/#/operations/iph-dhcpv6-relay-leases/get_reporting_ip_helper_dhcpv6_relay_leases)

#### [iph-policies](https://sonicos-api.sonicwall.com/\#/iph-policies)      IP helper policies reporting API.

GET[/reporting/ip-helper/policies](https://sonicos-api.sonicwall.com/#/operations/iph-policies/get_reporting_ip_helper_policies)

#### [iph-protocols](https://sonicos-api.sonicwall.com/\#/iph-protocols)      IP helper protocols reporting API.

GET[/reporting/ip-helper/protocols](https://sonicos-api.sonicwall.com/#/operations/iph-protocols/get_reporting_ip_helper_protocols)

GET[/reporting/ip-helper/protocols/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/iph-protocols/get_reporting_ip_helper_protocols_name__NAME_)

#### [mac-ip-anti-spoof-ipv4](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-ipv4)      MAC IP anti spoof IPv4 interface object configuration API.

GET[/mac-ip-anti-spoof/ipv4/interfaces](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv4/get_mac_ip_anti_spoof_ipv4_interfaces)

PUT[/mac-ip-anti-spoof/ipv4/interfaces](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv4/put_mac_ip_anti_spoof_ipv4_interfaces)

GET[/mac-ip-anti-spoof/ipv4/interfaces/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv4/get_mac_ip_anti_spoof_ipv4_interfaces_name__NAME_)

PUT[/mac-ip-anti-spoof/ipv4/interfaces/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv4/put_mac_ip_anti_spoof_ipv4_interfaces_name__NAME_)

#### [mac-ip-anti-spoof-cache-ipv4](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-cache-ipv4)      MAC IP anti spoof IPv4 cache entry object configuration API.

GET[/mac-ip-anti-spoof/ipv4/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/get_mac_ip_anti_spoof_ipv4_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

PUT[/mac-ip-anti-spoof/ipv4/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/put_mac_ip_anti_spoof_ipv4_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

PATCH[/mac-ip-anti-spoof/ipv4/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/patch_mac_ip_anti_spoof_ipv4_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

DELETE[/mac-ip-anti-spoof/ipv4/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/delete_mac_ip_anti_spoof_ipv4_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

GET[/mac-ip-anti-spoof/ipv4/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/get_mac_ip_anti_spoof_ipv4_cache_entries)

POST[/mac-ip-anti-spoof/ipv4/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/post_mac_ip_anti_spoof_ipv4_cache_entries)

PUT[/mac-ip-anti-spoof/ipv4/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/put_mac_ip_anti_spoof_ipv4_cache_entries)

PATCH[/mac-ip-anti-spoof/ipv4/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv4/patch_mac_ip_anti_spoof_ipv4_cache_entries)

#### [mac-ip-anti-spoof-ipv6](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-ipv6)      MAC IP anti spoof IPv6 interface object configuration API.

GET[/mac-ip-anti-spoof/ipv6/interfaces](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv6/get_mac_ip_anti_spoof_ipv6_interfaces)

PUT[/mac-ip-anti-spoof/ipv6/interfaces](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv6/put_mac_ip_anti_spoof_ipv6_interfaces)

GET[/mac-ip-anti-spoof/ipv6/interfaces/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv6/get_mac_ip_anti_spoof_ipv6_interfaces_name__NAME_)

PUT[/mac-ip-anti-spoof/ipv6/interfaces/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-ipv6/put_mac_ip_anti_spoof_ipv6_interfaces_name__NAME_)

#### [mac-ip-anti-spoof-cache-ipv6](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-cache-ipv6)      MAC IP anti spoof IPv6 cache entry object configuration API.

GET[/mac-ip-anti-spoof/ipv6/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/get_mac_ip_anti_spoof_ipv6_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

PUT[/mac-ip-anti-spoof/ipv6/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/put_mac_ip_anti_spoof_ipv6_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

PATCH[/mac-ip-anti-spoof/ipv6/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/patch_mac_ip_anti_spoof_ipv6_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

DELETE[/mac-ip-anti-spoof/ipv6/cache/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/delete_mac_ip_anti_spoof_ipv6_cache_entries_ip__IP__mac__MAC__interface__IFNAME_)

GET[/mac-ip-anti-spoof/ipv6/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/get_mac_ip_anti_spoof_ipv6_cache_entries)

POST[/mac-ip-anti-spoof/ipv6/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/post_mac_ip_anti_spoof_ipv6_cache_entries)

PUT[/mac-ip-anti-spoof/ipv6/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/put_mac_ip_anti_spoof_ipv6_cache_entries)

PATCH[/mac-ip-anti-spoof/ipv6/cache/entries](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-ipv6/patch_mac_ip_anti_spoof_ipv6_cache_entries)

#### [mac-ip-anti-spoof-detected-list-ipv4](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-detected-list-ipv4)      MAC IPv4 anti-spoof detected list reporting API.

GET[/reporting/mac-ip-anti-spoof/detected-list/ipv4](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-detected-list-ipv4/get_reporting_mac_ip_anti_spoof_detected_list_ipv4)

#### [mac-ip-anti-spoof-detected-list-ipv6](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-detected-list-ipv6)      MAC IPv6 anti-spoof detected list reporting API.

GET[/reporting/mac-ip-anti-spoof/detected-list/ipv6](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-detected-list-ipv6/get_reporting_mac_ip_anti_spoof_detected_list_ipv6)

#### [mac-ip-anti-spoof-lookup-statistics-ipv4](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-lookup-statistics-ipv4)      MAC IPv4 anti-spoof lookup reporting API.

GET[/reporting/mac-ip-anti-spoof/lookup-statistics/ipv4](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-lookup-statistics-ipv4/get_reporting_mac_ip_anti_spoof_lookup_statistics_ipv4)

#### [mac-ip-anti-spoof-lookup-statistics-ipv6](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-lookup-statistics-ipv6)      MAC IPv6 anti-spoof lookup reporting API.

GET[/reporting/mac-ip-anti-spoof/lookup-statistics/ipv6](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-lookup-statistics-ipv6/get_reporting_mac_ip_anti_spoof_lookup_statistics_ipv6)

#### [mac-ip-anti-spoof-cache-statistics-ipv4](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-cache-statistics-ipv4)      MAC IPv4 anti-spoof cache reporting API.

GET[/reporting/mac-ip-anti-spoof/cache/ipv4](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-statistics-ipv4/get_reporting_mac_ip_anti_spoof_cache_ipv4)

#### [mac-ip-anti-spoof-cache-statistics-ipv6](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-cache-statistics-ipv6)      MAC IPv6 anti-spoof cache reporting API.

GET[/reporting/mac-ip-anti-spoof/cache/ipv6](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-cache-statistics-ipv6/get_reporting_mac_ip_anti_spoof_cache_ipv6)

#### [mac-ip-anti-spoof-resolve-spoof-ipv4](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-resolve-spoof-ipv4)      Resolve names for the MAC IPv4 whole spoof detected list API.

POST[/mac-ip-anti-spoof/resolve/spoof-detected-list/ipv4](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-resolve-spoof-ipv4/post_mac_ip_anti_spoof_resolve_spoof_detected_list_ipv4)

#### [mac-ip-anti-spoof-resolve-spoof-ipv6](https://sonicos-api.sonicwall.com/\#/mac-ip-anti-spoof-resolve-spoof-ipv6)      Resolve names for the whole MAC IPv6 spoof detected list API.

POST[/mac-ip-anti-spoof/resolve/spoof-detected-list/ipv6](https://sonicos-api.sonicwall.com/#/operations/mac-ip-anti-spoof-resolve-spoof-ipv6/post_mac_ip_anti_spoof_resolve_spoof_detected_list_ipv6)

#### [ndp](https://sonicos-api.sonicwall.com/\#/ndp)      Neighbor discovery configuration API.

GET[/ndp/base](https://sonicos-api.sonicwall.com/#/operations/ndp/get_ndp_base)

PUT[/ndp/base](https://sonicos-api.sonicwall.com/#/operations/ndp/put_ndp_base)

#### [ndp-entry](https://sonicos-api.sonicwall.com/\#/ndp-entry)      Neighbor discovery entry object configuration API.

GET[/ndp/entries](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/get_ndp_entries)

POST[/ndp/entries](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/post_ndp_entries)

PUT[/ndp/entries](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/put_ndp_entries)

PATCH[/ndp/entries](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/patch_ndp_entries)

GET[/ndp/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/get_ndp_entries_ip__IP__mac__MAC__interface__IFNAME_)

PUT[/ndp/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/put_ndp_entries_ip__IP__mac__MAC__interface__IFNAME_)

PATCH[/ndp/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/patch_ndp_entries_ip__IP__mac__MAC__interface__IFNAME_)

DELETE[/ndp/entries/ip/{IP}/mac/{MAC}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/ndp-entry/delete_ndp_entries_ip__IP__mac__MAC__interface__IFNAME_)

#### [ndp-cache-entry](https://sonicos-api.sonicwall.com/\#/ndp-cache-entry)      Neighbor discovery cache reporting API.

DELETE[/ndp/cache/entries](https://sonicos-api.sonicwall.com/#/operations/ndp-cache-entry/delete_ndp_cache_entries)

DELETE[/ndp/cache/entries/ip/{IP}/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/ndp-cache-entry/delete_ndp_cache_entries_ip__IP__interface__IFNAME_)

#### [ndp-cache](https://sonicos-api.sonicwall.com/\#/ndp-cache)      Neighbor discovery cache reporting API.

GET[/reporting/ndp/cache](https://sonicos-api.sonicwall.com/#/operations/ndp-cache/get_reporting_ndp_cache)

#### [ndp-entries-status](https://sonicos-api.sonicwall.com/\#/ndp-entries-status)      Neighbor discovery entries status reporting API.

GET[/reporting/ndp/entries/status](https://sonicos-api.sonicwall.com/#/operations/ndp-entries-status/get_reporting_ndp_entries_status)

#### [dns-proxy](https://sonicos-api.sonicwall.com/\#/dns-proxy)      DNS proxy base configuration API.

GET[/dns-proxy/base](https://sonicos-api.sonicwall.com/#/operations/dns-proxy/get_dns_proxy_base)

PUT[/dns-proxy/base](https://sonicos-api.sonicwall.com/#/operations/dns-proxy/put_dns_proxy_base)

#### [dns-proxy-cache-entry](https://sonicos-api.sonicwall.com/\#/dns-proxy-cache-entry)      DNS proxy cache entry object configuration API.

GET[/dns-proxy/cache-entries](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/get_dns_proxy_cache_entries)

POST[/dns-proxy/cache-entries](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/post_dns_proxy_cache_entries)

PUT[/dns-proxy/cache-entries](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/put_dns_proxy_cache_entries)

PATCH[/dns-proxy/cache-entries](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/patch_dns_proxy_cache_entries)

GET[/dns-proxy/cache-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/get_dns_proxy_cache_entries_domain__NAME_)

PUT[/dns-proxy/cache-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/put_dns_proxy_cache_entries_domain__NAME_)

PATCH[/dns-proxy/cache-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/patch_dns_proxy_cache_entries_domain__NAME_)

DELETE[/dns-proxy/cache-entries/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-entry/delete_dns_proxy_cache_entries_domain__NAME_)

#### [dns-proxy-flush-cache-entry-ipv4](https://sonicos-api.sonicwall.com/\#/dns-proxy-flush-cache-entry-ipv4)      Flush the IPv4 dynamic DNS cache entry action API.

POST[/dns-proxy/flush/cache-entries/ipv4](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-flush-cache-entry-ipv4/post_dns_proxy_flush_cache_entries_ipv4)

POST[/dns-proxy/flush/cache-entries/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-flush-cache-entry-ipv4/post_dns_proxy_flush_cache_entries_ipv4_name__NAME_)

#### [dns-proxy-flush-cache-entry-ipv6](https://sonicos-api.sonicwall.com/\#/dns-proxy-flush-cache-entry-ipv6)      Flush the IPv6 dynamic DNS cache entry action API.

POST[/dns-proxy/flush/cache-entries/ipv6](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-flush-cache-entry-ipv6/post_dns_proxy_flush_cache_entries_ipv6)

POST[/dns-proxy/flush/cache-entries/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-flush-cache-entry-ipv6/post_dns_proxy_flush_cache_entries_ipv6_name__NAME_)

#### [dns-proxy-server](https://sonicos-api.sonicwall.com/\#/dns-proxy-server)      DNS proxy DNS server status reporting API.

GET[/reporting/dns-proxy/server](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-server/get_reporting_dns_proxy_server)

#### [dns-proxy-split-entry](https://sonicos-api.sonicwall.com/\#/dns-proxy-split-entry)      DNS proxy split entry status reporting API.

GET[/reporting/dns-proxy/split-entries](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-split-entry/get_reporting_dns_proxy_split_entries)

GET[/reporting/dns-proxy/split-entries/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-split-entry/get_reporting_dns_proxy_split_entries_name__NAME_)

#### [dns-proxy-cache-ipv4](https://sonicos-api.sonicwall.com/\#/dns-proxy-cache-ipv4)      DNS proxy IPv4 DNS cache status reporting API.

GET[/reporting/dns-proxy/caches/ipv4](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-ipv4/get_reporting_dns_proxy_caches_ipv4)

GET[/reporting/dns-proxy/caches/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-ipv4/get_reporting_dns_proxy_caches_ipv4_name__NAME_)

#### [dns-proxy-cache-ipv6](https://sonicos-api.sonicwall.com/\#/dns-proxy-cache-ipv6)      DNS proxy IPv6 DNS cache status reporting API.

GET[/reporting/dns-proxy/caches/ipv6](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-ipv6/get_reporting_dns_proxy_caches_ipv6)

GET[/reporting/dns-proxy/caches/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/dns-proxy-cache-ipv6/get_reporting_dns_proxy_caches_ipv6_name__NAME_)

#### [tcp](https://sonicos-api.sonicwall.com/\#/tcp)      TCP configuration API.

GET[/tcp](https://sonicos-api.sonicwall.com/#/operations/tcp/get_tcp)

PUT[/tcp](https://sonicos-api.sonicwall.com/#/operations/tcp/put_tcp)

#### [tcp-statistics](https://sonicos-api.sonicwall.com/\#/tcp-statistics)      TCP reporting API.

GET[/reporting/tcp](https://sonicos-api.sonicwall.com/#/operations/tcp-statistics/get_reporting_tcp)

DELETE[/reporting/tcp](https://sonicos-api.sonicwall.com/#/operations/tcp-statistics/delete_reporting_tcp)

#### [udp](https://sonicos-api.sonicwall.com/\#/udp)      UDP configuration API.

GET[/udp](https://sonicos-api.sonicwall.com/#/operations/udp/get_udp)

PUT[/udp](https://sonicos-api.sonicwall.com/#/operations/udp/put_udp)

#### [udp-statistics](https://sonicos-api.sonicwall.com/\#/udp-statistics)      UDP reporting API.

GET[/reporting/udp](https://sonicos-api.sonicwall.com/#/operations/udp-statistics/get_reporting_udp)

DELETE[/reporting/udp](https://sonicos-api.sonicwall.com/#/operations/udp-statistics/delete_reporting_udp)

#### [udpv6](https://sonicos-api.sonicwall.com/\#/udpv6)      UDPv6 configuration API.

GET[/udpv6](https://sonicos-api.sonicwall.com/#/operations/udpv6/get_udpv6)

PUT[/udpv6](https://sonicos-api.sonicwall.com/#/operations/udpv6/put_udpv6)

#### [udpv6-statistics](https://sonicos-api.sonicwall.com/\#/udpv6-statistics)      UDPv6 reporting API.

GET[/reporting/udpv6](https://sonicos-api.sonicwall.com/#/operations/udpv6-statistics/get_reporting_udpv6)

DELETE[/reporting/udpv6](https://sonicos-api.sonicwall.com/#/operations/udpv6-statistics/delete_reporting_udpv6)

#### [icmp](https://sonicos-api.sonicwall.com/\#/icmp)      ICMP configuration API.

GET[/icmp](https://sonicos-api.sonicwall.com/#/operations/icmp/get_icmp)

PUT[/icmp](https://sonicos-api.sonicwall.com/#/operations/icmp/put_icmp)

#### [icmp-statistics](https://sonicos-api.sonicwall.com/\#/icmp-statistics)      ICMP reporting API.

GET[/reporting/icmp](https://sonicos-api.sonicwall.com/#/operations/icmp-statistics/get_reporting_icmp)

DELETE[/reporting/icmp](https://sonicos-api.sonicwall.com/#/operations/icmp-statistics/delete_reporting_icmp)

#### [icmpv6](https://sonicos-api.sonicwall.com/\#/icmpv6)      ICMPv6 configuration API.

GET[/icmpv6](https://sonicos-api.sonicwall.com/#/operations/icmpv6/get_icmpv6)

PUT[/icmpv6](https://sonicos-api.sonicwall.com/#/operations/icmpv6/put_icmpv6)

#### [icmpv6-statistics](https://sonicos-api.sonicwall.com/\#/icmpv6-statistics)      ICMPv6 reporting API.

GET[/reporting/icmpv6](https://sonicos-api.sonicwall.com/#/operations/icmpv6-statistics/get_reporting_icmpv6)

DELETE[/reporting/icmpv6](https://sonicos-api.sonicwall.com/#/operations/icmpv6-statistics/delete_reporting_icmpv6)

#### [qos-mapping](https://sonicos-api.sonicwall.com/\#/qos-mapping)      QOS mapping configuration API.

GET[/qos-mapping/base](https://sonicos-api.sonicwall.com/#/operations/qos-mapping/get_qos_mapping_base)

PUT[/qos-mapping/base](https://sonicos-api.sonicwall.com/#/operations/qos-mapping/put_qos_mapping_base)

#### [qos-mapping-reset](https://sonicos-api.sonicwall.com/\#/qos-mapping-reset)      QOS mapping reset API.

POST[/qos-mapping/reset](https://sonicos-api.sonicwall.com/#/operations/qos-mapping-reset/post_qos_mapping_reset)

#### [multicast](https://sonicos-api.sonicwall.com/\#/multicast)      multicast configuration API.

GET[/multicast/base](https://sonicos-api.sonicwall.com/#/operations/multicast/get_multicast_base)

PUT[/multicast/base](https://sonicos-api.sonicwall.com/#/operations/multicast/put_multicast_base)

#### [multicast-state-entries](https://sonicos-api.sonicwall.com/\#/multicast-state-entries)      multicast statistics API.

DELETE[/multicast/state-entries](https://sonicos-api.sonicwall.com/#/operations/multicast-state-entries/delete_multicast_state_entries)

#### [multicast-state-entry](https://sonicos-api.sonicwall.com/\#/multicast-state-entry)      multicast statistics API.

DELETE[/multicast/state-entry/address/{IP}/interface/{IFNUM}](https://sonicos-api.sonicwall.com/#/operations/multicast-state-entry/delete_multicast_state_entry_address__IP__interface__IFNUM_)

#### [multicast-state-entries-reporting](https://sonicos-api.sonicwall.com/\#/multicast-state-entries-reporting)      Multicast IGMP state entries.

GET[/reporting/multicast/state-entries](https://sonicos-api.sonicwall.com/#/operations/multicast-state-entries-reporting/get_reporting_multicast_state_entries)

#### [multicast-state-entry-reporting](https://sonicos-api.sonicwall.com/\#/multicast-state-entry-reporting)      Multicast IGMP state entry.

GET[/reporting/multicast/state-entry/address/{IP}/interface/{IFNUM}](https://sonicos-api.sonicwall.com/#/operations/multicast-state-entry-reporting/get_reporting_multicast_state_entry_address__IP__interface__IFNUM_)

#### [web-proxy](https://sonicos-api.sonicwall.com/\#/web-proxy)      Web proxy base settings API.

GET[/web-proxy/base](https://sonicos-api.sonicwall.com/#/operations/web-proxy/get_web_proxy_base)

PUT[/web-proxy/base](https://sonicos-api.sonicwall.com/#/operations/web-proxy/put_web_proxy_base)

#### [web-proxy-servers](https://sonicos-api.sonicwall.com/\#/web-proxy-servers)      Web user proxy servers setting API.

GET[/web-proxy/proxy-servers](https://sonicos-api.sonicwall.com/#/operations/web-proxy-servers/get_web_proxy_proxy_servers)

POST[/web-proxy/proxy-servers](https://sonicos-api.sonicwall.com/#/operations/web-proxy-servers/post_web_proxy_proxy_servers)

GET[/web-proxy/proxy-servers/name/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/web-proxy-servers/get_web_proxy_proxy_servers_name__HOSTIP_)

DELETE[/web-proxy/proxy-servers/name/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/web-proxy-servers/delete_web_proxy_proxy_servers_name__HOSTIP_)

#### [network-monitor-ipv4](https://sonicos-api.sonicwall.com/\#/network-monitor-ipv4)      Network monitor IPv4 policies configuration API.

GET[/network-monitor/policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/get_network_monitor_policies_ipv4)

POST[/network-monitor/policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/post_network_monitor_policies_ipv4)

PUT[/network-monitor/policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/put_network_monitor_policies_ipv4)

PATCH[/network-monitor/policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/patch_network_monitor_policies_ipv4)

GET[/network-monitor/policies/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/get_network_monitor_policies_ipv4_name__NAME_)

PUT[/network-monitor/policies/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/put_network_monitor_policies_ipv4_name__NAME_)

PATCH[/network-monitor/policies/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/patch_network_monitor_policies_ipv4_name__NAME_)

DELETE[/network-monitor/policies/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4/delete_network_monitor_policies_ipv4_name__NAME_)

#### [network-monitor-ipv6](https://sonicos-api.sonicwall.com/\#/network-monitor-ipv6)      Network monitor IPv6 policies configuration API.

GET[/network-monitor/policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/get_network_monitor_policies_ipv6)

POST[/network-monitor/policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/post_network_monitor_policies_ipv6)

PUT[/network-monitor/policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/put_network_monitor_policies_ipv6)

PATCH[/network-monitor/policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/patch_network_monitor_policies_ipv6)

GET[/network-monitor/policies/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/get_network_monitor_policies_ipv6_name__NAME_)

PUT[/network-monitor/policies/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/put_network_monitor_policies_ipv6_name__NAME_)

PATCH[/network-monitor/policies/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/patch_network_monitor_policies_ipv6_name__NAME_)

DELETE[/network-monitor/policies/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6/delete_network_monitor_policies_ipv6_name__NAME_)

#### [network-monitor-statistics](https://sonicos-api.sonicwall.com/\#/network-monitor-statistics)      Clear network monitor statistics API.

DELETE[/network-monitor/statistics](https://sonicos-api.sonicwall.com/#/operations/network-monitor-statistics/delete_network_monitor_statistics)

#### [network-monitor-ipv4-status](https://sonicos-api.sonicwall.com/\#/network-monitor-ipv4-status)      Network monitor IPv4 policies status reporting API.

GET[/reporting/network-monitor/policies/ipv4](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4-status/get_reporting_network_monitor_policies_ipv4)

GET[/reporting/network-monitor/policies/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv4-status/get_reporting_network_monitor_policies_ipv4_name__NAME_)

#### [network-monitor-ipv6-status](https://sonicos-api.sonicwall.com/\#/network-monitor-ipv6-status)      Network monitor IPv6 policies status reporting API.

GET[/reporting/network-monitor/policies/ipv6](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6-status/get_reporting_network_monitor_policies_ipv6)

GET[/reporting/network-monitor/policies/ipv6/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/network-monitor-ipv6-status/get_reporting_network_monitor_policies_ipv6_name__NAME_)

#### [vlan-translation](https://sonicos-api.sonicwall.com/\#/vlan-translation)      Vlan translation configuration API.

GET[/vlan-translations](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/get_vlan_translations)

POST[/vlan-translations](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/post_vlan_translations)

PUT[/vlan-translations](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/put_vlan_translations)

PATCH[/vlan-translations](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/patch_vlan_translations)

GET[/vlan-translations/ingress/interface/{INGRESSIF}/vlan/{INGRESSID}/egress/interface/{EGRESSIF}/vlan/{EGRESSID}](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/get_vlan_translations_ingress_interface__INGRESSIF__vlan__INGRESSID__egress_interface__EGRESSIF__vlan__EGRESSID_)

PUT[/vlan-translations/ingress/interface/{INGRESSIF}/vlan/{INGRESSID}/egress/interface/{EGRESSIF}/vlan/{EGRESSID}](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/put_vlan_translations_ingress_interface__INGRESSIF__vlan__INGRESSID__egress_interface__EGRESSIF__vlan__EGRESSID_)

PATCH[/vlan-translations/ingress/interface/{INGRESSIF}/vlan/{INGRESSID}/egress/interface/{EGRESSIF}/vlan/{EGRESSID}](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/patch_vlan_translations_ingress_interface__INGRESSIF__vlan__INGRESSID__egress_interface__EGRESSIF__vlan__EGRESSID_)

DELETE[/vlan-translations/ingress/interface/{INGRESSIF}/vlan/{INGRESSID}/egress/interface/{EGRESSIF}/vlan/{EGRESSID}](https://sonicos-api.sonicwall.com/#/operations/vlan-translation/delete_vlan_translations_ingress_interface__INGRESSIF__vlan__INGRESSID__egress_interface__EGRESSIF__vlan__EGRESSID_)

#### [vlan-translation-status](https://sonicos-api.sonicwall.com/\#/vlan-translation-status)      Vlan translation reporting API.

GET[/reporting/vlan-translations](https://sonicos-api.sonicwall.com/#/operations/vlan-translation-status/get_reporting_vlan_translations)

#### [wwan-status](https://sonicos-api.sonicwall.com/\#/wwan-status)      VoIP reporting API.

GET[/reporting/wwan](https://sonicos-api.sonicwall.com/#/operations/wwan-status/get_reporting_wwan)

#### [sonicpoint-vap-group](https://sonicos-api.sonicwall.com/\#/sonicpoint-vap-group)      SonicPoint/SonicWave virtual access point group configuration API.

GET[/sonicpoint/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/get_sonicpoint_virtual_access_point_groups)

POST[/sonicpoint/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/post_sonicpoint_virtual_access_point_groups)

PUT[/sonicpoint/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/put_sonicpoint_virtual_access_point_groups)

PATCH[/sonicpoint/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/patch_sonicpoint_virtual_access_point_groups)

GET[/sonicpoint/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/get_sonicpoint_virtual_access_point_groups_name__NAME_)

PUT[/sonicpoint/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/put_sonicpoint_virtual_access_point_groups_name__NAME_)

PATCH[/sonicpoint/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/patch_sonicpoint_virtual_access_point_groups_name__NAME_)

DELETE[/sonicpoint/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-group/delete_sonicpoint_virtual_access_point_groups_name__NAME_)

#### [sonicpoint-vap-profile](https://sonicos-api.sonicwall.com/\#/sonicpoint-vap-profile)      SonicPoint/SonicWave virtual access point profile configuration API.

GET[/sonicpoint/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/get_sonicpoint_virtual_access_point_profiles)

POST[/sonicpoint/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/post_sonicpoint_virtual_access_point_profiles)

PUT[/sonicpoint/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/put_sonicpoint_virtual_access_point_profiles)

PATCH[/sonicpoint/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/patch_sonicpoint_virtual_access_point_profiles)

GET[/sonicpoint/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/get_sonicpoint_virtual_access_point_profiles_name__NAME_)

PUT[/sonicpoint/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/put_sonicpoint_virtual_access_point_profiles_name__NAME_)

PATCH[/sonicpoint/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/patch_sonicpoint_virtual_access_point_profiles_name__NAME_)

DELETE[/sonicpoint/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-profile/delete_sonicpoint_virtual_access_point_profiles_name__NAME_)

#### [sonicpoint-vap-object](https://sonicos-api.sonicwall.com/\#/sonicpoint-vap-object)      SonicPoint/SonicWave virtual access point object configuration API.

GET[/sonicpoint/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/get_sonicpoint_virtual_access_point_objects)

POST[/sonicpoint/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/post_sonicpoint_virtual_access_point_objects)

PUT[/sonicpoint/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/put_sonicpoint_virtual_access_point_objects)

PATCH[/sonicpoint/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/patch_sonicpoint_virtual_access_point_objects)

GET[/sonicpoint/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/get_sonicpoint_virtual_access_point_objects_name__NAME_)

PUT[/sonicpoint/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/put_sonicpoint_virtual_access_point_objects_name__NAME_)

PATCH[/sonicpoint/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/patch_sonicpoint_virtual_access_point_objects_name__NAME_)

DELETE[/sonicpoint/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-object/delete_sonicpoint_virtual_access_point_objects_name__NAME_)

#### [wireless-vap-group](https://sonicos-api.sonicwall.com/\#/wireless-vap-group)      Wireless virtual access point group configuration API.

GET[/wireless/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/get_wireless_virtual_access_point_groups)

POST[/wireless/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/post_wireless_virtual_access_point_groups)

PUT[/wireless/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/put_wireless_virtual_access_point_groups)

PATCH[/wireless/virtual-access-point/groups](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/patch_wireless_virtual_access_point_groups)

GET[/wireless/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/get_wireless_virtual_access_point_groups_name__NAME_)

PUT[/wireless/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/put_wireless_virtual_access_point_groups_name__NAME_)

PATCH[/wireless/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/patch_wireless_virtual_access_point_groups_name__NAME_)

DELETE[/wireless/virtual-access-point/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-group/delete_wireless_virtual_access_point_groups_name__NAME_)

#### [wireless-vap-profile](https://sonicos-api.sonicwall.com/\#/wireless-vap-profile)      Wireless virtual access point profile configuration API.

GET[/wireless/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/get_wireless_virtual_access_point_profiles)

POST[/wireless/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/post_wireless_virtual_access_point_profiles)

PUT[/wireless/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/put_wireless_virtual_access_point_profiles)

PATCH[/wireless/virtual-access-point/profiles](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/patch_wireless_virtual_access_point_profiles)

GET[/wireless/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/get_wireless_virtual_access_point_profiles_name__NAME_)

PUT[/wireless/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/put_wireless_virtual_access_point_profiles_name__NAME_)

PATCH[/wireless/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/patch_wireless_virtual_access_point_profiles_name__NAME_)

DELETE[/wireless/virtual-access-point/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-profile/delete_wireless_virtual_access_point_profiles_name__NAME_)

#### [wireless-vap-object](https://sonicos-api.sonicwall.com/\#/wireless-vap-object)      Wireless virtual access point object configuration API.

GET[/wireless/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/get_wireless_virtual_access_point_objects)

POST[/wireless/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/post_wireless_virtual_access_point_objects)

PUT[/wireless/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/put_wireless_virtual_access_point_objects)

PATCH[/wireless/virtual-access-point/objects](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/patch_wireless_virtual_access_point_objects)

GET[/wireless/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/get_wireless_virtual_access_point_objects_name__NAME_)

PUT[/wireless/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/put_wireless_virtual_access_point_objects_name__NAME_)

PATCH[/wireless/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/patch_wireless_virtual_access_point_objects_name__NAME_)

DELETE[/wireless/virtual-access-point/objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wireless-vap-object/delete_wireless_virtual_access_point_objects_name__NAME_)

#### [wireless-radio](https://sonicos-api.sonicwall.com/\#/wireless-radio)      Wireless radio configuration API.

GET[/wireless/radio](https://sonicos-api.sonicwall.com/#/operations/wireless-radio/get_wireless_radio)

PUT[/wireless/radio](https://sonicos-api.sonicwall.com/#/operations/wireless-radio/put_wireless_radio)

#### [wireless-ids](https://sonicos-api.sonicwall.com/\#/wireless-ids)      Wireless IDS configuration API.

GET[/wireless/ids/base](https://sonicos-api.sonicwall.com/#/operations/wireless-ids/get_wireless_ids_base)

PUT[/wireless/ids/base](https://sonicos-api.sonicwall.com/#/operations/wireless-ids/put_wireless_ids_base)

#### [wireless-access-point-station-connect](https://sonicos-api.sonicwall.com/\#/wireless-access-point-station-connect)      Wireless access point station mode: connect to the specified access point API.

POST[/wireless/access-point-station/connect/{APSSID}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-connect/post_wireless_access_point_station_connect__APSSID_)

#### [wireless-access-point-station-scan](https://sonicos-api.sonicwall.com/\#/wireless-access-point-station-scan)      Wireless access point station mode: Scan nearby access points API.

POST[/wireless/access-point-station/scan](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-scan/post_wireless_access_point_station_scan)

#### [wireless-access-point-station-block-station](https://sonicos-api.sonicwall.com/\#/wireless-access-point-station-block-station)      Wireless access point station mode: Block specified station API.

POST[/wireless/access-point-station/block-station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-block-station/post_wireless_access_point_station_block_station__STATIONMAC_)

POST[/wireless/access-point-station/block-station/{STATIONMAC}/enable-mac](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-block-station/post_wireless_access_point_station_block_station__STATIONMAC__enable_mac)

#### [wireless-access-point-station-allow-station](https://sonicos-api.sonicwall.com/\#/wireless-access-point-station-allow-station)      Wireless access point station mode: Allow specified station API.

POST[/wireless/access-point-station/allow-station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-allow-station/post_wireless_access_point_station_allow_station__STATIONMAC_)

POST[/wireless/access-point-station/allow-station/{STATIONMAC}/enable-mac](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-allow-station/post_wireless_access_point_station_allow_station__STATIONMAC__enable_mac)

#### [wireless-access-point-station-disassociate-station](https://sonicos-api.sonicwall.com/\#/wireless-access-point-station-disassociate-station)      Wireless access point station mode: Logout and disassociate specified station API.

POST[/wireless/access-point-station/disassociate-station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-disassociate-station/post_wireless_access_point_station_disassociate_station__STATIONMAC_)

#### [wireless-access-point-station-disassociate-stations](https://sonicos-api.sonicwall.com/\#/wireless-access-point-station-disassociate-stations)      Wireless access point station mode: Logout and disassociate all stations API.

POST[/wireless/access-point-station/disassociate-stations](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-station-disassociate-stations/post_wireless_access_point_station_disassociate_stations)

#### [wireless-access-point-block-station](https://sonicos-api.sonicwall.com/\#/wireless-access-point-block-station)      Wireless access point mode: Block specified station API.

POST[/wireless/access-point/block-station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-block-station/post_wireless_access_point_block_station__STATIONMAC_)

POST[/wireless/access-point/block-station/{STATIONMAC}/enable-mac](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-block-station/post_wireless_access_point_block_station__STATIONMAC__enable_mac)

#### [wireless-access-point-allow-station](https://sonicos-api.sonicwall.com/\#/wireless-access-point-allow-station)      Wireless access point mode: Allow specified station API.

POST[/wireless/access-point/allow-station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-allow-station/post_wireless_access_point_allow_station__STATIONMAC_)

POST[/wireless/access-point/allow-station/{STATIONMAC}/enable-mac](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-allow-station/post_wireless_access_point_allow_station__STATIONMAC__enable_mac)

#### [wireless-access-point-disassociate-station](https://sonicos-api.sonicwall.com/\#/wireless-access-point-disassociate-station)      Wireless access point mode: Logout and disassociate specified station API.

POST[/wireless/access-point/disassociate-station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-disassociate-station/post_wireless_access_point_disassociate_station__STATIONMAC_)

#### [wireless-access-point-disassociate-stations](https://sonicos-api.sonicwall.com/\#/wireless-access-point-disassociate-stations)      Wireless access point mode: Logout and disassociate all stations API.

POST[/wireless/access-point/disassociate-stations](https://sonicos-api.sonicwall.com/#/operations/wireless-access-point-disassociate-stations/post_wireless_access_point_disassociate_stations)

#### [wireless-wds-station-connect](https://sonicos-api.sonicwall.com/\#/wireless-wds-station-connect)      Wireless wds station mode: Connect to the specified access point API.

POST[/wireless/wds-station/connect/{APSSID}](https://sonicos-api.sonicwall.com/#/operations/wireless-wds-station-connect/post_wireless_wds_station_connect__APSSID_)

#### [wireless-wds-station-scan](https://sonicos-api.sonicwall.com/\#/wireless-wds-station-scan)      Wireless wds station mode: Scan nearby access points API.

POST[/wireless/wds-station/scan](https://sonicos-api.sonicwall.com/#/operations/wireless-wds-station-scan/post_wireless_wds_station_scan)

#### [wireless-ids-authorizing](https://sonicos-api.sonicwall.com/\#/wireless-ids-authorizing)      Wireless IDS authorizing the access point API.

POST[/wireless/ids/authorizing-access-point/{APMAC}](https://sonicos-api.sonicwall.com/#/operations/wireless-ids-authorizing/post_wireless_ids_authorizing_access_point__APMAC_)

#### [wireless-ids-scan](https://sonicos-api.sonicwall.com/\#/wireless-ids-scan)      Wireless IDS scan API.

POST[/wireless/ids/scan](https://sonicos-api.sonicwall.com/#/operations/wireless-ids-scan/post_wireless_ids_scan)

#### [wireless-status](https://sonicos-api.sonicwall.com/\#/wireless-status)      Wireless status reporting API.

GET[/reporting/wireless/status](https://sonicos-api.sonicwall.com/#/operations/wireless-status/get_reporting_wireless_status)

#### [wireless-mix-mode-status-station](https://sonicos-api.sonicwall.com/\#/wireless-mix-mode-status-station)      Wireless status reporting API.

GET[/reporting/wireless/mix-mode/status/station](https://sonicos-api.sonicwall.com/#/operations/wireless-mix-mode-status-station/get_reporting_wireless_mix_mode_status_station)

#### [wireless-mix-mode-status-ap](https://sonicos-api.sonicwall.com/\#/wireless-mix-mode-status-ap)      Wireless status reporting API.

GET[/reporting/wireless/mix-mode/status/ap](https://sonicos-api.sonicwall.com/#/operations/wireless-mix-mode-status-ap/get_reporting_wireless_mix_mode_status_ap)

#### [wireless-statistics](https://sonicos-api.sonicwall.com/\#/wireless-statistics)      Wireless statistics reporting API.

GET[/reporting/wireless/statistics](https://sonicos-api.sonicwall.com/#/operations/wireless-statistics/get_reporting_wireless_statistics)

#### [wireless-activities](https://sonicos-api.sonicwall.com/\#/wireless-activities)      Wireless activities reporting API.

GET[/reporting/wireless/activities](https://sonicos-api.sonicwall.com/#/operations/wireless-activities/get_reporting_wireless_activities)

#### [wireless-stations](https://sonicos-api.sonicwall.com/\#/wireless-stations)      Wireless stations reporting API.

GET[/reporting/wireless/stations](https://sonicos-api.sonicwall.com/#/operations/wireless-stations/get_reporting_wireless_stations)

#### [wireless-discovered-access-points](https://sonicos-api.sonicwall.com/\#/wireless-discovered-access-points)      Wireless discovered access points reporting API.

GET[/reporting/wireless/discovered-access-points](https://sonicos-api.sonicwall.com/#/operations/wireless-discovered-access-points/get_reporting_wireless_discovered_access_points)

#### [sonicpoint-floor-plan](https://sonicos-api.sonicwall.com/\#/sonicpoint-floor-plan)      Floor plan configuration API.

GET[/sonicpoint/floor-plans](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/get_sonicpoint_floor_plans)

POST[/sonicpoint/floor-plans](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/post_sonicpoint_floor_plans)

PUT[/sonicpoint/floor-plans](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/put_sonicpoint_floor_plans)

PATCH[/sonicpoint/floor-plans](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/patch_sonicpoint_floor_plans)

GET[/sonicpoint/floor-plans/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/get_sonicpoint_floor_plans_name__NAME_)

PUT[/sonicpoint/floor-plans/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/put_sonicpoint_floor_plans_name__NAME_)

PATCH[/sonicpoint/floor-plans/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/patch_sonicpoint_floor_plans_name__NAME_)

DELETE[/sonicpoint/floor-plans/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-floor-plan/delete_sonicpoint_floor_plans_name__NAME_)

#### [export-floor-plan-png](https://sonicos-api.sonicwall.com/\#/export-floor-plan-png)      Export floor plan png configurations.

GET[/export/sonicpoint/floor-plan/png/{FLOORPLANNAME}](https://sonicos-api.sonicwall.com/#/operations/export-floor-plan-png/get_export_sonicpoint_floor_plan_png__FLOORPLANNAME_)

#### [export-floor-plan-jpg](https://sonicos-api.sonicwall.com/\#/export-floor-plan-jpg)      Export floor plan jpg configurations.

GET[/export/sonicpoint/floor-plan/jpg/{FLOORPLANNAME}](https://sonicos-api.sonicwall.com/#/operations/export-floor-plan-jpg/get_export_sonicpoint_floor_plan_jpg__FLOORPLANNAME_)

#### [import-floor-plan](https://sonicos-api.sonicwall.com/\#/import-floor-plan)      import floor plan jpg configurations.

POST[/import/sonicpoint/floor-plan/{FLOORPLANNAME}](https://sonicos-api.sonicwall.com/#/operations/import-floor-plan/post_import_sonicpoint_floor_plan__FLOORPLANNAME_)

#### [sonicpoint-profile](https://sonicos-api.sonicwall.com/\#/sonicpoint-profile)      SonicPoint/SonicWave provisioning profile configuration API.

GET[/sonicpoint/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/get_sonicpoint_profiles)

POST[/sonicpoint/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/post_sonicpoint_profiles)

PUT[/sonicpoint/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/put_sonicpoint_profiles)

PATCH[/sonicpoint/profiles](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/patch_sonicpoint_profiles)

GET[/sonicpoint/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/get_sonicpoint_profiles_name__NAME_)

PUT[/sonicpoint/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/put_sonicpoint_profiles_name__NAME_)

PATCH[/sonicpoint/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/patch_sonicpoint_profiles_name__NAME_)

DELETE[/sonicpoint/profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-profile/delete_sonicpoint_profiles_name__NAME_)

#### [sonicpoint-object](https://sonicos-api.sonicwall.com/\#/sonicpoint-object)      SonicPoint/SonicWave objects configuration API.

GET[/sonicpoint/sonicpoints](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/get_sonicpoint_sonicpoints)

PUT[/sonicpoint/sonicpoints](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/put_sonicpoint_sonicpoints)

PATCH[/sonicpoint/sonicpoints](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/patch_sonicpoint_sonicpoints)

GET[/sonicpoint/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/get_sonicpoint_sonicpoints_name__NAME_)

PUT[/sonicpoint/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/put_sonicpoint_sonicpoints_name__NAME_)

PATCH[/sonicpoint/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/patch_sonicpoint_sonicpoints_name__NAME_)

DELETE[/sonicpoint/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-object/delete_sonicpoint_sonicpoints_name__NAME_)

#### [firmware-management](https://sonicos-api.sonicwall.com/\#/firmware-management)      SonicPoint firmware management configuration API.

GET[/sonicpoint/firmware-management](https://sonicos-api.sonicwall.com/#/operations/firmware-management/get_sonicpoint_firmware_management)

PUT[/sonicpoint/firmware-management](https://sonicos-api.sonicwall.com/#/operations/firmware-management/put_sonicpoint_firmware_management)

#### [firmware-management-reset-sonicpoint-raw](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicpoint-raw)      Reset SonicPoint firmware API.

POST[/sonicpoint/firmware-management-reset/sonicpoint-raw](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicpoint-raw/post_sonicpoint_firmware_management_reset_sonicpoint_raw)

#### [firmware-management-reset-sonicpoint-n](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicpoint-n)      Reset SonicPoint N firmware API.

POST[/sonicpoint/firmware-management-reset/sonicpoint-n](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicpoint-n/post_sonicpoint_firmware_management_reset_sonicpoint_n)

#### [firmware-management-reset-sonicpoint-nv](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicpoint-nv)      Reset SonicPoint N firmware API.

POST[/sonicpoint/firmware-management-reset/sonicpoint-nv](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicpoint-nv/post_sonicpoint_firmware_management_reset_sonicpoint_nv)

#### [firmware-management-reset-sonicpoint-ndr](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicpoint-ndr)      Reset SonicPoint N firmware API.

POST[/sonicpoint/firmware-management-reset/sonicpoint-ndr](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicpoint-ndr/post_sonicpoint_firmware_management_reset_sonicpoint_ndr)

#### [firmware-management-reset-sonicpoint-ac](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicpoint-ac)      Reset SonicPoint N firmware API.

POST[/sonicpoint/firmware-management-reset/sonicpoint-ac](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicpoint-ac/post_sonicpoint_firmware_management_reset_sonicpoint_ac)

#### [firmware-management-reset-sonicwave400](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicwave400)      Reset SonicPoint N firmware API.

POST[/sonicpoint/firmware-management-reset/sonicwave400](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicwave400/post_sonicpoint_firmware_management_reset_sonicwave400)

#### [firmware-management-reset-sonicwave200](https://sonicos-api.sonicwall.com/\#/firmware-management-reset-sonicwave200)      Reset SonicPoint N firmware API.

POST[/sonicpoint/firmware-management-reset/sonicwave200](https://sonicos-api.sonicwall.com/#/operations/firmware-management-reset-sonicwave200/post_sonicpoint_firmware_management_reset_sonicwave200)

#### [import-sonicpoint-firmware-sonicpoint-raw](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicpoint-raw)      Upload sonicpoint firmware.

PUT[/import/sonicpoint/firmware/sonicpoint-raw](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicpoint-raw/put_import_sonicpoint_firmware_sonicpoint_raw)

#### [import-sonicpoint-firmware-sonicpoint-n](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicpoint-n)      Upload sonicpoint N firmware.

PUT[/import/sonicpoint/firmware/sonicpoint-n](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicpoint-n/put_import_sonicpoint_firmware_sonicpoint_n)

#### [import-sonicpoint-firmware-sonicpoint-nv](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicpoint-nv)      Upload SonicPoint N firmware API.

PUT[/import/sonicpoint/firmware/sonicpoint-nv](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicpoint-nv/put_import_sonicpoint_firmware_sonicpoint_nv)

#### [import-sonicpoint-firmware-sonicpoint-ndr](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicpoint-ndr)      Upload SonicPoint N firmware API.

PUT[/import/sonicpoint/firmware/sonicpoint-ndr](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicpoint-ndr/put_import_sonicpoint_firmware_sonicpoint_ndr)

#### [import-sonicpoint-firmware-sonicpoint-ac](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicpoint-ac)      Upload SonicPoint N firmware API.

PUT[/import/sonicpoint/firmware/sonicpoint-ac](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicpoint-ac/put_import_sonicpoint_firmware_sonicpoint_ac)

#### [import-sonicpoint-firmware-sonicwave400](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicwave400)      Upload SonicPoint N firmware API.

PUT[/import/sonicpoint/firmware/sonicwave400](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicwave400/put_import_sonicpoint_firmware_sonicwave400)

#### [import-sonicpoint-firmware-sonicwave200](https://sonicos-api.sonicwall.com/\#/import-sonicpoint-firmware-sonicwave200)      Upload SonicPoint N firmware API.

PUT[/import/sonicpoint/firmware/sonicwave200](https://sonicos-api.sonicwall.com/#/operations/import-sonicpoint-firmware-sonicwave200/put_import_sonicpoint_firmware_sonicwave200)

#### [widp](https://sonicos-api.sonicwall.com/\#/widp)      SonicPoint wireless intrusion detection and prevention configuration API.

GET[/sonicpoint/widp](https://sonicos-api.sonicwall.com/#/operations/widp/get_sonicpoint_widp)

PUT[/sonicpoint/widp](https://sonicos-api.sonicwall.com/#/operations/widp/put_sonicpoint_widp)

#### [rf-monitoring](https://sonicos-api.sonicwall.com/\#/rf-monitoring)      RF monitoring configuration API.

GET[/sonicpoint/rf-monitoring/base](https://sonicos-api.sonicwall.com/#/operations/rf-monitoring/get_sonicpoint_rf_monitoring_base)

PUT[/sonicpoint/rf-monitoring/base](https://sonicos-api.sonicwall.com/#/operations/rf-monitoring/put_sonicpoint_rf_monitoring_base)

#### [fairnet](https://sonicos-api.sonicwall.com/\#/fairnet)      FairNet base settings API.

GET[/sonicpoint/fairnet/base](https://sonicos-api.sonicwall.com/#/operations/fairnet/get_sonicpoint_fairnet_base)

PUT[/sonicpoint/fairnet/base](https://sonicos-api.sonicwall.com/#/operations/fairnet/put_sonicpoint_fairnet_base)

#### [fairnet-policies](https://sonicos-api.sonicwall.com/\#/fairnet-policies)      FairNet policies API.

GET[/sonicpoint/fairnet/policies/direction/{DIRECT}/range/{START}/{END}/interface/{IF}](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/get_sonicpoint_fairnet_policies_direction__DIRECT__range__START___END__interface__IF_)

PUT[/sonicpoint/fairnet/policies/direction/{DIRECT}/range/{START}/{END}/interface/{IF}](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/put_sonicpoint_fairnet_policies_direction__DIRECT__range__START___END__interface__IF_)

PATCH[/sonicpoint/fairnet/policies/direction/{DIRECT}/range/{START}/{END}/interface/{IF}](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/patch_sonicpoint_fairnet_policies_direction__DIRECT__range__START___END__interface__IF_)

DELETE[/sonicpoint/fairnet/policies/direction/{DIRECT}/range/{START}/{END}/interface/{IF}](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/delete_sonicpoint_fairnet_policies_direction__DIRECT__range__START___END__interface__IF_)

GET[/sonicpoint/fairnet/policies](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/get_sonicpoint_fairnet_policies)

POST[/sonicpoint/fairnet/policies](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/post_sonicpoint_fairnet_policies)

PUT[/sonicpoint/fairnet/policies](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/put_sonicpoint_fairnet_policies)

PATCH[/sonicpoint/fairnet/policies](https://sonicos-api.sonicwall.com/#/operations/fairnet-policies/patch_sonicpoint_fairnet_policies)

#### [sonicpoint-synchronize](https://sonicos-api.sonicwall.com/\#/sonicpoint-synchronize)      Synchronize sonicpoints API.

POST[/sonicpoint/synchronize](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-synchronize/post_sonicpoint_synchronize)

#### [sonicpoint-register](https://sonicos-api.sonicwall.com/\#/sonicpoint-register)      Register sonicpoints API.

POST[/sonicpoint/register/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-register/post_sonicpoint_register_name__NAME_)

POST[/sonicpoint/register/name/{NAME}/country-code/{CODE}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-register/post_sonicpoint_register_name__NAME__country_code__CODE_)

#### [sonicpoint-upgrade](https://sonicos-api.sonicwall.com/\#/sonicpoint-upgrade)      Upgrade sonicpoint API.

PUT[/sonicpoint/upgrade](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-upgrade/put_sonicpoint_upgrade)

#### [sonicpoint-reboot](https://sonicos-api.sonicwall.com/\#/sonicpoint-reboot)      Reboot sonicpoints API.

POST[/sonicpoint/reboot/sonicpoints](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-reboot/post_sonicpoint_reboot_sonicpoints)

POST[/sonicpoint/reboot/sonicpoints/factory-default](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-reboot/post_sonicpoint_reboot_sonicpoints_factory_default)

#### [sonicpoint-reboot-sonicpoint](https://sonicos-api.sonicwall.com/\#/sonicpoint-reboot-sonicpoint)      Reboot the specific sonicpoint API.

POST[/sonicpoint/reboot/sonicpoint/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-reboot-sonicpoint/post_sonicpoint_reboot_sonicpoint__NAME_)

POST[/sonicpoint/reboot/sonicpoint/{NAME}/factory-default](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-reboot-sonicpoint/post_sonicpoint_reboot_sonicpoint__NAME__factory_default)

#### [sonicpoint-ids-scan-all](https://sonicos-api.sonicwall.com/\#/sonicpoint-ids-scan-all)      IDS scan all sonicpoints API.

POST[/sonicpoint/ids/scan/all](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-ids-scan-all/post_sonicpoint_ids_scan_all)

#### [sonicpoint-ids-scan-both](https://sonicos-api.sonicwall.com/\#/sonicpoint-ids-scan-both)      IDS scan specific sonicpoint on its both 2.4G and 5G radio API.

POST[/sonicpoint/ids/scan/radio/both/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-ids-scan-both/post_sonicpoint_ids_scan_radio_both_sonicpoints_name__NAME_)

#### [sonicpoint-ids-scan-2400mhz](https://sonicos-api.sonicwall.com/\#/sonicpoint-ids-scan-2400mhz)      IDS scan specific sonicpoint on its 2.4G radio API.

POST[/sonicpoint/ids/scan/radio/2400mhz/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-ids-scan-2400mhz/post_sonicpoint_ids_scan_radio_2400mhz_sonicpoints_name__NAME_)

#### [sonicpoint-ids-scan-5000mhz](https://sonicos-api.sonicwall.com/\#/sonicpoint-ids-scan-5000mhz)      IDS scan specific sonicpoint on its 5G radio API.

POST[/sonicpoint/ids/scan/radio/5000mhz/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-ids-scan-5000mhz/post_sonicpoint_ids_scan_radio_5000mhz_sonicpoints_name__NAME_)

#### [sonicpoint-ids-authorizing-ap](https://sonicos-api.sonicwall.com/\#/sonicpoint-ids-authorizing-ap)      Authorizing the access point API.

POST[/sonicpoint/ids/authorizing-access-point/{APMAC}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-ids-authorizing-ap/post_sonicpoint_ids_authorizing_access_point__APMAC_)

#### [sonicpoint-rf-monitoring-watch-station](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-monitoring-watch-station)      Add/Remove station into/from watch list API.

POST[/sonicpoint/rf-monitoring/watch/station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-monitoring-watch-station/post_sonicpoint_rf_monitoring_watch_station__STATIONMAC_)

DELETE[/sonicpoint/rf-monitoring/watch/station/{STATIONMAC}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-monitoring-watch-station/delete_sonicpoint_rf_monitoring_watch_station__STATIONMAC_)

#### [rf-monitoring-statistics](https://sonicos-api.sonicwall.com/\#/rf-monitoring-statistics)      Clear RF monitoring statistics action API.

DELETE[/sonicpoint/rf-monitoring/statistics](https://sonicos-api.sonicwall.com/#/operations/rf-monitoring-statistics/delete_sonicpoint_rf_monitoring_statistics)

#### [sonicpoint-status](https://sonicos-api.sonicwall.com/\#/sonicpoint-status)      Sonicpoint reporting API.

GET[/reporting/sonicpoint/status](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-status/get_reporting_sonicpoint_status)

GET[/reporting/sonicpoint/status/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-status/get_reporting_sonicpoint_status_sonicpoints_name__NAME_)

#### [sonicpoint-vap-status](https://sonicos-api.sonicwall.com/\#/sonicpoint-vap-status)      Sonicpoint virtual access point reporting API.

GET[/reporting/sonicpoint/virtual-access-point-status](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-status/get_reporting_sonicpoint_virtual_access_point_status)

GET[/reporting/sonicpoint/virtual-access-point-status/radio/{RADIOTYPE}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-status/get_reporting_sonicpoint_virtual_access_point_status_radio__RADIOTYPE_)

GET[/reporting/sonicpoint/virtual-access-point-status/sonicpoints/name/{NAME}/radio/{RADIOTYPE}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-vap-status/get_reporting_sonicpoint_virtual_access_point_status_sonicpoints_name__NAME__radio__RADIOTYPE_)

#### [sonicpoint-statistics-radio](https://sonicos-api.sonicwall.com/\#/sonicpoint-statistics-radio)      Sonicpoint radio statistics reporting API.

GET[/reporting/sonicpoint/statistics/radio](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-statistics-radio/get_reporting_sonicpoint_statistics_radio)

GET[/reporting/sonicpoint/statistics/radio/sonicpoint/{SPNAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-statistics-radio/get_reporting_sonicpoint_statistics_radio_sonicpoint__SPNAME_)

#### [sonicpoint-statistics-traffic](https://sonicos-api.sonicwall.com/\#/sonicpoint-statistics-traffic)      Sonicpoint traffic statistics reporting API.

GET[/reporting/sonicpoint/statistics/traffic](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-statistics-traffic/get_reporting_sonicpoint_statistics_traffic)

GET[/reporting/sonicpoint/statistics/traffic/sonicpoint/{SPNAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-statistics-traffic/get_reporting_sonicpoint_statistics_traffic_sonicpoint__SPNAME_)

#### [sonicpoint-station-status](https://sonicos-api.sonicwall.com/\#/sonicpoint-station-status)      Sonicpoint station reporting API.

GET[/reporting/sonicpoint/station/status](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-station-status/get_reporting_sonicpoint_station_status)

GET[/reporting/sonicpoint/station/status/sonicpoints/name/{NAME}/station-mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-station-status/get_reporting_sonicpoint_station_status_sonicpoints_name__NAME__station_mac__MAC_)

#### [sonicpoint-station-statistics-radio](https://sonicos-api.sonicwall.com/\#/sonicpoint-station-statistics-radio)      Sonicpoint station radio statistics reporting API.

GET[/reporting/sonicpoint/station/statistics/radio](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-station-statistics-radio/get_reporting_sonicpoint_station_statistics_radio)

GET[/reporting/sonicpoint/station/statistics/radio/sonicpoint/{SPNAME}/station-mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-station-statistics-radio/get_reporting_sonicpoint_station_statistics_radio_sonicpoint__SPNAME__station_mac__MAC_)

#### [sonicpoint-station-statistics-traffic](https://sonicos-api.sonicwall.com/\#/sonicpoint-station-statistics-traffic)      Sonicpoint station traffic statistics reporting API.

GET[/reporting/sonicpoint/station/statistics/traffic](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-station-statistics-traffic/get_reporting_sonicpoint_station_statistics_traffic)

GET[/reporting/sonicpoint/station/statistics/traffic/sonicpoint/{SPNAME}/station-mac/{MAC}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-station-statistics-traffic/get_reporting_sonicpoint_station_statistics_traffic_sonicpoint__SPNAME__station_mac__MAC_)

#### [sonicpoint-discovered-access-points](https://sonicos-api.sonicwall.com/\#/sonicpoint-discovered-access-points)      Sonicpoint discovered access points reporting API.

GET[/reporting/sonicpoint/discovered-access-points](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-discovered-access-points/get_reporting_sonicpoint_discovered_access_points)

GET[/reporting/sonicpoint/discovered-access-points/sonicpoints/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-discovered-access-points/get_reporting_sonicpoint_discovered_access_points_sonicpoints_name__NAME_)

#### [sonicpoint-widp-sensor-unit](https://sonicos-api.sonicwall.com/\#/sonicpoint-widp-sensor-unit)      Sonicpoint widp sensor unit reporting API.

GET[/reporting/sonicpoint/widp/sensor-unit](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-widp-sensor-unit/get_reporting_sonicpoint_widp_sensor_unit)

#### [sonicpoint-rf-monitoring-statistics](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-monitoring-statistics)      Sonicpoint rf monitoring statistics reporting API.

GET[/reporting/sonicpoint/rf/monitoring/statistics](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-monitoring-statistics/get_reporting_sonicpoint_rf_monitoring_statistics)

#### [sonicpoint-rf-monitoring-discovered-threat-stations](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-monitoring-discovered-threat-stations)      Sonicpoint rf monitoring discovered threat stations reporting API.

GET[/reporting/sonicpoint/rf/monitoring/discovered-threat-stations](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-monitoring-discovered-threat-stations/get_reporting_sonicpoint_rf_monitoring_discovered_threat_stations)

#### [sonicpoint-rf-monitoring-watch-list-stations](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-monitoring-watch-list-stations)      Sonicpoint rf monitoring stations in watch list group reporting API.

GET[/reporting/sonicpoint/rf/monitoring/watch-list-stations](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-monitoring-watch-list-stations/get_reporting_sonicpoint_rf_monitoring_watch_list_stations)

#### [sonicpoint-rf-analysis-score](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-analysis-score)      Sonicpoint rf analysis RF score reporting API.

GET[/reporting/sonicpoint/rf/analysis/score](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-analysis-score/get_reporting_sonicpoint_rf_analysis_score)

#### [sonicpoint-rf-analysis-channel-overloaded](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-analysis-channel-overloaded)      Sonicpoint rf analysis channel overloaded statistics reporting API.

GET[/reporting/sonicpoint/rf/analysis/channel/overloaded](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-analysis-channel-overloaded/get_reporting_sonicpoint_rf_analysis_channel_overloaded)

#### [sonicpoint-rf-analysis-channel-highly-interfered](https://sonicos-api.sonicwall.com/\#/sonicpoint-rf-analysis-channel-highly-interfered)      Sonicpoint rf analysis channel highly-interfered statistics reporting API.

GET[/reporting/sonicpoint/rf/analysis/channel/highly-interfered](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rf-analysis-channel-highly-interfered/get_reporting_sonicpoint_rf_analysis_channel_highly_interfered)

#### [sonicpoint-krack-sniffer-clear](https://sonicos-api.sonicwall.com/\#/sonicpoint-krack-sniffer-clear)      Sonicpoint KRACK sniffer clear buffer API.

DELETE[/sonicpoint/krack-sniffer/clear](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-krack-sniffer-clear/delete_sonicpoint_krack_sniffer_clear)

#### [sonicpoint-packet-capture-clear](https://sonicos-api.sonicwall.com/\#/sonicpoint-packet-capture-clear)      Sonicpoint packet capture clear buffer API.

DELETE[/sonicpoint/packet-capture/clear](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-packet-capture-clear/delete_sonicpoint_packet_capture_clear)

#### [sonicpoint-stations-logout](https://sonicos-api.sonicwall.com/\#/sonicpoint-stations-logout)      Logout and disassociate sonicpoint station API.

DELETE[/sonicpoint/station/logout](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-stations-logout/delete_sonicpoint_station_logout)

#### [rrm](https://sonicos-api.sonicwall.com/\#/rrm)      SonicPoint RRM function configuration API.

GET[/sonicpoint/rrm](https://sonicos-api.sonicwall.com/#/operations/rrm/get_sonicpoint_rrm)

PUT[/sonicpoint/rrm](https://sonicos-api.sonicwall.com/#/operations/rrm/put_sonicpoint_rrm)

#### [sonicpoint-rrm-force-switch](https://sonicos-api.sonicwall.com/\#/sonicpoint-rrm-force-switch)      Force to Switch 2.4G/5G channel

POST[/sonicpoint/rrm-force-switch/24g](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rrm-force-switch/post_sonicpoint_rrm_force_switch_24g)

POST[/sonicpoint/rrm-force-switch/5g](https://sonicos-api.sonicwall.com/#/operations/sonicpoint-rrm-force-switch/post_sonicpoint_rrm_force_switch_5g)

#### [wmm](https://sonicos-api.sonicwall.com/\#/wmm)      WiFi multimedia profile configuration API.

GET[/sonicpoint/wmm](https://sonicos-api.sonicwall.com/#/operations/wmm/get_sonicpoint_wmm)

POST[/sonicpoint/wmm](https://sonicos-api.sonicwall.com/#/operations/wmm/post_sonicpoint_wmm)

PUT[/sonicpoint/wmm](https://sonicos-api.sonicwall.com/#/operations/wmm/put_sonicpoint_wmm)

PATCH[/sonicpoint/wmm](https://sonicos-api.sonicwall.com/#/operations/wmm/patch_sonicpoint_wmm)

GET[/sonicpoint/wmm/profile/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wmm/get_sonicpoint_wmm_profile__NAME_)

PUT[/sonicpoint/wmm/profile/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wmm/put_sonicpoint_wmm_profile__NAME_)

PATCH[/sonicpoint/wmm/profile/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wmm/patch_sonicpoint_wmm_profile__NAME_)

DELETE[/sonicpoint/wmm/profile/{NAME}](https://sonicos-api.sonicwall.com/#/operations/wmm/delete_sonicpoint_wmm_profile__NAME_)

#### [cli-idle-timeout](https://sonicos-api.sonicwall.com/\#/cli-idle-timeout)      CLI idle timeout configuration API.

GET[/cli/idle-timeout](https://sonicos-api.sonicwall.com/#/operations/cli-idle-timeout/get_cli_idle_timeout)

PUT[/cli/idle-timeout](https://sonicos-api.sonicwall.com/#/operations/cli-idle-timeout/put_cli_idle_timeout)

#### [cli-screen](https://sonicos-api.sonicwall.com/\#/cli-screen)      CLI screen configuration API.

GET[/cli/screen](https://sonicos-api.sonicwall.com/#/operations/cli-screen/get_cli_screen)

PUT[/cli/screen](https://sonicos-api.sonicwall.com/#/operations/cli-screen/put_cli_screen)

#### [cli-show-unmodified](https://sonicos-api.sonicwall.com/\#/cli-show-unmodified)      CLI show unmodified configuration API.

GET[/cli/show-unmodified](https://sonicos-api.sonicwall.com/#/operations/cli-show-unmodified/get_cli_show_unmodified)

PUT[/cli/show-unmodified](https://sonicos-api.sonicwall.com/#/operations/cli-show-unmodified/put_cli_show_unmodified)

#### [cli-pager](https://sonicos-api.sonicwall.com/\#/cli-pager)      CLI pager configuration API.

GET[/cli/pager](https://sonicos-api.sonicwall.com/#/operations/cli-pager/get_cli_pager)

PUT[/cli/pager](https://sonicos-api.sonicwall.com/#/operations/cli-pager/put_cli_pager)

#### [cli-interactive-prompts](https://sonicos-api.sonicwall.com/\#/cli-interactive-prompts)      CLI interactive prompts configuration API.

GET[/cli/interactive-prompts](https://sonicos-api.sonicwall.com/#/operations/cli-interactive-prompts/get_cli_interactive_prompts)

PUT[/cli/interactive-prompts](https://sonicos-api.sonicwall.com/#/operations/cli-interactive-prompts/put_cli_interactive_prompts)

#### [cli-ftp](https://sonicos-api.sonicwall.com/\#/cli-ftp)      CLI FTP configuration API.

GET[/cli/ftp](https://sonicos-api.sonicwall.com/#/operations/cli-ftp/get_cli_ftp)

PUT[/cli/ftp](https://sonicos-api.sonicwall.com/#/operations/cli-ftp/put_cli_ftp)

#### [cli-banner](https://sonicos-api.sonicwall.com/\#/cli-banner)      CLI banner configuration API.

GET[/cli/banner](https://sonicos-api.sonicwall.com/#/operations/cli-banner/get_cli_banner)

PUT[/cli/banner](https://sonicos-api.sonicwall.com/#/operations/cli-banner/put_cli_banner)

#### [security-services](https://sonicos-api.sonicwall.com/\#/security-services)      Security services configuration API.

GET[/security-services/base](https://sonicos-api.sonicwall.com/#/operations/security-services/get_security_services_base)

PUT[/security-services/base](https://sonicos-api.sonicwall.com/#/operations/security-services/put_security_services_base)

#### [security-services-synchronize](https://sonicos-api.sonicwall.com/\#/security-services-synchronize)      Security services synchronize API.

POST[/security-services/synchronize](https://sonicos-api.sonicwall.com/#/operations/security-services-synchronize/post_security_services_synchronize)

#### [import-security-services-signature](https://sonicos-api.sonicwall.com/\#/import-security-services-signature)      Upload signature API.

POST[/import/security-services/signature](https://sonicos-api.sonicwall.com/#/operations/import-security-services-signature/post_import_security_services_signature)

#### [import-security-services-geoip](https://sonicos-api.sonicwall.com/\#/import-security-services-geoip)      Upload geoip database API.

POST[/import/security-services/geoip](https://sonicos-api.sonicwall.com/#/operations/import-security-services-geoip/post_import_security_services_geoip)

#### [import-security-services-botnet](https://sonicos-api.sonicwall.com/\#/import-security-services-botnet)      Upload botnet database API.

POST[/import/security-services/botnet](https://sonicos-api.sonicwall.com/#/operations/import-security-services-botnet/post_import_security_services_botnet)

#### [geo-ip-base](https://sonicos-api.sonicwall.com/\#/geo-ip-base)      Geo-IP base configuration API.

GET[/geo-ip/base](https://sonicos-api.sonicwall.com/#/operations/geo-ip-base/get_geo_ip_base)

PUT[/geo-ip/base](https://sonicos-api.sonicwall.com/#/operations/geo-ip-base/put_geo_ip_base)

#### [geo-ip-countries](https://sonicos-api.sonicwall.com/\#/geo-ip-countries)      Geo-IP countries configuration API.

GET[/geo-ip/countries](https://sonicos-api.sonicwall.com/#/operations/geo-ip-countries/get_geo_ip_countries)

PUT[/geo-ip/countries](https://sonicos-api.sonicwall.com/#/operations/geo-ip-countries/put_geo_ip_countries)

PATCH[/geo-ip/countries](https://sonicos-api.sonicwall.com/#/operations/geo-ip-countries/patch_geo_ip_countries)

#### [geo-ip-addresses](https://sonicos-api.sonicwall.com/\#/geo-ip-addresses)      Addresses in the custom Geo-IP list configuration API.

GET[/geo-ip/addresses](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/get_geo_ip_addresses)

POST[/geo-ip/addresses](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/post_geo_ip_addresses)

PUT[/geo-ip/addresses](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/put_geo_ip_addresses)

PATCH[/geo-ip/addresses](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/patch_geo_ip_addresses)

GET[/geo-ip/addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/get_geo_ip_addresses_name__NAME_)

PUT[/geo-ip/addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/put_geo_ip_addresses_name__NAME_)

PATCH[/geo-ip/addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/patch_geo_ip_addresses_name__NAME_)

DELETE[/geo-ip/addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/delete_geo_ip_addresses_name__NAME_)

GET[/geo-ip/addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/get_geo_ip_addresses_group__GRPNAME_)

PUT[/geo-ip/addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/put_geo_ip_addresses_group__GRPNAME_)

PATCH[/geo-ip/addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/patch_geo_ip_addresses_group__GRPNAME_)

DELETE[/geo-ip/addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/geo-ip-addresses/delete_geo_ip_addresses_group__GRPNAME_)

#### [geo-ip-status](https://sonicos-api.sonicwall.com/\#/geo-ip-status)      Geo-IP status reporting API.

GET[/reporting/geo-ip/status](https://sonicos-api.sonicwall.com/#/operations/geo-ip-status/get_reporting_geo_ip_status)

#### [geo-ip-resolved-locations](https://sonicos-api.sonicwall.com/\#/geo-ip-resolved-locations)      Geo-IP statistics reporting API.

GET[/reporting/geo-ip/resolved-locations](https://sonicos-api.sonicwall.com/#/operations/geo-ip-resolved-locations/get_reporting_geo_ip_resolved_locations)

#### [geo-ip-cache-statistics](https://sonicos-api.sonicwall.com/\#/geo-ip-cache-statistics)      Geo-IP cache statistics reporting API.

GET[/reporting/geo-ip/cache-statistics](https://sonicos-api.sonicwall.com/#/operations/geo-ip-cache-statistics/get_reporting_geo_ip_cache_statistics)

#### [geo-ip-custom-countries-statistics](https://sonicos-api.sonicwall.com/\#/geo-ip-custom-countries-statistics)      Geo-IP custom countries statistics reporting API.

GET[/reporting/geo-ip/custom-countries-statistics](https://sonicos-api.sonicwall.com/#/operations/geo-ip-custom-countries-statistics/get_reporting_geo_ip_custom_countries_statistics)

#### [botnet](https://sonicos-api.sonicwall.com/\#/botnet)      Botnet configuration API.

GET[/botnet/base](https://sonicos-api.sonicwall.com/#/operations/botnet/get_botnet_base)

PUT[/botnet/base](https://sonicos-api.sonicwall.com/#/operations/botnet/put_botnet_base)

#### [botnet-custom-list-address](https://sonicos-api.sonicwall.com/\#/botnet-custom-list-address)      Botnet custom list addresses configuration API.

GET[/botnet/custom-list-addresses](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/get_botnet_custom_list_addresses)

POST[/botnet/custom-list-addresses](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/post_botnet_custom_list_addresses)

PUT[/botnet/custom-list-addresses](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/put_botnet_custom_list_addresses)

PATCH[/botnet/custom-list-addresses](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/patch_botnet_custom_list_addresses)

GET[/botnet/custom-list-addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/get_botnet_custom_list_addresses_name__NAME_)

PUT[/botnet/custom-list-addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/put_botnet_custom_list_addresses_name__NAME_)

PATCH[/botnet/custom-list-addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/patch_botnet_custom_list_addresses_name__NAME_)

DELETE[/botnet/custom-list-addresses/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/delete_botnet_custom_list_addresses_name__NAME_)

GET[/botnet/custom-list-addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/get_botnet_custom_list_addresses_group__GRPNAME_)

PUT[/botnet/custom-list-addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/put_botnet_custom_list_addresses_group__GRPNAME_)

PATCH[/botnet/custom-list-addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/patch_botnet_custom_list_addresses_group__GRPNAME_)

DELETE[/botnet/custom-list-addresses/group/{GRPNAME}](https://sonicos-api.sonicwall.com/#/operations/botnet-custom-list-address/delete_botnet_custom_list_addresses_group__GRPNAME_)

#### [botnet-flush](https://sonicos-api.sonicwall.com/\#/botnet-flush)      Flush the IPs downloaded from dynamic botnet servers.

POST[/botnet/dynamic-list/flush](https://sonicos-api.sonicwall.com/#/operations/botnet-flush/post_botnet_dynamic_list_flush)

#### [botnet-download](https://sonicos-api.sonicwall.com/\#/botnet-download)      Download the IPs downloaded from dynamic botnet servers.

POST[/botnet/dynamic-list/download](https://sonicos-api.sonicwall.com/#/operations/botnet-download/post_botnet_dynamic_list_download)

#### [botnet-blocked-page-default](https://sonicos-api.sonicwall.com/\#/botnet-blocked-page-default)      Set the blocked page settings to default.

POST[/botnet/default/blocked-page](https://sonicos-api.sonicwall.com/#/operations/botnet-blocked-page-default/post_botnet_default_blocked_page)

#### [botnet-status](https://sonicos-api.sonicwall.com/\#/botnet-status)      Botnet status statistics reporting API.

GET[/reporting/botnet/status](https://sonicos-api.sonicwall.com/#/operations/botnet-status/get_reporting_botnet_status)

#### [botnet-resolved-locations](https://sonicos-api.sonicwall.com/\#/botnet-resolved-locations)      Botnet resolved locations statistics reporting API.

GET[/reporting/botnet/resolved-locations](https://sonicos-api.sonicwall.com/#/operations/botnet-resolved-locations/get_reporting_botnet_resolved_locations)

#### [botnet-cache](https://sonicos-api.sonicwall.com/\#/botnet-cache)      Botnet cache statistics reporting API.

GET[/reporting/botnet/cache](https://sonicos-api.sonicwall.com/#/operations/botnet-cache/get_reporting_botnet_cache)

#### [anti-spyware-global](https://sonicos-api.sonicwall.com/\#/anti-spyware-global)      Anti spyware global configuration API.

GET[/anti-spyware/base](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-global/get_anti_spyware_base)

PUT[/anti-spyware/base](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-global/put_anti_spyware_base)

#### [anti-spyware-exclusion-list](https://sonicos-api.sonicwall.com/\#/anti-spyware-exclusion-list)      Anti spyware exclusion list configuration API.

GET[/anti-spyware/exclusion-list/base](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-list/get_anti_spyware_exclusion_list_base)

PUT[/anti-spyware/exclusion-list/base](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-list/put_anti_spyware_exclusion_list_base)

#### [anti-spyware-exclusion-entry](https://sonicos-api.sonicwall.com/\#/anti-spyware-exclusion-entry)      Anti spyware exclusion entries configuration API.

GET[/anti-spyware/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/get_anti_spyware_exclusion_list_entries)

POST[/anti-spyware/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/post_anti_spyware_exclusion_list_entries)

PUT[/anti-spyware/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/put_anti_spyware_exclusion_list_entries)

PATCH[/anti-spyware/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/patch_anti_spyware_exclusion_list_entries)

GET[/anti-spyware/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/get_anti_spyware_exclusion_list_entries_from__FROMIP__to__TOIP_)

PUT[/anti-spyware/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/put_anti_spyware_exclusion_list_entries_from__FROMIP__to__TOIP_)

PATCH[/anti-spyware/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/patch_anti_spyware_exclusion_list_entries_from__FROMIP__to__TOIP_)

DELETE[/anti-spyware/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-exclusion-entry/delete_anti_spyware_exclusion_list_entries_from__FROMIP__to__TOIP_)

#### [anti-spyware-product](https://sonicos-api.sonicwall.com/\#/anti-spyware-product)      Anti spyware product object configuration API.

GET[/anti-spyware/products](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-product/get_anti_spyware_products)

PUT[/anti-spyware/products](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-product/put_anti_spyware_products)

GET[/anti-spyware/products/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-product/get_anti_spyware_products_name__NAME_)

PUT[/anti-spyware/products/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-product/put_anti_spyware_products_name__NAME_)

GET[/anti-spyware/products/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-product/get_anti_spyware_products_id__ID_)

PUT[/anti-spyware/products/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-product/put_anti_spyware_products_id__ID_)

#### [anti-spyware-policy](https://sonicos-api.sonicwall.com/\#/anti-spyware-policy)      Anti spyware policy object configuration API.

GET[/anti-spyware/policies](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-policy/get_anti_spyware_policies)

PUT[/anti-spyware/policies](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-policy/put_anti_spyware_policies)

GET[/anti-spyware/policies/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-policy/get_anti_spyware_policies_id__ID_)

PUT[/anti-spyware/policies/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-policy/put_anti_spyware_policies_id__ID_)

#### [anti-spyware-update-signatures](https://sonicos-api.sonicwall.com/\#/anti-spyware-update-signatures)      Anti spyware update signatures action API.

POST[/anti-spyware/update-signatures](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-update-signatures/post_anti_spyware_update_signatures)

#### [anti-spyware-reset](https://sonicos-api.sonicwall.com/\#/anti-spyware-reset)      Anti spyware reset action API.

POST[/anti-spyware/reset](https://sonicos-api.sonicwall.com/#/operations/anti-spyware-reset/post_anti_spyware_reset)

#### [anti-spyware](https://sonicos-api.sonicwall.com/\#/anti-spyware)      Anti spyware reporting API.

GET[/reporting/anti-spyware](https://sonicos-api.sonicwall.com/#/operations/anti-spyware/get_reporting_anti_spyware)

#### [intrusion-prevention-global](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-global)      Intrusion prevention global configuration API.

GET[/intrusion-prevention/base](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-global/get_intrusion_prevention_base)

PUT[/intrusion-prevention/base](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-global/put_intrusion_prevention_base)

#### [intrusion-prevention-exclusion-list](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-exclusion-list)      Intrusion prevention exclusion list configuration API.

GET[/intrusion-prevention/exclusion-list/base](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list/get_intrusion_prevention_exclusion_list_base)

PUT[/intrusion-prevention/exclusion-list/base](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list/put_intrusion_prevention_exclusion_list_base)

#### [intrusion-prevention-exclusion-list-entry](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-exclusion-list-entry)      Intrusion prevention exclusion entries configuration API.

GET[/intrusion-prevention/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/get_intrusion_prevention_exclusion_list_entries)

POST[/intrusion-prevention/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/post_intrusion_prevention_exclusion_list_entries)

PUT[/intrusion-prevention/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/put_intrusion_prevention_exclusion_list_entries)

PATCH[/intrusion-prevention/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/patch_intrusion_prevention_exclusion_list_entries)

GET[/intrusion-prevention/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/get_intrusion_prevention_exclusion_list_entries_from__FROMIP__to__TOIP_)

PUT[/intrusion-prevention/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/put_intrusion_prevention_exclusion_list_entries_from__FROMIP__to__TOIP_)

PATCH[/intrusion-prevention/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/patch_intrusion_prevention_exclusion_list_entries_from__FROMIP__to__TOIP_)

DELETE[/intrusion-prevention/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-exclusion-list-entry/delete_intrusion_prevention_exclusion_list_entries_from__FROMIP__to__TOIP_)

#### [intrusion-prevention-category](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-category)      Intrusion prevention category object configuration API.

GET[/intrusion-prevention/categories](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-category/get_intrusion_prevention_categories)

PUT[/intrusion-prevention/categories](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-category/put_intrusion_prevention_categories)

GET[/intrusion-prevention/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-category/get_intrusion_prevention_categories_name__NAME_)

PUT[/intrusion-prevention/categories/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-category/put_intrusion_prevention_categories_name__NAME_)

GET[/intrusion-prevention/categories/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-category/get_intrusion_prevention_categories_id__ID_)

PUT[/intrusion-prevention/categories/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-category/put_intrusion_prevention_categories_id__ID_)

#### [intrusion-prevention-policy](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-policy)      Intrusion prevention policy object configuration API.

GET[/intrusion-prevention/policies](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-policy/get_intrusion_prevention_policies)

PUT[/intrusion-prevention/policies](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-policy/put_intrusion_prevention_policies)

GET[/intrusion-prevention/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-policy/get_intrusion_prevention_policies_name__NAME_)

PUT[/intrusion-prevention/policies/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-policy/put_intrusion_prevention_policies_name__NAME_)

GET[/intrusion-prevention/policies/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-policy/get_intrusion_prevention_policies_id__ID_)

PUT[/intrusion-prevention/policies/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-policy/put_intrusion_prevention_policies_id__ID_)

#### [intrusion-prevention-update-signatures](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-update-signatures)      Intrusion prevention update signatures action API.

POST[/intrusion-prevention/update-signatures](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-update-signatures/post_intrusion_prevention_update_signatures)

#### [intrusion-prevention-reset](https://sonicos-api.sonicwall.com/\#/intrusion-prevention-reset)      Intrusion prevention reset action API.

POST[/intrusion-prevention/reset](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention-reset/post_intrusion_prevention_reset)

#### [intrusion-prevention](https://sonicos-api.sonicwall.com/\#/intrusion-prevention)      Intrusion prevention reporting API.

GET[/reporting/intrusion-prevention](https://sonicos-api.sonicwall.com/#/operations/intrusion-prevention/get_reporting_intrusion_prevention)

#### [gateway-antivirus](https://sonicos-api.sonicwall.com/\#/gateway-antivirus)      Gateway antivirus configuration API.

GET[/gateway-antivirus/base](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus/get_gateway_antivirus_base)

PUT[/gateway-antivirus/base](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus/put_gateway_antivirus_base)

#### [gateway-antivirus-exclusion-list](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-exclusion-list)      Gateway antivirus exclusion list configuration API.

GET[/gateway-antivirus/exclusion-list/base](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-list/get_gateway_antivirus_exclusion_list_base)

PUT[/gateway-antivirus/exclusion-list/base](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-list/put_gateway_antivirus_exclusion_list_base)

#### [gateway-antivirus-exclusion-entry](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-exclusion-entry)      Gateway antivirus exclusion entry configuration API.

GET[/gateway-antivirus/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/get_gateway_antivirus_exclusion_list_entries)

POST[/gateway-antivirus/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/post_gateway_antivirus_exclusion_list_entries)

PUT[/gateway-antivirus/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/put_gateway_antivirus_exclusion_list_entries)

PATCH[/gateway-antivirus/exclusion-list/entries](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/patch_gateway_antivirus_exclusion_list_entries)

GET[/gateway-antivirus/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/get_gateway_antivirus_exclusion_list_entries_from__FROMIP__to__TOIP_)

PUT[/gateway-antivirus/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/put_gateway_antivirus_exclusion_list_entries_from__FROMIP__to__TOIP_)

PATCH[/gateway-antivirus/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/patch_gateway_antivirus_exclusion_list_entries_from__FROMIP__to__TOIP_)

DELETE[/gateway-antivirus/exclusion-list/entries/from/{FROMIP}/to/{TOIP}](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-exclusion-entry/delete_gateway_antivirus_exclusion_list_entries_from__FROMIP__to__TOIP_)

#### [gateway-antivirus-cloud](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-cloud)      Cloud Anti-Virus Database API.

GET[/gateway-antivirus/cloud/base](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-cloud/get_gateway_antivirus_cloud_base)

PUT[/gateway-antivirus/cloud/base](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-cloud/put_gateway_antivirus_cloud_base)

#### [gateway-antivirus-cloud-exclusion](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-cloud-exclusion)      Cloud Anti-Virus Database exclusions API.

GET[/gateway-antivirus/cloud/exclusions](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-cloud-exclusion/get_gateway_antivirus_cloud_exclusions)

POST[/gateway-antivirus/cloud/exclusions](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-cloud-exclusion/post_gateway_antivirus_cloud_exclusions)

#### [gateway-antivirus-signatures](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-signatures)      Gateway Anti-Virus signatures API.

GET[/gateway-antivirus/signatures](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-signatures/get_gateway_antivirus_signatures)

PUT[/gateway-antivirus/signatures](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-signatures/put_gateway_antivirus_signatures)

#### [gateway-antivirus-reset-settings](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-reset-settings)      Reset Gateway Anti-Virus Settings to default API.

POST[/gateway-antivirus/reset-settings](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-reset-settings/post_gateway_antivirus_reset_settings)

#### [gateway-antivirus-update-signatures](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-update-signatures)      Update signature database API.

POST[/gateway-antivirus/update-signatures](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-update-signatures/post_gateway_antivirus_update_signatures)

#### [gateway-antivirus-status](https://sonicos-api.sonicwall.com/\#/gateway-antivirus-status)      Gateway antivirus reporting API.

GET[/reporting/gateway-antivirus](https://sonicos-api.sonicwall.com/#/operations/gateway-antivirus-status/get_reporting_gateway_antivirus)

#### [capture-atp-base](https://sonicos-api.sonicwall.com/\#/capture-atp-base)      Capture ATP base settings API.

GET[/capture-atp/base](https://sonicos-api.sonicwall.com/#/operations/capture-atp-base/get_capture_atp_base)

PUT[/capture-atp/base](https://sonicos-api.sonicwall.com/#/operations/capture-atp-base/put_capture_atp_base)

#### [capture-atp-md5-exclusions](https://sonicos-api.sonicwall.com/\#/capture-atp-md5-exclusions)      Capture ATP MD5 exclusions list settings API.

GET[/capture-atp/md5-exclusions](https://sonicos-api.sonicwall.com/#/operations/capture-atp-md5-exclusions/get_capture_atp_md5_exclusions)

POST[/capture-atp/md5-exclusions](https://sonicos-api.sonicwall.com/#/operations/capture-atp-md5-exclusions/post_capture_atp_md5_exclusions)

#### [capture-atp-http-exclusions](https://sonicos-api.sonicwall.com/\#/capture-atp-http-exclusions)      Capture ATP HTTP host names exclusions list settings API.

GET[/capture-atp/http-exclusions](https://sonicos-api.sonicwall.com/#/operations/capture-atp-http-exclusions/get_capture_atp_http_exclusions)

POST[/capture-atp/http-exclusions](https://sonicos-api.sonicwall.com/#/operations/capture-atp-http-exclusions/post_capture_atp_http_exclusions)

#### [capture-atp-test-uftp-connectivity](https://sonicos-api.sonicwall.com/\#/capture-atp-test-uftp-connectivity)      Test UFTP Connectivity.

POST[/capture-atp/test/uftp-connectivity](https://sonicos-api.sonicwall.com/#/operations/capture-atp-test-uftp-connectivity/post_capture_atp_test_uftp_connectivity)

#### [capture-atp-clear-uftp-connectivity](https://sonicos-api.sonicwall.com/\#/capture-atp-clear-uftp-connectivity)      Test UFTP Connectivity.

POST[/capture-atp/clear/uftp-connectivity](https://sonicos-api.sonicwall.com/#/operations/capture-atp-clear-uftp-connectivity/post_capture_atp_clear_uftp_connectivity)

#### [capture-atp-refresh-uftp-connectivity](https://sonicos-api.sonicwall.com/\#/capture-atp-refresh-uftp-connectivity)      Refresh UFTP Connectivity.

POST[/capture-atp/refresh/uftp-connectivity](https://sonicos-api.sonicwall.com/#/operations/capture-atp-refresh-uftp-connectivity/post_capture_atp_refresh_uftp_connectivity)

#### [capture-atp-check-md5-query-status](https://sonicos-api.sonicwall.com/\#/capture-atp-check-md5-query-status)      Check MD5 query status.

POST[/capture-atp/check/md5-query-status/{MD5QUERYCONTENT}](https://sonicos-api.sonicwall.com/#/operations/capture-atp-check-md5-query-status/post_capture_atp_check_md5_query_status__MD5QUERYCONTENT_)

#### [capture-atp-clear-md5-query-status](https://sonicos-api.sonicwall.com/\#/capture-atp-clear-md5-query-status)      Cear MD5 query status.

POST[/capture-atp/clear/md5-query-status](https://sonicos-api.sonicwall.com/#/operations/capture-atp-clear-md5-query-status/post_capture_atp_clear_md5_query_status)

#### [capture-atp-refresh-md5-query-status](https://sonicos-api.sonicwall.com/\#/capture-atp-refresh-md5-query-status)      Refresh MD5 query status.

POST[/capture-atp/refresh/md5-query-status](https://sonicos-api.sonicwall.com/#/operations/capture-atp-refresh-md5-query-status/post_capture_atp_refresh_md5_query_status)

#### [anti-spam](https://sonicos-api.sonicwall.com/\#/anti-spam)      Anti spam configuration API.

GET[/anti-spam/base](https://sonicos-api.sonicwall.com/#/operations/anti-spam/get_anti_spam_base)

PUT[/anti-spam/base](https://sonicos-api.sonicwall.com/#/operations/anti-spam/put_anti_spam_base)

#### [anti-spam-allow-list](https://sonicos-api.sonicwall.com/\#/anti-spam-allow-list)      Anti spam allow client list configuration API.

GET[/anti-spam/allow-list](https://sonicos-api.sonicwall.com/#/operations/anti-spam-allow-list/get_anti_spam_allow_list)

POST[/anti-spam/allow-list](https://sonicos-api.sonicwall.com/#/operations/anti-spam-allow-list/post_anti_spam_allow_list)

#### [anti-spam-reject-list](https://sonicos-api.sonicwall.com/\#/anti-spam-reject-list)      Anti spam reject client list configuration API.

GET[/anti-spam/reject-list](https://sonicos-api.sonicwall.com/#/operations/anti-spam-reject-list/get_anti_spam_reject_list)

POST[/anti-spam/reject-list](https://sonicos-api.sonicwall.com/#/operations/anti-spam-reject-list/post_anti_spam_reject_list)

#### [anti-spam-start-capture](https://sonicos-api.sonicwall.com/\#/anti-spam-start-capture)      Start e-mail stream packet capture API.

POST[/anti-spam/capture/start](https://sonicos-api.sonicwall.com/#/operations/anti-spam-start-capture/post_anti_spam_capture_start)

#### [anti-spam-stop-capture](https://sonicos-api.sonicwall.com/\#/anti-spam-stop-capture)      Stop e-mail stream packet capture API.

POST[/anti-spam/capture/stop](https://sonicos-api.sonicwall.com/#/operations/anti-spam-stop-capture/post_anti_spam_capture_stop)

#### [anti-spam-export-capture-ftp](https://sonicos-api.sonicwall.com/\#/anti-spam-export-capture-ftp)      Download e-mail stream capture data using FTP protocol API.

POST[/anti-spam/capture/export/ftp/{URL}](https://sonicos-api.sonicwall.com/#/operations/anti-spam-export-capture-ftp/post_anti_spam_capture_export_ftp__URL_)

#### [anti-spam-export-capture-scp](https://sonicos-api.sonicwall.com/\#/anti-spam-export-capture-scp)      Download e-mail stream capture data using SCP protocol API.

POST[/anti-spam/capture/export/scp/{URL}](https://sonicos-api.sonicwall.com/#/operations/anti-spam-export-capture-scp/post_anti_spam_capture_export_scp__URL_)

#### [anti-spam-grid-ip-check](https://sonicos-api.sonicwall.com/\#/anti-spam-grid-ip-check)      Do the IP reputation check with the SonicWall GRID network with the given ip address API.

POST[/anti-spam/grid-ip-check/{IP}](https://sonicos-api.sonicwall.com/#/operations/anti-spam-grid-ip-check/post_anti_spam_grid_ip_check__IP_)

#### [anti-spam-mxlookup](https://sonicos-api.sonicwall.com/\#/anti-spam-mxlookup)      MX lookup and banner check the specified domain name and SMTP port API.

POST[/anti-spam/mxlookup/{IP}](https://sonicos-api.sonicwall.com/#/operations/anti-spam-mxlookup/post_anti_spam_mxlookup__IP_)

POST[/anti-spam/mxlookup/{IP}/port/{SMTPPORT}](https://sonicos-api.sonicwall.com/#/operations/anti-spam-mxlookup/post_anti_spam_mxlookup__IP__port__SMTPPORT_)

#### [anti-spam-destination-mail-server](https://sonicos-api.sonicwall.com/\#/anti-spam-destination-mail-server)      Set the destination mail server configuration API.

POST[/anti-spam/destination-mail-server/public/{PUB\_IP}/private/{PRI\_IP}/zone/{NAME}/port/{PORT}](https://sonicos-api.sonicwall.com/#/operations/anti-spam-destination-mail-server/post_anti_spam_destination_mail_server_public__PUB_IP__private__PRI_IP__zone__NAME__port__PORT_)

#### [anti-spam-statistics-capture](https://sonicos-api.sonicwall.com/\#/anti-spam-statistics-capture)      Packet capture API.

GET[/reporting/anti-spam/statistics/capture](https://sonicos-api.sonicwall.com/#/operations/anti-spam-statistics-capture/get_reporting_anti_spam_statistics_capture)

DELETE[/reporting/anti-spam/statistics/capture](https://sonicos-api.sonicwall.com/#/operations/anti-spam-statistics-capture/delete_reporting_anti_spam_statistics_capture)

#### [anti-spam-statistics-probe](https://sonicos-api.sonicwall.com/\#/anti-spam-statistics-probe)      Anti spam probe statistics reporting API.

GET[/reporting/anti-spam/statistics/probe](https://sonicos-api.sonicwall.com/#/operations/anti-spam-statistics-probe/get_reporting_anti_spam_statistics_probe)

#### [anti-spam-statistics-general](https://sonicos-api.sonicwall.com/\#/anti-spam-statistics-general)      Anti spam general statistics reporting API.

GET[/reporting/anti-spam/statistics/general](https://sonicos-api.sonicwall.com/#/operations/anti-spam-statistics-general/get_reporting_anti_spam_statistics_general)

#### [anti-spam-statistics-threats](https://sonicos-api.sonicwall.com/\#/anti-spam-statistics-threats)      Anti spam threats statistics reporting API.

GET[/reporting/anti-spam/statistics/threats](https://sonicos-api.sonicwall.com/#/operations/anti-spam-statistics-threats/get_reporting_anti_spam_statistics_threats)

#### [anti-spam-status-service](https://sonicos-api.sonicwall.com/\#/anti-spam-status-service)      Anti spam service status reporting API.

GET[/reporting/anti-spam/status/service](https://sonicos-api.sonicwall.com/#/operations/anti-spam-status-service/get_reporting_anti_spam_status_service)

#### [anti-spam-status-monitoring](https://sonicos-api.sonicwall.com/\#/anti-spam-status-monitoring)      Anti spam monitoring status reporting API.

GET[/reporting/anti-spam/status/monitoring](https://sonicos-api.sonicwall.com/#/operations/anti-spam-status-monitoring/get_reporting_anti_spam_status_monitoring)

#### [rbl-base](https://sonicos-api.sonicwall.com/\#/rbl-base)      Real-time blacklist base configuration API.

GET[/rbl/base](https://sonicos-api.sonicwall.com/#/operations/rbl-base/get_rbl_base)

PUT[/rbl/base](https://sonicos-api.sonicwall.com/#/operations/rbl-base/put_rbl_base)

#### [rbl-services](https://sonicos-api.sonicwall.com/\#/rbl-services)      Real-Time blacklist services configuration API.

GET[/rbl/services](https://sonicos-api.sonicwall.com/#/operations/rbl-services/get_rbl_services)

POST[/rbl/services](https://sonicos-api.sonicwall.com/#/operations/rbl-services/post_rbl_services)

PUT[/rbl/services](https://sonicos-api.sonicwall.com/#/operations/rbl-services/put_rbl_services)

PATCH[/rbl/services](https://sonicos-api.sonicwall.com/#/operations/rbl-services/patch_rbl_services)

GET[/rbl/services/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/rbl-services/get_rbl_services_domain__NAME_)

PUT[/rbl/services/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/rbl-services/put_rbl_services_domain__NAME_)

PATCH[/rbl/services/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/rbl-services/patch_rbl_services_domain__NAME_)

DELETE[/rbl/services/domain/{NAME}](https://sonicos-api.sonicwall.com/#/operations/rbl-services/delete_rbl_services_domain__NAME_)

#### [rbl](https://sonicos-api.sonicwall.com/\#/rbl)      RBL service reporting API.

GET[/reporting/rbl](https://sonicos-api.sonicwall.com/#/operations/rbl/get_reporting_rbl)

GET[/reporting/rbl/services/{RBLSERVICEDOMAINNAME}](https://sonicos-api.sonicwall.com/#/operations/rbl/get_reporting_rbl_services__RBLSERVICEDOMAINNAME_)

DELETE[/reporting/rbl/services/{RBLSERVICEDOMAINNAME}](https://sonicos-api.sonicwall.com/#/operations/rbl/delete_reporting_rbl_services__RBLSERVICEDOMAINNAME_)

#### [dpi-ssh](https://sonicos-api.sonicwall.com/\#/dpi-ssh)      DPI-SSH configuration API.

GET[/dpi-ssh](https://sonicos-api.sonicwall.com/#/operations/dpi-ssh/get_dpi_ssh)

PUT[/dpi-ssh](https://sonicos-api.sonicwall.com/#/operations/dpi-ssh/put_dpi_ssh)

#### [dpi-ssl-server](https://sonicos-api.sonicwall.com/\#/dpi-ssl-server)      DPI-SSL server base settings API.

GET[/dpi-ssl/server/base](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-server/get_dpi_ssl_server_base)

PUT[/dpi-ssl/server/base](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-server/put_dpi_ssl_server_base)

#### [dpi-ssl-server-ssl-servers](https://sonicos-api.sonicwall.com/\#/dpi-ssl-server-ssl-servers)      DPI-SSL server SSL servers settings API.

GET[/dpi-ssl/server/ssl-servers](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-server-ssl-servers/get_dpi_ssl_server_ssl_servers)

POST[/dpi-ssl/server/ssl-servers](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-server-ssl-servers/post_dpi_ssl_server_ssl_servers)

GET[/dpi-ssl/server/ssl-servers/name/{SSLSERVER}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-server-ssl-servers/get_dpi_ssl_server_ssl_servers_name__SSLSERVER_)

DELETE[/dpi-ssl/server/ssl-servers/name/{SSLSERVER}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-server-ssl-servers/delete_dpi_ssl_server_ssl_servers_name__SSLSERVER_)

#### [dpi-ssl-client](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client)      DPI-SSL client base settings API.

GET[/dpi-ssl/client/base](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client/get_dpi_ssl_client_base)

PUT[/dpi-ssl/client/base](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client/put_dpi_ssl_client_base)

#### [dpi-ssl-client-cfs-categories](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-cfs-categories)      DPI-SSL client content filter categories setting API.

GET[/dpi-ssl/client/cfs-categories](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-cfs-categories/get_dpi_ssl_client_cfs_categories)

POST[/dpi-ssl/client/cfs-categories](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-cfs-categories/post_dpi_ssl_client_cfs_categories)

#### [dpi-ssl-client-common-names-statistics](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-common-names-statistics)      Show DPI-SSL client common names API.

GET[/reporting/dpi-ssl/client/statistics](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-common-names-statistics/get_reporting_dpi_ssl_client_statistics)

GET[/reporting/dpi-ssl/client/statistics/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-common-names-statistics/get_reporting_dpi_ssl_client_statistics_common_name__CNAME_)

#### [dpi-ssl-client-common-names](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-common-names)      DPI-SSL client common names setting API.

GET[/dpi-ssl/client/common-names](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-common-names/get_dpi_ssl_client_common_names)

POST[/dpi-ssl/client/common-names](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-common-names/post_dpi_ssl_client_common_names)

GET[/dpi-ssl/client/common-names/name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-common-names/get_dpi_ssl_client_common_names_name__CNAME_)

DELETE[/dpi-ssl/client/common-names/name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-common-names/delete_dpi_ssl_client_common_names_name__CNAME_)

#### [dpi-ssl-client-reject](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-reject)      Reject DPI-SSL client build-in common name.

POST[/dpi-ssl/client/reject/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-reject/post_dpi_ssl_client_reject__CNAME_)

#### [dpi-ssl-client-accept](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-accept)      Accept DPI-SSL client build-in common name.

POST[/dpi-ssl/client/accept/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-accept/post_dpi_ssl_client_accept__CNAME_)

#### [dpi-ssl-client-export-cert](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-export-cert)      Export DPI-SSL client certificate to file API.

GET[/export/dpi-ssl-client/certificate/default](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-export-cert/get_export_dpi_ssl_client_certificate_default)

GET[/export/dpi-ssl-client/certificate/default-2048-bit](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-export-cert/get_export_dpi_ssl_client_certificate_default_2048_bit)

#### [dpi-ssl-client-default-exclusions-status](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-default-exclusions-status)      DPI-SSL client default exclusion status reporting API.

GET[/reporting/dpi-ssl/client/default-exclusions-status](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-default-exclusions-status/get_reporting_dpi_ssl_client_default_exclusions_status)

#### [dpi-ssl-client-import-excl](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-import-excl)      Update default exclusions manually.

POST[/import/dpi-ssl-client/exclusions](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-import-excl/post_import_dpi_ssl_client_exclusions)

#### [dpi-ssl-client-connection-failures](https://sonicos-api.sonicwall.com/\#/dpi-ssl-client-connection-failures)      DPI-SSL client connection failures reporting API.

GET[/reporting/dpi-ssl/client/connection-failures](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-connection-failures/get_reporting_dpi_ssl_client_connection_failures)

GET[/reporting/dpi-ssl/client/connection-failures/name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-connection-failures/get_reporting_dpi_ssl_client_connection_failures_name__CNAME_)

DELETE[/reporting/dpi-ssl/client/connection-failures/name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/dpi-ssl-client-connection-failures/delete_reporting_dpi_ssl_client_connection_failures_name__CNAME_)

#### [cipher-control-tls-cipher](https://sonicos-api.sonicwall.com/\#/cipher-control-tls-cipher)      Cipher control TLS block/unblock cipher API.

POST[/cipher-control/tls/cipher/{CIPHERNAME}](https://sonicos-api.sonicwall.com/#/operations/cipher-control-tls-cipher/post_cipher_control_tls_cipher__CIPHERNAME_)

DELETE[/cipher-control/tls/cipher/{CIPHERNAME}](https://sonicos-api.sonicwall.com/#/operations/cipher-control-tls-cipher/delete_cipher_control_tls_cipher__CIPHERNAME_)

#### [cipher-control-tls](https://sonicos-api.sonicwall.com/\#/cipher-control-tls)      Cipher control ssh ciphers API.

GET[/cipher-control/tls-ciphers](https://sonicos-api.sonicwall.com/#/operations/cipher-control-tls/get_cipher_control_tls_ciphers)

#### [cipher-control-tls-cipher-list](https://sonicos-api.sonicwall.com/\#/cipher-control-tls-cipher-list)      Cipher control TLS cipher lists API.

GET[/reporting/cipher-control/tls-cipher-list](https://sonicos-api.sonicwall.com/#/operations/cipher-control-tls-cipher-list/get_reporting_cipher_control_tls_cipher_list)

#### [cipher-control-ssh](https://sonicos-api.sonicwall.com/\#/cipher-control-ssh)      Cipher control ssh ciphers API.

GET[/cipher-control/ssh](https://sonicos-api.sonicwall.com/#/operations/cipher-control-ssh/get_cipher_control_ssh)

PUT[/cipher-control/ssh](https://sonicos-api.sonicwall.com/#/operations/cipher-control-ssh/put_cipher_control_ssh)

#### [appflow](https://sonicos-api.sonicwall.com/\#/appflow)      Appflow configuration API.

GET[/appflow/base](https://sonicos-api.sonicwall.com/#/operations/appflow/get_appflow_base)

PUT[/appflow/base](https://sonicos-api.sonicwall.com/#/operations/appflow/put_appflow_base)

#### [appflow-gmsflow-server](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server)      Appflow GMS flow server configuration API.

GET[/appflow/gmsflow-server/base](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server/get_appflow_gmsflow_server_base)

PUT[/appflow/gmsflow-server/base](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server/put_appflow_gmsflow_server_base)

#### [appflow-server](https://sonicos-api.sonicwall.com/\#/appflow-server)      Appflow server configuration API.

GET[/appflow/appflow-server/base](https://sonicos-api.sonicwall.com/#/operations/appflow-server/get_appflow_appflow_server_base)

PUT[/appflow/appflow-server/base](https://sonicos-api.sonicwall.com/#/operations/appflow-server/put_appflow_appflow_server_base)

#### [appflow-sfr-mailing](https://sonicos-api.sonicwall.com/\#/appflow-sfr-mailing)      Appflow sfr mailing configuration API.

GET[/appflow/sfr-mailing/base](https://sonicos-api.sonicwall.com/#/operations/appflow-sfr-mailing/get_appflow_sfr_mailing_base)

PUT[/appflow/sfr-mailing/base](https://sonicos-api.sonicwall.com/#/operations/appflow-sfr-mailing/put_appflow_sfr_mailing_base)

#### [appflow-external-collector](https://sonicos-api.sonicwall.com/\#/appflow-external-collector)      Appflow external collector configuration API.

GET[/appflow/external-collector/base](https://sonicos-api.sonicwall.com/#/operations/appflow-external-collector/get_appflow_external_collector_base)

PUT[/appflow/external-collector/base](https://sonicos-api.sonicwall.com/#/operations/appflow-external-collector/put_appflow_external_collector_base)

#### [appflow-default](https://sonicos-api.sonicwall.com/\#/appflow-default)      Appflow Clear all settings to default configuration API.

POST[/appflow/default](https://sonicos-api.sonicwall.com/#/operations/appflow-default/post_appflow_default)

#### [appflow-gmsflow-server-synchronize](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server-synchronize)      Appflow Synchronize GMS flow server API.

POST[/appflow/gmsflow-server/server-ip/synchronize](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server-synchronize/post_appflow_gmsflow_server_server_ip_synchronize)

#### [appflow-gmsflow-server-synchronize-log-settings](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server-synchronize-log-settings)      Send All Log Settings GMSFlow Server API.

POST[/appflow/gmsflow-server/server-ip/synchronize-logs](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server-synchronize-log-settings/post_appflow_gmsflow_server_server_ip_synchronize_logs)

#### [appflow-gmsflow-server-test-connectivity](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server-test-connectivity)      Appflow Test connectivity of GMS flow server API.

POST[/appflow/gmsflow-server/server-ip/test-connectivity](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server-test-connectivity/post_appflow_gmsflow_server_server_ip_test_connectivity)

#### [appflow-gmsflow-server-2-synchronize](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server-2-synchronize)      Appflow Synchronize GMS flow server 2 API.

POST[/appflow/gmsflow-server/server-2-ip/synchronize](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server-2-synchronize/post_appflow_gmsflow_server_server_2_ip_synchronize)

#### [appflow-gmsflow-server-2-synchronize-log-settings](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server-2-synchronize-log-settings)      Send All Log Settings GMSFlow Server API.

POST[/appflow/gmsflow-server/server-2-ip/synchronize-logs](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server-2-synchronize-log-settings/post_appflow_gmsflow_server_server_2_ip_synchronize_logs)

#### [appflow-gmsflow-server-2-test-connectivity](https://sonicos-api.sonicwall.com/\#/appflow-gmsflow-server-2-test-connectivity)      Appflow Test connectivity of GMS flow server API.

POST[/appflow/gmsflow-server/server-2-ip/test-connectivity](https://sonicos-api.sonicwall.com/#/operations/appflow-gmsflow-server-2-test-connectivity/post_appflow_gmsflow_server_server_2_ip_test_connectivity)

#### [appflow-server-synchronize](https://sonicos-api.sonicwall.com/\#/appflow-server-synchronize)      Synchronize appflow server API.

POST[/appflow/appflow-server/server-ip/synchronize](https://sonicos-api.sonicwall.com/#/operations/appflow-server-synchronize/post_appflow_appflow_server_server_ip_synchronize)

#### [appflow-server-2-synchronize](https://sonicos-api.sonicwall.com/\#/appflow-server-2-synchronize)      Synchronize appflow server 2 API.

POST[/appflow/appflow-server/server-2-ip/synchronize](https://sonicos-api.sonicwall.com/#/operations/appflow-server-2-synchronize/post_appflow_appflow_server_server_2_ip_synchronize)

#### [appflow-server-synchronize-logs](https://sonicos-api.sonicwall.com/\#/appflow-server-synchronize-logs)      Synchronize appflow server log settings API.

POST[/appflow/appflow-server/server-ip/synchronize-logs](https://sonicos-api.sonicwall.com/#/operations/appflow-server-synchronize-logs/post_appflow_appflow_server_server_ip_synchronize_logs)

#### [appflow-server-2-synchronize-logs](https://sonicos-api.sonicwall.com/\#/appflow-server-2-synchronize-logs)      Synchronize appflow server 2 log settings API.

POST[/appflow/appflow-server/server-2-ip/synchronize-logs](https://sonicos-api.sonicwall.com/#/operations/appflow-server-2-synchronize-logs/post_appflow_appflow_server_server_2_ip_synchronize_logs)

#### [appflow-server-test-connectivity](https://sonicos-api.sonicwall.com/\#/appflow-server-test-connectivity)      Test connectivity of appflow server API.

POST[/appflow/appflow-server/server-ip/test-connectivity](https://sonicos-api.sonicwall.com/#/operations/appflow-server-test-connectivity/post_appflow_appflow_server_server_ip_test_connectivity)

#### [appflow-server-2-test-connectivity](https://sonicos-api.sonicwall.com/\#/appflow-server-2-test-connectivity)      Test connectivity of appflow server 2 API.

POST[/appflow/appflow-server/server-2-ip/test-connectivity](https://sonicos-api.sonicwall.com/#/operations/appflow-server-2-test-connectivity/post_appflow_appflow_server_server_2_ip_test_connectivity)

#### [appflow-server-flush-servers](https://sonicos-api.sonicwall.com/\#/appflow-server-flush-servers)      Flush a specified or all discovered appflow servers API.

POST[/appflow/appflow-server/flush/servers](https://sonicos-api.sonicwall.com/#/operations/appflow-server-flush-servers/post_appflow_appflow_server_flush_servers)

POST[/appflow/appflow-server/flush/servers/ip/{IP}](https://sonicos-api.sonicwall.com/#/operations/appflow-server-flush-servers/post_appflow_appflow_server_flush_servers_ip__IP_)

#### [appflow-server-discover](https://sonicos-api.sonicwall.com/\#/appflow-server-discover)      Discover appflow servers API.

POST[/appflow/appflow-server/discover/interface/{IFID}](https://sonicos-api.sonicwall.com/#/operations/appflow-server-discover/post_appflow_appflow_server_discover_interface__IFID_)

#### [appflow-sfr-mailing-test-email](https://sonicos-api.sonicwall.com/\#/appflow-sfr-mailing-test-email)      Appflow SFR mailing configuration testing.

POST[/appflow/sfr-mailing/test-email](https://sonicos-api.sonicwall.com/#/operations/appflow-sfr-mailing-test-email/post_appflow_sfr_mailing_test_email)

#### [appflow-external-collector-generate-all-templates](https://sonicos-api.sonicwall.com/\#/appflow-external-collector-generate-all-templates)      Appflow generate all templates API.

POST[/appflow/external-collector/generate/all-templates](https://sonicos-api.sonicwall.com/#/operations/appflow-external-collector-generate-all-templates/post_appflow_external_collector_generate_all_templates)

#### [appflow-external-collector-generate-static-appflow-data](https://sonicos-api.sonicwall.com/\#/appflow-external-collector-generate-static-appflow-data)      Generate static appflow data API.

POST[/appflow/external-collector/generate/static-appflow-data](https://sonicos-api.sonicwall.com/#/operations/appflow-external-collector-generate-static-appflow-data/post_appflow_external_collector_generate_static_appflow_data)

#### [appflow-external-collector-send-all-entries](https://sonicos-api.sonicwall.com/\#/appflow-external-collector-send-all-entries)      Send the necessary fields of log settings to external collector for log display API.

POST[/appflow/external-collector/send-all-entries](https://sonicos-api.sonicwall.com/#/operations/appflow-external-collector-send-all-entries/post_appflow_external_collector_send_all_entries)

#### [appflow-flow-reporting](https://sonicos-api.sonicwall.com/\#/appflow-flow-reporting)      Appflow flow reporting statistics API.

DELETE[/appflow/flow-reporting](https://sonicos-api.sonicwall.com/#/operations/appflow-flow-reporting/delete_appflow_flow_reporting)

#### [appflow-status-appflow](https://sonicos-api.sonicwall.com/\#/appflow-status-appflow)      Appflow server status reporting API.

GET[/reporting/appflow/status/appflow-server](https://sonicos-api.sonicwall.com/#/operations/appflow-status-appflow/get_reporting_appflow_status_appflow_server)

#### [appflow-status-gmsflow](https://sonicos-api.sonicwall.com/\#/appflow-status-gmsflow)      Appflow gmsflow server status reporting API.

GET[/reporting/appflow/status/gmsflow-server](https://sonicos-api.sonicwall.com/#/operations/appflow-status-gmsflow/get_reporting_appflow_status_gmsflow_server)

#### [appflow-statistics-external](https://sonicos-api.sonicwall.com/\#/appflow-statistics-external)      Appflow external reporting API.

GET[/reporting/appflow/statistics/external](https://sonicos-api.sonicwall.com/#/operations/appflow-statistics-external/get_reporting_appflow_statistics_external)

#### [appflow-statistics-internal](https://sonicos-api.sonicwall.com/\#/appflow-statistics-internal)      Appflow internal reporting API.

GET[/reporting/appflow/statistics/internal](https://sonicos-api.sonicwall.com/#/operations/appflow-statistics-internal/get_reporting_appflow_statistics_internal)

#### [appflow-statistics-ipfix](https://sonicos-api.sonicwall.com/\#/appflow-statistics-ipfix)      Appflow ipfix reporting API.

GET[/reporting/appflow/statistics/ipfix](https://sonicos-api.sonicwall.com/#/operations/appflow-statistics-ipfix/get_reporting_appflow_statistics_ipfix)

#### [appflow-send-report](https://sonicos-api.sonicwall.com/\#/appflow-send-report)      Send Data for backend Appflow report generation using the SonicOS WebUI (.sfr) format.

GET[/appflow/send-report/{QUERY}](https://sonicos-api.sonicwall.com/#/operations/appflow-send-report/get_appflow_send_report__QUERY_)

#### [cta-report](https://sonicos-api.sonicwall.com/\#/cta-report)      Export CTA report.

POST[/cta-report](https://sonicos-api.sonicwall.com/#/operations/cta-report/post_cta_report)

#### [delete-cta-report](https://sonicos-api.sonicwall.com/\#/delete-cta-report)      Delete generated CTA report.

DELETE[/cta-report/{TS}](https://sonicos-api.sonicwall.com/#/operations/delete-cta-report/delete_cta_report__TS_)

#### [reset-appflow-report](https://sonicos-api.sonicwall.com/\#/reset-appflow-report)      Reset appflow report.

POST[/appflow-report/reset](https://sonicos-api.sonicwall.com/#/operations/reset-appflow-report/post_appflow_report_reset)

#### [vpn](https://sonicos-api.sonicwall.com/\#/vpn)      VPN base settings API.

GET[/vpn/base](https://sonicos-api.sonicwall.com/#/operations/vpn/get_vpn_base)

PUT[/vpn/base](https://sonicos-api.sonicwall.com/#/operations/vpn/put_vpn_base)

#### [vpn-renegotiate-tunnel](https://sonicos-api.sonicwall.com/\#/vpn-renegotiate-tunnel)      Renegotiate the specific VPN tunnel.

POST[/renegotiate/tunnel/{SRCIPTYPE}/{SRCNET}/{SRCMASK}/{DSTIPTYPE}/{DSTNET}/{DSTMASK}/{INITCOOKIE}/{DSTGW}/{DSTGWPORT}/{ISDHCPCL}/{INSPI}](https://sonicos-api.sonicwall.com/#/operations/vpn-renegotiate-tunnel/post_renegotiate_tunnel__SRCIPTYPE___SRCNET___SRCMASK___DSTIPTYPE___DSTNET___DSTMASK___INITCOOKIE___DSTGW___DSTGWPORT___ISDHCPCL___INSPI_)

#### [vpn-policies-all](https://sonicos-api.sonicwall.com/\#/vpn-policies-all)      VPN all policies API.

GET[/vpn/policies/all](https://sonicos-api.sonicwall.com/#/operations/vpn-policies-all/get_vpn_policies_all)

DELETE[/vpn/policies/all](https://sonicos-api.sonicwall.com/#/operations/vpn-policies-all/delete_vpn_policies_all)

#### [vpn-policies-all-ipv4](https://sonicos-api.sonicwall.com/\#/vpn-policies-all-ipv4)      Delete all IPv4 VPN policies API.

DELETE[/vpn/policies/ipv4/all](https://sonicos-api.sonicwall.com/#/operations/vpn-policies-all-ipv4/delete_vpn_policies_ipv4_all)

#### [vpn-policies-all-ipv6](https://sonicos-api.sonicwall.com/\#/vpn-policies-all-ipv6)      Delete all IPv6 VPN policies API.

DELETE[/vpn/policies/ipv6/all](https://sonicos-api.sonicwall.com/#/operations/vpn-policies-all-ipv6/delete_vpn_policies_ipv6_all)

#### [vpn-policy-ipv4-group-vpn](https://sonicos-api.sonicwall.com/\#/vpn-policy-ipv4-group-vpn)      IPv4 group VPN policy configuration API.

GET[/vpn/policies/ipv4/group-vpn](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-group-vpn/get_vpn_policies_ipv4_group_vpn)

PUT[/vpn/policies/ipv4/group-vpn](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-group-vpn/put_vpn_policies_ipv4_group_vpn)

GET[/vpn/policies/ipv4/group-vpn/name/{GROUP\_VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-group-vpn/get_vpn_policies_ipv4_group_vpn_name__GROUP_VPN_NAME_)

PUT[/vpn/policies/ipv4/group-vpn/name/{GROUP\_VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-group-vpn/put_vpn_policies_ipv4_group_vpn_name__GROUP_VPN_NAME_)

#### [vpn-policy-ipv4-site-to-site](https://sonicos-api.sonicwall.com/\#/vpn-policy-ipv4-site-to-site)      IPv4 site-to-site VPN policy configuration API.

GET[/vpn/policies/ipv4/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/get_vpn_policies_ipv4_site_to_site)

POST[/vpn/policies/ipv4/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/post_vpn_policies_ipv4_site_to_site)

PUT[/vpn/policies/ipv4/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/put_vpn_policies_ipv4_site_to_site)

PATCH[/vpn/policies/ipv4/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/patch_vpn_policies_ipv4_site_to_site)

GET[/vpn/policies/ipv4/site-to-site/name/{SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/get_vpn_policies_ipv4_site_to_site_name__SITE_TO_SITE_NAME_)

PUT[/vpn/policies/ipv4/site-to-site/name/{SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/put_vpn_policies_ipv4_site_to_site_name__SITE_TO_SITE_NAME_)

PATCH[/vpn/policies/ipv4/site-to-site/name/{SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/patch_vpn_policies_ipv4_site_to_site_name__SITE_TO_SITE_NAME_)

DELETE[/vpn/policies/ipv4/site-to-site/name/{SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-site-to-site/delete_vpn_policies_ipv4_site_to_site_name__SITE_TO_SITE_NAME_)

#### [vpn-policy-ipv4-tunnel-interface](https://sonicos-api.sonicwall.com/\#/vpn-policy-ipv4-tunnel-interface)      IPv4 tunnel interface VPN policy configuration API.

GET[/vpn/policies/ipv4/tunnel-interface](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/get_vpn_policies_ipv4_tunnel_interface)

POST[/vpn/policies/ipv4/tunnel-interface](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/post_vpn_policies_ipv4_tunnel_interface)

PUT[/vpn/policies/ipv4/tunnel-interface](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/put_vpn_policies_ipv4_tunnel_interface)

PATCH[/vpn/policies/ipv4/tunnel-interface](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/patch_vpn_policies_ipv4_tunnel_interface)

GET[/vpn/policies/ipv4/tunnel-interface/name/{TUNNEL\_VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/get_vpn_policies_ipv4_tunnel_interface_name__TUNNEL_VPN_NAME_)

PUT[/vpn/policies/ipv4/tunnel-interface/name/{TUNNEL\_VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/put_vpn_policies_ipv4_tunnel_interface_name__TUNNEL_VPN_NAME_)

PATCH[/vpn/policies/ipv4/tunnel-interface/name/{TUNNEL\_VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/patch_vpn_policies_ipv4_tunnel_interface_name__TUNNEL_VPN_NAME_)

DELETE[/vpn/policies/ipv4/tunnel-interface/name/{TUNNEL\_VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-tunnel-interface/delete_vpn_policies_ipv4_tunnel_interface_name__TUNNEL_VPN_NAME_)

#### [vpn-policy-ipv4-provision-client](https://sonicos-api.sonicwall.com/\#/vpn-policy-ipv4-provision-client)      SonicWALL auto provisioning client VPN policy configuration API.

GET[/vpn/policies/ipv4/provision-client](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/get_vpn_policies_ipv4_provision_client)

POST[/vpn/policies/ipv4/provision-client](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/post_vpn_policies_ipv4_provision_client)

PUT[/vpn/policies/ipv4/provision-client](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/put_vpn_policies_ipv4_provision_client)

PATCH[/vpn/policies/ipv4/provision-client](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/patch_vpn_policies_ipv4_provision_client)

GET[/vpn/policies/ipv4/provision-client/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/get_vpn_policies_ipv4_provision_client_name__VPN_NAME_)

PUT[/vpn/policies/ipv4/provision-client/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/put_vpn_policies_ipv4_provision_client_name__VPN_NAME_)

PATCH[/vpn/policies/ipv4/provision-client/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/patch_vpn_policies_ipv4_provision_client_name__VPN_NAME_)

DELETE[/vpn/policies/ipv4/provision-client/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-client/delete_vpn_policies_ipv4_provision_client_name__VPN_NAME_)

#### [vpn-policy-ipv4-provision-server](https://sonicos-api.sonicwall.com/\#/vpn-policy-ipv4-provision-server)      SonicWALL auto provisioning server VPN policy configuration API.

GET[/vpn/policies/ipv4/provision-server](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/get_vpn_policies_ipv4_provision_server)

POST[/vpn/policies/ipv4/provision-server](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/post_vpn_policies_ipv4_provision_server)

PUT[/vpn/policies/ipv4/provision-server](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/put_vpn_policies_ipv4_provision_server)

PATCH[/vpn/policies/ipv4/provision-server](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/patch_vpn_policies_ipv4_provision_server)

GET[/vpn/policies/ipv4/provision-server/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/get_vpn_policies_ipv4_provision_server_name__VPN_NAME_)

PUT[/vpn/policies/ipv4/provision-server/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/put_vpn_policies_ipv4_provision_server_name__VPN_NAME_)

PATCH[/vpn/policies/ipv4/provision-server/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/patch_vpn_policies_ipv4_provision_server_name__VPN_NAME_)

DELETE[/vpn/policies/ipv4/provision-server/name/{VPN\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv4-provision-server/delete_vpn_policies_ipv4_provision_server_name__VPN_NAME_)

#### [vpn-policy-ipv6](https://sonicos-api.sonicwall.com/\#/vpn-policy-ipv6)      IPv6 site to site VPN policy configuration API.

GET[/vpn/policies/ipv6/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/get_vpn_policies_ipv6_site_to_site)

POST[/vpn/policies/ipv6/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/post_vpn_policies_ipv6_site_to_site)

PUT[/vpn/policies/ipv6/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/put_vpn_policies_ipv6_site_to_site)

PATCH[/vpn/policies/ipv6/site-to-site](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/patch_vpn_policies_ipv6_site_to_site)

GET[/vpn/policies/ipv6/site-to-site/name/{IPV6\_SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/get_vpn_policies_ipv6_site_to_site_name__IPV6_SITE_TO_SITE_NAME_)

PUT[/vpn/policies/ipv6/site-to-site/name/{IPV6\_SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/put_vpn_policies_ipv6_site_to_site_name__IPV6_SITE_TO_SITE_NAME_)

PATCH[/vpn/policies/ipv6/site-to-site/name/{IPV6\_SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/patch_vpn_policies_ipv6_site_to_site_name__IPV6_SITE_TO_SITE_NAME_)

DELETE[/vpn/policies/ipv6/site-to-site/name/{IPV6\_SITE\_TO\_SITE\_NAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-policy-ipv6/delete_vpn_policies_ipv6_site_to_site_name__IPV6_SITE_TO_SITE_NAME_)

#### [export-group-vpn-policy-spd](https://sonicos-api.sonicwall.com/\#/export-group-vpn-policy-spd)      Export the group VPN client policy in spd format.

GET[/export/vpn/spd/group-vpn/{GROUPVPNNAME}](https://sonicos-api.sonicwall.com/#/operations/export-group-vpn-policy-spd/get_export_vpn_spd_group_vpn__GROUPVPNNAME_)

#### [export-group-vpn-policy-rcf](https://sonicos-api.sonicwall.com/\#/export-group-vpn-policy-rcf)      Export the group VPN client policy in rcf format.

GET[/export/vpn/rcf/group-vpn/{GROUPVPNNAME}/network/{NETLOCAL}](https://sonicos-api.sonicwall.com/#/operations/export-group-vpn-policy-rcf/get_export_vpn_rcf_group_vpn__GROUPVPNNAME__network__NETLOCAL_)

GET[/export/vpn/rcf/group-vpn/{GROUPVPNNAME}/network/{NETLOCAL}/password/{EXPPWD}](https://sonicos-api.sonicwall.com/#/operations/export-group-vpn-policy-rcf/get_export_vpn_rcf_group_vpn__GROUPVPNNAME__network__NETLOCAL__password__EXPPWD_)

#### [vpn-dhcp-over-vpn-leases](https://sonicos-api.sonicwall.com/\#/vpn-dhcp-over-vpn-leases)      VPN DHCP over VPN leases reporting API.

GET[/reporting/vpn/dhcp-over-vpn/leases](https://sonicos-api.sonicwall.com/#/operations/vpn-dhcp-over-vpn-leases/get_reporting_vpn_dhcp_over_vpn_leases)

#### [vpn-dhcp-over-vpn-statistics](https://sonicos-api.sonicwall.com/\#/vpn-dhcp-over-vpn-statistics)      VPN DHCP over VPN lease counts reporting API.

GET[/reporting/vpn/dhcp-over-vpn/statistics](https://sonicos-api.sonicwall.com/#/operations/vpn-dhcp-over-vpn-statistics/get_reporting_vpn_dhcp_over_vpn_statistics)

#### [vpn-l2tp-server](https://sonicos-api.sonicwall.com/\#/vpn-l2tp-server)      VPN L2TP server base settings API.

GET[/vpn/l2tp-server/base](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server/get_vpn_l2tp_server_base)

PUT[/vpn/l2tp-server/base](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server/put_vpn_l2tp_server_base)

#### [vpn-l2tp-server-ppp](https://sonicos-api.sonicwall.com/\#/vpn-l2tp-server-ppp)      VPN L2TP server PPP settings API.

GET[/vpn/l2tp-server/ppp](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/get_vpn_l2tp_server_ppp)

PUT[/vpn/l2tp-server/ppp](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/put_vpn_l2tp_server_ppp)

PATCH[/vpn/l2tp-server/ppp](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/patch_vpn_l2tp_server_ppp)

GET[/vpn/l2tp-server/ppp/protocol/{PROTONAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/get_vpn_l2tp_server_ppp_protocol__PROTONAME_)

PUT[/vpn/l2tp-server/ppp/protocol/{PROTONAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/put_vpn_l2tp_server_ppp_protocol__PROTONAME_)

PATCH[/vpn/l2tp-server/ppp/protocol/{PROTONAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/patch_vpn_l2tp_server_ppp_protocol__PROTONAME_)

DELETE[/vpn/l2tp-server/ppp/protocol/{PROTONAME}](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-ppp/delete_vpn_l2tp_server_ppp_protocol__PROTONAME_)

#### [l2tp-server-disconnect-sessions](https://sonicos-api.sonicwall.com/\#/l2tp-server-disconnect-sessions)      Disconnect L2TP server active sessions.

DELETE[/vpn/l2tp-server/disconnect/{USERIP}](https://sonicos-api.sonicwall.com/#/operations/l2tp-server-disconnect-sessions/delete_vpn_l2tp_server_disconnect__USERIP_)

#### [vpn-l2tp-server-sessions](https://sonicos-api.sonicwall.com/\#/vpn-l2tp-server-sessions)      Retrieve L2TP server active sessions

GET[/reporting/l2tp-server/sessions](https://sonicos-api.sonicwall.com/#/operations/vpn-l2tp-server-sessions/get_reporting_l2tp_server_sessions)

#### [dhcp-over-vpn-global](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-global)      DHCP over VPN global base settings API.

GET[/vpn/dhcp-over-vpn/base/global](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-global/get_vpn_dhcp_over_vpn_base_global)

PUT[/vpn/dhcp-over-vpn/base/global](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-global/put_vpn_dhcp_over_vpn_base_global)

#### [dhcp-over-vpn-base-central](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-base-central)      DHCP over VPN cantral gateway base settings API.

GET[/vpn/dhcp-over-vpn/base/central](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-base-central/get_vpn_dhcp_over_vpn_base_central)

PUT[/vpn/dhcp-over-vpn/base/central](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-base-central/put_vpn_dhcp_over_vpn_base_central)

#### [dhcp-over-vpn-base-remote](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-base-remote)      DHCP over VPN remote gateway base settings API.

GET[/vpn/dhcp-over-vpn/base/remote](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-base-remote/get_vpn_dhcp_over_vpn_base_remote)

PUT[/vpn/dhcp-over-vpn/base/remote](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-base-remote/put_vpn_dhcp_over_vpn_base_remote)

#### [dhcp-over-vpn-static-devices](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-static-devices)      DHCP over VPN static devices setting API.

GET[/vpn/dhcp-over-vpn/static-devices](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-static-devices/get_vpn_dhcp_over_vpn_static_devices)

POST[/vpn/dhcp-over-vpn/static-devices](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-static-devices/post_vpn_dhcp_over_vpn_static_devices)

PUT[/vpn/dhcp-over-vpn/static-devices](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-static-devices/put_vpn_dhcp_over_vpn_static_devices)

GET[/vpn/dhcp-over-vpn/static-devices/ip/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-static-devices/get_vpn_dhcp_over_vpn_static_devices_ip__HOSTIP_)

PUT[/vpn/dhcp-over-vpn/static-devices/ip/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-static-devices/put_vpn_dhcp_over_vpn_static_devices_ip__HOSTIP_)

DELETE[/vpn/dhcp-over-vpn/static-devices/ip/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-static-devices/delete_vpn_dhcp_over_vpn_static_devices_ip__HOSTIP_)

#### [dhcp-over-vpn-excluded-devices](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-excluded-devices)      DHCP over VPN excluded devices setting API.

GET[/vpn/dhcp-over-vpn/excluded-devices](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-excluded-devices/get_vpn_dhcp_over_vpn_excluded_devices)

POST[/vpn/dhcp-over-vpn/excluded-devices](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-excluded-devices/post_vpn_dhcp_over_vpn_excluded_devices)

PUT[/vpn/dhcp-over-vpn/excluded-devices](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-excluded-devices/put_vpn_dhcp_over_vpn_excluded_devices)

GET[/vpn/dhcp-over-vpn/excluded-devices/mac/{MACADDR}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-excluded-devices/get_vpn_dhcp_over_vpn_excluded_devices_mac__MACADDR_)

PUT[/vpn/dhcp-over-vpn/excluded-devices/mac/{MACADDR}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-excluded-devices/put_vpn_dhcp_over_vpn_excluded_devices_mac__MACADDR_)

DELETE[/vpn/dhcp-over-vpn/excluded-devices/mac/{MACADDR}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-excluded-devices/delete_vpn_dhcp_over_vpn_excluded_devices_mac__MACADDR_)

#### [dhcp-over-vpn-servers](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-servers)      DHCP over VPN DHCP servers setting API.

GET[/vpn/dhcp-over-vpn/dhcp-servers](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-servers/get_vpn_dhcp_over_vpn_dhcp_servers)

POST[/vpn/dhcp-over-vpn/dhcp-servers](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-servers/post_vpn_dhcp_over_vpn_dhcp_servers)

PUT[/vpn/dhcp-over-vpn/dhcp-servers](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-servers/put_vpn_dhcp_over_vpn_dhcp_servers)

GET[/vpn/dhcp-over-vpn/dhcp-servers/ip/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-servers/get_vpn_dhcp_over_vpn_dhcp_servers_ip__HOSTIP_)

PUT[/vpn/dhcp-over-vpn/dhcp-servers/ip/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-servers/put_vpn_dhcp_over_vpn_dhcp_servers_ip__HOSTIP_)

DELETE[/vpn/dhcp-over-vpn/dhcp-servers/ip/{HOSTIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-servers/delete_vpn_dhcp_over_vpn_dhcp_servers_ip__HOSTIP_)

#### [dhcp-over-vpn-leases](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-leases)      DHCP over VPN leases

GET[/reporting/dhcp-over-vpn/leases](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-leases/get_reporting_dhcp_over_vpn_leases)

GET[/reporting/dhcp-over-vpn/leases/ip/{LEASEIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-leases/get_reporting_dhcp_over_vpn_leases_ip__LEASEIP_)

DELETE[/reporting/dhcp-over-vpn/leases/ip/{LEASEIP}](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-leases/delete_reporting_dhcp_over_vpn_leases_ip__LEASEIP_)

#### [dhcp-over-vpn-delete-all-dhcp-servers](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-delete-all-dhcp-servers)      DHCP over VPN delete all DHCP servers.

DELETE[/vpn/dhcp-over-vpn/dhcp-servers-all](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-delete-all-dhcp-servers/delete_vpn_dhcp_over_vpn_dhcp_servers_all)

#### [dhcp-over-vpn-delete-all-static-devices](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-delete-all-static-devices)      DHCP over VPN delete all static devices.

DELETE[/vpn/dhcp-over-vpn/static-devices-all](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-delete-all-static-devices/delete_vpn_dhcp_over_vpn_static_devices_all)

#### [dhcp-over-vpn-delete-all-excluded-lan-devices](https://sonicos-api.sonicwall.com/\#/dhcp-over-vpn-delete-all-excluded-lan-devices)      DHCP over VPN delete all excluded lan devices.

DELETE[/vpn/dhcp-over-vpn/excluded-lan-devices-all](https://sonicos-api.sonicwall.com/#/operations/dhcp-over-vpn-delete-all-excluded-lan-devices/delete_vpn_dhcp_over_vpn_excluded_lan_devices_all)

#### [ssl-control-base](https://sonicos-api.sonicwall.com/\#/ssl-control-base)      SSL control base settings API.

GET[/ssl-control/base](https://sonicos-api.sonicwall.com/#/operations/ssl-control-base/get_ssl_control_base)

PUT[/ssl-control/base](https://sonicos-api.sonicwall.com/#/operations/ssl-control-base/put_ssl_control_base)

#### [ssl-control-whitelist-certificates](https://sonicos-api.sonicwall.com/\#/ssl-control-whitelist-certificates)      SSL control whitelist certificates configuration API.

GET[/ssl-control/whitelist-certificates](https://sonicos-api.sonicwall.com/#/operations/ssl-control-whitelist-certificates/get_ssl_control_whitelist_certificates)

POST[/ssl-control/whitelist-certificates](https://sonicos-api.sonicwall.com/#/operations/ssl-control-whitelist-certificates/post_ssl_control_whitelist_certificates)

PUT[/ssl-control/whitelist-certificates](https://sonicos-api.sonicwall.com/#/operations/ssl-control-whitelist-certificates/put_ssl_control_whitelist_certificates)

GET[/ssl-control/whitelist-certificates/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-control-whitelist-certificates/get_ssl_control_whitelist_certificates_common_name__CNAME_)

PUT[/ssl-control/whitelist-certificates/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-control-whitelist-certificates/put_ssl_control_whitelist_certificates_common_name__CNAME_)

DELETE[/ssl-control/whitelist-certificates/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-control-whitelist-certificates/delete_ssl_control_whitelist_certificates_common_name__CNAME_)

#### [ssl-control-blacklist-certificates](https://sonicos-api.sonicwall.com/\#/ssl-control-blacklist-certificates)      SSL control blacklist certificates configuration API.

GET[/ssl-control/blacklist-certificates](https://sonicos-api.sonicwall.com/#/operations/ssl-control-blacklist-certificates/get_ssl_control_blacklist_certificates)

POST[/ssl-control/blacklist-certificates](https://sonicos-api.sonicwall.com/#/operations/ssl-control-blacklist-certificates/post_ssl_control_blacklist_certificates)

PUT[/ssl-control/blacklist-certificates](https://sonicos-api.sonicwall.com/#/operations/ssl-control-blacklist-certificates/put_ssl_control_blacklist_certificates)

GET[/ssl-control/blacklist-certificates/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-control-blacklist-certificates/get_ssl_control_blacklist_certificates_common_name__CNAME_)

PUT[/ssl-control/blacklist-certificates/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-control-blacklist-certificates/put_ssl_control_blacklist_certificates_common_name__CNAME_)

DELETE[/ssl-control/blacklist-certificates/common-name/{CNAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-control-blacklist-certificates/delete_ssl_control_blacklist_certificates_common_name__CNAME_)

#### [ssl-vpn-server-logout](https://sonicos-api.sonicwall.com/\#/ssl-vpn-server-logout)      SSL VPN server logout action API.

POST[/ssl-vpn/server-logout/{IP}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-server-logout/post_ssl_vpn_server_logout__IP_)

#### [ssl-vpn-logout](https://sonicos-api.sonicwall.com/\#/ssl-vpn-logout)      SSL VPN logout action API.

POST[/ssl-vpn/logout/{IP}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-logout/post_ssl_vpn_logout__IP_)

#### [ssl-vpn-server](https://sonicos-api.sonicwall.com/\#/ssl-vpn-server)      SSL VPN server configuration API.

GET[/ssl-vpn/server/base](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-server/get_ssl_vpn_server_base)

PUT[/ssl-vpn/server/base](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-server/put_ssl_vpn_server_base)

#### [ssl-vpn-server-access](https://sonicos-api.sonicwall.com/\#/ssl-vpn-server-access)      SSL VPN server accesses configuration API.

GET[/ssl-vpn/server/accesses](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-server-access/get_ssl_vpn_server_accesses)

PUT[/ssl-vpn/server/accesses](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-server-access/put_ssl_vpn_server_accesses)

#### [ssl-vpn-portal](https://sonicos-api.sonicwall.com/\#/ssl-vpn-portal)      SSL VPN portal configuration API.

GET[/ssl-vpn/portal](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-portal/get_ssl_vpn_portal)

PUT[/ssl-vpn/portal](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-portal/put_ssl_vpn_portal)

#### [ssl-vpn-device-profile](https://sonicos-api.sonicwall.com/\#/ssl-vpn-device-profile)      SSL VPN device profile object configuration API.

GET[/ssl-vpn/device-profiles](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile/get_ssl_vpn_device_profiles)

PUT[/ssl-vpn/device-profiles](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile/put_ssl_vpn_device_profiles)

PATCH[/ssl-vpn/device-profiles](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile/patch_ssl_vpn_device_profiles)

GET[/ssl-vpn/device-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile/get_ssl_vpn_device_profiles_name__NAME_)

PUT[/ssl-vpn/device-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile/put_ssl_vpn_device_profiles_name__NAME_)

PATCH[/ssl-vpn/device-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile/patch_ssl_vpn_device_profiles_name__NAME_)

#### [ssl-vpn-device-profile-client-dns-inherit](https://sonicos-api.sonicwall.com/\#/ssl-vpn-device-profile-client-dns-inherit)      Set DNS server IP address for NetExtender client action API.

PUT[/ssl-vpn/device-profile-client-dns-inherit/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-device-profile-client-dns-inherit/put_ssl_vpn_device_profile_client_dns_inherit_name__NAME_)

#### [ssl-vpn-bookmark](https://sonicos-api.sonicwall.com/\#/ssl-vpn-bookmark)      SSL VPN bookmark object configuration API.

GET[/ssl-vpn/bookmarks](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/get_ssl_vpn_bookmarks)

POST[/ssl-vpn/bookmarks](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/post_ssl_vpn_bookmarks)

PUT[/ssl-vpn/bookmarks](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/put_ssl_vpn_bookmarks)

PATCH[/ssl-vpn/bookmarks](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/patch_ssl_vpn_bookmarks)

GET[/ssl-vpn/bookmarks/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/get_ssl_vpn_bookmarks_name__NAME_)

PUT[/ssl-vpn/bookmarks/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/put_ssl_vpn_bookmarks_name__NAME_)

PATCH[/ssl-vpn/bookmarks/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/patch_ssl_vpn_bookmarks_name__NAME_)

DELETE[/ssl-vpn/bookmarks/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmark/delete_ssl_vpn_bookmarks_name__NAME_)

#### [ssl-vpn-sessions](https://sonicos-api.sonicwall.com/\#/ssl-vpn-sessions)      SSL VPN sessions reporting API.

GET[/reporting/ssl-vpn/sessions](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-sessions/get_reporting_ssl_vpn_sessions)

#### [ssl-vpn-statistics](https://sonicos-api.sonicwall.com/\#/ssl-vpn-statistics)      SSL VPN reporting API.

GET[/reporting/ssl-vpn/statistics/{IP}](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-statistics/get_reporting_ssl_vpn_statistics__IP_)

#### [ssl-vpn-bookmarks-sessions](https://sonicos-api.sonicwall.com/\#/ssl-vpn-bookmarks-sessions)      SSL VPN bookmarks sessions reporting API.

GET[/reporting/ssl-vpn/bookmarks/sessions](https://sonicos-api.sonicwall.com/#/operations/ssl-vpn-bookmarks-sessions/get_reporting_ssl_vpn_bookmarks_sessions)

#### [virtual-assist](https://sonicos-api.sonicwall.com/\#/virtual-assist)      Virtual assist configuration API.

GET[/virtual-assist/base](https://sonicos-api.sonicwall.com/#/operations/virtual-assist/get_virtual_assist_base)

PUT[/virtual-assist/base](https://sonicos-api.sonicwall.com/#/operations/virtual-assist/put_virtual_assist_base)

#### [virtual-assist-deny-requests](https://sonicos-api.sonicwall.com/\#/virtual-assist-deny-requests)      Virtual assist deny requests configuration API.

GET[/virtual-assist/deny-requests](https://sonicos-api.sonicwall.com/#/operations/virtual-assist-deny-requests/get_virtual_assist_deny_requests)

POST[/virtual-assist/deny-requests](https://sonicos-api.sonicwall.com/#/operations/virtual-assist-deny-requests/post_virtual_assist_deny_requests)

#### [virtual-assist-logout](https://sonicos-api.sonicwall.com/\#/virtual-assist-logout)      Logout specified virtual assist customer.

POST[/virtual-assist/logout/{ID}](https://sonicos-api.sonicwall.com/#/operations/virtual-assist-logout/post_virtual_assist_logout__ID_)

#### [virtual-assist-sessions](https://sonicos-api.sonicwall.com/\#/virtual-assist-sessions)      Virtual assist sessions reporting API.

GET[/reporting/virtual-assist/sessions](https://sonicos-api.sonicwall.com/#/operations/virtual-assist-sessions/get_reporting_virtual_assist_sessions)

#### [voip](https://sonicos-api.sonicwall.com/\#/voip)      VoIP configuration API.

GET[/voip](https://sonicos-api.sonicwall.com/#/operations/voip/get_voip)

PUT[/voip](https://sonicos-api.sonicwall.com/#/operations/voip/put_voip)

#### [voip-status](https://sonicos-api.sonicwall.com/\#/voip-status)      VoIP reporting API.

GET[/reporting/voip](https://sonicos-api.sonicwall.com/#/operations/voip-status/get_reporting_voip)

#### [voip-flush](https://sonicos-api.sonicwall.com/\#/voip-flush)      VoIP flush API.

POST[/voip/flush](https://sonicos-api.sonicwall.com/#/operations/voip-flush/post_voip_flush)

#### [ha-base](https://sonicos-api.sonicwall.com/\#/ha-base)      High availability base configuration API.

GET[/high-availability/base](https://sonicos-api.sonicwall.com/#/operations/ha-base/get_high_availability_base)

PUT[/high-availability/base](https://sonicos-api.sonicwall.com/#/operations/ha-base/put_high_availability_base)

#### [ha-monitoring-ipv4](https://sonicos-api.sonicwall.com/\#/ha-monitoring-ipv4)      High availability IPv4 monitoring configuration API.

GET[/high-availability/monitoring/ipv4](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv4/get_high_availability_monitoring_ipv4)

PUT[/high-availability/monitoring/ipv4](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv4/put_high_availability_monitoring_ipv4)

GET[/high-availability/monitoring/ipv4/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv4/get_high_availability_monitoring_ipv4_interface__INTERFACENAME_)

PUT[/high-availability/monitoring/ipv4/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv4/put_high_availability_monitoring_ipv4_interface__INTERFACENAME_)

#### [ha-monitoring-ipv6](https://sonicos-api.sonicwall.com/\#/ha-monitoring-ipv6)      High availability IPv6 monitoring configuration API.

GET[/high-availability/monitoring/ipv6](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv6/get_high_availability_monitoring_ipv6)

PUT[/high-availability/monitoring/ipv6](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv6/put_high_availability_monitoring_ipv6)

GET[/high-availability/monitoring/ipv6/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv6/get_high_availability_monitoring_ipv6_interface__INTERFACENAME_)

PUT[/high-availability/monitoring/ipv6/interface/{INTERFACENAME}](https://sonicos-api.sonicwall.com/#/operations/ha-monitoring-ipv6/put_high_availability_monitoring_ipv6_interface__INTERFACENAME_)

#### [ha](https://sonicos-api.sonicwall.com/\#/ha)      High availability status reporting API.

GET[/reporting/high-availability](https://sonicos-api.sonicwall.com/#/operations/ha/get_reporting_high_availability)

#### [ha-synchronize-settings](https://sonicos-api.sonicwall.com/\#/ha-synchronize-settings)      High availability synchronize settings API.

POST[/high-availability/synchronize/settings](https://sonicos-api.sonicwall.com/#/operations/ha-synchronize-settings/post_high_availability_synchronize_settings)

#### [ha-synchronize-firmware](https://sonicos-api.sonicwall.com/\#/ha-synchronize-firmware)      High availability synchronize firmware API.

POST[/high-availability/synchronize/firmware](https://sonicos-api.sonicwall.com/#/operations/ha-synchronize-firmware/post_high_availability_synchronize_firmware)

#### [ha-force-failover](https://sonicos-api.sonicwall.com/\#/ha-force-failover)      High availability force failover API.

POST[/high-availability/force-failover](https://sonicos-api.sonicwall.com/#/operations/ha-force-failover/post_high_availability_force_failover)

#### [sdwan-sla-class-objects](https://sonicos-api.sonicwall.com/\#/sdwan-sla-class-objects)      SD-WAN SLA class object configuration API.

GET[/sdwan/sla-class-objects](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/get_sdwan_sla_class_objects)

POST[/sdwan/sla-class-objects](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/post_sdwan_sla_class_objects)

PUT[/sdwan/sla-class-objects](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/put_sdwan_sla_class_objects)

PATCH[/sdwan/sla-class-objects](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/patch_sdwan_sla_class_objects)

GET[/sdwan/sla-class-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/get_sdwan_sla_class_objects_name__NAME_)

PUT[/sdwan/sla-class-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/put_sdwan_sla_class_objects_name__NAME_)

PATCH[/sdwan/sla-class-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/patch_sdwan_sla_class_objects_name__NAME_)

DELETE[/sdwan/sla-class-objects/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects/delete_sdwan_sla_class_objects_name__NAME_)

#### [sdwan-sla-class-objects-all](https://sonicos-api.sonicwall.com/\#/sdwan-sla-class-objects-all)      SD-WAN all SLA class objects configuration API.

DELETE[/sdwan/all-sla-class-objects](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-class-objects-all/delete_sdwan_all_sla_class_objects)

#### [sdwan-path-selection-profiles](https://sonicos-api.sonicwall.com/\#/sdwan-path-selection-profiles)      SD-WAN path selection profile configuration API.

GET[/sdwan/path-selection-profiles](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/get_sdwan_path_selection_profiles)

POST[/sdwan/path-selection-profiles](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/post_sdwan_path_selection_profiles)

PUT[/sdwan/path-selection-profiles](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/put_sdwan_path_selection_profiles)

PATCH[/sdwan/path-selection-profiles](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/patch_sdwan_path_selection_profiles)

GET[/sdwan/path-selection-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/get_sdwan_path_selection_profiles_name__NAME_)

PUT[/sdwan/path-selection-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/put_sdwan_path_selection_profiles_name__NAME_)

PATCH[/sdwan/path-selection-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/patch_sdwan_path_selection_profiles_name__NAME_)

DELETE[/sdwan/path-selection-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles/delete_sdwan_path_selection_profiles_name__NAME_)

#### [sdwan-path-selection-profiles-all](https://sonicos-api.sonicwall.com/\#/sdwan-path-selection-profiles-all)      SD-WAN all path selection profiles configuration API.

DELETE[/sdwan/all-path-selection-profiles](https://sonicos-api.sonicwall.com/#/operations/sdwan-path-selection-profiles-all/delete_sdwan_all_path_selection_profiles)

#### [sdwan-sla-probe-ipv4](https://sonicos-api.sonicwall.com/\#/sdwan-sla-probe-ipv4)      SD-WAN IPv4 SLA probe configuration API.

GET[/sdwan/sla-probes/ipv4](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/get_sdwan_sla_probes_ipv4)

POST[/sdwan/sla-probes/ipv4](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/post_sdwan_sla_probes_ipv4)

PUT[/sdwan/sla-probes/ipv4](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/put_sdwan_sla_probes_ipv4)

PATCH[/sdwan/sla-probes/ipv4](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/patch_sdwan_sla_probes_ipv4)

GET[/sdwan/sla-probes/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/get_sdwan_sla_probes_ipv4_name__NAME_)

PUT[/sdwan/sla-probes/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/put_sdwan_sla_probes_ipv4_name__NAME_)

PATCH[/sdwan/sla-probes/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/patch_sdwan_sla_probes_ipv4_name__NAME_)

DELETE[/sdwan/sla-probes/ipv4/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4/delete_sdwan_sla_probes_ipv4_name__NAME_)

#### [sdwan-sla-probe-ipv4-all](https://sonicos-api.sonicwall.com/\#/sdwan-sla-probe-ipv4-all)      SD-WAN all IPv4 performance class objects configuration API.

DELETE[/sdwan/all-sla-probes/ipv4](https://sonicos-api.sonicwall.com/#/operations/sdwan-sla-probe-ipv4-all/delete_sdwan_all_sla_probes_ipv4)

#### [sdwan-group](https://sonicos-api.sonicwall.com/\#/sdwan-group)      SD-WAN group configuration API.

GET[/sdwan/groups](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/get_sdwan_groups)

POST[/sdwan/groups](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/post_sdwan_groups)

PUT[/sdwan/groups](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/put_sdwan_groups)

PATCH[/sdwan/groups](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/patch_sdwan_groups)

GET[/sdwan/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/get_sdwan_groups_name__NAME_)

PUT[/sdwan/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/put_sdwan_groups_name__NAME_)

PATCH[/sdwan/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/patch_sdwan_groups_name__NAME_)

DELETE[/sdwan/groups/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/sdwan-group/delete_sdwan_groups_name__NAME_)

#### [sdwan-group-all](https://sonicos-api.sonicwall.com/\#/sdwan-group-all)      SD-WAN all groups configuration API.

DELETE[/sdwan/all-groups](https://sonicos-api.sonicwall.com/#/operations/sdwan-group-all/delete_sdwan_all_groups)

#### [sdwan-group-status](https://sonicos-api.sonicwall.com/\#/sdwan-group-status)      SD-WAN group reporting API.

GET[/reporting/sdwan/groups](https://sonicos-api.sonicwall.com/#/operations/sdwan-group-status/get_reporting_sdwan_groups)

#### [threat](https://sonicos-api.sonicwall.com/\#/threat)      Threat API.

POST[/threat](https://sonicos-api.sonicwall.com/#/operations/threat/post_threat)

#### [packet-replay-replay](https://sonicos-api.sonicwall.com/\#/packet-replay-replay)      Packet Replay configurations

POST[/packet-replay/replay/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-replay/post_packet_replay_replay_action_val)

#### [packet-replay-replay-mac](https://sonicos-api.sonicwall.com/\#/packet-replay-replay-mac)      Packet Replay configurations

POST[/packet-replay/replay-mac/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-replay-mac/post_packet_replay_replay_mac_action_val)

#### [import-packet-replay](https://sonicos-api.sonicwall.com/\#/import-packet-replay)      Upload packet replay file API.

POST[/import/packet-replay](https://sonicos-api.sonicwall.com/#/operations/import-packet-replay/post_import_packet_replay)

#### [packet-replay-delete-packet-replay-file](https://sonicos-api.sonicwall.com/\#/packet-replay-delete-packet-replay-file)      Upload packet replay file API.

POST[/packet-replay/delete/packet-replay-file](https://sonicos-api.sonicwall.com/#/operations/packet-replay-delete-packet-replay-file/post_packet_replay_delete_packet_replay_file)

#### [packet-replay-clear-packets](https://sonicos-api.sonicwall.com/\#/packet-replay-clear-packets)      Packet Replay Clear configurations

POST[/packet-replay/clear-packets](https://sonicos-api.sonicwall.com/#/operations/packet-replay-clear-packets/post_packet_replay_clear_packets)

#### [packet-replay-refresh-packets](https://sonicos-api.sonicwall.com/\#/packet-replay-refresh-packets)      Packet Replay Refresh configurations

POST[/packet-replay/refresh-packets](https://sonicos-api.sonicwall.com/#/operations/packet-replay-refresh-packets/post_packet_replay_refresh_packets)

#### [packet-replay-packet-crafting-udp](https://sonicos-api.sonicwall.com/\#/packet-replay-packet-crafting-udp)      Packet Replay packet crafting using UDP configurations

POST[/packet-replay/packet-crafting-udp/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-packet-crafting-udp/post_packet_replay_packet_crafting_udp_action_val)

#### [packet-replay-packet-crafting-icmp](https://sonicos-api.sonicwall.com/\#/packet-replay-packet-crafting-icmp)      Packet Replay packet crafting using ICMP configurations

POST[/packet-replay/packet-crafting-icmp/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-packet-crafting-icmp/post_packet_replay_packet_crafting_icmp_action_val)

#### [packet-replay-packet-crafting-igmp](https://sonicos-api.sonicwall.com/\#/packet-replay-packet-crafting-igmp)      Packet Replay packet crafting using IGMP configurations

POST[/packet-replay/packet-crafting-igmp/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-packet-crafting-igmp/post_packet_replay_packet_crafting_igmp_action_val)

#### [packet-replay-packet-crafting-buffer](https://sonicos-api.sonicwall.com/\#/packet-replay-packet-crafting-buffer)      Packet Replay packet crafting buffer configurations

POST[/packet-replay/packet-crafting-buffer/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-packet-crafting-buffer/post_packet_replay_packet_crafting_buffer_action_val)

#### [export-replayed-packets](https://sonicos-api.sonicwall.com/\#/export-replayed-packets)      Export captured packets from the device.

GET[/export/replayed-packets/html](https://sonicos-api.sonicwall.com/#/operations/export-replayed-packets/get_export_replayed_packets_html)

GET[/export/replayed-packets/app-data](https://sonicos-api.sonicwall.com/#/operations/export-replayed-packets/get_export_replayed_packets_app_data)

GET[/export/replayed-packets/pcapng](https://sonicos-api.sonicwall.com/#/operations/export-replayed-packets/get_export_replayed_packets_pcapng)

GET[/export/replayed-packets/libpcap](https://sonicos-api.sonicwall.com/#/operations/export-replayed-packets/get_export_replayed_packets_libpcap)

GET[/export/replayed-packets/text](https://sonicos-api.sonicwall.com/#/operations/export-replayed-packets/get_export_replayed_packets_text)

#### [packet-replay-individual-replay](https://sonicos-api.sonicwall.com/\#/packet-replay-individual-replay)      Packet Replay configurations

POST[/packet-replay/individual-replay/action-val](https://sonicos-api.sonicwall.com/#/operations/packet-replay-individual-replay/post_packet_replay_individual_replay_action_val)

#### [amazon-web-services-connection](https://sonicos-api.sonicwall.com/\#/amazon-web-services-connection)      amazon-web-services-connection configuration API.

GET[/amazon-web-services/connection](https://sonicos-api.sonicwall.com/#/operations/amazon-web-services-connection/get_amazon_web_services_connection)

PUT[/amazon-web-services/connection](https://sonicos-api.sonicwall.com/#/operations/amazon-web-services-connection/put_amazon_web_services_connection)

#### [amazon\_web\_services\_objects](https://sonicos-api.sonicwall.com/\#/amazon_web_services_objects)      Amazon Web Services objects configuration API.

GET[/amazon-web-services/objects/base](https://sonicos-api.sonicwall.com/#/operations/amazon_web_services_objects/get_amazon_web_services_objects_base)

PUT[/amazon-web-services/objects/base](https://sonicos-api.sonicwall.com/#/operations/amazon_web_services_objects/put_amazon_web_services_objects_base)

#### [amazon\_web\_services\_no\_address\_objects](https://sonicos-api.sonicwall.com/\#/amazon_web_services_no_address_objects)      Delete all Amazon web services related address objects and groups.

DELETE[/amazon-web-services/address-objects](https://sonicos-api.sonicwall.com/#/operations/amazon_web_services_no_address_objects/delete_amazon_web_services_address_objects)

#### [amazon\_web\_services\_force\_sync](https://sonicos-api.sonicwall.com/\#/amazon_web_services_force_sync)      Delete all Amazon web services related address objects and groups.

GET[/amazon-web-services/force-sync](https://sonicos-api.sonicwall.com/#/operations/amazon_web_services_force_sync/get_amazon_web_services_force_sync)

#### [aws\_object\_address\_group\_mapping](https://sonicos-api.sonicwall.com/\#/aws_object_address_group_mapping)      Amazon web services object address group mapping configuration.

GET[/amazon-web-services/objects/group-mappings](https://sonicos-api.sonicwall.com/#/operations/aws_object_address_group_mapping/get_amazon_web_services_objects_group_mappings)

POST[/amazon-web-services/objects/group-mappings](https://sonicos-api.sonicwall.com/#/operations/aws_object_address_group_mapping/post_amazon_web_services_objects_group_mappings)

PUT[/amazon-web-services/objects/group-mappings](https://sonicos-api.sonicwall.com/#/operations/aws_object_address_group_mapping/put_amazon_web_services_objects_group_mappings)

GET[/amazon-web-services/objects/group-mappings/index/{INDEX}](https://sonicos-api.sonicwall.com/#/operations/aws_object_address_group_mapping/get_amazon_web_services_objects_group_mappings_index__INDEX_)

PUT[/amazon-web-services/objects/group-mappings/index/{INDEX}](https://sonicos-api.sonicwall.com/#/operations/aws_object_address_group_mapping/put_amazon_web_services_objects_group_mappings_index__INDEX_)

DELETE[/amazon-web-services/objects/group-mappings/index/{INDEX}](https://sonicos-api.sonicwall.com/#/operations/aws_object_address_group_mapping/delete_amazon_web_services_objects_group_mappings_index__INDEX_)

#### [switch-trunk-ports](https://sonicos-api.sonicwall.com/\#/switch-trunk-ports)      Switch VLAN trunks configuration API.

GET[/switch/trunk/ports](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/get_switch_trunk_ports)

POST[/switch/trunk/ports](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/post_switch_trunk_ports)

PUT[/switch/trunk/ports](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/put_switch_trunk_ports)

PATCH[/switch/trunk/ports](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/patch_switch_trunk_ports)

GET[/switch/trunk/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/get_switch_trunk_ports_name__NAME_)

PUT[/switch/trunk/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/put_switch_trunk_ports_name__NAME_)

PATCH[/switch/trunk/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/patch_switch_trunk_ports_name__NAME_)

DELETE[/switch/trunk/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-trunk-ports/delete_switch_trunk_ports_name__NAME_)

#### [switch-vlan-trunk-enable-vlan](https://sonicos-api.sonicwall.com/\#/switch-vlan-trunk-enable-vlan)      Enable a custom VLAN ID on specific trunk port.

POST[/switch/trunk/interface/{INTERFACE}/vlan/{VLAN}](https://sonicos-api.sonicwall.com/#/operations/switch-vlan-trunk-enable-vlan/post_switch_trunk_interface__INTERFACE__vlan__VLAN_)

DELETE[/switch/trunk/interface/{INTERFACE}/vlan/{VLAN}](https://sonicos-api.sonicwall.com/#/operations/switch-vlan-trunk-enable-vlan/delete_switch_trunk_interface__INTERFACE__vlan__VLAN_)

#### [switch-portshield-ports](https://sonicos-api.sonicwall.com/\#/switch-portshield-ports)      Switch portshield ports configuration API.

GET[/switch/portshield/ports](https://sonicos-api.sonicwall.com/#/operations/switch-portshield-ports/get_switch_portshield_ports)

PUT[/switch/portshield/ports](https://sonicos-api.sonicwall.com/#/operations/switch-portshield-ports/put_switch_portshield_ports)

PATCH[/switch/portshield/ports](https://sonicos-api.sonicwall.com/#/operations/switch-portshield-ports/patch_switch_portshield_ports)

GET[/switch/portshield/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-portshield-ports/get_switch_portshield_ports_name__NAME_)

PUT[/switch/portshield/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-portshield-ports/put_switch_portshield_ports_name__NAME_)

PATCH[/switch/portshield/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-portshield-ports/patch_switch_portshield_ports_name__NAME_)

#### [switch-l2-discover-interface](https://sonicos-api.sonicwall.com/\#/switch-l2-discover-interface)      Switch L2 discover interfaces configuration API.

GET[/switch/l2-discover/interfaces](https://sonicos-api.sonicwall.com/#/operations/switch-l2-discover-interface/get_switch_l2_discover_interfaces)

PUT[/switch/l2-discover/interfaces](https://sonicos-api.sonicwall.com/#/operations/switch-l2-discover-interface/put_switch_l2_discover_interfaces)

#### [switch-lldp](https://sonicos-api.sonicwall.com/\#/switch-lldp)      Switch LLDP base configuration API.

GET[/switch/lldp](https://sonicos-api.sonicwall.com/#/operations/switch-lldp/get_switch_lldp)

PUT[/switch/lldp](https://sonicos-api.sonicwall.com/#/operations/switch-lldp/put_switch_lldp)

#### [switch-lldp-profiles](https://sonicos-api.sonicwall.com/\#/switch-lldp-profiles)      Switch LLDP profiles configuration API.

GET[/switch/lldp-profiles](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/get_switch_lldp_profiles)

POST[/switch/lldp-profiles](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/post_switch_lldp_profiles)

PUT[/switch/lldp-profiles](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/put_switch_lldp_profiles)

PATCH[/switch/lldp-profiles](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/patch_switch_lldp_profiles)

GET[/switch/lldp-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/get_switch_lldp_profiles_name__NAME_)

PUT[/switch/lldp-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/put_switch_lldp_profiles_name__NAME_)

PATCH[/switch/lldp-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/patch_switch_lldp_profiles_name__NAME_)

DELETE[/switch/lldp-profiles/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-lldp-profiles/delete_switch_lldp_profiles_name__NAME_)

#### [switch-link-aggregation-ports](https://sonicos-api.sonicwall.com/\#/switch-link-aggregation-ports)      Switch link aggregation configuration API.

GET[/switch/link-aggregation/ports](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/get_switch_link_aggregation_ports)

POST[/switch/link-aggregation/ports](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/post_switch_link_aggregation_ports)

PUT[/switch/link-aggregation/ports](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/put_switch_link_aggregation_ports)

PATCH[/switch/link-aggregation/ports](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/patch_switch_link_aggregation_ports)

GET[/switch/link-aggregation/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/get_switch_link_aggregation_ports_name__NAME_)

PUT[/switch/link-aggregation/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/put_switch_link_aggregation_ports_name__NAME_)

PATCH[/switch/link-aggregation/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/patch_switch_link_aggregation_ports_name__NAME_)

DELETE[/switch/link-aggregation/ports/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-link-aggregation-ports/delete_switch_link_aggregation_ports_name__NAME_)

#### [switch-port-mirrors](https://sonicos-api.sonicwall.com/\#/switch-port-mirrors)      Switch port mirroring configuration API.

GET[/switch/port/mirrors](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/get_switch_port_mirrors)

POST[/switch/port/mirrors](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/post_switch_port_mirrors)

PUT[/switch/port/mirrors](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/put_switch_port_mirrors)

PATCH[/switch/port/mirrors](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/patch_switch_port_mirrors)

GET[/switch/port/mirrors/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/get_switch_port_mirrors_name__NAME_)

PUT[/switch/port/mirrors/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/put_switch_port_mirrors_name__NAME_)

PATCH[/switch/port/mirrors/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/patch_switch_port_mirrors_name__NAME_)

DELETE[/switch/port/mirrors/name/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-port-mirrors/delete_switch_port_mirrors_name__NAME_)

#### [switch-discover](https://sonicos-api.sonicwall.com/\#/switch-discover)      Refresh L2 discovery.

POST[/switch/discover](https://sonicos-api.sonicwall.com/#/operations/switch-discover/post_switch_discover)

POST[/switch/discover/interface/{IFNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-discover/post_switch_discover_interface__IFNAME_)

#### [switch-reserved-vlan](https://sonicos-api.sonicwall.com/\#/switch-reserved-vlan)      Switch reserved VLAN information reporting API.

GET[/reporting/switch/reserved-vlan](https://sonicos-api.sonicwall.com/#/operations/switch-reserved-vlan/get_reporting_switch_reserved_vlan)

#### [switch-l2-vlans](https://sonicos-api.sonicwall.com/\#/switch-l2-vlans)      Switch VLAN table reporting API.

GET[/reporting/switch/l2-vlans](https://sonicos-api.sonicwall.com/#/operations/switch-l2-vlans/get_reporting_switch_l2_vlans)

#### [switch-lag-status](https://sonicos-api.sonicwall.com/\#/switch-lag-status)      Switch link aggregation status reporting API.

GET[/reporting/switch/link-aggregation/ports/status](https://sonicos-api.sonicwall.com/#/operations/switch-lag-status/get_reporting_switch_link_aggregation_ports_status)

#### [switch-controller-switch](https://sonicos-api.sonicwall.com/\#/switch-controller-switch)      SonicWall Switch Configuration

GET[/switch-controller/switch](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch/get_switch_controller_switch)

POST[/switch-controller/switch](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch/post_switch_controller_switch)

PUT[/switch-controller/switch](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch/put_switch_controller_switch)

GET[/switch-controller/switch/id/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch/get_switch_controller_switch_id__SWITCHNAME_)

PUT[/switch-controller/switch/id/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch/put_switch_controller_switch_id__SWITCHNAME_)

DELETE[/switch-controller/switch/id/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch/delete_switch_controller_switch_id__SWITCHNAME_)

#### [switch-controller-port](https://sonicos-api.sonicwall.com/\#/switch-controller-port)      SonicWall Switch Configuration

GET[/switch-controller/port](https://sonicos-api.sonicwall.com/#/operations/switch-controller-port/get_switch_controller_port)

PUT[/switch-controller/port](https://sonicos-api.sonicwall.com/#/operations/switch-controller-port/put_switch_controller_port)

GET[/switch-controller/port/name/{PORTNAME}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-port/get_switch_controller_port_name__PORTNAME__switch__SWITCHNAME_)

PUT[/switch-controller/port/name/{PORTNAME}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-port/put_switch_controller_port_name__PORTNAME__switch__SWITCHNAME_)

#### [switch-controller-voice-vlan](https://sonicos-api.sonicwall.com/\#/switch-controller-voice-vlan)      SonicWall Switch Configuration

GET[/switch-controller/voice-vlan](https://sonicos-api.sonicwall.com/#/operations/switch-controller-voice-vlan/get_switch_controller_voice_vlan)

PUT[/switch-controller/voice-vlan](https://sonicos-api.sonicwall.com/#/operations/switch-controller-voice-vlan/put_switch_controller_voice_vlan)

GET[/switch-controller/voice-vlan/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-voice-vlan/get_switch_controller_voice_vlan_switch__SWITCHNAME_)

PUT[/switch-controller/voice-vlan/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-voice-vlan/put_switch_controller_voice_vlan_switch__SWITCHNAME_)

#### [switch-controller-authorize](https://sonicos-api.sonicwall.com/\#/switch-controller-authorize)      Authorize Switch from Pending List to be added

POST[/switch-controller/authorize/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-authorize/post_switch_controller_authorize__NAME_)

#### [switch-controller-restart](https://sonicos-api.sonicwall.com/\#/switch-controller-restart)      Restart a sonicwall switch.

POST[/switch-controller/restart/{NAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-restart/post_switch_controller_restart__NAME_)

#### [switch-controller-fw-upgrade](https://sonicos-api.sonicwall.com/\#/switch-controller-fw-upgrade)      Upgrade firmware.

POST[/switch-controller/firmware-cloud/{NAME}/partition/{PARTITION\_NUM}/version/{VERSION}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-fw-upgrade/post_switch_controller_firmware_cloud__NAME__partition__PARTITION_NUM__version__VERSION_)

#### [switch-controller-network](https://sonicos-api.sonicwall.com/\#/switch-controller-network)      SonicWall Switch Configuration

GET[/switch-controller/network](https://sonicos-api.sonicwall.com/#/operations/switch-controller-network/get_switch_controller_network)

POST[/switch-controller/network](https://sonicos-api.sonicwall.com/#/operations/switch-controller-network/post_switch_controller_network)

PUT[/switch-controller/network](https://sonicos-api.sonicwall.com/#/operations/switch-controller-network/put_switch_controller_network)

GET[/switch-controller/network/vlan/{VLANID}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-network/get_switch_controller_network_vlan__VLANID__switch__SWITCHNAME_)

PUT[/switch-controller/network/vlan/{VLANID}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-network/put_switch_controller_network_vlan__VLANID__switch__SWITCHNAME_)

DELETE[/switch-controller/network/vlan/{VLANID}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-network/delete_switch_controller_network_vlan__VLANID__switch__SWITCHNAME_)

#### [switch-controller-radius](https://sonicos-api.sonicwall.com/\#/switch-controller-radius)      SonicWall Switch Radius Server Configuration

GET[/switch-controller/radius](https://sonicos-api.sonicwall.com/#/operations/switch-controller-radius/get_switch_controller_radius)

POST[/switch-controller/radius](https://sonicos-api.sonicwall.com/#/operations/switch-controller-radius/post_switch_controller_radius)

PUT[/switch-controller/radius](https://sonicos-api.sonicwall.com/#/operations/switch-controller-radius/put_switch_controller_radius)

GET[/switch-controller/radius/server-ip/{SERVERIP}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-radius/get_switch_controller_radius_server_ip__SERVERIP__switch__SWITCHNAME_)

PUT[/switch-controller/radius/server-ip/{SERVERIP}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-radius/put_switch_controller_radius_server_ip__SERVERIP__switch__SWITCHNAME_)

DELETE[/switch-controller/radius/server-ip/{SERVERIP}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-radius/delete_switch_controller_radius_server_ip__SERVERIP__switch__SWITCHNAME_)

#### [switch-controller-user](https://sonicos-api.sonicwall.com/\#/switch-controller-user)      SonicWall Switch Users Configuration

GET[/switch-controller/user](https://sonicos-api.sonicwall.com/#/operations/switch-controller-user/get_switch_controller_user)

POST[/switch-controller/user](https://sonicos-api.sonicwall.com/#/operations/switch-controller-user/post_switch_controller_user)

PUT[/switch-controller/user](https://sonicos-api.sonicwall.com/#/operations/switch-controller-user/put_switch_controller_user)

GET[/switch-controller/user/user-name/{USERNAME}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-user/get_switch_controller_user_user_name__USERNAME__switch__SWITCHNAME_)

PUT[/switch-controller/user/user-name/{USERNAME}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-user/put_switch_controller_user_user_name__USERNAME__switch__SWITCHNAME_)

DELETE[/switch-controller/user/user-name/{USERNAME}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-user/delete_switch_controller_user_user_name__USERNAME__switch__SWITCHNAME_)

#### [switch-controller-route](https://sonicos-api.sonicwall.com/\#/switch-controller-route)      SonicWall Switch Static Routes Configuration

GET[/switch-controller/route](https://sonicos-api.sonicwall.com/#/operations/switch-controller-route/get_switch_controller_route)

POST[/switch-controller/route](https://sonicos-api.sonicwall.com/#/operations/switch-controller-route/post_switch_controller_route)

PUT[/switch-controller/route](https://sonicos-api.sonicwall.com/#/operations/switch-controller-route/put_switch_controller_route)

#### [switch-controller-arp](https://sonicos-api.sonicwall.com/\#/switch-controller-arp)      SonicWall Switch ARP Configuration

GET[/switch-controller/arp](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp/get_switch_controller_arp)

POST[/switch-controller/arp](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp/post_switch_controller_arp)

PUT[/switch-controller/arp](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp/put_switch_controller_arp)

GET[/switch-controller/arp/mac/{MACADDR}/vlan/{VLANID}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp/get_switch_controller_arp_mac__MACADDR__vlan__VLANID__switch__SWITCHNAME_)

PUT[/switch-controller/arp/mac/{MACADDR}/vlan/{VLANID}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp/put_switch_controller_arp_mac__MACADDR__vlan__VLANID__switch__SWITCHNAME_)

DELETE[/switch-controller/arp/mac/{MACADDR}/vlan/{VLANID}/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp/delete_switch_controller_arp_mac__MACADDR__vlan__VLANID__switch__SWITCHNAME_)

#### [switch-controller-arp-aging-time](https://sonicos-api.sonicwall.com/\#/switch-controller-arp-aging-time)      SonicWall Switch ARP Configuration

GET[/switch-controller/arp-aging-time](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp-aging-time/get_switch_controller_arp_aging_time)

PUT[/switch-controller/arp-aging-time](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp-aging-time/put_switch_controller_arp_aging_time)

GET[/switch-controller/arp-aging-time/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp-aging-time/get_switch_controller_arp_aging_time_switch__SWITCHNAME_)

PUT[/switch-controller/arp-aging-time/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-arp-aging-time/put_switch_controller_arp_aging_time_switch__SWITCHNAME_)

#### [switch-controller-qos](https://sonicos-api.sonicwall.com/\#/switch-controller-qos)      SonicWall Switch QoS Configuration

GET[/switch-controller/qos](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos/get_switch_controller_qos)

PUT[/switch-controller/qos](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos/put_switch_controller_qos)

GET[/switch-controller/qos/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos/get_switch_controller_qos_switch__SWITCHNAME_)

PUT[/switch-controller/qos/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos/put_switch_controller_qos_switch__SWITCHNAME_)

#### [switch-controller-qos-dscp](https://sonicos-api.sonicwall.com/\#/switch-controller-qos-dscp)      SonicWall Switch QoS DSCP Configuration

GET[/switch-controller/qos-dscp](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-dscp/get_switch_controller_qos_dscp)

PUT[/switch-controller/qos-dscp](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-dscp/put_switch_controller_qos_dscp)

GET[/switch-controller/qos-dscp/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-dscp/get_switch_controller_qos_dscp_switch__SWITCHNAME_)

PUT[/switch-controller/qos-dscp/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-dscp/put_switch_controller_qos_dscp_switch__SWITCHNAME_)

#### [switch-controller-qos-cos](https://sonicos-api.sonicwall.com/\#/switch-controller-qos-cos)      SonicWall Switch QoS CoS Configuration

GET[/switch-controller/qos-cos](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-cos/get_switch_controller_qos_cos)

PUT[/switch-controller/qos-cos](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-cos/put_switch_controller_qos_cos)

GET[/switch-controller/qos-cos/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-cos/get_switch_controller_qos_cos_switch__SWITCHNAME_)

PUT[/switch-controller/qos-cos/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-qos-cos/put_switch_controller_qos_cos_switch__SWITCHNAME_)

#### [switch-controller-statistics-clear](https://sonicos-api.sonicwall.com/\#/switch-controller-statistics-clear)      Interface disconnect API.

POST[/switch-controller/clear-statistics/switch/{SWITCHNAME}](https://sonicos-api.sonicwall.com/#/operations/switch-controller-statistics-clear/post_switch_controller_clear_statistics_switch__SWITCHNAME_)

#### [switch-controller-switch-info](https://sonicos-api.sonicwall.com/\#/switch-controller-switch-info)      SonicWall Switch Configuration

GET[/switch-controller/switch-info](https://sonicos-api.sonicwall.com/#/operations/switch-controller-switch-info/get_switch_controller_switch_info)

#### [dell-switch-switch](https://sonicos-api.sonicwall.com/\#/dell-switch-switch)      Dell Switch Configuration

GET[/dell-switch/switch](https://sonicos-api.sonicwall.com/#/operations/dell-switch-switch/get_dell_switch_switch)

POST[/dell-switch/switch](https://sonicos-api.sonicwall.com/#/operations/dell-switch-switch/post_dell_switch_switch)

PUT[/dell-switch/switch](https://sonicos-api.sonicwall.com/#/operations/dell-switch-switch/put_dell_switch_switch)

GET[/dell-switch/switch/id/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-switch/get_dell_switch_switch_id__SWITCHID_)

PUT[/dell-switch/switch/id/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-switch/put_dell_switch_switch_id__SWITCHID_)

DELETE[/dell-switch/switch/id/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-switch/delete_dell_switch_switch_id__SWITCHID_)

#### [dell-switch-port](https://sonicos-api.sonicwall.com/\#/dell-switch-port)      Dell Switch Configuration

GET[/dell-switch/port](https://sonicos-api.sonicwall.com/#/operations/dell-switch-port/get_dell_switch_port)

PUT[/dell-switch/port](https://sonicos-api.sonicwall.com/#/operations/dell-switch-port/put_dell_switch_port)

GET[/dell-switch/port/name/{PORTNAME}/switch/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-port/get_dell_switch_port_name__PORTNAME__switch__SWITCHID_)

PUT[/dell-switch/port/name/{PORTNAME}/switch/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-port/put_dell_switch_port_name__PORTNAME__switch__SWITCHID_)

#### [dell-switch-restart](https://sonicos-api.sonicwall.com/\#/dell-switch-restart)      Restart a sonicwall switch.

POST[/dell-switch/restart/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-restart/post_dell_switch_restart__SWITCHID_)

#### [dell-switch-statistics-clear](https://sonicos-api.sonicwall.com/\#/dell-switch-statistics-clear)      Interface disconnect API.

POST[/dell-switch/clear-statistics/switch/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-statistics-clear/post_dell_switch_clear_statistics_switch__SWITCHID_)

#### [dell-switch-upload-firmware](https://sonicos-api.sonicwall.com/\#/dell-switch-upload-firmware)      Upload dell-switch firmware API.

POST[/import/dell-switch/firmware](https://sonicos-api.sonicwall.com/#/operations/dell-switch-upload-firmware/post_import_dell_switch_firmware)

#### [dell-switch-statistics](https://sonicos-api.sonicwall.com/\#/dell-switch-statistics)      Statistics of dell switch

GET[/reporting/dell-switch/statistics/switch/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-statistics/get_reporting_dell_switch_statistics_switch__SWITCHID_)

#### [dell-switch-firmware-mgmt](https://sonicos-api.sonicwall.com/\#/dell-switch-firmware-mgmt)      Statistics of dell switch

GET[/reporting/dell-switch/firmware-mgmt/switch/{SWITCHID}](https://sonicos-api.sonicwall.com/#/operations/dell-switch-firmware-mgmt/get_reporting_dell_switch_firmware_mgmt_switch__SWITCHID_)

#### [dell-switch-ports](https://sonicos-api.sonicwall.com/\#/dell-switch-ports)      Ports information of dell switch

GET[/reporting/dell-switch/ports](https://sonicos-api.sonicwall.com/#/operations/dell-switch-ports/get_reporting_dell_switch_ports)

#### [dell-switch-status](https://sonicos-api.sonicwall.com/\#/dell-switch-status)      Status of all dell switches

GET[/reporting/dell-switch/status](https://sonicos-api.sonicwall.com/#/operations/dell-switch-status/get_reporting_dell_switch_status)

#### [dell-switch-product-info](https://sonicos-api.sonicwall.com/\#/dell-switch-product-info)      Status of all dell switches

GET[/reporting/dell-switch/product-info](https://sonicos-api.sonicwall.com/#/operations/dell-switch-product-info/get_reporting_dell_switch_product_info)

#### [portshield-groups-external-switch](https://sonicos-api.sonicwall.com/\#/portshield-groups-external-switch)      Portshield groups external switch objects configuration API.

GET[/portshield-groups/external-switches](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/get_portshield_groups_external_switches)

POST[/portshield-groups/external-switches](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/post_portshield_groups_external_switches)

PUT[/portshield-groups/external-switches](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/put_portshield_groups_external_switches)

PATCH[/portshield-groups/external-switches](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/patch_portshield_groups_external_switches)

GET[/portshield-groups/external-switches/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/get_portshield_groups_external_switches_id__ID_)

PUT[/portshield-groups/external-switches/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/put_portshield_groups_external_switches_id__ID_)

PATCH[/portshield-groups/external-switches/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/patch_portshield_groups_external_switches_id__ID_)

DELETE[/portshield-groups/external-switches/id/{ID}](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch/delete_portshield_groups_external_switches_id__ID_)

#### [portshield-groups-external-switch-diagnostics-statistics](https://sonicos-api.sonicwall.com/\#/portshield-groups-external-switch-diagnostics-statistics)      Portshield group external switch diagnostics statistics reporting API.

GET[/reporting/portshield-groups/external-switch-diagnostics/statistics](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch-diagnostics-statistics/get_reporting_portshield_groups_external_switch_diagnostics_statistics)

#### [portshield-groups-external-switch-diagnostics-firmware-management](https://sonicos-api.sonicwall.com/\#/portshield-groups-external-switch-diagnostics-firmware-management)      Portshield group external switch diagnostics firmware management reporting API.

GET[/reporting/portshield-groups/external-switch-diagnostics/firmware-management](https://sonicos-api.sonicwall.com/#/operations/portshield-groups-external-switch-diagnostics-firmware-management/get_reporting_portshield_groups_external_switch_diagnostics_firmware_management)

#### [portshield-port-configuration](https://sonicos-api.sonicwall.com/\#/portshield-port-configuration)      Portshield port configuration reporting API.

GET[/reporting/portshield/port-configuration](https://sonicos-api.sonicwall.com/#/operations/portshield-port-configuration/get_reporting_portshield_port_configuration)

#### [diag-advanced](https://sonicos-api.sonicwall.com/\#/diag-advanced)      Advanced diag configuration API.

GET[/diag/advanced/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced/get_diag_advanced_base)

PUT[/diag/advanced/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced/put_diag_advanced_base)

#### [diag-advanced-log](https://sonicos-api.sonicwall.com/\#/diag-advanced-log)      Advanced diag log configuration API.

GET[/diag/advanced/log](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-log/get_diag_advanced_log)

PUT[/diag/advanced/log](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-log/put_diag_advanced_log)

#### [diag-advanced-threat-api](https://sonicos-api.sonicwall.com/\#/diag-advanced-threat-api)      Advanced diag threat API configuration API.

GET[/diag/advanced/threat-api](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-threat-api/get_diag_advanced_threat_api)

PUT[/diag/advanced/threat-api](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-threat-api/put_diag_advanced_threat_api)

#### [diag-advanced-dpi-stateful-firewall-security](https://sonicos-api.sonicwall.com/\#/diag-advanced-dpi-stateful-firewall-security)      DPI and stateful firewall security action API.

POST[/diag/advanced/dpi-stateful-firewall-security](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dpi-stateful-firewall-security/post_diag_advanced_dpi_stateful_firewall_security)

#### [diag-advanced-stateful-firewall-security](https://sonicos-api.sonicwall.com/\#/diag-advanced-stateful-firewall-security)      Stateful firewall security action API.

POST[/diag/advanced/stateful-firewall-security](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-stateful-firewall-security/post_diag_advanced_stateful_firewall_security)

#### [diag-advanced-arp](https://sonicos-api.sonicwall.com/\#/diag-advanced-arp)      Advanced diag ARP configuration API.

GET[/diag/advanced/arp/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-arp/get_diag_advanced_arp_base)

PUT[/diag/advanced/arp/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-arp/put_diag_advanced_arp_base)

#### [diag-advanced-arp-send-system-arps](https://sonicos-api.sonicwall.com/\#/diag-advanced-arp-send-system-arps)      Send system ARPs action API.

POST[/diag/advanced/arp/send-system-arps](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-arp-send-system-arps/post_diag_advanced_arp_send_system_arps)

#### [diag-advanced-preference](https://sonicos-api.sonicwall.com/\#/diag-advanced-preference)      Advanced diag preference configuration API.

GET[/diag/advanced/preference](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-preference/get_diag_advanced_preference)

PUT[/diag/advanced/preference](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-preference/put_diag_advanced_preference)

#### [diag-advanced-user-authentication](https://sonicos-api.sonicwall.com/\#/diag-advanced-user-authentication)      Advanced diag user authentication configuration API.

GET[/diag/advanced/user-authentication/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication/get_diag_advanced_user_authentication_base)

PUT[/diag/advanced/user-authentication/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication/put_diag_advanced_user_authentication_base)

#### [diag-advanced-user-authentication-flush-cached-redirect-files](https://sonicos-api.sonicwall.com/\#/diag-advanced-user-authentication-flush-cached-redirect-files)      Advanced diag user authentication configuration API.

POST[/diag/advanced/user-authentication/flush-cached-redirect-files](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-flush-cached-redirect-files/post_diag_advanced_user_authentication_flush_cached_redirect_files)

#### [diag-advanced-user-authentication-logout-users](https://sonicos-api.sonicwall.com/\#/diag-advanced-user-authentication-logout-users)      Advanced diag user authentication logout users API.

POST[/diag/advanced/user-authentication/logout-users](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-logout-users/post_diag_advanced_user_authentication_logout_users)

#### [diag-advanced-user-authentication-kill-all-inactive-users](https://sonicos-api.sonicwall.com/\#/diag-advanced-user-authentication-kill-all-inactive-users)      Advanced diag user authentication kill all inactive users API.

POST[/diag/advanced/user-authentication/kill-all-inactive-users/ntlm](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-kill-all-inactive-users/post_diag_advanced_user_authentication_kill_all_inactive_users_ntlm)

POST[/diag/advanced/user-authentication/kill-all-inactive-users/tsa](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-kill-all-inactive-users/post_diag_advanced_user_authentication_kill_all_inactive_users_tsa)

POST[/diag/advanced/user-authentication/kill-all-inactive-users/all](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-kill-all-inactive-users/post_diag_advanced_user_authentication_kill_all_inactive_users_all)

POST[/diag/advanced/user-authentication/kill-all-inactive-users/sso-agent](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-kill-all-inactive-users/post_diag_advanced_user_authentication_kill_all_inactive_users_sso_agent)

POST[/diag/advanced/user-authentication/kill-all-inactive-users/rad-acct](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-user-authentication-kill-all-inactive-users/post_diag_advanced_user_authentication_kill_all_inactive_users_rad_acct)

#### [diag-advanced-network](https://sonicos-api.sonicwall.com/\#/diag-advanced-network)      Advanced diag network and routing configuration API.

GET[/diag/advanced/network/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-network/get_diag_advanced_network_base)

PUT[/diag/advanced/network/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-network/put_diag_advanced_network_base)

#### [diag-advanced-network-clear-ospf](https://sonicos-api.sonicwall.com/\#/diag-advanced-network-clear-ospf)      Clear OSPF process action API.

DELETE[/diag/advanced/network/ospf](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-network-clear-ospf/delete_diag_advanced_network_ospf)

#### [diag-advanced-dns](https://sonicos-api.sonicwall.com/\#/diag-advanced-dns)      Advanced diag DNS configuration API.

GET[/diag/advanced/dns](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dns/get_diag_advanced_dns)

PUT[/diag/advanced/dns](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dns/put_diag_advanced_dns)

#### [diag-advanced-dns-proxy](https://sonicos-api.sonicwall.com/\#/diag-advanced-dns-proxy)      Advanced diag DNS proxy configuration API.

GET[/diag/advanced/dns-proxy](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dns-proxy/get_diag_advanced_dns_proxy)

PUT[/diag/advanced/dns-proxy](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dns-proxy/put_diag_advanced_dns_proxy)

#### [diag-advanced-dns-security](https://sonicos-api.sonicwall.com/\#/diag-advanced-dns-security)      Advanced diag DNS security configuration API.

GET[/diag/advanced/dns-security](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dns-security/get_diag_advanced_dns_security)

PUT[/diag/advanced/dns-security](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dns-security/put_diag_advanced_dns_security)

#### [diag-advanced-pppoe](https://sonicos-api.sonicwall.com/\#/diag-advanced-pppoe)      Advanced diag pppoe API

GET[/diag/advanced/pppoe](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-pppoe/get_diag_advanced_pppoe)

PUT[/diag/advanced/pppoe](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-pppoe/put_diag_advanced_pppoe)

#### [diag-advanced-dial-up](https://sonicos-api.sonicwall.com/\#/diag-advanced-dial-up)      Advanced diag dial-up API

GET[/diag/advanced/dial-up/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dial-up/get_diag_advanced_dial_up_base)

PUT[/diag/advanced/dial-up/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dial-up/put_diag_advanced_dial_up_base)

#### [diag-advanced-dial-up-reset](https://sonicos-api.sonicwall.com/\#/diag-advanced-dial-up-reset)      Reset Dial-up Configuration API.

POST[/diag/advanced/dial-up/reset](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dial-up-reset/post_diag_advanced_dial_up_reset)

#### [diag-advanced-ssl-vpn](https://sonicos-api.sonicwall.com/\#/diag-advanced-ssl-vpn)      Advanced diag ssl-vpn API

GET[/diag/advanced/ssl-vpn](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-ssl-vpn/get_diag_advanced_ssl_vpn)

PUT[/diag/advanced/ssl-vpn](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-ssl-vpn/put_diag_advanced_ssl_vpn)

#### [diag-advanced-backend](https://sonicos-api.sonicwall.com/\#/diag-advanced-backend)      Advanced diag backend server API

GET[/diag/advanced/backend](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-backend/get_diag_advanced_backend)

PUT[/diag/advanced/backend](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-backend/put_diag_advanced_backend)

#### [diag-advanced-wireless](https://sonicos-api.sonicwall.com/\#/diag-advanced-wireless)      Advanced diag wireless API

GET[/diag/advanced/wireless/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wireless/get_diag_advanced_wireless_base)

PUT[/diag/advanced/wireless/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wireless/put_diag_advanced_wireless_base)

#### [diag-advanced-wireless-sonicpoint-firmware-update](https://sonicos-api.sonicwall.com/\#/diag-advanced-wireless-sonicpoint-firmware-update)      Firmware Update Configuration API.

POST[/diag/advanced/wireless/sonicpoint/update-firmware](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wireless-sonicpoint-firmware-update/post_diag_advanced_wireless_sonicpoint_update_firmware)

#### [diag-advanced-watchdog](https://sonicos-api.sonicwall.com/\#/diag-advanced-watchdog)      Advanced diag Watchdog configuration API.

GET[/diag/advanced/watchdog](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-watchdog/get_diag_advanced_watchdog)

PUT[/diag/advanced/watchdog](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-watchdog/put_diag_advanced_watchdog)

#### [diag-advanced-wan-acceleration](https://sonicos-api.sonicwall.com/\#/diag-advanced-wan-acceleration)      Advanced diag WAN Acceleration API

GET[/diag/advanced/wan-acceleration](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wan-acceleration/get_diag_advanced_wan_acceleration)

PUT[/diag/advanced/wan-acceleration](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wan-acceleration/put_diag_advanced_wan_acceleration)

#### [diag-advanced-wan-acceleration-clear-debug-stats](https://sonicos-api.sonicwall.com/\#/diag-advanced-wan-acceleration-clear-debug-stats)      Clear Debug Stats Action API.

POST[/diag/advanced/wan-acceleration/clear-debug-stats](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wan-acceleration-clear-debug-stats/post_diag_advanced_wan_acceleration_clear_debug_stats)

#### [diag-advanced-wan-acceleration-clear-tcp-acceleration](https://sonicos-api.sonicwall.com/\#/diag-advanced-wan-acceleration-clear-tcp-acceleration)      Clear TCP acceleration Action API.

POST[/diag/advanced/wan-acceleration/clear-tcp-acceleration](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-wan-acceleration-clear-tcp-acceleration/post_diag_advanced_wan_acceleration_clear_tcp_acceleration)

#### [diag-advanced-flow-reporting](https://sonicos-api.sonicwall.com/\#/diag-advanced-flow-reporting)      Advanced diag Flow Reporting API

GET[/diag/advanced/flow-reporting/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-flow-reporting/get_diag_advanced_flow_reporting_base)

PUT[/diag/advanced/flow-reporting/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-flow-reporting/put_diag_advanced_flow_reporting_base)

#### [diag-advanced-flow-reporting-clear-location-map](https://sonicos-api.sonicwall.com/\#/diag-advanced-flow-reporting-clear-location-map)      Send system ARPs action API.

POST[/diag/advanced/flow-reporting/clear-location-map](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-flow-reporting-clear-location-map/post_diag_advanced_flow_reporting_clear_location_map)

#### [diag-advanced-flow-reporting-clear-database-tables](https://sonicos-api.sonicwall.com/\#/diag-advanced-flow-reporting-clear-database-tables)      Send system ARPs action API.

POST[/diag/advanced/flow-reporting/clear-database-tables](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-flow-reporting-clear-database-tables/post_diag_advanced_flow_reporting_clear_database_tables)

#### [diag-advanced-dhcp](https://sonicos-api.sonicwall.com/\#/diag-advanced-dhcp)      Advanced diag DHCP configuration API.

GET[/diag/advanced/dhcp/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dhcp/get_diag_advanced_dhcp_base)

PUT[/diag/advanced/dhcp/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dhcp/put_diag_advanced_dhcp_base)

#### [diag-advanced-dhcp-leases-to-flash](https://sonicos-api.sonicwall.com/\#/diag-advanced-dhcp-leases-to-flash)      Save DHCP leases to flash action API.

POST[/diag/advanced/dhcp/save-leases](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dhcp-leases-to-flash/post_diag_advanced_dhcp_save_leases)

#### [diag-advanced-vpn](https://sonicos-api.sonicwall.com/\#/diag-advanced-vpn)      Advanced diag vpn API

GET[/diag/advanced/vpn](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-vpn/get_diag_advanced_vpn)

PUT[/diag/advanced/vpn](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-vpn/put_diag_advanced_vpn)

#### [diag-advanced-management](https://sonicos-api.sonicwall.com/\#/diag-advanced-management)      Advanced diag management API

GET[/diag/advanced/management](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-management/get_diag_advanced_management)

PUT[/diag/advanced/management](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-management/put_diag_advanced_management)

#### [diag-advanced-security-service](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service)      Advanced diag security service API

GET[/diag/advanced/security-service/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service/get_diag_advanced_security_service_base)

PUT[/diag/advanced/security-service/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service/put_diag_advanced_security_service_base)

#### [diag-advanced-security-service-reset-av-info](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-av-info)      Advanced diag security service reset av info API.

POST[/diag/advanced/security-service/reset/av-info](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-av-info/post_diag_advanced_security_service_reset_av_info)

#### [diag-advanced-security-service-reset-ngav-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-ngav-cache)      Advanced diag security service reset ngav cache API.

POST[/diag/advanced/security-service/reset/next-gen-av-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-ngav-cache/post_diag_advanced_security_service_reset_next_gen_av_cache)

#### [diag-advanced-security-service-reset-licenses](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-licenses)      Advanced diag security service reset licenses API.

POST[/diag/advanced/security-service/reset/licenses](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-licenses/post_diag_advanced_security_service_reset_licenses)

#### [diag-advanced-security-service-reset-client-cfs-info](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-client-cfs-info)      Advanced diag security service reset client cfs info API.

POST[/diag/advanced/security-service/reset/client-content-filtering/info](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-client-cfs-info/post_diag_advanced_security_service_reset_client_content_filtering_info)

#### [diag-advanced-security-service-reset-client-cfs-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-client-cfs-cache)      Advanced diag security service reset client cfs cache API.

POST[/diag/advanced/security-service/reset/client-content-filtering/cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-client-cfs-cache/post_diag_advanced_security_service_reset_client_content_filtering_cache)

#### [diag-advanced-security-service-reset-http-clientless-notification-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-http-clientless-notification-cache)      Advanced diag security service reset http cache API.

POST[/diag/advanced/security-service/reset/http-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-http-clientless-notification-cache/post_diag_advanced_security_service_reset_http_cache)

#### [diag-advanced-security-service-reset-cloud-av-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-cloud-av-cache)      Advanced diag security service reset cloud av cache API.

POST[/diag/advanced/security-service/reset/cloud-av-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-cloud-av-cache/post_diag_advanced_security_service_reset_cloud_av_cache)

#### [diag-advanced-security-service-reset-cfs-memory-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-cfs-memory-cache)      Advanced diag security service reset cfs memory cache API.

POST[/diag/advanced/security-service/reset/cfs-memory-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-cfs-memory-cache/post_diag_advanced_security_service_reset_cfs_memory_cache)

#### [diag-advanced-security-service-reset-cfs-persistent-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-cfs-persistent-cache)      Advanced diag security service reset cfs persistent cache API.

POST[/diag/advanced/security-service/reset/cfs-persistent-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-cfs-persistent-cache/post_diag_advanced_security_service_reset_cfs_persistent_cache)

#### [diag-advanced-security-service-reset-client-enforcement-status-info](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-client-enforcement-status-info)      Advanced diag security service reset cfs persistent cache API.

POST[/diag/advanced/security-service/reset/client-enforcement-status-info](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-client-enforcement-status-info/post_diag_advanced_security_service_reset_client_enforcement_status_info)

#### [diag-advanced-security-service-reset-registration-log](https://sonicos-api.sonicwall.com/\#/diag-advanced-security-service-reset-registration-log)      Advanced diag security service reset registration log.

POST[/diag/advanced/security-service/reset/registration-log](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-security-service-reset-registration-log/post_diag_advanced_security_service_reset_registration_log)

#### [diag-advanced-voip](https://sonicos-api.sonicwall.com/\#/diag-advanced-voip)      Advanced diag VoIP configuration API.

GET[/diag/advanced/voip/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-voip/get_diag_advanced_voip_base)

PUT[/diag/advanced/voip/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-voip/put_diag_advanced_voip_base)

#### [diag-advanced-voip-reset-sip-database](https://sonicos-api.sonicwall.com/\#/diag-advanced-voip-reset-sip-database)      Reset sip database action API.

POST[/diag/advanced/voip/reset-sip-database](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-voip-reset-sip-database/post_diag_advanced_voip_reset_sip_database)

#### [diag-advanced-anti-spam](https://sonicos-api.sonicwall.com/\#/diag-advanced-anti-spam)      Advanced diag anti-spam configuration API.

GET[/diag/advanced/anti-spam/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-anti-spam/get_diag_advanced_anti_spam_base)

PUT[/diag/advanced/anti-spam/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-anti-spam/put_diag_advanced_anti_spam_base)

#### [diag-advanced-anti-spam-clear-statistics](https://sonicos-api.sonicwall.com/\#/diag-advanced-anti-spam-clear-statistics)      Advanced diag anti spam clear statistics configuration API.

DELETE[/diag/advanced/anti-spam/statistics](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-anti-spam-clear-statistics/delete_diag_advanced_anti_spam_statistics)

#### [diag-advanced-anti-spam-reset-grid-name-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-anti-spam-reset-grid-name-cache)      Advanced diag anti spam reset GRID name cache API.

POST[/diag/advanced/anti-spam/reset-grid-name-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-anti-spam-reset-grid-name-cache/post_diag_advanced_anti_spam_reset_grid_name_cache)

#### [diag-advanced-anti-spam-policies-and-obects](https://sonicos-api.sonicwall.com/\#/diag-advanced-anti-spam-policies-and-obects)      Advanced diag anti spam deletes policies and objects API.

DELETE[/diag/advanced/anti-spam/policies-and-objects](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-anti-spam-policies-and-obects/delete_diag_advanced_anti_spam_policies_and_objects)

#### [diag-advanced-firewall](https://sonicos-api.sonicwall.com/\#/diag-advanced-firewall)      Advanced diag firewall configuration API

GET[/diag/advanced/firewall](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-firewall/get_diag_advanced_firewall)

PUT[/diag/advanced/firewall](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-firewall/put_diag_advanced_firewall)

#### [diag\_advanced\_firewall\_flush\_connections](https://sonicos-api.sonicwall.com/\#/diag_advanced_firewall_flush_connections)      Advanced diag flush firewall connections action API

DELETE[/diag/advanced/firewall-connections](https://sonicos-api.sonicwall.com/#/operations/diag_advanced_firewall_flush_connections/delete_diag_advanced_firewall_connections)

#### [diag-advanced-diagnostics](https://sonicos-api.sonicwall.com/\#/diag-advanced-diagnostics)      Advanced diag diagnostics configuration API

GET[/diag/advanced/diagnostics/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-diagnostics/get_diag_advanced_diagnostics_base)

PUT[/diag/advanced/diagnostics/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-diagnostics/put_diag_advanced_diagnostics_base)

#### [diag-advanced-encryption](https://sonicos-api.sonicwall.com/\#/diag-advanced-encryption)      Advanced diag encryption API

GET[/diag/advanced/encryption](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-encryption/get_diag_advanced_encryption)

PUT[/diag/advanced/encryption](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-encryption/put_diag_advanced_encryption)

#### [diag\_advanced\_diagnostics\_wan\_connectivity\_test\_start](https://sonicos-api.sonicwall.com/\#/diag_advanced_diagnostics_wan_connectivity_test_start)      WAN connectivity test start

POST[/diag/advanced/diagnostics/wan-connectivity-test-start](https://sonicos-api.sonicwall.com/#/operations/diag_advanced_diagnostics_wan_connectivity_test_start/post_diag_advanced_diagnostics_wan_connectivity_test_start)

#### [diag\_advanced\_diagnostics\_wan\_connectivity\_test\_stop](https://sonicos-api.sonicwall.com/\#/diag_advanced_diagnostics_wan_connectivity_test_stop)      WAN connectivity test stop

POST[/diag/advanced/diagnostics/wan-connectivity-test-stop](https://sonicos-api.sonicwall.com/#/operations/diag_advanced_diagnostics_wan_connectivity_test_stop/post_diag_advanced_diagnostics_wan_connectivity_test_stop)

#### [diag\_advanced\_diagnostics\_wan\_connectivity\_test\_send\_log](https://sonicos-api.sonicwall.com/\#/diag_advanced_diagnostics_wan_connectivity_test_send_log)      WAN connectivity test send log

POST[/diag/advanced/diagnostics/wan-connectivity-test-send-log](https://sonicos-api.sonicwall.com/#/operations/diag_advanced_diagnostics_wan_connectivity_test_send_log/post_diag_advanced_diagnostics_wan_connectivity_test_send_log)

#### [diag-advanced-geoip-location-service](https://sonicos-api.sonicwall.com/\#/diag-advanced-geoip-location-service)      Advanced diag geoip location server.

GET[/diag/advanced/geoip-location-service/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-geoip-location-service/get_diag_advanced_geoip_location_service_base)

PUT[/diag/advanced/geoip-location-service/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-geoip-location-service/put_diag_advanced_geoip_location_service_base)

#### [diag-advanced-geoip-location-service-clear-location-cache](https://sonicos-api.sonicwall.com/\#/diag-advanced-geoip-location-service-clear-location-cache)      Clear Geoip location cache API.

POST[/diag/advanced/geoip-location-service/clear-location-cache](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-geoip-location-service-clear-location-cache/post_diag_advanced_geoip_location_service_clear_location_cache)

#### [diag-advanced-high-availability](https://sonicos-api.sonicwall.com/\#/diag-advanced-high-availability)      High Availabilty Configuration API.

GET[/diag/advanced/high-availability/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-high-availability/get_diag_advanced_high_availability_base)

PUT[/diag/advanced/high-availability/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-high-availability/put_diag_advanced_high_availability_base)

#### [diag-advanced-dpi-ssl](https://sonicos-api.sonicwall.com/\#/diag-advanced-dpi-ssl)      High Availabilty Configuration API.

GET[/diag/advanced/dpi-ssl/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dpi-ssl/get_diag_advanced_dpi_ssl_base)

PUT[/diag/advanced/dpi-ssl/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dpi-ssl/put_diag_advanced_dpi_ssl_base)

#### [diag-advanced-dpi-ssl-update-security-services-info](https://sonicos-api.sonicwall.com/\#/diag-advanced-dpi-ssl-update-security-services-info)      High Availabilty Configuration API.

POST[/diag/advanced/dpi-ssl/update-security-services-info](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dpi-ssl-update-security-services-info/post_diag_advanced_dpi_ssl_update_security_services_info)

#### [diag-advanced-dpi-ssl-clear-internal-session-and-cache-state](https://sonicos-api.sonicwall.com/\#/diag-advanced-dpi-ssl-clear-internal-session-and-cache-state)      High Availabilty Configuration API.

POST[/diag/advanced/dpi-ssl/clear-internal-session-and-cache-state](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-dpi-ssl-clear-internal-session-and-cache-state/post_diag_advanced_dpi_ssl_clear_internal_session_and_cache_state)

#### [diag-advanced-network-fo-lb](https://sonicos-api.sonicwall.com/\#/diag-advanced-network-fo-lb)      Advanced diag network failover and load balancing configuration API.

GET[/diag/advanced/network-fo-lb](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-network-fo-lb/get_diag_advanced_network_fo_lb)

PUT[/diag/advanced/network-fo-lb](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-network-fo-lb/put_diag_advanced_network_fo_lb)

#### [diag-advanced-trace-log](https://sonicos-api.sonicwall.com/\#/diag-advanced-trace-log)      Advanced diag trace log configuration API.

GET[/diag/advanced/trace-log/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-trace-log/get_diag_advanced_trace_log_base)

PUT[/diag/advanced/trace-log/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-trace-log/put_diag_advanced_trace_log_base)

#### [diag-advanced-clear-trace-log](https://sonicos-api.sonicwall.com/\#/diag-advanced-clear-trace-log)      Clear trace log information.

POST[/diag/advanced/clear/trace-log/current](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-clear-trace-log/post_diag_advanced_clear_trace_log_current)

POST[/diag/advanced/clear/trace-log/all](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-clear-trace-log/post_diag_advanced_clear_trace_log_all)

POST[/diag/advanced/clear/trace-log/all-current](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-clear-trace-log/post_diag_advanced_clear_trace_log_all_current)

POST[/diag/advanced/clear/trace-log/last](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-clear-trace-log/post_diag_advanced_clear_trace_log_last)

#### [diag-advanced-fqdn-dyn-addr-obj](https://sonicos-api.sonicwall.com/\#/diag-advanced-fqdn-dyn-addr-obj)      Advanced diag trace log configuration API.

GET[/diag/advanced/fqdn-dynamic-address-object](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-fqdn-dyn-addr-obj/get_diag_advanced_fqdn_dynamic_address_object)

PUT[/diag/advanced/fqdn-dynamic-address-object](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-fqdn-dyn-addr-obj/put_diag_advanced_fqdn_dynamic_address_object)

#### [diag-advanced-cta-report](https://sonicos-api.sonicwall.com/\#/diag-advanced-cta-report)      Advanced capture threat assessment report configuration API.

GET[/diag/advanced/cta-report](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-cta-report/get_diag_advanced_cta_report)

PUT[/diag/advanced/cta-report](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-cta-report/put_diag_advanced_cta_report)

#### [diag-advanced-zero-touch](https://sonicos-api.sonicwall.com/\#/diag-advanced-zero-touch)      Advanced diag Zero Touch configuration API.

GET[/diag/advanced/zero-touch/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-zero-touch/get_diag_advanced_zero_touch_base)

PUT[/diag/advanced/zero-touch/base](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-zero-touch/put_diag_advanced_zero_touch_base)

#### [diag-advanced-zero-touch-restart](https://sonicos-api.sonicwall.com/\#/diag-advanced-zero-touch-restart)      Restart Zero Touch.

POST[/diag/advanced/zero-touch/restart](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-zero-touch-restart/post_diag_advanced_zero_touch_restart)

#### [diag-advanced-zero-touch-enable](https://sonicos-api.sonicwall.com/\#/diag-advanced-zero-touch-enable)      Enable Zero Touch.

POST[/diag/advanced/zero-touch/enable](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-zero-touch-enable/post_diag_advanced_zero_touch_enable)

#### [diag-advanced-zero-touch-disable](https://sonicos-api.sonicwall.com/\#/diag-advanced-zero-touch-disable)      Disable Zero Touch.

POST[/diag/advanced/zero-touch/disable](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-zero-touch-disable/post_diag_advanced_zero_touch_disable)

#### [diag-advanced-analyzer-next-gen](https://sonicos-api.sonicwall.com/\#/diag-advanced-analyzer-next-gen)      Advanced diag Analyzer Next Gen configuration API.

GET[/diag/advanced/analyzer-next-gen](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-analyzer-next-gen/get_diag_advanced_analyzer_next_gen)

PUT[/diag/advanced/analyzer-next-gen](https://sonicos-api.sonicwall.com/#/operations/diag-advanced-analyzer-next-gen/put_diag_advanced_analyzer_next_gen)

#### [debug-cmd](https://sonicos-api.sonicwall.com/\#/debug-cmd)      Debug Configuration

GET[/dbg](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/get_dbg)

PUT[/dbg](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/put_dbg)

GET[/dbg/vpn](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/get_dbg_vpn)

PUT[/dbg/vpn](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/put_dbg_vpn)

GET[/dbg/auth](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/get_dbg_auth)

PUT[/dbg/auth](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/put_dbg_auth)

GET[/dbg/user](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/get_dbg_user)

PUT[/dbg/user](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/put_dbg_user)

GET[/dbg/ha](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/get_dbg_ha)

PUT[/dbg/ha](https://sonicos-api.sonicwall.com/#/operations/debug-cmd/put_dbg_ha)

#### Models

api\_status

tfa

auth

config\_pending

administration\_password

administration\_regenerate\_certificate\_action

administration\_unbind\_totp\_key\_action

administration\_web\_management\_certificate\_use\_self\_signed

administration\_web\_management\_certificate\_name

administration\_language\_override\_chinese

administration\_language\_override\_japanese

administration\_language\_override\_portuguese

administration\_language\_override\_chinese\_traditional

administration\_language\_override\_korean

administration\_language\_override\_english

administration\_gms\_management\_ipsec\_tunnel

administration\_gms\_management\_existing\_tunnel

administration\_gms\_management\_https

administration\_sonicos\_api\_integrity\_protection\_allowed

administration\_sonicos\_api\_integrity\_protection\_enforced

administration\_sonicos\_api\_session\_variant\_allowed

administration\_sonicos\_api\_session\_variant\_enforced

administration\_force\_through\_any

administration\_force\_through\_interface

administration

zone\_wireless\_wifi\_sec\_enforcement\_exception\_service\_name

zone\_wireless\_wifi\_sec\_enforcement\_exception\_service\_protocol

zone\_guest\_services\_custom\_auth\_page\_header\_text

zone\_guest\_services\_custom\_auth\_page\_header\_url

zone\_guest\_services\_custom\_auth\_page\_footer\_text

zone\_guest\_services\_custom\_auth\_page\_footer\_url

zone\_guest\_services\_bypass\_guest\_auth\_all

zone\_guest\_services\_bypass\_guest\_auth\_name

zone\_guest\_services\_bypass\_guest\_auth\_group

zone\_guest\_services\_bypass\_guest\_auth\_mac

zone\_guest\_services\_smtp\_redirect\_name

zone\_guest\_services\_smtp\_redirect\_host

zone\_guest\_services\_deny\_networks\_name

zone\_guest\_services\_deny\_networks\_group

zone\_guest\_services\_pass\_networks\_name

zone\_guest\_services\_pass\_networks\_group

zone

zone\_collection

address\_group\_ipv4

address\_group\_ipv4\_collection

address\_group\_ipv6

address\_group\_ipv6\_collection

address\_object\_ipv4\_host

address\_object\_ipv4\_range

address\_object\_ipv4\_network

address\_object\_ipv4

address\_object\_ipv4\_collection

address\_object\_ipv6\_host

address\_object\_ipv6\_range

address\_object\_ipv6\_network

address\_object\_ipv6

address\_object\_ipv6\_collection

address\_object\_mac

address\_object\_mac\_collection

address\_object\_fqdn

address\_object\_fqdn\_collection

address\_object\_resolve\_action

address\_object\_purge\_action

scheduler\_occurs\_once

scheduler\_occurs\_recurring

scheduler\_occurs\_mixed

scheduler

scheduler\_collection

service\_object\_custom

service\_object\_icmp

service\_object\_igmp

service\_object\_tcp

service\_object\_udp

service\_object\_gre

service\_object\_esp

service\_object\_6over4

service\_object\_ah

service\_object\_icmpv6\_custom

service\_object\_icmpv6

service\_object\_eigrp

service\_object\_ospf

service\_object\_pim

service\_object\_l2tp

service\_object\_ipcomp

service\_object

service\_object\_collection

service\_group

service\_group\_collection

packet\_dissection\_object\_family\_ipv4

packet\_dissection\_object\_family\_ipv6

packet\_dissection\_object\_family\_icmpv4

packet\_dissection\_object\_family\_icmpv6

packet\_dissection\_object\_family\_tcp

packet\_dissection\_object\_family\_udp

packet\_dissection\_object\_data\_type\_numeric

packet\_dissection\_object\_data\_type\_range

packet\_dissection\_object\_data\_type\_hex

packet\_dissection\_object\_data\_type\_range\_hex

packet\_dissection\_object\_data\_type\_ipv4\_address

packet\_dissection\_object\_data\_type\_ipv4\_range

packet\_dissection\_object\_data\_type\_ipv6\_address

packet\_dissection\_object\_data\_type\_ipv6\_range

packet\_dissection\_object\_data\_type\_ipv4\_bitset

packet\_dissection\_object\_data\_type\_tcp\_bitset

packet\_dissection\_object

packet\_dissection\_object\_collection

packet\_dissection\_group

packet\_dissection\_group\_collection

user\_management

user\_status

user\_sessions\_statistics\_reporting

send\_message

kill\_user\_session\_mixed

kill\_user\_session\_mixed\_collection

user\_radius\_base\_radius\_user\_group\_mechanism\_ldap

user\_radius\_base\_radius\_user\_group\_mechanism\_local\_only

user\_radius\_base\_radius\_user\_group\_mechanism\_radius\_attribute

user\_radius\_base

user\_radius\_server\_user\_name\_format\_any

user\_radius\_server\_user\_name\_format\_user\_name

user\_radius\_server\_user\_name\_format\_user\_principle

user\_radius\_server\_user\_name\_format\_down\_level\_logon

user\_radius\_server\_user\_name\_format\_name\_dot\_domain

user\_radius\_server

user\_radius\_server\_collection

user\_radius\_test\_radius\_test\_user\_auth\_method\_chap

user\_radius\_test\_radius\_test\_user\_auth\_method\_mschap

user\_radius\_test\_radius\_test\_user\_auth\_method\_mschapv2

user\_radius\_test

user\_radius\_accounting\_server\_user\_name\_format\_user\_name

user\_radius\_accounting\_server\_user\_name\_format\_user\_principle

user\_radius\_accounting\_server\_user\_name\_format\_down\_level\_logon

user\_radius\_accounting\_server\_user\_name\_format\_name\_dot\_domain

user\_radius\_accounting\_server

user\_radius\_accounting\_server\_collection

user\_radius\_accounting\_base

user\_radius\_acct\_test

user\_tacacs\_base\_tacacs\_user\_group\_mechanism\_local\_only

user\_tacacs\_base\_tacacs\_user\_group\_mechanism\_ldap

user\_tacacs\_base

user\_tacacs\_server

user\_tacacs\_server\_collection

user\_tacacs\_test\_tacacs\_test\_user\_auth\_method\_password\_auth

user\_tacacs\_test\_tacacs\_test\_user\_auth\_method\_chap

user\_tacacs\_test\_tacacs\_test\_user\_auth\_method\_mschap

user\_tacacs\_test

user\_tacacs\_accounting\_base\_tacacs\_accounting\_include\_domain\_users

user\_tacacs\_accounting\_base\_tacacs\_accounting\_include\_local\_users

user\_tacacs\_accounting\_base\_tacacs\_accounting\_include\_domain\_and\_local\_users

user\_tacacs\_accounting\_base

user\_tacacs\_accounting\_server

user\_tacacs\_accounting\_server\_collection

user\_tacacs\_accounting\_test

user\_ldap\_base\_ldap\_check\_deleted\_groups\_method\_read\_from\_servers

user\_ldap\_base\_ldap\_check\_deleted\_groups\_method\_after\_every\_periodic\_checks

user\_ldap\_base\_ldap\_check\_deleted\_groups\_method\_disabled

user\_ldap\_base

user\_ldap\_exclude\_tree

user\_ldap\_exclude\_tree\_collection

user\_ldap\_server\_role\_primary

user\_ldap\_server\_role\_secondary

user\_ldap\_server\_role\_backup

user\_ldap\_server\_bind\_anonymous

user\_ldap\_server\_bind\_distinguished\_name

user\_ldap\_server\_bind\_acct

user\_ldap\_server

user\_ldap\_server\_collection

user\_ldap\_server\_auto\_config\_trees\_directory\_read\_trees\_from\_server\_type\_append\_add

user\_ldap\_server\_auto\_config\_trees\_directory\_read\_trees\_from\_server\_type\_append\_ignore

user\_ldap\_server\_auto\_config\_trees\_directory\_read\_trees\_from\_server\_type\_append

user\_ldap\_server\_auto\_config\_trees\_directory\_read\_trees\_from\_server\_type\_replace\_add

user\_ldap\_server\_auto\_config\_trees\_directory\_read\_trees\_from\_server\_type\_replace\_ignore

user\_ldap\_server\_auto\_config\_trees\_directory\_read\_trees\_from\_server\_type\_replace

user\_ldap\_server\_auto\_config\_trees

user\_ldap\_server\_auto\_config\_trees\_collection

user\_ldap\_mirror\_user\_group\_refresh\_action

user\_ldap\_test\_normal\_ldap\_test\_type\_connectivity\_bind

user\_ldap\_test\_normal\_ldap\_test\_type\_user\_authentication

user\_ldap\_test\_normal

user\_ldap\_test\_basic\_search\_ldap\_test\_type\_ldap\_search\_basic\_use\_user

user\_ldap\_test\_basic\_search\_ldap\_test\_type\_ldap\_search\_basic\_use\_group

user\_ldap\_test\_basic\_search

user\_ldap\_test\_advanced\_search\_ldap\_test\_type\_ldap\_search\_filter\_base\_top\_domain\_tree

user\_ldap\_test\_advanced\_search\_ldap\_test\_type\_ldap\_search\_filter\_base\_root\_directory

user\_ldap\_test\_advanced\_search\_ldap\_test\_type\_ldap\_search\_filter\_base\_other

user\_ldap\_test\_advanced\_search

user\_ldap\_import\_partition\_action

read\_schema\_from\_ldap\_server

user\_guest\_base

user\_guest\_profile\_account\_lifetime\_minutes

user\_guest\_profile\_account\_lifetime\_hours

user\_guest\_profile\_account\_lifetime\_days

user\_guest\_profile\_quota\_cycle\_day

user\_guest\_profile\_quota\_cycle\_week

user\_guest\_profile\_quota\_cycle\_month

user\_guest\_profile\_session\_lifetime\_minutes

user\_guest\_profile\_session\_lifetime\_hours

user\_guest\_profile\_session\_lifetime\_days

user\_guest\_profile\_idle\_timeout\_minutes

user\_guest\_profile\_idle\_timeout\_hours

user\_guest\_profile\_idle\_timeout\_days

user\_guest\_profile

user\_guest\_profile\_collection

user\_guest\_user\_account\_lifetime\_minutes

user\_guest\_user\_account\_lifetime\_hours

user\_guest\_user\_account\_lifetime\_days

user\_guest\_user\_quota\_cycle\_day

user\_guest\_user\_quota\_cycle\_week

user\_guest\_user\_quota\_cycle\_month

user\_guest\_user\_session\_lifetime\_minutes

user\_guest\_user\_session\_lifetime\_hours

user\_guest\_user\_session\_lifetime\_days

user\_guest\_user\_idle\_timeout\_minutes

user\_guest\_user\_idle\_timeout\_hours

user\_guest\_user\_idle\_timeout\_days

user\_guest\_user

user\_guest\_user\_collection

user\_guest\_generate\_guest\_generate\_account\_lifetime\_minutes

user\_guest\_generate\_guest\_generate\_account\_lifetime\_hours

user\_guest\_generate\_guest\_generate\_account\_lifetime\_days

user\_guest\_generate\_guest\_generate\_quota\_cycle\_day

user\_guest\_generate\_guest\_generate\_quota\_cycle\_week

user\_guest\_generate\_guest\_generate\_quota\_cycle\_month

user\_guest\_generate\_guest\_generate\_session\_lifetime\_minutes

user\_guest\_generate\_guest\_generate\_session\_lifetime\_hours

user\_guest\_generate\_guest\_generate\_session\_lifetime\_days

user\_guest\_generate\_guest\_generate\_idle\_timeout\_minutes

user\_guest\_generate\_guest\_generate\_idle\_timeout\_hours

user\_guest\_generate\_guest\_generate\_idle\_timeout\_days

user\_guest\_generate

export\_user\_guest

user\_local\_base\_local\_domain\_name\_display\_format\_name\_at\_domain

user\_local\_base\_local\_domain\_name\_display\_format\_domain\_backslash\_name

user\_local\_base\_local\_domain\_name\_display\_format\_name\_dot\_domain

user\_local\_base\_local\_domain\_name\_display\_format\_automatic

user\_local\_base

user\_local\_group\_memberships\_by\_ldap\_location\_at

user\_local\_group\_memberships\_by\_ldap\_location\_under\_or\_at

user\_local\_group\_one\_time\_password\_otp

user\_local\_group\_one\_time\_password\_totp

user\_local\_group\_vpn\_client\_access\_name

user\_local\_group\_vpn\_client\_access\_group

user\_local\_group\_bookmark\_service\_rdp\_automatic\_login\_ssl\_vpn

user\_local\_group\_bookmark\_service\_rdp\_automatic\_login\_custom

user\_local\_group

user\_local\_group\_collection

user\_local\_user\_one\_time\_password\_otp

user\_local\_user\_one\_time\_password\_totp

user\_local\_user\_account\_lifetime\_minutes

user\_local\_user\_account\_lifetime\_hours

user\_local\_user\_account\_lifetime\_days

user\_local\_user\_account\_lifetime\_expired

user\_local\_user\_quota\_cycle\_day

user\_local\_user\_quota\_cycle\_week

user\_local\_user\_quota\_cycle\_month

user\_local\_user\_session\_lifetime\_minutes

user\_local\_user\_session\_lifetime\_hours

user\_local\_user\_session\_lifetime\_days

user\_local\_user\_guest\_idle\_timeout\_minutes

user\_local\_user\_guest\_idle\_timeout\_hours

user\_local\_user\_guest\_idle\_timeout\_days

user\_local\_user\_vpn\_client\_access\_name

user\_local\_user\_vpn\_client\_access\_group

user\_local\_user\_bookmark\_service\_rdp\_automatic\_login\_ssl\_vpn

user\_local\_user\_bookmark\_service\_rdp\_automatic\_login\_custom

user\_local\_user

user\_local\_user\_collection

user\_local\_unbind\_totp\_key\_action

user\_sso\_agent

user\_sso\_agent\_collection

user\_sso\_base\_sso\_method\_browser\_ntlm\_before\_sso\_agent

user\_sso\_base\_sso\_method\_browser\_ntlm\_after\_sso\_agent\_failed

user\_sso\_base\_sso\_method\_browser\_ntlm\_enabled

user\_sso\_base\_sso\_including\_for\_access\_rules\_all

user\_sso\_base\_sso\_including\_for\_access\_rules\_selected

user\_sso\_base\_sso\_probe\_netapi\_over\_netbios

user\_sso\_base\_sso\_probe\_netapi\_over\_tcp

user\_sso\_base\_sso\_user\_group\_mechanism\_ldap

user\_sso\_base\_sso\_user\_group\_mechanism\_local\_only

user\_sso\_base\_sso\_poll\_users\_windows\_agent

user\_sso\_base\_sso\_poll\_users\_windows\_re\_authentication\_ntlm

user\_sso\_base\_sso\_poll\_users\_windows\_bypass\_re\_authentication

user\_sso\_base\_sso\_poll\_users\_linux\_agent

user\_sso\_base\_sso\_poll\_users\_linux\_re\_authentication\_ntlm

user\_sso\_base\_sso\_poll\_users\_linux\_bypass\_re\_authentication

user\_sso\_base\_sso\_poll\_users\_macintosh\_agent

user\_sso\_base\_sso\_poll\_users\_macintosh\_re\_authentication\_ntlm

user\_sso\_base\_sso\_poll\_users\_macintosh\_bypass\_re\_authentication

user\_sso\_base\_sso\_user\_domain\_name\_received

user\_sso\_base\_sso\_user\_domain\_name\_consistent

user\_sso\_base\_sso\_ignore\_addr\_none

user\_sso\_base\_sso\_ignore\_addr\_name

user\_sso\_base\_sso\_ignore\_addr\_group

user\_sso\_base\_sso\_include\_addr\_all

user\_sso\_base\_sso\_include\_addr\_name

user\_sso\_base\_sso\_include\_addr\_group

user\_sso\_base\_sso\_authentication\_domain\_custom

user\_sso\_base\_sso\_authentication\_domain\_inherit\_from\_ldap

user\_sso\_base\_sso\_redirect\_browser\_ip\_address

user\_sso\_base\_sso\_redirect\_browser\_domain\_name\_reverse\_dns\_look\_up

user\_sso\_base\_sso\_redirect\_browser\_domain\_name\_configured

user\_sso\_base\_sso\_redirect\_browser\_domain\_name

user\_sso\_base\_sso\_redirect\_browser\_certificate\_name

user\_sso\_base

user\_sso\_radius\_accounting\_client\_user\_name\_format\_user\_name

user\_sso\_radius\_accounting\_client\_user\_name\_format\_down\_level\_logon

user\_sso\_radius\_accounting\_client\_user\_name\_format\_canonical

user\_sso\_radius\_accounting\_client\_user\_name\_format\_user\_principle

user\_sso\_radius\_accounting\_client\_user\_name\_format\_sonicwall\_aventail

user\_sso\_radius\_accounting\_client\_user\_name\_format\_custom

user\_sso\_radius\_accounting\_client\_missing\_domain\_local\_user

user\_sso\_radius\_accounting\_client\_missing\_domain\_ldap\_look\_up

user\_sso\_radius\_accounting\_client\_log\_user\_out\_if\_no\_interim\_enable

user\_sso\_radius\_accounting\_client\_log\_user\_out\_if\_no\_interim\_auto

user\_sso\_radius\_accounting\_client\_proxy\_forward\_type\_try\_next\_on\_timeout

user\_sso\_radius\_accounting\_client\_proxy\_forward\_type\_forward\_to\_all

user\_sso\_radius\_accounting\_client

user\_sso\_radius\_accounting\_client\_collection

user\_sso\_radius\_user\_name\_exclusion

user\_sso\_radius\_user\_name\_exclusion\_collection

user\_sso\_security\_service\_bypass\_address\_name

user\_sso\_security\_service\_bypass\_address\_group

user\_sso\_security\_service\_bypass\_service\_name

user\_sso\_security\_service\_bypass\_service\_group

user\_sso\_security\_service\_bypass\_service\_protocol

user\_sso\_security\_service\_bypass\_service\_built\_in

user\_sso\_security\_service\_bypass

user\_sso\_security\_service\_bypass\_collection

user\_sso\_terminal\_services\_agent

user\_sso\_terminal\_services\_agent\_collection

user\_sso\_windows\_service\_user\_name

user\_sso\_windows\_service\_user\_name\_collection

user\_sso\_enforce\_on\_zone

user\_sso\_enforce\_on\_zone\_collection

user\_sso\_global\_statistic\_reporting

user\_sso\_status\_reporting

user\_sso\_test\_sso\_test\_agent\_mechanism\_from\_domain\_controller

user\_sso\_test\_sso\_test\_agent\_mechanism\_from\_novell\_server

user\_sso\_test\_sso\_test\_agent\_mechanism\_from\_exchange\_server

user\_sso\_test\_sso\_test\_agent\_mechanism\_from\_terminal\_server

user\_sso\_test\_sso\_test\_agent\_mechanism\_from\_3rd\_party\_api

user\_sso\_test\_sso\_test\_agent\_mechanism\_from\_other\_mechanisms

user\_sso\_test\_sso\_test\_agent\_mechanism\_via\_netapi\_or\_wmi

user\_sso\_test\_sso\_test\_agent\_mechanism\_allow\_both

user\_sso\_test\_sso\_test\_agent

user\_sso\_test\_sso\_test\_terminal\_services\_agent

user\_sso\_test

user\_sso\_3rd\_party\_api\_base\_sso\_third\_party\_api\_https\_port\_management

user\_sso\_3rd\_party\_api\_base\_sso\_third\_party\_api\_https\_port\_number

user\_sso\_3rd\_party\_api\_base

user\_sso\_3rd\_party\_api\_client\_security\_level\_low

user\_sso\_3rd\_party\_api\_client\_security\_level\_medium

user\_sso\_3rd\_party\_api\_client\_security\_level\_high

user\_sso\_3rd\_party\_api\_client

user\_sso\_3rd\_party\_api\_client\_collection

user\_sso\_capture\_client\_base

user\_sso\_consistent\_domain\_name

user\_sso\_consistent\_domain\_name\_collection

user\_partitioning\_base

user\_partitioning\_partitions

user\_partitioning\_partitions\_collection

user\_partitioning\_policies

user\_partitioning\_policies\_collection

user\_partitioning\_auto\_assign\_action

user\_auth\_base\_auth\_one\_time\_password\_format\_characters

user\_auth\_base\_auth\_one\_time\_password\_format\_mixed

user\_auth\_base\_auth\_one\_time\_password\_format\_numbers

user\_auth\_base\_auth\_one\_time\_password\_email\_format\_plain\_text

user\_auth\_base\_auth\_one\_time\_password\_email\_format\_html

user\_auth\_base\_auth\_browser\_redirect\_via\_interface\_ip

user\_auth\_base\_auth\_browser\_redirect\_via\_reverse\_dns

user\_auth\_base\_auth\_browser\_redirect\_via\_host\_name

user\_auth\_base\_auth\_browser\_redirect\_via\_name\_from\_certificate

user\_auth\_base\_auth\_redirect\_to\_login\_page\_via\_info\_page

user\_auth\_base\_auth\_redirect\_to\_login\_page\_directly

user\_auth\_base\_auth\_prevent\_inactivity\_logout\_service\_name

user\_auth\_base\_auth\_prevent\_inactivity\_logout\_service\_group

user\_auth\_base\_auth\_prevent\_inactivity\_logout\_service\_protocol

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_authentication\_keep\_alive

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_authentication\_terminate\_now

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_authentication\_terminate\_after

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_authentication\_terminate

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_other\_keep\_alive

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_other\_terminate\_now

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_other\_terminate\_after

user\_auth\_base\_auth\_user\_connections\_logout\_inactivity\_other\_terminate

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_authentication\_keep\_alive

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_authentication\_terminate\_now

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_authentication\_terminate\_after

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_authentication\_terminate

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_other\_keep\_alive

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_other\_terminate\_now

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_other\_terminate\_after

user\_auth\_base\_auth\_user\_connections\_logout\_reported\_other\_terminate

user\_auth\_base\_auth\_acceptable\_use\_policy\_aup\_on\_zones\_trusted

user\_auth\_base\_auth\_acceptable\_use\_policy\_aup\_on\_zones\_wan

user\_auth\_base\_auth\_acceptable\_use\_policy\_aup\_on\_zones\_public

user\_auth\_base\_auth\_acceptable\_use\_policy\_aup\_on\_zones\_wireless

user\_auth\_base\_auth\_acceptable\_use\_policy\_aup\_on\_zones\_vpn

user\_auth\_base

user\_auth\_methods\_auth\_sso\_method\_browser\_ntlm\_before\_sso\_agent

user\_auth\_methods\_auth\_sso\_method\_browser\_ntlm\_after\_sso\_agent\_failed

user\_auth\_methods\_auth\_sso\_method\_browser\_ntlm\_enabled

user\_auth\_methods\_auth\_partition\_sso\_method\_browser\_ntlm\_before\_sso\_agent

user\_auth\_methods\_auth\_partition\_sso\_method\_browser\_ntlm\_after\_sso\_agent\_failed

user\_auth\_methods\_auth\_partition\_sso\_method\_browser\_ntlm\_enabled

user\_auth\_methods

user\_auth\_bypass

user\_auth\_bypass\_collection

user\_authentication\_bypass\_track\_traffic\_action

interface\_ipv4\_ip\_assignment\_mode\_static

interface\_ipv4\_ip\_assignment\_mode\_dhcp

interface\_ipv4\_ip\_assignment\_mode\_transparent\_transparent\_range\_name

interface\_ipv4\_ip\_assignment\_mode\_transparent\_transparent\_range\_group

interface\_ipv4\_ip\_assignment\_mode\_transparent

interface\_ipv4\_ip\_assignment\_mode\_l2bridge

interface\_ipv4\_ip\_assignment\_mode\_wire\_mode

interface\_ipv4\_ip\_assignment\_mode\_tap\_mode

interface\_ipv4\_ip\_assignment\_mode\_l2tp\_schedule\_always\_on

interface\_ipv4\_ip\_assignment\_mode\_l2tp\_schedule\_name

interface\_ipv4\_ip\_assignment\_mode\_l2tp\_schedule\_days

interface\_ipv4\_ip\_assignment\_mode\_l2tp

interface\_ipv4\_ip\_assignment\_mode\_pptp\_schedule\_always\_on

interface\_ipv4\_ip\_assignment\_mode\_pptp\_schedule\_name

interface\_ipv4\_ip\_assignment\_mode\_pptp\_schedule\_days

interface\_ipv4\_ip\_assignment\_mode\_pptp

interface\_ipv4\_ip\_assignment\_mode\_unnumbered

interface\_ipv4\_ip\_assignment\_mode\_pppoe\_schedule\_always\_on

interface\_ipv4\_ip\_assignment\_mode\_pppoe\_schedule\_name

interface\_ipv4\_ip\_assignment\_mode\_pppoe\_schedule\_days

interface\_ipv4\_ip\_assignment\_mode\_pppoe

interface\_ipv4\_ip\_assignment\_mode\_portshield

interface\_ipv4\_mac\_default

interface\_ipv4\_mac\_override

interface\_ipv4\_link\_speed\_auto\_negotiate

interface\_ipv4\_link\_speed\_half

interface\_ipv4\_link\_speed\_full

interface\_ipv4\_sonicpoint\_reserve\_address\_dynamic

interface\_ipv4\_sonicpoint\_reserve\_address\_manual

interface\_ipv4\_port\_aggregation

interface\_ipv4\_port\_redundancy

interface\_ipv4\_port\_redundancy\_aggregation

interface\_ipv4\_routed\_mode\_any

interface\_ipv4\_routed\_mode\_interface

interface\_ipv4

interface\_ipv4\_collection

interface\_vlan\_ipv4\_ip\_assignment\_mode\_static

interface\_vlan\_ipv4\_ip\_assignment\_mode\_dhcp

interface\_vlan\_ipv4\_ip\_assignment\_mode\_transparent\_transparent\_range\_name

interface\_vlan\_ipv4\_ip\_assignment\_mode\_transparent\_transparent\_range\_group

interface\_vlan\_ipv4\_ip\_assignment\_mode\_transparent

interface\_vlan\_ipv4\_ip\_assignment\_mode\_l2bridge

interface\_vlan\_ipv4\_ip\_assignment\_mode\_wire\_mode

interface\_vlan\_ipv4\_ip\_assignment\_mode\_tap\_mode

interface\_vlan\_ipv4\_ip\_assignment\_mode\_l2tp\_schedule\_always\_on

interface\_vlan\_ipv4\_ip\_assignment\_mode\_l2tp\_schedule\_name

interface\_vlan\_ipv4\_ip\_assignment\_mode\_l2tp\_schedule\_days

interface\_vlan\_ipv4\_ip\_assignment\_mode\_l2tp

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pptp\_schedule\_always\_on

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pptp\_schedule\_name

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pptp\_schedule\_days

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pptp

interface\_vlan\_ipv4\_ip\_assignment\_mode\_unnumbered

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pppoe\_schedule\_always\_on

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pppoe\_schedule\_name

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pppoe\_schedule\_days

interface\_vlan\_ipv4\_ip\_assignment\_mode\_pppoe

interface\_vlan\_ipv4\_ip\_assignment\_mode\_portshield

interface\_vlan\_ipv4\_mac\_default

interface\_vlan\_ipv4\_mac\_override

interface\_vlan\_ipv4\_link\_speed\_auto\_negotiate

interface\_vlan\_ipv4\_link\_speed\_half

interface\_vlan\_ipv4\_link\_speed\_full

interface\_vlan\_ipv4\_sonicpoint\_reserve\_address\_dynamic

interface\_vlan\_ipv4\_sonicpoint\_reserve\_address\_manual

interface\_vlan\_ipv4\_port\_aggregation

interface\_vlan\_ipv4\_port\_redundancy

interface\_vlan\_ipv4\_port\_redundancy\_aggregation

interface\_vlan\_ipv4\_routed\_mode\_any

interface\_vlan\_ipv4\_routed\_mode\_interface

interface\_vlan\_ipv4

interface\_vlan\_ipv4\_collection

tunnel\_interface\_4to6\_type\_dslite\_local\_dynamic

tunnel\_interface\_4to6\_type\_dslite\_local\_ipv6

tunnel\_interface\_4to6\_type\_dslite\_remote\_dynamic

tunnel\_interface\_4to6\_type\_dslite\_remote\_ipv6

tunnel\_interface\_4to6\_type\_dslite\_remote\_fqdn

tunnel\_interface\_4to6\_type\_dslite

tunnel\_interface\_4to6\_type\_gre4to6\_local\_dynamic

tunnel\_interface\_4to6\_type\_gre4to6\_local\_ipv6

tunnel\_interface\_4to6\_type\_gre4to6

tunnel\_interface\_4to6

tunnel\_interface\_4to6\_collection

tunnel\_interface\_vpn

tunnel\_interface\_vpn\_collection

interfaces\_display\_traffic

interface\_shutdown

interface\_renew\_ipv4\_action

interface\_renew\_ipv6\_action

interface\_release\_ipv4\_action

interface\_release\_ipv6\_action

interface\_connect\_action

interface\_disconnect\_action

interface\_ipv6\_prefixes\_ipv6\_ip\_assignment\_mode\_static

interface\_ipv6\_prefixes\_ipv6\_ip\_assignment\_mode\_pppoe6

interface\_ipv6\_prefixes

interface\_ipv6\_prefixes\_collection

interface\_ipv6\_extra\_ip\_ipv6\_ip\_assignment\_mode\_static\_extra\_ip\_type\_static

interface\_ipv6\_extra\_ip\_ipv6\_ip\_assignment\_mode\_static\_extra\_ip\_type\_prefix\_delegation

interface\_ipv6\_extra\_ip\_ipv6\_ip\_assignment\_mode\_static\_extra\_ip\_type\_6rd

interface\_ipv6\_extra\_ip

interface\_ipv6\_extra\_ip\_collection

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_auto

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_l2bridge

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_static

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_dhcpv6

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_pppoe6\_schedule\_always\_on

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_pppoe6\_schedule\_name

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_pppoe6\_schedule\_days

interface\_ipv6\_base\_ipv6\_ip\_assignment\_mode\_pppoe6

interface\_ipv6\_base

interface\_ipv6\_base\_collection

tunnel\_interface\_ipv6\_type\_manual\_remote\_ipv6\_network\_name

tunnel\_interface\_ipv6\_type\_manual\_remote\_ipv6\_network\_group

tunnel\_interface\_ipv6\_type\_manual\_bound\_to\_any

tunnel\_interface\_ipv6\_type\_manual\_bound\_to\_interface

tunnel\_interface\_ipv6\_type\_manual

tunnel\_interface\_ipv6\_type\_gre\_remote\_ipv6\_network\_name

tunnel\_interface\_ipv6\_type\_gre\_remote\_ipv6\_network\_group

tunnel\_interface\_ipv6\_type\_gre\_bound\_to\_any

tunnel\_interface\_ipv6\_type\_gre\_bound\_to\_interface

tunnel\_interface\_ipv6\_type\_gre

tunnel\_interface\_ipv6\_type\_6to4\_bound\_to\_any

tunnel\_interface\_ipv6\_type\_6to4\_bound\_to\_interface

tunnel\_interface\_ipv6\_type\_6to4

tunnel\_interface\_ipv6\_type\_6rd

tunnel\_interface\_ipv6\_type\_isatap

tunnel\_interface\_ipv6

tunnel\_interface\_ipv6\_collection

bandwidth\_object\_guaranteed\_kbps

bandwidth\_object\_guaranteed\_mbps

bandwidth\_object\_maximum\_kbps

bandwidth\_object\_maximum\_mbps

bandwidth\_object\_per\_ip\_management\_kbps

bandwidth\_object\_per\_ip\_management\_mbps

bandwidth\_object

bandwidth\_object\_collection

dynamic\_external\_object

dynamic\_external\_object\_collection

dynamic\_external\_object\_download\_action

email\_object

email\_object\_collection

match\_object\_ips\_category\_name

match\_object\_ips\_category\_id

match\_object\_ips\_policy\_category\_name

match\_object\_ips\_policy\_category\_id

match\_object\_ips\_policy\_signature\_name

match\_object\_ips\_policy\_signature\_id

match\_object\_category\_name

match\_object\_category\_id

match\_object\_application\_category\_name

match\_object\_application\_category\_id

match\_object\_application\_app\_name

match\_object\_application\_app\_id

match\_object\_signature\_category\_name

match\_object\_signature\_category\_id

match\_object\_signature\_app\_name

match\_object\_signature\_app\_id

match\_object\_signature\_sig\_name

match\_object\_signature\_sig\_id

match\_object

match\_object\_collection

action\_object

action\_object\_collection

action\_object\_default\_reporting

action\_object\_default\_bandwidth\_management\_reporting

app\_rule

app\_rule\_policy\_type\_smtp\_client

app\_rule\_policy\_type\_http

app\_rule\_policy\_type\_ftp

app\_rule\_policy\_type\_pop3

app\_rule\_policy\_type\_custom

app\_rule\_policy\_type\_ips

app\_rule\_policy\_type\_app\_control

app\_rule\_policy\_type\_cfs

app\_rule\_policy\_source\_address\_any

app\_rule\_policy\_source\_address\_name

app\_rule\_policy\_source\_address\_group

app\_rule\_policy\_source\_service\_any

app\_rule\_policy\_source\_service\_name

app\_rule\_policy\_source\_service\_group

app\_rule\_policy\_destination\_address\_any

app\_rule\_policy\_destination\_address\_name

app\_rule\_policy\_destination\_address\_group

app\_rule\_policy\_destination\_service\_any

app\_rule\_policy\_destination\_service\_name

app\_rule\_policy\_destination\_service\_group

app\_rule\_policy\_address\_any

app\_rule\_policy\_address\_name

app\_rule\_policy\_address\_group

app\_rule\_policy\_exclusion\_address\_any

app\_rule\_policy\_exclusion\_address\_name

app\_rule\_policy\_exclusion\_address\_group

app\_rule\_policy\_exclusion\_service\_name

app\_rule\_policy\_exclusion\_service\_group

app\_rule\_policy\_users\_included\_all

app\_rule\_policy\_users\_included\_guests

app\_rule\_policy\_users\_included\_administrator

app\_rule\_policy\_users\_included\_name

app\_rule\_policy\_users\_included\_group

app\_rule\_policy\_users\_excluded\_all

app\_rule\_policy\_users\_excluded\_guests

app\_rule\_policy\_users\_excluded\_administrator

app\_rule\_policy\_users\_excluded\_name

app\_rule\_policy\_users\_excluded\_group

app\_rule\_policy\_schedule\_always\_on

app\_rule\_policy\_schedule\_name

app\_rule\_policy\_schedule\_days

app\_rule\_policy\_log\_redundancy\_global

app\_rule\_policy\_log\_redundancy\_interval

app\_rule\_policy\_direction\_basic

app\_rule\_policy\_direction\_advanced\_from\_any

app\_rule\_policy\_direction\_advanced\_from\_zone

app\_rule\_policy\_direction\_advanced\_to\_any

app\_rule\_policy\_direction\_advanced\_to\_zone

app\_rule\_policy\_direction\_advanced

app\_rule\_policy\_zone\_any

app\_rule\_policy\_zone\_name

app\_rule\_policy

app\_rule\_policy\_collection

app\_control

app\_control\_category\_log\_enable

app\_control\_category\_log\_global

app\_control\_category\_included\_users\_all

app\_control\_category\_included\_users\_guests

app\_control\_category\_included\_users\_administrator

app\_control\_category\_included\_users\_name

app\_control\_category\_included\_users\_group

app\_control\_category\_included\_ip\_all

app\_control\_category\_included\_ip\_name

app\_control\_category\_included\_ip\_group

app\_control\_category\_excluded\_users\_guests

app\_control\_category\_excluded\_users\_administrator

app\_control\_category\_excluded\_users\_name

app\_control\_category\_excluded\_users\_group

app\_control\_category\_excluded\_ip\_name

app\_control\_category\_excluded\_ip\_group

app\_control\_category\_schedule\_always\_on

app\_control\_category\_schedule\_name

app\_control\_category\_schedule\_days

app\_control\_category

app\_control\_category\_collection

app\_control\_application\_block\_enable

app\_control\_application\_block\_category

app\_control\_application\_log\_enable

app\_control\_application\_log\_category

app\_control\_application\_included\_users\_category

app\_control\_application\_included\_users\_all

app\_control\_application\_included\_users\_guests

app\_control\_application\_included\_users\_administrator

app\_control\_application\_included\_users\_name

app\_control\_application\_included\_users\_group

app\_control\_application\_included\_ip\_category

app\_control\_application\_included\_ip\_all

app\_control\_application\_included\_ip\_name

app\_control\_application\_included\_ip\_group

app\_control\_application\_excluded\_users\_category

app\_control\_application\_excluded\_users\_guests

app\_control\_application\_excluded\_users\_administrator

app\_control\_application\_excluded\_users\_name

app\_control\_application\_excluded\_users\_group

app\_control\_application\_excluded\_ip\_category

app\_control\_application\_excluded\_ip\_name

app\_control\_application\_excluded\_ip\_group

app\_control\_application\_schedule\_category

app\_control\_application\_schedule\_always\_on

app\_control\_application\_schedule\_name

app\_control\_application\_schedule\_days

app\_control\_application

app\_control\_application\_collection

app\_control\_signature\_block\_enable

app\_control\_signature\_block\_app

app\_control\_signature\_log\_enable

app\_control\_signature\_log\_app

app\_control\_signature\_included\_users\_app

app\_control\_signature\_included\_users\_all

app\_control\_signature\_included\_users\_guests

app\_control\_signature\_included\_users\_administrator

app\_control\_signature\_included\_users\_name

app\_control\_signature\_included\_users\_group

app\_control\_signature\_included\_ip\_app

app\_control\_signature\_included\_ip\_all

app\_control\_signature\_included\_ip\_name

app\_control\_signature\_included\_ip\_group

app\_control\_signature\_excluded\_users\_app

app\_control\_signature\_excluded\_users\_guests

app\_control\_signature\_excluded\_users\_administrator

app\_control\_signature\_excluded\_users\_name

app\_control\_signature\_excluded\_users\_group

app\_control\_signature\_excluded\_ip\_app

app\_control\_signature\_excluded\_ip\_name

app\_control\_signature\_excluded\_ip\_group

app\_control\_signature\_schedule\_app

app\_control\_signature\_schedule\_always\_on

app\_control\_signature\_schedule\_name

app\_control\_signature\_schedule\_days

app\_control\_signature

app\_control\_signature\_collection

app\_control\_exclusion\_list\_exclusion\_list\_ips

app\_control\_exclusion\_list\_exclusion\_list\_object\_name

app\_control\_exclusion\_list\_exclusion\_list\_object\_group

app\_control\_exclusion\_list\_exclusion\_list\_object

app\_control\_exclusion\_list

app\_control\_update\_signatures\_action

app\_control\_reset\_action

app\_control\_applications\_list\_block\_enable

app\_control\_applications\_list\_block\_category

app\_control\_applications\_list\_log\_enable

app\_control\_applications\_list\_log\_category

app\_control\_applications\_list\_included\_users\_category

app\_control\_applications\_list\_included\_users\_all

app\_control\_applications\_list\_included\_users\_guests

app\_control\_applications\_list\_included\_users\_administrator

app\_control\_applications\_list\_included\_users\_name

app\_control\_applications\_list\_included\_users\_group

app\_control\_applications\_list\_included\_ip\_category

app\_control\_applications\_list\_included\_ip\_all

app\_control\_applications\_list\_included\_ip\_name

app\_control\_applications\_list\_included\_ip\_group

app\_control\_applications\_list\_excluded\_users\_category

app\_control\_applications\_list\_excluded\_users\_guests

app\_control\_applications\_list\_excluded\_users\_administrator

app\_control\_applications\_list\_excluded\_users\_name

app\_control\_applications\_list\_excluded\_users\_group

app\_control\_applications\_list\_excluded\_ip\_category

app\_control\_applications\_list\_excluded\_ip\_name

app\_control\_applications\_list\_excluded\_ip\_group

app\_control\_applications\_list\_schedule\_category

app\_control\_applications\_list\_schedule\_always\_on

app\_control\_applications\_list\_schedule\_name

app\_control\_applications\_list\_schedule\_days

app\_control\_applications\_list

app\_control\_applications\_list\_collection

app\_control\_signatures\_list\_block\_enable

app\_control\_signatures\_list\_block\_app

app\_control\_signatures\_list\_log\_enable

app\_control\_signatures\_list\_log\_app

app\_control\_signatures\_list\_included\_users\_app

app\_control\_signatures\_list\_included\_users\_all

app\_control\_signatures\_list\_included\_users\_guests

app\_control\_signatures\_list\_included\_users\_administrator

app\_control\_signatures\_list\_included\_users\_name

app\_control\_signatures\_list\_included\_users\_group

app\_control\_signatures\_list\_included\_ip\_app

app\_control\_signatures\_list\_included\_ip\_all

app\_control\_signatures\_list\_included\_ip\_name

app\_control\_signatures\_list\_included\_ip\_group

app\_control\_signatures\_list\_excluded\_users\_app

app\_control\_signatures\_list\_excluded\_users\_guests

app\_control\_signatures\_list\_excluded\_users\_administrator

app\_control\_signatures\_list\_excluded\_users\_name

app\_control\_signatures\_list\_excluded\_users\_group

app\_control\_signatures\_list\_excluded\_ip\_app

app\_control\_signatures\_list\_excluded\_ip\_name

app\_control\_signatures\_list\_excluded\_ip\_group

app\_control\_signatures\_list\_schedule\_app

app\_control\_signatures\_list\_schedule\_always\_on

app\_control\_signatures\_list\_schedule\_name

app\_control\_signatures\_list\_schedule\_days

app\_control\_signatures\_list

app\_control\_signatures\_list\_collection

content\_filter\_uri\_list\_object

content\_filter\_uri\_list\_object\_collection

content\_filter\_uri\_list\_group

content\_filter\_uri\_list\_group\_collection

content\_filter\_action\_block\_page\_custom

content\_filter\_action\_block\_page\_default

content\_filter\_action\_passphrase\_page\_custom

content\_filter\_action\_passphrase\_page\_default

content\_filter\_action\_confirm\_page\_custom

content\_filter\_action\_confirm\_page\_default

content\_filter\_action

content\_filter\_action\_collection

content\_filter\_profile\_consent\_mandatory\_address\_any

content\_filter\_profile\_consent\_mandatory\_address\_name

content\_filter\_profile\_consent\_mandatory\_address\_group

content\_filter\_profile\_consent\_mandatory\_address\_host

content\_filter\_profile\_consent\_mandatory\_address\_range

content\_filter\_profile\_consent\_mandatory\_address\_network

content\_filter\_profile\_consent\_mandatory\_address\_ipv6\_host

content\_filter\_profile\_consent\_mandatory\_address\_ipv6\_range

content\_filter\_profile\_consent\_mandatory\_address\_ipv6\_network

content\_filter\_profile\_consent\_mandatory\_address\_ipv6

content\_filter\_profile

content\_filter\_profile\_collection

content\_filter\_uri\_list\_object\_import\_uris

content\_filter\_uri\_list\_object\_import\_keywords

content\_filter\_uri\_list\_object\_export\_uris

content\_filter\_uri\_list\_object\_export\_keywords

content\_filter\_cfs\_exclude\_address\_name

content\_filter\_cfs\_exclude\_address\_group

content\_filter\_cfs

content\_filter\_cfs\_policy\_source\_address\_included\_any

content\_filter\_cfs\_policy\_source\_address\_included\_name

content\_filter\_cfs\_policy\_source\_address\_included\_group

content\_filter\_cfs\_policy\_source\_address\_excluded\_none

content\_filter\_cfs\_policy\_source\_address\_excluded\_name

content\_filter\_cfs\_policy\_source\_address\_excluded\_group

content\_filter\_cfs\_policy\_user\_included\_all

content\_filter\_cfs\_policy\_user\_included\_guests

content\_filter\_cfs\_policy\_user\_included\_administrator

content\_filter\_cfs\_policy\_user\_included\_name

content\_filter\_cfs\_policy\_user\_included\_group

content\_filter\_cfs\_policy\_user\_excluded\_none

content\_filter\_cfs\_policy\_user\_excluded\_guests

content\_filter\_cfs\_policy\_user\_excluded\_administrator

content\_filter\_cfs\_policy\_user\_excluded\_name

content\_filter\_cfs\_policy\_user\_excluded\_group

content\_filter\_cfs\_policy\_schedule\_always\_on

content\_filter\_cfs\_policy\_schedule\_name

content\_filter\_cfs\_policy\_schedule\_object

content\_filter\_cfs\_policy

content\_filter\_cfs\_policy\_collection

content\_filter\_cfs\_custom\_category

content\_filter\_cfs\_custom\_category\_category\_entry

content\_filter\_cfs\_custom\_category\_category\_entry\_collection

content\_filter\_cfs\_custom\_category\_export

content\_filter\_cfs\_custom\_category\_import

cfs\_get\_latest\_local\_server\_info\_action

content\_filter\_settings\_cfs\_exclude\_address\_name

content\_filter\_settings\_cfs\_exclude\_address\_group

content\_filter\_settings\_websense\_exclude\_address\_name

content\_filter\_settings\_websense\_exclude\_address\_group

content\_filter\_settings\_websense\_blocking\_page\_custom

content\_filter\_settings\_websense\_blocking\_page\_default

content\_filter\_settings

content\_filter\_websense\_exclude\_address\_name

content\_filter\_websense\_exclude\_address\_group

content\_filter\_websense\_blocking\_page\_custom

content\_filter\_websense\_blocking\_page\_default

content\_filter\_websense

endpoint\_security\_profile

endpoint\_security\_profile\_collection

endpoint\_security\_policy\_source\_address\_included\_any

endpoint\_security\_policy\_source\_address\_included\_name

endpoint\_security\_policy\_source\_address\_included\_group

endpoint\_security\_policy\_source\_address\_excluded\_none

endpoint\_security\_policy\_source\_address\_excluded\_name

endpoint\_security\_policy\_source\_address\_excluded\_group

endpoint\_security\_policy

endpoint\_security\_policy\_collection

endpoint\_security\_settings

custom\_match\_type\_smtp\_client

custom\_match\_type\_http

custom\_match\_type\_ftp

custom\_match\_type\_pop3

custom\_match\_type\_custom

custom\_match\_type\_ips

custom\_match\_type\_app\_control

custom\_match\_direction\_basic

custom\_match\_direction\_advanced\_from\_any

custom\_match\_direction\_advanced\_from\_zone

custom\_match\_direction\_advanced\_to\_any

custom\_match\_direction\_advanced\_to\_zone

custom\_match\_direction\_advanced

custom\_match

custom\_match\_collection

custom\_match\_group

custom\_match\_group\_collection

custom\_match\_clone

custom\_match\_clone\_collection

custom\_match\_group\_clone

custom\_match\_group\_clone\_collection

reporting\_profiles\_color\_rgb

reporting\_profiles\_color\_hex

reporting\_profiles\_color\_black

reporting\_profiles\_color\_red

reporting\_profiles\_color\_yellow

reporting\_profiles\_color\_blue

reporting\_profiles\_color\_green

reporting\_profiles\_color\_orange

reporting\_profiles\_color\_purple

reporting\_profiles

reporting\_profiles\_collection

reporting\_profile\_clone

reporting\_profile\_clone\_collection

dos\_action\_profile

dos\_action\_profile\_collection

dos\_action\_profile\_clone

dos\_action\_profile\_clone\_collection

security\_action\_profiles\_quality\_of\_service\_class\_of\_service\_explicit

security\_action\_profiles\_quality\_of\_service\_class\_of\_service\_map

security\_action\_profiles\_quality\_of\_service\_class\_of\_service\_preserve

security\_action\_profiles\_quality\_of\_service\_dscp\_explicit

security\_action\_profiles\_quality\_of\_service\_dscp\_map

security\_action\_profiles\_quality\_of\_service\_dscp\_preserve

security\_action\_profiles\_threat\_prevent\_profile\_all

security\_action\_profiles\_threat\_prevent\_profile\_group

security\_action\_profiles\_threat\_packet\_monitor\_profile\_all

security\_action\_profiles\_threat\_packet\_monitor\_profile\_group

security\_action\_profiles\_threat\_log\_profile\_all

security\_action\_profiles\_threat\_log\_profile\_group

security\_action\_profiles\_content\_filter\_passphrase\_page\_custom

security\_action\_profiles\_content\_filter\_passphrase\_page\_default

security\_action\_profiles\_content\_filter\_confirm\_page\_custom

security\_action\_profiles\_content\_filter\_confirm\_page\_default

security\_action\_profiles\_content\_filter\_consent\_mandatory\_address\_any

security\_action\_profiles\_content\_filter\_consent\_mandatory\_address\_name

security\_action\_profiles\_content\_filter\_consent\_mandatory\_address\_group

security\_action\_profiles\_reporting\_profile\_default

security\_action\_profiles\_reporting\_profile\_global

security\_action\_profiles\_reporting\_profile\_name

security\_action\_profiles\_user\_actions\_block\_page\_object\_default

security\_action\_profiles\_user\_actions\_block\_page\_object\_global

security\_action\_profiles\_user\_actions\_block\_page\_object\_name

security\_action\_profiles\_packet\_dissection\_filter\_name

security\_action\_profiles\_packet\_dissection\_filter\_group

security\_action\_profiles

security\_action\_profiles\_collection

security\_action\_profile\_clone

security\_action\_profile\_clone\_collection

website\_object

website\_object\_collection

website\_group

website\_group\_collection

website\_object\_clone

website\_object\_clone\_collection

website\_group\_clone

website\_group\_clone\_collection

country\_group

country\_group\_collection

web\_category\_group

web\_category\_group\_collection

threat\_prevention\_profile

threat\_prevention\_profile\_collection

policies\_setting\_base\_threat\_profile\_for\_zone\_prevent\_profile\_all

policies\_setting\_base\_threat\_profile\_for\_zone\_prevent\_profile\_group

policies\_setting\_base\_threat\_profile\_for\_zone\_packet\_monitor\_profile\_all

policies\_setting\_base\_threat\_profile\_for\_zone\_packet\_monitor\_profile\_group

policies\_setting\_base\_threat\_profile\_for\_zone\_log\_profile\_all

policies\_setting\_base\_threat\_profile\_for\_zone\_log\_profile\_group

policies\_setting\_base

policies\_setting\_enforcement\_action

policies\_setting\_clear\_app\_cache\_action

block\_page

block\_page\_collection

application\_group

application\_group\_collection

security\_policy\_ipv4\_priority\_begin

security\_policy\_ipv4\_priority\_end

security\_policy\_ipv4\_priority\_manual

security\_policy\_ipv4\_source\_address\_any

security\_policy\_ipv4\_source\_address\_name

security\_policy\_ipv4\_source\_address\_group

security\_policy\_ipv4\_source\_port\_any

security\_policy\_ipv4\_source\_port\_name

security\_policy\_ipv4\_source\_port\_group

security\_policy\_ipv4\_destination\_address\_any

security\_policy\_ipv4\_destination\_address\_name

security\_policy\_ipv4\_destination\_address\_group

security\_policy\_ipv4\_service\_any

security\_policy\_ipv4\_service\_name

security\_policy\_ipv4\_service\_group

security\_policy\_ipv4\_users\_all

security\_policy\_ipv4\_users\_guests

security\_policy\_ipv4\_users\_administrator

security\_policy\_ipv4\_users\_name

security\_policy\_ipv4\_users\_group

security\_policy\_ipv4\_application\_any

security\_policy\_ipv4\_application\_group

security\_policy\_ipv4\_web\_category\_any

security\_policy\_ipv4\_web\_category\_group

security\_policy\_ipv4\_url\_list\_any

security\_policy\_ipv4\_url\_list\_name

security\_policy\_ipv4\_url\_list\_group

security\_policy\_ipv4\_custom\_match\_any

security\_policy\_ipv4\_custom\_match\_group

security\_policy\_ipv4\_country\_any

security\_policy\_ipv4\_country\_group

security\_policy\_ipv4\_schedule\_always\_on

security\_policy\_ipv4\_schedule\_name

security\_policy\_ipv4\_schedule\_days

security\_policy\_ipv4

security\_policy\_ipv4\_collection

security\_policy\_ipv6\_priority\_begin

security\_policy\_ipv6\_priority\_end

security\_policy\_ipv6\_priority\_manual

security\_policy\_ipv6\_source\_address\_any

security\_policy\_ipv6\_source\_address\_name

security\_policy\_ipv6\_source\_address\_group

security\_policy\_ipv6\_source\_port\_any

security\_policy\_ipv6\_source\_port\_name

security\_policy\_ipv6\_source\_port\_group

security\_policy\_ipv6\_destination\_address\_any

security\_policy\_ipv6\_destination\_address\_name

security\_policy\_ipv6\_destination\_address\_group

security\_policy\_ipv6\_service\_any

security\_policy\_ipv6\_service\_name

security\_policy\_ipv6\_service\_group

security\_policy\_ipv6\_users\_all

security\_policy\_ipv6\_users\_guests

security\_policy\_ipv6\_users\_administrator

security\_policy\_ipv6\_users\_name

security\_policy\_ipv6\_users\_group

security\_policy\_ipv6\_application\_any

security\_policy\_ipv6\_application\_group

security\_policy\_ipv6\_web\_category\_any

security\_policy\_ipv6\_web\_category\_group

security\_policy\_ipv6\_url\_list\_any

security\_policy\_ipv6\_url\_list\_name

security\_policy\_ipv6\_url\_list\_group

security\_policy\_ipv6\_custom\_match\_any

security\_policy\_ipv6\_custom\_match\_group

security\_policy\_ipv6\_country\_any

security\_policy\_ipv6\_country\_group

security\_policy\_ipv6\_schedule\_always\_on

security\_policy\_ipv6\_schedule\_name

security\_policy\_ipv6\_schedule\_days

security\_policy\_ipv6

security\_policy\_ipv6\_collection

security\_policy\_all\_ipv4\_action

security\_policy\_all\_ipv6\_action

security\_policies\_max\_count

policy\_section

policy\_section\_collection

security\_policy\_ipv4\_clone

security\_policy\_ipv4\_clone\_collection

security\_policy\_ipv6\_clone

security\_policy\_ipv6\_clone\_collection

decryption\_policy\_client\_priority\_begin

decryption\_policy\_client\_priority\_end

decryption\_policy\_client\_priority\_manual

decryption\_policy\_client\_source\_address\_any

decryption\_policy\_client\_source\_address\_name

decryption\_policy\_client\_source\_address\_group

decryption\_policy\_client\_destination\_address\_any

decryption\_policy\_client\_destination\_address\_name

decryption\_policy\_client\_destination\_address\_group

decryption\_policy\_client\_service\_any

decryption\_policy\_client\_service\_name

decryption\_policy\_client\_service\_group

decryption\_policy\_client\_users\_included\_all

decryption\_policy\_client\_users\_included\_guests

decryption\_policy\_client\_users\_included\_administrator

decryption\_policy\_client\_users\_included\_name

decryption\_policy\_client\_users\_included\_group

decryption\_policy\_client\_web\_category\_any

decryption\_policy\_client\_web\_category\_group

decryption\_policy\_client\_web\_site\_any

decryption\_policy\_client\_web\_site\_name

decryption\_policy\_client\_web\_site\_group

decryption\_policy\_client\_match\_operation\_or

decryption\_policy\_client\_match\_operation\_and

decryption\_policy\_client\_country\_any

decryption\_policy\_client\_country\_group

decryption\_policy\_client\_schedule\_always\_on

decryption\_policy\_client\_schedule\_name

decryption\_policy\_client\_schedule\_days

decryption\_policy\_client\_action\_decrypt

decryption\_policy\_client\_action\_bypass

decryption\_policy\_client

decryption\_policy\_client\_collection

decryption\_policy\_server\_priority\_begin

decryption\_policy\_server\_priority\_end

decryption\_policy\_server\_priority\_manual

decryption\_policy\_server\_source\_address\_any

decryption\_policy\_server\_source\_address\_name

decryption\_policy\_server\_source\_address\_group

decryption\_policy\_server\_destination\_address\_any

decryption\_policy\_server\_destination\_address\_name

decryption\_policy\_server\_destination\_address\_group

decryption\_policy\_server\_service\_any

decryption\_policy\_server\_service\_name

decryption\_policy\_server\_service\_group

decryption\_policy\_server\_users\_included\_all

decryption\_policy\_server\_users\_included\_guests

decryption\_policy\_server\_users\_included\_administrator

decryption\_policy\_server\_users\_included\_name

decryption\_policy\_server\_users\_included\_group

decryption\_policy\_server\_web\_category\_any

decryption\_policy\_server\_web\_category\_group

decryption\_policy\_server\_web\_site\_any

decryption\_policy\_server\_web\_site\_name

decryption\_policy\_server\_web\_site\_group

decryption\_policy\_server\_match\_operation\_or

decryption\_policy\_server\_match\_operation\_and

decryption\_policy\_server\_country\_any

decryption\_policy\_server\_country\_group

decryption\_policy\_server\_schedule\_always\_on

decryption\_policy\_server\_schedule\_name

decryption\_policy\_server\_schedule\_days

decryption\_policy\_server\_action\_decrypt

decryption\_policy\_server\_action\_bypass

decryption\_policy\_server

decryption\_policy\_server\_collection

decryption\_policy\_ssh\_priority\_begin

decryption\_policy\_ssh\_priority\_end

decryption\_policy\_ssh\_priority\_manual

decryption\_policy\_ssh\_source\_address\_any

decryption\_policy\_ssh\_source\_address\_name

decryption\_policy\_ssh\_source\_address\_group

decryption\_policy\_ssh\_destination\_address\_any

decryption\_policy\_ssh\_destination\_address\_name

decryption\_policy\_ssh\_destination\_address\_group

decryption\_policy\_ssh\_service\_any

decryption\_policy\_ssh\_service\_name

decryption\_policy\_ssh\_service\_group

decryption\_policy\_ssh\_users\_included\_all

decryption\_policy\_ssh\_users\_included\_guests

decryption\_policy\_ssh\_users\_included\_administrator

decryption\_policy\_ssh\_users\_included\_name

decryption\_policy\_ssh\_users\_included\_group

decryption\_policy\_ssh\_web\_category\_any

decryption\_policy\_ssh\_web\_category\_group

decryption\_policy\_ssh\_web\_site\_any

decryption\_policy\_ssh\_web\_site\_name

decryption\_policy\_ssh\_web\_site\_group

decryption\_policy\_ssh\_match\_operation\_or

decryption\_policy\_ssh\_match\_operation\_and

decryption\_policy\_ssh\_country\_any

decryption\_policy\_ssh\_country\_group

decryption\_policy\_ssh\_schedule\_always\_on

decryption\_policy\_ssh\_schedule\_name

decryption\_policy\_ssh\_schedule\_days

decryption\_policy\_ssh\_action\_decrypt

decryption\_policy\_ssh\_action\_bypass

decryption\_policy\_ssh

decryption\_policy\_ssh\_collection

all\_decryption\_policies\_action

reset\_decryption\_policy\_status\_action

decryption\_policy\_client\_clone

decryption\_policy\_client\_clone\_collection

decryption\_policy\_server\_clone

decryption\_policy\_server\_clone\_collection

decryption\_policy\_ssh\_clone

decryption\_policy\_ssh\_clone\_collection

dos\_policy\_priority\_auto

dos\_policy\_priority\_end

dos\_policy\_priority\_manual

dos\_policy\_destination\_address\_any

dos\_policy\_destination\_address\_name

dos\_policy\_destination\_address\_group

dos\_policy\_source\_address\_any

dos\_policy\_source\_address\_name

dos\_policy\_source\_address\_group

dos\_policy\_service\_any

dos\_policy\_service\_name

dos\_policy\_service\_group

dos\_policy\_service\_protocol

dos\_policy\_schedule\_always\_on

dos\_policy\_schedule\_name

dos\_policy\_schedule\_days

dos\_policy

dos\_policy\_collection

dos\_policy\_all\_action

dos\_policy\_clone

dos\_policy\_clone\_collection

nat\_policy\_ipv4\_source\_any

nat\_policy\_ipv4\_source\_name

nat\_policy\_ipv4\_source\_group

nat\_policy\_ipv4\_translated\_source\_original

nat\_policy\_ipv4\_translated\_source\_name

nat\_policy\_ipv4\_translated\_source\_group

nat\_policy\_ipv4\_destination\_any

nat\_policy\_ipv4\_destination\_name

nat\_policy\_ipv4\_destination\_group

nat\_policy\_ipv4\_translated\_destination\_original

nat\_policy\_ipv4\_translated\_destination\_name

nat\_policy\_ipv4\_translated\_destination\_group

nat\_policy\_ipv4\_service\_any

nat\_policy\_ipv4\_service\_name

nat\_policy\_ipv4\_service\_group

nat\_policy\_ipv4\_translated\_service\_original

nat\_policy\_ipv4\_translated\_service\_name

nat\_policy\_ipv4\_translated\_service\_group

nat\_policy\_ipv4\_priority\_auto

nat\_policy\_ipv4\_priority\_manual

nat\_policy\_ipv4\_high\_availability\_probing\_probe\_type\_icmp\_ping

nat\_policy\_ipv4\_high\_availability\_probing\_probe\_type\_tcp

nat\_policy\_ipv4

nat\_policy\_ipv4\_collection

nat\_policy\_ipv6\_source\_any

nat\_policy\_ipv6\_source\_name

nat\_policy\_ipv6\_source\_group

nat\_policy\_ipv6\_translated\_source\_original

nat\_policy\_ipv6\_translated\_source\_name

nat\_policy\_ipv6\_translated\_source\_group

nat\_policy\_ipv6\_destination\_any

nat\_policy\_ipv6\_destination\_name

nat\_policy\_ipv6\_destination\_group

nat\_policy\_ipv6\_translated\_destination\_original

nat\_policy\_ipv6\_translated\_destination\_name

nat\_policy\_ipv6\_translated\_destination\_group

nat\_policy\_ipv6\_service\_any

nat\_policy\_ipv6\_service\_name

nat\_policy\_ipv6\_service\_group

nat\_policy\_ipv6\_translated\_service\_original

nat\_policy\_ipv6\_translated\_service\_name

nat\_policy\_ipv6\_translated\_service\_group

nat\_policy\_ipv6\_priority\_auto

nat\_policy\_ipv6\_priority\_manual

nat\_policy\_ipv6\_high\_availability\_probing\_probe\_type\_icmp\_ping

nat\_policy\_ipv6\_high\_availability\_probing\_probe\_type\_tcp

nat\_policy\_ipv6

nat\_policy\_ipv6\_collection

nat\_policy\_nat64\_source\_any

nat\_policy\_nat64\_source\_name

nat\_policy\_nat64\_source\_group

nat\_policy\_nat64\_translated\_source\_original

nat\_policy\_nat64\_translated\_source\_name

nat\_policy\_nat64\_translated\_source\_group

nat\_policy\_nat64\_pref64\_any

nat\_policy\_nat64\_pref64\_name

nat\_policy\_nat64\_pref64\_group

nat\_policy\_nat64\_priority\_auto

nat\_policy\_nat64\_priority\_manual

nat\_policy\_nat64

nat\_policy\_nat64\_collection

all\_nat\_policies\_action

access\_rule\_ipv4\_source\_address\_any

access\_rule\_ipv4\_source\_address\_name

access\_rule\_ipv4\_source\_address\_group

access\_rule\_ipv4\_source\_port\_any

access\_rule\_ipv4\_source\_port\_name

access\_rule\_ipv4\_source\_port\_group

access\_rule\_ipv4\_service\_any

access\_rule\_ipv4\_service\_name

access\_rule\_ipv4\_service\_group

access\_rule\_ipv4\_destination\_address\_any

access\_rule\_ipv4\_destination\_address\_name

access\_rule\_ipv4\_destination\_address\_group

access\_rule\_ipv4\_schedule\_always\_on

access\_rule\_ipv4\_schedule\_name

access\_rule\_ipv4\_schedule\_days

access\_rule\_ipv4\_users\_included\_all

access\_rule\_ipv4\_users\_included\_guests

access\_rule\_ipv4\_users\_included\_administrator

access\_rule\_ipv4\_users\_included\_name

access\_rule\_ipv4\_users\_included\_group

access\_rule\_ipv4\_users\_excluded\_none

access\_rule\_ipv4\_users\_excluded\_guests

access\_rule\_ipv4\_users\_excluded\_administrator

access\_rule\_ipv4\_users\_excluded\_name

access\_rule\_ipv4\_users\_excluded\_group

access\_rule\_ipv4\_packet\_dissection\_filter\_name

access\_rule\_ipv4\_packet\_dissection\_filter\_group

access\_rule\_ipv4\_priority\_auto

access\_rule\_ipv4\_priority\_end

access\_rule\_ipv4\_priority\_manual

access\_rule\_ipv4\_quality\_of\_service\_class\_of\_service\_explicit

access\_rule\_ipv4\_quality\_of\_service\_class\_of\_service\_map

access\_rule\_ipv4\_quality\_of\_service\_class\_of\_service\_preserve

access\_rule\_ipv4\_quality\_of\_service\_dscp\_explicit

access\_rule\_ipv4\_quality\_of\_service\_dscp\_map

access\_rule\_ipv4\_quality\_of\_service\_dscp\_preserve

access\_rule\_ipv4\_bandwidth\_management\_egress\_bandwidth\_object

access\_rule\_ipv4\_bandwidth\_management\_ingress\_bandwidth\_object

access\_rule\_ipv4

access\_rule\_ipv4\_collection

access\_rule\_ipv6\_source\_address\_any

access\_rule\_ipv6\_source\_address\_name

access\_rule\_ipv6\_source\_address\_group

access\_rule\_ipv6\_source\_port\_any

access\_rule\_ipv6\_source\_port\_name

access\_rule\_ipv6\_source\_port\_group

access\_rule\_ipv6\_service\_any

access\_rule\_ipv6\_service\_name

access\_rule\_ipv6\_service\_group

access\_rule\_ipv6\_destination\_address\_any

access\_rule\_ipv6\_destination\_address\_name

access\_rule\_ipv6\_destination\_address\_group

access\_rule\_ipv6\_schedule\_always\_on

access\_rule\_ipv6\_schedule\_name

access\_rule\_ipv6\_schedule\_days

access\_rule\_ipv6\_users\_included\_all

access\_rule\_ipv6\_users\_included\_guests

access\_rule\_ipv6\_users\_included\_administrator

access\_rule\_ipv6\_users\_included\_name

access\_rule\_ipv6\_users\_included\_group

access\_rule\_ipv6\_users\_excluded\_none

access\_rule\_ipv6\_users\_excluded\_guests

access\_rule\_ipv6\_users\_excluded\_administrator

access\_rule\_ipv6\_users\_excluded\_name

access\_rule\_ipv6\_users\_excluded\_group

access\_rule\_ipv6\_packet\_dissection\_filter\_name

access\_rule\_ipv6\_packet\_dissection\_filter\_group

access\_rule\_ipv6\_priority\_auto

access\_rule\_ipv6\_priority\_end

access\_rule\_ipv6\_priority\_manual

access\_rule\_ipv6\_quality\_of\_service\_class\_of\_service\_explicit

access\_rule\_ipv6\_quality\_of\_service\_class\_of\_service\_map

access\_rule\_ipv6\_quality\_of\_service\_class\_of\_service\_preserve

access\_rule\_ipv6\_quality\_of\_service\_dscp\_explicit

access\_rule\_ipv6\_quality\_of\_service\_dscp\_map

access\_rule\_ipv6\_quality\_of\_service\_dscp\_preserve

access\_rule\_ipv6\_bandwidth\_management\_egress\_bandwidth\_object

access\_rule\_ipv6\_bandwidth\_management\_ingress\_bandwidth\_object

access\_rule\_ipv6

access\_rule\_ipv6\_collection

access\_rule\_all\_ipv4\_action

access\_rule\_all\_ipv6\_action

access\_rules\_max\_count

access\_rules\_restore\_defaults\_action

clear\_policy\_lookup\_action

generate\_shadow\_list\_access\_rules\_action

generate\_shadow\_list\_nat\_policies\_action

generate\_shadow\_list\_route\_policies\_action

generate\_shadow\_list\_decryption\_policies\_action

generate\_shadow\_list\_dos\_policies\_action

access\_rules\_ipv4\_reporting

access\_rules\_ipv6\_reporting

route\_policy\_ipv4\_source\_any

route\_policy\_ipv4\_source\_name

route\_policy\_ipv4\_source\_group

route\_policy\_ipv4\_destination\_any

route\_policy\_ipv4\_destination\_name

route\_policy\_ipv4\_destination\_group

route\_policy\_ipv4\_service\_any

route\_policy\_ipv4\_service\_name

route\_policy\_ipv4\_service\_group

route\_policy\_ipv4\_gateway\_default

route\_policy\_ipv4\_gateway\_name

route\_policy\_ipv4\_gateway\_host

route\_policy\_ipv4\_distance\_auto

route\_policy\_ipv4\_distance\_value

route\_policy\_ipv4\_gateway2\_default

route\_policy\_ipv4\_gateway2\_name

route\_policy\_ipv4\_gateway2\_host

route\_policy\_ipv4\_gateway3\_default

route\_policy\_ipv4\_gateway3\_name

route\_policy\_ipv4\_gateway3\_host

route\_policy\_ipv4\_gateway4\_default

route\_policy\_ipv4\_gateway4\_name

route\_policy\_ipv4\_gateway4\_host

route\_policy\_ipv4

route\_policy\_ipv4\_collection

route\_policy\_ipv6\_source\_any

route\_policy\_ipv6\_source\_name

route\_policy\_ipv6\_source\_group

route\_policy\_ipv6\_destination\_any

route\_policy\_ipv6\_destination\_name

route\_policy\_ipv6\_destination\_group

route\_policy\_ipv6\_service\_any

route\_policy\_ipv6\_service\_name

route\_policy\_ipv6\_service\_group

route\_policy\_ipv6\_gateway\_default

route\_policy\_ipv6\_gateway\_name

route\_policy\_ipv6\_gateway\_host

route\_policy\_ipv6\_distance\_auto

route\_policy\_ipv6\_distance\_value

route\_policy\_ipv6\_gateway2\_default

route\_policy\_ipv6\_gateway2\_name

route\_policy\_ipv6\_gateway2\_host

route\_policy\_ipv6\_gateway3\_default

route\_policy\_ipv6\_gateway3\_name

route\_policy\_ipv6\_gateway3\_host

route\_policy\_ipv6\_gateway4\_default

route\_policy\_ipv6\_gateway4\_name

route\_policy\_ipv6\_gateway4\_host

route\_policy\_ipv6

route\_policy\_ipv6\_collection

routing

restart

boot\_current\_action

boot\_uploaded\_action

sys\_ext\_storage\_logs\_enable\_action

sys\_ext\_storage\_logs\_disable\_action

local\_backup\_boot

cloud\_backup\_boot\_action

config\_mode\_action

non\_config\_mode\_action

sysfile\_export\_sysdata

sysfile\_export\_diagdata

sysfile\_export\_log

sysfile\_storage

export\_current\_config\_exp

export\_current\_config\_cli

export\_firmware\_current

export\_firmware\_uploaded

export\_firmware\_system\_backup

export\_tech\_support\_report

export\_ssoauth\_log

export\_and\_reset\_ssoauth\_log

export\_swarm\_report

export\_trace\_log

export\_core\_dump

export\_address\_objects\_api

export\_services\_api

export\_country\_objects\_api

export\_applications\_api

export\_web\_categories\_api

export\_url\_list\_api

export\_custom\_matches\_api

export\_threat\_prevention\_profiles\_api

export\_actions\_api

export\_security\_policies\_api

export\_nat\_policies\_api

export\_route\_policies\_api

export\_decryption\_policies\_api

export\_dos\_policies\_api

export\_access\_rules\_shadow\_rule\_list\_api

export\_nat\_policies\_shadow\_rule\_list\_api

export\_route\_policies\_shadow\_rule\_list\_api

export\_decryption\_policies\_shadow\_rule\_list\_api

export\_dos\_policies\_shadow\_rule\_list\_api

export\_console\_logs

export\_safe\_mode\_logs

export\_cloud\_backup\_exp

import\_exp\_confirm\_action

import\_exp\_abort\_action

firmware

ftp

local\_backups\_action

export\_local\_backup\_firmware

local\_backup

local\_backup\_retain

local\_backup\_comment

local\_backup\_gold

cloud\_backup

cloud\_backup\_retain

cloud\_backup\_comment

cloud\_backup\_gold

auto\_upgrade\_action

firmware\_download\_action

log\_view\_option

log\_syslog

log\_syslog\_servers

log\_syslog\_servers\_collection

log\_syslog\_servers\_delete\_action

log\_syslog\_servers\_enable\_action

log\_syslog\_servers\_disable\_action

log\_analyzer

log\_analyzer\_syslog\_servers

log\_analyzer\_syslog\_servers\_collection

log\_viewpoint

log\_viewpoint\_syslog\_servers

log\_viewpoint\_syslog\_servers\_collection

log\_name\_resolution\_name\_resolution\_dns\_inherit

log\_name\_resolution\_name\_resolution\_dns\_static

log\_name\_resolution

name\_resolution\_reset\_name\_cache\_action

log\_automation\_send\_log\_when\_full

log\_automation\_send\_log\_daily

log\_automation\_send\_log\_weekly\_sun

log\_automation\_send\_log\_weekly\_mon

log\_automation\_send\_log\_weekly\_tue

log\_automation\_send\_log\_weekly\_wed

log\_automation\_send\_log\_weekly\_thu

log\_automation\_send\_log\_weekly\_fri

log\_automation\_send\_log\_weekly\_sat

log\_automation\_send\_log\_weekly

log\_automation\_email\_format\_log\_plain\_text

log\_automation\_email\_format\_log\_html

log\_automation\_email\_format\_log\_csv

log\_automation\_send\_audit\_when\_full

log\_automation\_send\_audit\_daily

log\_automation\_send\_audit\_weekly\_sun

log\_automation\_send\_audit\_weekly\_mon

log\_automation\_send\_audit\_weekly\_tue

log\_automation\_send\_audit\_weekly\_wed

log\_automation\_send\_audit\_weekly\_thu

log\_automation\_send\_audit\_weekly\_fri

log\_automation\_send\_audit\_weekly\_sat

log\_automation\_send\_audit\_weekly

log\_automation\_email\_format\_audit\_plain\_text

log\_automation\_email\_format\_audit\_html

log\_automation\_email\_format\_audit\_csv

log\_automation\_health\_check\_email\_schedule\_name

log\_automation\_health\_check\_email\_schedule\_days

log\_automation\_mail\_server\_advanced\_connection\_security\_method\_ssl\_tls

log\_automation\_mail\_server\_advanced\_connection\_security\_method\_start\_tls

log\_automation\_ftp\_log\_send\_log\_when\_full

log\_automation\_ftp\_log\_send\_log\_daily

log\_automation\_ftp\_log\_send\_log\_weekly\_sun

log\_automation\_ftp\_log\_send\_log\_weekly\_mon

log\_automation\_ftp\_log\_send\_log\_weekly\_tue

log\_automation\_ftp\_log\_send\_log\_weekly\_wed

log\_automation\_ftp\_log\_send\_log\_weekly\_thu

log\_automation\_ftp\_log\_send\_log\_weekly\_fri

log\_automation\_ftp\_log\_send\_log\_weekly\_sat

log\_automation\_ftp\_log\_send\_log\_weekly

log\_automation\_ftp\_log\_file\_format\_plain\_text

log\_automation\_ftp\_log\_file\_format\_html

log\_automation\_ftp\_log\_file\_format\_attachment

log\_automation\_solera\_server\_name

log\_automation\_solera\_server\_host

log\_automation\_solera\_server\_fqdn

log\_automation

log\_global\_categories\_global\_category\_attribute\_event\_profile\_mixed

log\_global\_categories\_global\_category\_attribute\_event\_profile\_syslog\_server\_profile

log\_global\_categories\_global\_category\_attribute\_log\_digest\_enabled

log\_global\_categories\_global\_category\_attribute\_log\_digest\_mixed

log\_global\_categories\_global\_category\_attribute\_color\_leave\_unchanged

log\_global\_categories\_global\_category\_attribute\_color\_rgb

log\_global\_categories\_global\_category\_attribute\_color\_hex

log\_global\_categories\_global\_category\_attribute\_color\_black

log\_global\_categories\_global\_category\_attribute\_color\_red

log\_global\_categories\_global\_category\_attribute\_color\_yellow

log\_global\_categories\_global\_category\_attribute\_color\_blue

log\_global\_categories\_global\_category\_attribute\_color\_green

log\_global\_categories\_global\_category\_attribute\_color\_orange

log\_global\_categories\_global\_category\_attribute\_color\_purple

log\_global\_categories\_global\_category\_attribute\_alert\_email\_leave\_unchanged

log\_global\_categories\_global\_category\_attribute\_alert\_email\_address

log\_global\_categories\_global\_category\_attribute\_log\_email\_leave\_unchanged

log\_global\_categories\_global\_category\_attribute\_log\_email\_address

log\_global\_categories

log\_categories\_event\_profile\_mixed

log\_categories\_event\_profile\_syslog\_server\_profile

log\_categories\_log\_digest\_enabled

log\_categories\_log\_digest\_mixed

log\_categories\_color\_leave\_unchanged

log\_categories\_color\_rgb

log\_categories\_color\_hex

log\_categories\_color\_black

log\_categories\_color\_red

log\_categories\_color\_yellow

log\_categories\_color\_blue

log\_categories\_color\_green

log\_categories\_color\_orange

log\_categories\_color\_purple

log\_categories\_alert\_email\_leave\_unchanged

log\_categories\_alert\_email\_address

log\_categories

log\_categories\_collection

log\_category\_groups\_event\_profile\_mixed

log\_category\_groups\_event\_profile\_syslog\_server\_profile

log\_category\_groups\_log\_digest\_enabled

log\_category\_groups\_log\_digest\_mixed

log\_category\_groups\_color\_leave\_unchanged

log\_category\_groups\_color\_rgb

log\_category\_groups\_color\_hex

log\_category\_groups\_color\_black

log\_category\_groups\_color\_red

log\_category\_groups\_color\_yellow

log\_category\_groups\_color\_blue

log\_category\_groups\_color\_green

log\_category\_groups\_color\_orange

log\_category\_groups\_color\_purple

log\_category\_groups\_alert\_email\_leave\_unchanged

log\_category\_groups\_alert\_email\_address

log\_category\_groups

log\_category\_groups\_collection

log\_category\_events\_color\_rgb

log\_category\_events\_color\_hex

log\_category\_events\_color\_black

log\_category\_events\_color\_red

log\_category\_events\_color\_yellow

log\_category\_events\_color\_blue

log\_category\_events\_color\_green

log\_category\_events\_color\_orange

log\_category\_events\_color\_purple

log\_category\_events

log\_category\_events\_collection

log\_display\_time\_range\_all

log\_display\_time\_range\_last

log\_display

log\_aws

log\_mail\_server\_test\_action

log\_clear\_log\_action

log\_export\_log

log\_email\_log\_action

log\_save\_template\_action

log\_import\_template\_default\_action

log\_import\_template\_minimal\_action

log\_import\_template\_analyzer\_viewpoint\_gms\_action

log\_import\_template\_firewall\_action\_action

log\_import\_template\_custom\_action

log\_reset\_event\_count\_all\_action

log\_reset\_event\_count\_event\_id\_action

log\_reset\_event\_count\_action

log\_disable\_event\_id\_action

export\_sdwan\_conn\_log

log\_reports\_start\_action

log\_reports\_stop\_action

log\_reports\_report\_refresh\_action

log\_reports\_report\_reset\_action

log\_audit\_view

time

time\_ntp\_servers

time\_ntp\_servers\_collection

firewall\_ftp\_transforms\_in\_service\_object\_name

firewall\_ftp\_transforms\_in\_service\_object\_group

firewall

firewall\_deregister\_action

diag\_purge\_coredump\_action

diag\_acm\_filter\_reset\_action

diag\_acm\_filter

packet\_monitor

packet\_monitor\_log\_to\_ftp\_action

packet\_monitor\_monitor\_all\_action

packet\_monitor\_monitor\_default\_action

packet\_monitor\_capture\_action

packet\_monitor\_start\_capture\_action

packet\_monitor\_start\_mirror\_action

packet\_monitor\_stop\_capture\_action

packet\_monitor\_stop\_mirror\_action

export\_captured\_packets

standby\_trace

packet\_monitor\_standby\_default\_trace\_action

tsr\_options

tsr\_secure\_send\_action

certificates\_generate\_signing\_request\_alternate\_name\_domain\_name

certificates\_generate\_signing\_request\_alternate\_name\_email\_address

certificates\_generate\_signing\_request\_alternate\_name\_ipv4\_address

certificates\_generate\_signing\_request

certificates\_generate\_signing\_request\_collection

certificates\_scep

certificates\_scep\_collection

certificates\_export\_signing\_request

certificates\_export\_cert\_key\_pair

certificates\_import\_cert\_key\_pair

certificates\_import\_ca\_cert

certificates\_import\_signed\_cert

certificates\_import\_crl\_action

certificates\_import\_crl\_periodically\_action

certificates\_import\_crl\_directly

snmp

snmp\_view

snmp\_view\_collection

snmp\_group

snmp\_group\_collection

snmp\_user\_security\_level\_authentication\_only

snmp\_user\_security\_level\_authentication\_and\_privacy

snmp\_user\_authentication\_md5

snmp\_user\_authentication\_sha1

snmp\_user\_encryption\_aes

snmp\_user\_encryption\_des

snmp\_user

snmp\_user\_collection

snmp\_access\_security\_level\_authentication\_only

snmp\_access\_security\_level\_authentication\_and\_privacy

snmp\_access

snmp\_access\_collection

license

license\_collection

license\_register\_code

license\_synchronize\_action

license\_status\_reporting

ssh\_server

ssh\_server\_keygen\_action

ssh\_server\_restart\_action

ssh\_server\_enable\_action

ssh\_server\_terminate\_action

ssh\_server\_kill\_session\_action

version

fips

ndpp

log\_audit

log\_export\_audit

log\_email\_audit\_action

arp\_base

arp\_entries

arp\_entries\_collection

dns\_rebinding\_allowed\_domains\_name

dns\_rebinding\_allowed\_domains\_group

dns

dns\_split\_entry

dns\_split\_entry\_collection

dns\_cache\_reporting

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_bound\_to\_any

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_bound\_to\_interface

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_online\_settings\_set\_to\_wan

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_online\_settings\_detect

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_online\_settings\_manual

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_offline\_settings\_do\_nothing

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_offline\_settings\_use\_previous

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_offline\_settings\_make\_host\_unknown

dynamic\_dns\_profile\_ipv4\_profile\_ipv4\_offline\_settings\_manual

dynamic\_dns\_profile\_ipv4

dynamic\_dns\_profile\_ipv4\_collection

dynamic\_dns\_profile\_ipv6\_profile\_ipv6\_bound\_to\_any

dynamic\_dns\_profile\_ipv6\_profile\_ipv6\_bound\_to\_interface

dynamic\_dns\_profile\_ipv6\_profile\_ipv6\_online\_settings\_set\_to\_wan

dynamic\_dns\_profile\_ipv6\_profile\_ipv6\_online\_settings\_manual

dynamic\_dns\_profile\_ipv6\_profile\_ipv6\_offline\_settings\_do\_nothing

dynamic\_dns\_profile\_ipv6\_profile\_ipv6\_offline\_settings\_use\_previous

dynamic\_dns\_profile\_ipv6

dynamic\_dns\_profile\_ipv6\_collection

flb

flb\_group\_interface\_main\_target\_protocol\_tcp

flb\_group\_interface\_main\_target\_protocol\_ping

flb\_group\_interface\_alternate\_target\_protocol\_tcp

flb\_group\_interface\_alternate\_target\_protocol\_ping

flb\_group

flb\_group\_collection

flb\_group\_auto\_adjust\_ratio\_action

flb\_group\_member\_percent\_action

dhcp\_server\_base

dhcp\_server\_option\_object

dhcp\_server\_option\_object\_collection

dhcp\_server\_option\_group

dhcp\_server\_option\_group\_collection

dhcp\_server\_scope\_dynamic\_dns\_server\_inherit

dhcp\_server\_scope\_dynamic\_dns\_server\_static

dhcp\_server\_scope\_dynamic\_generic\_option\_object

dhcp\_server\_scope\_dynamic\_generic\_option\_group

dhcp\_server\_scope\_dynamic

dhcp\_server\_scope\_dynamic\_collection

dhcp\_server\_scope\_static\_dns\_server\_inherit

dhcp\_server\_scope\_static\_dns\_server\_static

dhcp\_server\_scope\_static\_generic\_option\_object

dhcp\_server\_scope\_static\_generic\_option\_group

dhcp\_server\_scope\_static

dhcp\_server\_scope\_static\_collection

dhcp\_server\_ipv6\_base

dhcp\_server\_ipv6\_option\_object

dhcp\_server\_ipv6\_option\_object\_collection

dhcp\_server\_ipv6\_option\_group

dhcp\_server\_ipv6\_option\_group\_collection

dhcp\_server\_ipv6\_scope\_dynamic\_dns\_server\_inherit

dhcp\_server\_ipv6\_scope\_dynamic\_dns\_server\_static

dhcp\_server\_ipv6\_scope\_dynamic\_generic\_option\_object

dhcp\_server\_ipv6\_scope\_dynamic\_generic\_option\_group

dhcp\_server\_ipv6\_scope\_dynamic

dhcp\_server\_ipv6\_scope\_dynamic\_collection

dhcp\_server\_ipv6\_scope\_static\_dns\_server\_inherit

dhcp\_server\_ipv6\_scope\_static\_dns\_server\_static

dhcp\_server\_ipv6\_scope\_static\_generic\_option\_object

dhcp\_server\_ipv6\_scope\_static\_generic\_option\_group

dhcp\_server\_ipv6\_scope\_static

dhcp\_server\_ipv6\_scope\_static\_collection

dns\_security\_sinkhole\_dns\_sinkhole\_action\_type\_dropping\_with\_logs

dns\_security\_sinkhole\_dns\_sinkhole\_action\_type\_dropping\_with\_negative\_dns\_reply\_to\_source

dns\_security\_sinkhole\_dns\_sinkhole\_action\_type\_dropping\_with\_dns\_reply\_of\_forged\_ip

dns\_security\_sinkhole

dns\_security\_sinkhole\_custom\_malicious\_entry

dns\_security\_sinkhole\_custom\_malicious\_entry\_collection

dns\_security\_sinkhole\_white\_list\_entry

dns\_security\_sinkhole\_white\_list\_entry\_collection

dns\_security\_tunnel

dns\_security\_tunnel\_white\_list\_entry

dns\_security\_tunnel\_white\_list\_entry\_collection

dns\_security\_tunnel\_block\_action

iph

iph\_policy\_source\_interface

iph\_policy\_source\_zone

iph\_policy\_source\_network

iph\_policy\_source\_name

iph\_policy\_source\_group

iph\_policy\_destination\_name

iph\_policy\_destination\_group

iph\_policy\_destination\_host

iph\_policy\_destination\_network

iph\_policy\_destination\_ipv6

iph\_policy

iph\_policy\_collection

iph\_protocol

iph\_protocol\_collection

mac\_ip\_anti\_spoof\_ipv4

mac\_ip\_anti\_spoof\_ipv4\_collection

mac\_ip\_anti\_spoof\_cache\_ipv4

mac\_ip\_anti\_spoof\_cache\_ipv4\_collection

mac\_ip\_anti\_spoof\_ipv6

mac\_ip\_anti\_spoof\_ipv6\_collection

mac\_ip\_anti\_spoof\_cache\_ipv6

mac\_ip\_anti\_spoof\_cache\_ipv6\_collection

mac\_ip\_anti\_spoof\_resolve\_spoof\_ipv4\_action

mac\_ip\_anti\_spoof\_resolve\_spoof\_ipv6\_action

ndp

ndp\_entry

ndp\_entry\_collection

dns\_proxy

dns\_proxy\_cache\_entry

dns\_proxy\_cache\_entry\_collection

dns\_proxy\_flush\_cache\_entry\_ipv4\_action

dns\_proxy\_flush\_cache\_entry\_ipv6\_action

tcp\_proxy\_connections\_service\_any

tcp\_proxy\_connections\_service\_name

tcp\_proxy\_connections\_service\_group

tcp\_proxy\_connections\_service\_protocol

tcp

udp\_flood\_protected\_dest\_list\_any

udp\_flood\_protected\_dest\_list\_name

udp\_flood\_protected\_dest\_list\_group

udp

udpv6\_ipv6\_flood\_protected\_dest\_list\_any

udpv6\_ipv6\_flood\_protected\_dest\_list\_name

udpv6\_ipv6\_flood\_protected\_dest\_list\_group

udpv6

icmp\_flood\_protected\_dest\_list\_any

icmp\_flood\_protected\_dest\_list\_name

icmp\_flood\_protected\_dest\_list\_group

icmp

icmpv6\_ipv6\_flood\_protected\_dest\_list\_any

icmpv6\_ipv6\_flood\_protected\_dest\_list\_name

icmpv6\_ipv6\_flood\_protected\_dest\_list\_group

icmpv6

qos\_mapping

qos\_mapping\_collection

qos\_mapping\_reset\_action

multicast\_reception\_all

multicast\_reception\_name

multicast\_reception\_group

multicast\_reception\_host

multicast\_reception\_range

multicast\_reception\_network

multicast

web\_proxy

web\_proxy\_servers

web\_proxy\_servers\_collection

network\_monitor\_ipv4\_policy\_ipv4\_probe\_target\_name

network\_monitor\_ipv4\_policy\_ipv4\_probe\_target\_group

network\_monitor\_ipv4\_policy\_ipv4\_probe\_target\_fqdn

network\_monitor\_ipv4\_policy\_ipv4\_probe\_target\_host

network\_monitor\_ipv4\_policy\_ipv4\_probe\_target\_range

network\_monitor\_ipv4\_policy\_ipv4\_probe\_type\_ping

network\_monitor\_ipv4\_policy\_ipv4\_probe\_type\_tcp\_explicit

network\_monitor\_ipv4\_policy\_ipv4\_probe\_type\_tcp\_non\_explicit

network\_monitor\_ipv4\_policy\_ipv4\_probe\_type\_tcp

network\_monitor\_ipv4\_policy\_ipv4\_next\_hop\_name

network\_monitor\_ipv4\_policy\_ipv4\_next\_hop\_host

network\_monitor\_ipv4\_policy\_ipv4\_local\_ip\_name

network\_monitor\_ipv4\_policy\_ipv4\_local\_ip\_host

network\_monitor\_ipv4

network\_monitor\_ipv4\_collection

network\_monitor\_ipv6\_policy\_ipv6\_probe\_target\_name

network\_monitor\_ipv6\_policy\_ipv6\_probe\_target\_group

network\_monitor\_ipv6\_policy\_ipv6\_probe\_target\_fqdn

network\_monitor\_ipv6\_policy\_ipv6\_probe\_target\_host

network\_monitor\_ipv6\_policy\_ipv6\_probe\_target\_range

network\_monitor\_ipv6\_policy\_ipv6\_probe\_type\_ping

network\_monitor\_ipv6\_policy\_ipv6\_probe\_type\_tcp\_explicit

network\_monitor\_ipv6\_policy\_ipv6\_probe\_type\_tcp\_non\_explicit

network\_monitor\_ipv6\_policy\_ipv6\_probe\_type\_tcp

network\_monitor\_ipv6\_policy\_ipv6\_next\_hop\_name

network\_monitor\_ipv6\_policy\_ipv6\_next\_hop\_host

network\_monitor\_ipv6\_policy\_ipv6\_local\_ip\_name

network\_monitor\_ipv6\_policy\_ipv6\_local\_ip\_host

network\_monitor\_ipv6

network\_monitor\_ipv6\_collection

vlan\_translation

vlan\_translation\_collection

sonicpoint\_vap\_group

sonicpoint\_vap\_group\_collection

sonicpoint\_vap\_profile\_schedule\_always\_on

sonicpoint\_vap\_profile\_schedule\_name

sonicpoint\_vap\_profile\_schedule\_time\_of\_day

sonicpoint\_vap\_profile\_access\_list\_allow\_all

sonicpoint\_vap\_profile\_access\_list\_allow\_default

sonicpoint\_vap\_profile\_access\_list\_allow\_group

sonicpoint\_vap\_profile\_access\_list\_deny\_default

sonicpoint\_vap\_profile\_access\_list\_deny\_group

sonicpoint\_vap\_profile\_authentication\_type\_wep

sonicpoint\_vap\_profile\_authentication\_type\_wpa

sonicpoint\_vap\_profile\_authentication\_type\_wpa2\_psk

sonicpoint\_vap\_profile\_authentication\_type\_wpa2\_eap

sonicpoint\_vap\_profile\_authentication\_type\_wpa2\_auto

sonicpoint\_vap\_profile\_authentication\_type\_wpa2

sonicpoint\_vap\_profile\_authentication\_type\_wpa3\_owe

sonicpoint\_vap\_profile\_authentication\_type\_wpa3\_psk

sonicpoint\_vap\_profile\_authentication\_type\_wpa3\_eap

sonicpoint\_vap\_profile\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_vap\_profile\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_vap\_profile\_authentication\_type\_wpa3

sonicpoint\_vap\_profile\_cipher\_type\_wep

sonicpoint\_vap\_profile\_cipher\_type\_tkip

sonicpoint\_vap\_profile\_cipher\_type\_aes

sonicpoint\_vap\_profile\_cipher\_type\_auto

sonicpoint\_vap\_profile\_cipher\_type\_gcmp

sonicpoint\_vap\_profile\_radius\_nas\_identifier\_sonicpoint\_name

sonicpoint\_vap\_profile\_radius\_nas\_identifier\_sonicpoint\_mac\_address

sonicpoint\_vap\_profile\_radius\_nas\_identifier\_sonicpoint\_ssid

sonicpoint\_vap\_profile

sonicpoint\_vap\_profile\_collection

sonicpoint\_vap\_object\_schedule\_always\_on

sonicpoint\_vap\_object\_schedule\_name

sonicpoint\_vap\_object\_schedule\_time\_of\_day

sonicpoint\_vap\_object\_access\_list\_allow\_all

sonicpoint\_vap\_object\_access\_list\_allow\_default

sonicpoint\_vap\_object\_access\_list\_allow\_group

sonicpoint\_vap\_object\_access\_list\_deny\_default

sonicpoint\_vap\_object\_access\_list\_deny\_group

sonicpoint\_vap\_object\_authentication\_type\_wep

sonicpoint\_vap\_object\_authentication\_type\_wpa

sonicpoint\_vap\_object\_authentication\_type\_wpa2\_psk

sonicpoint\_vap\_object\_authentication\_type\_wpa2\_eap

sonicpoint\_vap\_object\_authentication\_type\_wpa2\_auto

sonicpoint\_vap\_object\_authentication\_type\_wpa2

sonicpoint\_vap\_object\_authentication\_type\_wpa3\_owe

sonicpoint\_vap\_object\_authentication\_type\_wpa3\_psk

sonicpoint\_vap\_object\_authentication\_type\_wpa3\_eap

sonicpoint\_vap\_object\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_vap\_object\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_vap\_object\_authentication\_type\_wpa3

sonicpoint\_vap\_object\_cipher\_type\_wep

sonicpoint\_vap\_object\_cipher\_type\_tkip

sonicpoint\_vap\_object\_cipher\_type\_aes

sonicpoint\_vap\_object\_cipher\_type\_auto

sonicpoint\_vap\_object\_cipher\_type\_gcmp

sonicpoint\_vap\_object\_radius\_nas\_identifier\_sonicpoint\_name

sonicpoint\_vap\_object\_radius\_nas\_identifier\_sonicpoint\_mac\_address

sonicpoint\_vap\_object\_radius\_nas\_identifier\_sonicpoint\_ssid

sonicpoint\_vap\_object

sonicpoint\_vap\_object\_collection

wireless\_vap\_group

wireless\_vap\_group\_collection

wireless\_vap\_profile\_schedule\_always\_on

wireless\_vap\_profile\_schedule\_name

wireless\_vap\_profile\_schedule\_time\_of\_day

wireless\_vap\_profile\_access\_list\_allow\_all

wireless\_vap\_profile\_access\_list\_allow\_default

wireless\_vap\_profile\_access\_list\_allow\_group

wireless\_vap\_profile\_access\_list\_deny\_default

wireless\_vap\_profile\_access\_list\_deny\_group

wireless\_vap\_profile\_authentication\_type\_wep

wireless\_vap\_profile\_authentication\_type\_wpa

wireless\_vap\_profile\_authentication\_type\_wpa2\_psk

wireless\_vap\_profile\_authentication\_type\_wpa2\_eap

wireless\_vap\_profile\_authentication\_type\_wpa2\_auto

wireless\_vap\_profile\_authentication\_type\_wpa2

wireless\_vap\_profile\_authentication\_type\_wpa3\_owe

wireless\_vap\_profile\_authentication\_type\_wpa3\_psk

wireless\_vap\_profile\_authentication\_type\_wpa3\_eap

wireless\_vap\_profile\_authentication\_type\_wpa3\_wpa2\_auto

wireless\_vap\_profile\_authentication\_type\_wpa3\_eap\_192b

wireless\_vap\_profile\_authentication\_type\_wpa3

wireless\_vap\_profile\_cipher\_type\_wep

wireless\_vap\_profile\_cipher\_type\_tkip

wireless\_vap\_profile\_cipher\_type\_aes

wireless\_vap\_profile\_cipher\_type\_auto

wireless\_vap\_profile\_cipher\_type\_gcmp

wireless\_vap\_profile

wireless\_vap\_profile\_collection

wireless\_vap\_object\_schedule\_always\_on

wireless\_vap\_object\_schedule\_name

wireless\_vap\_object\_schedule\_time\_of\_day

wireless\_vap\_object\_access\_list\_allow\_all

wireless\_vap\_object\_access\_list\_allow\_default

wireless\_vap\_object\_access\_list\_allow\_group

wireless\_vap\_object\_access\_list\_deny\_default

wireless\_vap\_object\_access\_list\_deny\_group

wireless\_vap\_object\_authentication\_type\_wep

wireless\_vap\_object\_authentication\_type\_wpa

wireless\_vap\_object\_authentication\_type\_wpa2\_psk

wireless\_vap\_object\_authentication\_type\_wpa2\_eap

wireless\_vap\_object\_authentication\_type\_wpa2\_auto

wireless\_vap\_object\_authentication\_type\_wpa2

wireless\_vap\_object\_authentication\_type\_wpa3\_owe

wireless\_vap\_object\_authentication\_type\_wpa3\_psk

wireless\_vap\_object\_authentication\_type\_wpa3\_eap

wireless\_vap\_object\_authentication\_type\_wpa3\_wpa2\_auto

wireless\_vap\_object\_authentication\_type\_wpa3\_eap\_192b

wireless\_vap\_object\_authentication\_type\_wpa3

wireless\_vap\_object\_cipher\_type\_wep

wireless\_vap\_object\_cipher\_type\_tkip

wireless\_vap\_object\_cipher\_type\_aes

wireless\_vap\_object\_cipher\_type\_auto

wireless\_vap\_object\_cipher\_type\_gcmp

wireless\_vap\_object

wireless\_vap\_object\_collection

wireless\_radio\_radio\_role\_access\_point\_radio\_mode\_n\_only

wireless\_radio\_radio\_role\_access\_point\_radio\_mode\_ngb\_mixed

wireless\_radio\_radio\_role\_access\_point\_radio\_mode\_g\_only

wireless\_radio\_radio\_role\_access\_point\_radio\_mode\_gb\_mixed

wireless\_radio\_radio\_role\_access\_point\_radio\_mode\_5000mhz

wireless\_radio\_radio\_role\_access\_point\_schedule\_always\_on

wireless\_radio\_radio\_role\_access\_point\_schedule\_name

wireless\_radio\_radio\_role\_access\_point\_schedule\_time\_of\_day

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wep

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa2\_psk

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa2\_eap

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa2\_auto

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa2

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa3\_owe

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa3\_psk

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa3\_eap

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa3\_wpa2\_auto

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa3\_eap\_192b

wireless\_radio\_radio\_role\_access\_point\_authentication\_type\_wpa3

wireless\_radio\_radio\_role\_access\_point\_protection\_mode\_always

wireless\_radio\_radio\_role\_access\_point\_protection\_mode\_auto

wireless\_radio\_radio\_role\_access\_point\_access\_list\_allow\_all

wireless\_radio\_radio\_role\_access\_point\_access\_list\_allow\_default

wireless\_radio\_radio\_role\_access\_point\_access\_list\_allow\_group

wireless\_radio\_radio\_role\_access\_point\_access\_list\_deny\_default

wireless\_radio\_radio\_role\_access\_point\_access\_list\_deny\_group

wireless\_radio\_radio\_role\_access\_point

wireless\_radio\_radio\_role\_wds\_station\_radio\_mode\_ngb\_mixed

wireless\_radio\_radio\_role\_wds\_station\_radio\_mode\_5000mhz

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wep

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa2\_psk

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa2\_auto

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa2

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa3\_owe

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa3\_psk

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa3\_eap

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa3\_wpa2\_auto

wireless\_radio\_radio\_role\_wds\_station\_authentication\_type\_wpa3

wireless\_radio\_radio\_role\_wds\_station

wireless\_radio\_radio\_role\_access\_point\_station\_schedule\_always\_on

wireless\_radio\_radio\_role\_access\_point\_station\_schedule\_name

wireless\_radio\_radio\_role\_access\_point\_station\_schedule\_time\_of\_day

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wep

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa2\_psk

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa2\_eap

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa2\_auto

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa2

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa3\_owe

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa3\_psk

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa3\_eap

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa3\_wpa2\_auto

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa3\_eap\_192b

wireless\_radio\_radio\_role\_access\_point\_station\_authentication\_type\_wpa3

wireless\_radio\_radio\_role\_access\_point\_station\_protection\_mode\_always

wireless\_radio\_radio\_role\_access\_point\_station\_protection\_mode\_auto

wireless\_radio\_radio\_role\_access\_point\_station\_access\_list\_allow\_all

wireless\_radio\_radio\_role\_access\_point\_station\_access\_list\_allow\_default

wireless\_radio\_radio\_role\_access\_point\_station\_access\_list\_allow\_group

wireless\_radio\_radio\_role\_access\_point\_station\_access\_list\_deny\_default

wireless\_radio\_radio\_role\_access\_point\_station\_access\_list\_deny\_group

wireless\_radio\_radio\_role\_access\_point\_station\_radio\_mode\_ngb\_mixed

wireless\_radio\_radio\_role\_access\_point\_station\_radio\_mode\_5000mhz

wireless\_radio\_radio\_role\_access\_point\_station\_station\_access\_point\_authentication\_type\_open

wireless\_radio\_radio\_role\_access\_point\_station\_station\_access\_point\_authentication\_type\_wpa2\_auto

wireless\_radio\_radio\_role\_access\_point\_station\_station\_access\_point\_authentication\_type\_wpa2

wireless\_radio\_radio\_role\_access\_point\_station\_station\_access\_point\_authentication\_type\_wpa3\_psk

wireless\_radio\_radio\_role\_access\_point\_station\_station\_access\_point\_authentication\_type\_wpa3

wireless\_radio\_radio\_role\_access\_point\_station

wireless\_radio

wireless\_ids\_authorized\_access\_point\_all

wireless\_ids\_authorized\_access\_point\_group

wireless\_ids\_schedule\_name

wireless\_ids\_schedule\_time\_of\_day

wireless\_ids

wireless\_access\_point\_station\_connect\_action

wireless\_access\_point\_station\_scan\_action

wireless\_access\_point\_station\_block\_station\_action

wireless\_access\_point\_station\_allow\_station\_action

wireless\_access\_point\_station\_disassociate\_station\_action

wireless\_access\_point\_station\_disassociate\_stations\_action

wireless\_access\_point\_block\_station\_action

wireless\_access\_point\_allow\_station\_action

wireless\_access\_point\_disassociate\_station\_action

wireless\_access\_point\_disassociate\_stations\_action

wireless\_wds\_station\_connect\_action

wireless\_wds\_station\_scan\_action

wireless\_ids\_authorizing\_action

wireless\_ids\_scan\_action

wireless\_status\_reporting

sonicpoint\_floor\_plan

sonicpoint\_floor\_plan\_collection

export\_floor\_plan\_png

export\_floor\_plan\_jpg

import\_floor\_plan

sonicpoint\_profile\_band\_steering\_auto

sonicpoint\_profile\_band\_steering\_prefer\_5ghz

sonicpoint\_profile\_band\_steering\_force\_5ghz

sonicpoint\_profile\_widp\_sensor\_schedule\_always\_on

sonicpoint\_profile\_widp\_sensor\_schedule\_name

sonicpoint\_profile\_widp\_sensor\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_2400mhz\_mode\_n\_only

sonicpoint\_profile\_radio\_2400mhz\_mode\_ngb\_mixed

sonicpoint\_profile\_radio\_2400mhz\_mode\_g\_only

sonicpoint\_profile\_radio\_2400mhz\_access\_list\_allow\_all

sonicpoint\_profile\_radio\_2400mhz\_access\_list\_allow\_default

sonicpoint\_profile\_radio\_2400mhz\_access\_list\_allow\_group

sonicpoint\_profile\_radio\_2400mhz\_access\_list\_deny\_default

sonicpoint\_profile\_radio\_2400mhz\_access\_list\_deny\_group

sonicpoint\_profile\_radio\_2400mhz\_schedule\_always\_on

sonicpoint\_profile\_radio\_2400mhz\_schedule\_name

sonicpoint\_profile\_radio\_2400mhz\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wep

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa2\_psk

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa2\_eap

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa2\_auto

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa2

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa3\_owe

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa3\_psk

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa3\_eap

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_profile\_radio\_2400mhz\_authentication\_type\_wpa3

sonicpoint\_profile\_radio\_2400mhz\_ids\_scan\_schedule\_name

sonicpoint\_profile\_radio\_2400mhz\_ids\_scan\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_2400mhz\_protection\_mode\_always

sonicpoint\_profile\_radio\_2400mhz\_protection\_mode\_auto

sonicpoint\_profile\_radio\_5000mhz\_access\_list\_allow\_all

sonicpoint\_profile\_radio\_5000mhz\_access\_list\_allow\_default

sonicpoint\_profile\_radio\_5000mhz\_access\_list\_allow\_group

sonicpoint\_profile\_radio\_5000mhz\_access\_list\_deny\_default

sonicpoint\_profile\_radio\_5000mhz\_access\_list\_deny\_group

sonicpoint\_profile\_radio\_5000mhz\_schedule\_always\_on

sonicpoint\_profile\_radio\_5000mhz\_schedule\_name

sonicpoint\_profile\_radio\_5000mhz\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wep

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa2\_psk

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa2\_eap

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa2\_auto

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa2

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa3\_owe

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa3\_psk

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa3\_eap

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_profile\_radio\_5000mhz\_authentication\_type\_wpa3

sonicpoint\_profile\_radio\_5000mhz\_ids\_scan\_schedule\_name

sonicpoint\_profile\_radio\_5000mhz\_ids\_scan\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_mode\_n\_only

sonicpoint\_profile\_radio\_mode\_ngb\_mixed

sonicpoint\_profile\_radio\_mode\_g\_only

sonicpoint\_profile\_radio\_mode\_5000mhz

sonicpoint\_profile\_radio\_access\_list\_allow\_all

sonicpoint\_profile\_radio\_access\_list\_allow\_default

sonicpoint\_profile\_radio\_access\_list\_allow\_group

sonicpoint\_profile\_radio\_access\_list\_deny\_default

sonicpoint\_profile\_radio\_access\_list\_deny\_group

sonicpoint\_profile\_radio\_schedule\_always\_on

sonicpoint\_profile\_radio\_schedule\_name

sonicpoint\_profile\_radio\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_authentication\_type\_wep

sonicpoint\_profile\_radio\_authentication\_type\_wpa

sonicpoint\_profile\_radio\_authentication\_type\_wpa2\_psk

sonicpoint\_profile\_radio\_authentication\_type\_wpa2\_eap

sonicpoint\_profile\_radio\_authentication\_type\_wpa2\_auto

sonicpoint\_profile\_radio\_authentication\_type\_wpa2

sonicpoint\_profile\_radio\_authentication\_type\_wpa3\_owe

sonicpoint\_profile\_radio\_authentication\_type\_wpa3\_psk

sonicpoint\_profile\_radio\_authentication\_type\_wpa3\_eap

sonicpoint\_profile\_radio\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_profile\_radio\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_profile\_radio\_authentication\_type\_wpa3

sonicpoint\_profile\_radio\_ids\_scan\_schedule\_name

sonicpoint\_profile\_radio\_ids\_scan\_schedule\_time\_of\_day

sonicpoint\_profile\_radio\_protection\_mode\_always

sonicpoint\_profile\_radio\_protection\_mode\_auto

sonicpoint\_profile\_radius\_nas\_identifier\_sonicpoint\_name

sonicpoint\_profile\_radius\_nas\_identifier\_sonicpoint\_mac\_address

sonicpoint\_profile\_radius\_nas\_identifier\_sonicpoint\_ssid

sonicpoint\_profile

sonicpoint\_profile\_collection

sonicpoint\_object\_packet\_capture\_mode\_2400mhz

sonicpoint\_object\_packet\_capture\_mode\_5000mhz

sonicpoint\_object\_band\_steering\_auto

sonicpoint\_object\_band\_steering\_prefer\_5ghz

sonicpoint\_object\_band\_steering\_force\_5ghz

sonicpoint\_object\_widp\_sensor\_schedule\_always\_on

sonicpoint\_object\_widp\_sensor\_schedule\_name

sonicpoint\_object\_widp\_sensor\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_2400mhz\_mode\_n\_only

sonicpoint\_object\_radio\_2400mhz\_mode\_ngb\_mixed

sonicpoint\_object\_radio\_2400mhz\_mode\_g\_only

sonicpoint\_object\_radio\_2400mhz\_access\_list\_allow\_all

sonicpoint\_object\_radio\_2400mhz\_access\_list\_allow\_default

sonicpoint\_object\_radio\_2400mhz\_access\_list\_allow\_group

sonicpoint\_object\_radio\_2400mhz\_access\_list\_deny\_default

sonicpoint\_object\_radio\_2400mhz\_access\_list\_deny\_group

sonicpoint\_object\_radio\_2400mhz\_schedule\_always\_on

sonicpoint\_object\_radio\_2400mhz\_schedule\_name

sonicpoint\_object\_radio\_2400mhz\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wep

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa2\_psk

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa2\_eap

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa2\_auto

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa2

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa3\_owe

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa3\_psk

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa3\_eap

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_object\_radio\_2400mhz\_authentication\_type\_wpa3

sonicpoint\_object\_radio\_2400mhz\_ids\_scan\_schedule\_name

sonicpoint\_object\_radio\_2400mhz\_ids\_scan\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_2400mhz\_protection\_mode\_always

sonicpoint\_object\_radio\_2400mhz\_protection\_mode\_auto

sonicpoint\_object\_radio\_5000mhz\_access\_list\_allow\_all

sonicpoint\_object\_radio\_5000mhz\_access\_list\_allow\_default

sonicpoint\_object\_radio\_5000mhz\_access\_list\_allow\_group

sonicpoint\_object\_radio\_5000mhz\_access\_list\_deny\_default

sonicpoint\_object\_radio\_5000mhz\_access\_list\_deny\_group

sonicpoint\_object\_radio\_5000mhz\_schedule\_always\_on

sonicpoint\_object\_radio\_5000mhz\_schedule\_name

sonicpoint\_object\_radio\_5000mhz\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wep

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa2\_psk

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa2\_eap

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa2\_auto

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa2

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa3\_owe

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa3\_psk

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa3\_eap

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_object\_radio\_5000mhz\_authentication\_type\_wpa3

sonicpoint\_object\_radio\_5000mhz\_ids\_scan\_schedule\_name

sonicpoint\_object\_radio\_5000mhz\_ids\_scan\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_mode\_n\_only

sonicpoint\_object\_radio\_mode\_ngb\_mixed

sonicpoint\_object\_radio\_mode\_g\_only

sonicpoint\_object\_radio\_mode\_5000mhz

sonicpoint\_object\_radio\_access\_list\_allow\_all

sonicpoint\_object\_radio\_access\_list\_allow\_default

sonicpoint\_object\_radio\_access\_list\_allow\_group

sonicpoint\_object\_radio\_access\_list\_deny\_default

sonicpoint\_object\_radio\_access\_list\_deny\_group

sonicpoint\_object\_radio\_schedule\_always\_on

sonicpoint\_object\_radio\_schedule\_name

sonicpoint\_object\_radio\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_authentication\_type\_wep

sonicpoint\_object\_radio\_authentication\_type\_wpa

sonicpoint\_object\_radio\_authentication\_type\_wpa2\_psk

sonicpoint\_object\_radio\_authentication\_type\_wpa2\_eap

sonicpoint\_object\_radio\_authentication\_type\_wpa2\_auto

sonicpoint\_object\_radio\_authentication\_type\_wpa2

sonicpoint\_object\_radio\_authentication\_type\_wpa3\_owe

sonicpoint\_object\_radio\_authentication\_type\_wpa3\_psk

sonicpoint\_object\_radio\_authentication\_type\_wpa3\_eap

sonicpoint\_object\_radio\_authentication\_type\_wpa3\_wpa2\_auto

sonicpoint\_object\_radio\_authentication\_type\_wpa3\_eap\_192b

sonicpoint\_object\_radio\_authentication\_type\_wpa3

sonicpoint\_object\_radio\_ids\_scan\_schedule\_name

sonicpoint\_object\_radio\_ids\_scan\_schedule\_time\_of\_day

sonicpoint\_object\_radio\_protection\_mode\_always

sonicpoint\_object\_radio\_protection\_mode\_auto

sonicpoint\_object\_radius\_nas\_identifier\_sonicpoint\_name

sonicpoint\_object\_radius\_nas\_identifier\_sonicpoint\_mac\_address

sonicpoint\_object\_radius\_nas\_identifier\_sonicpoint\_ssid

sonicpoint\_object

sonicpoint\_object\_collection

firmware\_management

firmware\_management\_reset\_sonicpoint\_raw\_action

firmware\_management\_reset\_sonicpoint\_n\_action

firmware\_management\_reset\_sonicpoint\_nv\_action

firmware\_management\_reset\_sonicpoint\_ndr\_action

firmware\_management\_reset\_sonicpoint\_ac\_action

firmware\_management\_reset\_sonicwave400\_action

firmware\_management\_reset\_sonicwave200\_action

import\_sonicpoint\_firmware\_sonicpoint\_raw

import\_sonicpoint\_firmware\_sonicpoint\_n

import\_sonicpoint\_firmware\_sonicpoint\_nv

import\_sonicpoint\_firmware\_sonicpoint\_ndr

import\_sonicpoint\_firmware\_sonicpoint\_ac

import\_sonicpoint\_firmware\_sonicwave400

import\_sonicpoint\_firmware\_sonicwave200

widp\_authorized\_access\_point\_all

widp\_authorized\_access\_point\_group

widp\_rogue\_access\_point\_all

widp\_rogue\_access\_point\_group

widp\_block\_traffic\_all

widp\_block\_traffic\_group

widp

rf\_monitoring

fairnet

fairnet\_policies

fairnet\_policies\_collection

sonicpoint\_synchronize\_action

sonicpoint\_register\_action

sonicpoint\_upgrade

sonicpoint\_reboot\_action

sonicpoint\_reboot\_sonicpoint\_action

sonicpoint\_ids\_scan\_all\_action

sonicpoint\_ids\_scan\_both\_action

sonicpoint\_ids\_scan\_2400mhz\_action

sonicpoint\_ids\_scan\_5000mhz\_action

sonicpoint\_ids\_authorizing\_ap\_action

sonicpoint\_rf\_monitoring\_watch\_station\_action

rrm

sonicpoint\_rrm\_force\_switch\_action

wmm

wmm\_collection

cli\_idle\_timeout

cli\_screen

cli\_show\_unmodified

cli\_pager

cli\_interactive\_prompts

cli\_ftp

cli\_banner

security\_services

security\_services\_synchronize\_action

import\_security\_services\_signature

import\_security\_services\_geoip

import\_security\_services\_botnet

geo\_ip\_countries

geo\_ip\_countries\_collection

geo\_ip\_base\_block\_connections\_all

geo\_ip\_base\_block\_connections\_firewall\_rule\_based

geo\_ip\_base\_exclude\_name

geo\_ip\_base\_exclude\_group

geo\_ip\_base\_logo\_icon\_data

geo\_ip\_base\_logo\_icon\_ftp

geo\_ip\_base

geo\_ip\_addresses

geo\_ip\_addresses\_collection

botnet\_exclude\_name

botnet\_exclude\_group

botnet\_logo\_icon\_data

botnet\_logo\_icon\_ftp

botnet

botnet\_custom\_list\_address

botnet\_custom\_list\_address\_collection

botnet\_flush\_action

botnet\_download\_action

botnet\_blocked\_page\_default\_action

anti\_spyware\_global

anti\_spyware\_exclusion\_list\_exclusion\_address\_object\_name

anti\_spyware\_exclusion\_list\_exclusion\_address\_object\_group

anti\_spyware\_exclusion\_list

anti\_spyware\_exclusion\_entry

anti\_spyware\_exclusion\_entry\_collection

anti\_spyware\_product\_prevention\_global

anti\_spyware\_product\_prevention\_enable

anti\_spyware\_product\_detection\_global

anti\_spyware\_product\_detection\_enable

anti\_spyware\_product\_included\_users\_all

anti\_spyware\_product\_included\_users\_guests

anti\_spyware\_product\_included\_users\_administrator

anti\_spyware\_product\_included\_users\_name

anti\_spyware\_product\_included\_users\_group

anti\_spyware\_product\_included\_ip\_all

anti\_spyware\_product\_included\_ip\_name

anti\_spyware\_product\_included\_ip\_group

anti\_spyware\_product\_excluded\_users\_all

anti\_spyware\_product\_excluded\_users\_guests

anti\_spyware\_product\_excluded\_users\_administrator

anti\_spyware\_product\_excluded\_users\_name

anti\_spyware\_product\_excluded\_users\_group

anti\_spyware\_product\_excluded\_ip\_all

anti\_spyware\_product\_excluded\_ip\_name

anti\_spyware\_product\_excluded\_ip\_group

anti\_spyware\_product\_schedule\_always\_on

anti\_spyware\_product\_schedule\_name

anti\_spyware\_product\_schedule\_days

anti\_spyware\_product\_log\_redundancy\_global

anti\_spyware\_product\_log\_redundancy\_filter

anti\_spyware\_product

anti\_spyware\_product\_collection

anti\_spyware\_policy\_prevention\_product

anti\_spyware\_policy\_prevention\_enable

anti\_spyware\_policy\_detection\_product

anti\_spyware\_policy\_detection\_enable

anti\_spyware\_policy\_included\_users\_product

anti\_spyware\_policy\_included\_users\_all

anti\_spyware\_policy\_included\_users\_guests

anti\_spyware\_policy\_included\_users\_administrator

anti\_spyware\_policy\_included\_users\_name

anti\_spyware\_policy\_included\_users\_group

anti\_spyware\_policy\_included\_ip\_product

anti\_spyware\_policy\_included\_ip\_all

anti\_spyware\_policy\_included\_ip\_name

anti\_spyware\_policy\_included\_ip\_group

anti\_spyware\_policy\_excluded\_users\_product

anti\_spyware\_policy\_excluded\_users\_all

anti\_spyware\_policy\_excluded\_users\_guests

anti\_spyware\_policy\_excluded\_users\_administrator

anti\_spyware\_policy\_excluded\_users\_name

anti\_spyware\_policy\_excluded\_users\_group

anti\_spyware\_policy\_excluded\_ip\_product

anti\_spyware\_policy\_excluded\_ip\_all

anti\_spyware\_policy\_excluded\_ip\_name

anti\_spyware\_policy\_excluded\_ip\_group

anti\_spyware\_policy\_schedule\_product

anti\_spyware\_policy\_schedule\_always\_on

anti\_spyware\_policy\_schedule\_name

anti\_spyware\_policy\_schedule\_days

anti\_spyware\_policy\_log\_redundancy\_product

anti\_spyware\_policy\_log\_redundancy\_filter

anti\_spyware\_policy

anti\_spyware\_policy\_collection

anti\_spyware\_update\_signatures\_action

anti\_spyware\_reset\_action

intrusion\_prevention\_global

intrusion\_prevention\_exclusion\_list

intrusion\_prevention\_exclusion\_list\_entry

intrusion\_prevention\_exclusion\_list\_entry\_collection

intrusion\_prevention\_category\_prevention\_global

intrusion\_prevention\_category\_prevention\_enable

intrusion\_prevention\_category\_detection\_global

intrusion\_prevention\_category\_detection\_enable

intrusion\_prevention\_category\_included\_users\_all

intrusion\_prevention\_category\_included\_users\_guests

intrusion\_prevention\_category\_included\_users\_administrator

intrusion\_prevention\_category\_included\_users\_name

intrusion\_prevention\_category\_included\_users\_group

intrusion\_prevention\_category\_included\_ip\_all

intrusion\_prevention\_category\_included\_ip\_name

intrusion\_prevention\_category\_included\_ip\_group

intrusion\_prevention\_category\_excluded\_users\_guests

intrusion\_prevention\_category\_excluded\_users\_administrator

intrusion\_prevention\_category\_excluded\_users\_name

intrusion\_prevention\_category\_excluded\_users\_group

intrusion\_prevention\_category\_excluded\_ip\_name

intrusion\_prevention\_category\_excluded\_ip\_group

intrusion\_prevention\_category\_schedule\_always\_on

intrusion\_prevention\_category\_schedule\_name

intrusion\_prevention\_category\_schedule\_days

intrusion\_prevention\_category\_log\_redundancy\_global

intrusion\_prevention\_category\_log\_redundancy\_filter

intrusion\_prevention\_category

intrusion\_prevention\_category\_collection

intrusion\_prevention\_policy\_prevention\_category

intrusion\_prevention\_policy\_prevention\_enable

intrusion\_prevention\_policy\_detection\_category

intrusion\_prevention\_policy\_detection\_enable

intrusion\_prevention\_policy\_included\_users\_category

intrusion\_prevention\_policy\_included\_users\_all

intrusion\_prevention\_policy\_included\_users\_guests

intrusion\_prevention\_policy\_included\_users\_administrator

intrusion\_prevention\_policy\_included\_users\_name

intrusion\_prevention\_policy\_included\_users\_group

intrusion\_prevention\_policy\_included\_ip\_category

intrusion\_prevention\_policy\_included\_ip\_all

intrusion\_prevention\_policy\_included\_ip\_name

intrusion\_prevention\_policy\_included\_ip\_group

intrusion\_prevention\_policy\_excluded\_users\_category

intrusion\_prevention\_policy\_excluded\_users\_guests

intrusion\_prevention\_policy\_excluded\_users\_administrator

intrusion\_prevention\_policy\_excluded\_users\_name

intrusion\_prevention\_policy\_excluded\_users\_group

intrusion\_prevention\_policy\_excluded\_ip\_category

intrusion\_prevention\_policy\_excluded\_ip\_name

intrusion\_prevention\_policy\_excluded\_ip\_group

intrusion\_prevention\_policy\_schedule\_category

intrusion\_prevention\_policy\_schedule\_always\_on

intrusion\_prevention\_policy\_schedule\_name

intrusion\_prevention\_policy\_schedule\_days

intrusion\_prevention\_policy\_log\_redundancy\_category

intrusion\_prevention\_policy\_log\_redundancy\_filter

intrusion\_prevention\_policy\_direction\_both

intrusion\_prevention\_policy\_direction\_incoming

intrusion\_prevention\_policy\_direction\_outgoing

intrusion\_prevention\_policy

intrusion\_prevention\_policy\_collection

intrusion\_prevention\_update\_signatures\_action

intrusion\_prevention\_reset\_action

gateway\_antivirus\_exclusion\_object\_http\_name

gateway\_antivirus\_exclusion\_object\_http\_group

gateway\_antivirus\_exclusion\_object\_ftp\_name

gateway\_antivirus\_exclusion\_object\_ftp\_group

gateway\_antivirus\_exclusion\_object\_imap\_name

gateway\_antivirus\_exclusion\_object\_imap\_group

gateway\_antivirus\_exclusion\_object\_smtp\_name

gateway\_antivirus\_exclusion\_object\_smtp\_group

gateway\_antivirus\_exclusion\_object\_pop3\_name

gateway\_antivirus\_exclusion\_object\_pop3\_group

gateway\_antivirus\_exclusion\_object\_cifs\_netbios\_name

gateway\_antivirus\_exclusion\_object\_cifs\_netbios\_group

gateway\_antivirus

gateway\_antivirus\_cloud

gateway\_antivirus\_cloud\_exclusion

gateway\_antivirus\_cloud\_exclusion\_collection

gateway\_antivirus\_exclusion\_list

gateway\_antivirus\_exclusion\_entry

gateway\_antivirus\_exclusion\_entry\_collection

gateway\_antivirus\_signatures

gateway\_antivirus\_signatures\_collection

gateway\_antivirus\_reset\_settings\_action

gateway\_antivirus\_update\_signatures\_action

capture\_atp\_base\_file\_size\_default

capture\_atp\_base\_file\_size\_restrict

capture\_atp\_base\_exclude\_address\_for\_capture\_atp\_name

capture\_atp\_base\_exclude\_address\_for\_capture\_atp\_group

capture\_atp\_base\_exclude\_address\_for\_block\_until\_verdict\_name

capture\_atp\_base\_exclude\_address\_for\_block\_until\_verdict\_group

capture\_atp\_base

capture\_atp\_md5\_exclusions

capture\_atp\_md5\_exclusions\_collection

capture\_atp\_http\_exclusions

capture\_atp\_http\_exclusions\_collection

capture\_atp\_test\_uftp\_connectivity\_action

capture\_atp\_clear\_uftp\_connectivity\_action

capture\_atp\_refresh\_uftp\_connectivity\_action

capture\_atp\_check\_md5\_query\_status\_action

capture\_atp\_clear\_md5\_query\_status\_action

capture\_atp\_refresh\_md5\_query\_status\_action

anti\_spam

anti\_spam\_allow\_list\_name

anti\_spam\_allow\_list\_host

anti\_spam\_allow\_list\_fqdn

anti\_spam\_allow\_list\_range

anti\_spam\_allow\_list

anti\_spam\_allow\_list\_collection

anti\_spam\_reject\_list\_name

anti\_spam\_reject\_list\_host

anti\_spam\_reject\_list\_fqdn

anti\_spam\_reject\_list\_range

anti\_spam\_reject\_list

anti\_spam\_reject\_list\_collection

anti\_spam\_start\_capture\_action

anti\_spam\_stop\_capture\_action

anti\_spam\_export\_capture\_ftp\_action

anti\_spam\_export\_capture\_scp\_action

anti\_spam\_grid\_ip\_check\_action

anti\_spam\_mxlookup\_action

anti\_spam\_destination\_mail\_server\_action

rbl\_base\_dns\_inherit

rbl\_base\_dns\_static

rbl\_base

rbl\_services

rbl\_services\_collection

dpi\_ssh\_include\_address\_all

dpi\_ssh\_include\_address\_name

dpi\_ssh\_include\_address\_group

dpi\_ssh\_include\_service\_all

dpi\_ssh\_include\_service\_name

dpi\_ssh\_include\_service\_group

dpi\_ssh\_include\_service\_protocol

dpi\_ssh\_include\_user\_all

dpi\_ssh\_include\_user\_guests

dpi\_ssh\_include\_user\_administrator

dpi\_ssh\_include\_user\_name

dpi\_ssh\_include\_user\_group

dpi\_ssh\_exclude\_address\_name

dpi\_ssh\_exclude\_address\_group

dpi\_ssh\_exclude\_service\_name

dpi\_ssh\_exclude\_service\_group

dpi\_ssh\_exclude\_service\_protocol

dpi\_ssh\_exclude\_user\_administrator

dpi\_ssh\_exclude\_user\_guests

dpi\_ssh\_exclude\_user\_name

dpi\_ssh\_exclude\_user\_group

dpi\_ssh

dpi\_ssl\_server\_include\_address\_all

dpi\_ssl\_server\_include\_address\_name

dpi\_ssl\_server\_include\_address\_group

dpi\_ssl\_server\_include\_user\_all

dpi\_ssl\_server\_include\_user\_guests

dpi\_ssl\_server\_include\_user\_administrator

dpi\_ssl\_server\_include\_user\_name

dpi\_ssl\_server\_include\_user\_group

dpi\_ssl\_server\_exclude\_address\_name

dpi\_ssl\_server\_exclude\_address\_group

dpi\_ssl\_server\_exclude\_user\_administrator

dpi\_ssl\_server\_exclude\_user\_guests

dpi\_ssl\_server\_exclude\_user\_name

dpi\_ssl\_server\_exclude\_user\_group

dpi\_ssl\_server

dpi\_ssl\_server\_ssl\_servers

dpi\_ssl\_server\_ssl\_servers\_collection

dpi\_ssl\_client\_resigning\_authority\_default

dpi\_ssl\_client\_resigning\_authority\_certificate

dpi\_ssl\_client\_include\_address\_all

dpi\_ssl\_client\_include\_address\_name

dpi\_ssl\_client\_include\_address\_group

dpi\_ssl\_client\_include\_service\_all

dpi\_ssl\_client\_include\_service\_name

dpi\_ssl\_client\_include\_service\_group

dpi\_ssl\_client\_include\_service\_protocol

dpi\_ssl\_client\_include\_user\_all

dpi\_ssl\_client\_include\_user\_guests

dpi\_ssl\_client\_include\_user\_administrator

dpi\_ssl\_client\_include\_user\_name

dpi\_ssl\_client\_include\_user\_group

dpi\_ssl\_client\_exclude\_address\_name

dpi\_ssl\_client\_exclude\_address\_group

dpi\_ssl\_client\_exclude\_service\_name

dpi\_ssl\_client\_exclude\_service\_group

dpi\_ssl\_client\_exclude\_service\_protocol

dpi\_ssl\_client\_exclude\_user\_administrator

dpi\_ssl\_client\_exclude\_user\_guests

dpi\_ssl\_client\_exclude\_user\_name

dpi\_ssl\_client\_exclude\_user\_group

dpi\_ssl\_client\_cfs\_categories\_include

dpi\_ssl\_client\_cfs\_categories\_exclude

dpi\_ssl\_client

dpi\_ssl\_client\_cfs\_categories

dpi\_ssl\_client\_cfs\_categories\_collection

dpi\_ssl\_client\_common\_names\_statistics\_reporting

dpi\_ssl\_client\_common\_names\_action\_exclude\_authenticate\_server

dpi\_ssl\_client\_common\_names\_action\_exclude\_disable\_authenticate\_server

dpi\_ssl\_client\_common\_names\_action\_exclude

dpi\_ssl\_client\_common\_names\_action\_skip\_content\_filter\_exclusion

dpi\_ssl\_client\_common\_names\_action\_skip\_authentication

dpi\_ssl\_client\_common\_names

dpi\_ssl\_client\_common\_names\_collection

dpi\_ssl\_client\_reject\_action

dpi\_ssl\_client\_accept\_action

dpi\_ssl\_client\_export\_cert

dpi\_ssl\_client\_import\_excl

cipher\_control\_tls\_cipher\_action

cipher\_control\_tls

cipher\_control\_tls\_collection

cipher\_control\_ssh

appflow

appflow\_gmsflow\_server

appflow\_server

appflow\_sfr\_mailing

appflow\_external\_collector

appflow\_default\_action

appflow\_gmsflow\_server\_synchronize\_action

appflow\_gmsflow\_server\_synchronize\_log\_settings\_action

appflow\_gmsflow\_server\_test\_connectivity\_action

appflow\_gmsflow\_server\_2\_synchronize\_action

appflow\_gmsflow\_server\_2\_synchronize\_log\_settings\_action

appflow\_gmsflow\_server\_2\_test\_connectivity\_action

appflow\_server\_synchronize\_action

appflow\_server\_2\_synchronize\_action

appflow\_server\_synchronize\_logs\_action

appflow\_server\_2\_synchronize\_logs\_action

appflow\_server\_test\_connectivity\_action

appflow\_server\_2\_test\_connectivity\_action

appflow\_server\_flush\_servers\_action

appflow\_server\_discover\_action

appflow\_sfr\_mailing\_test\_email

appflow\_external\_collector\_generate\_all\_templates\_action

appflow\_external\_collector\_generate\_static\_appflow\_data\_action

appflow\_external\_collector\_send\_all\_entries\_action

appflow\_send\_report

cta\_report

reset\_appflow\_report\_action

vpn\_policies\_all

vpn\_renegotiate\_tunnel\_action

vpn\_use\_radius\_mschap

vpn\_use\_radius\_mschapv2

vpn\_dns\_server\_inherit

vpn\_dns\_server\_static

vpn

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_auth\_method\_shared\_secret

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_auth\_method\_certificate\_peer\_id\_domain\_name

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_auth\_method\_certificate\_peer\_id\_email\_id

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_auth\_method\_certificate\_peer\_id\_distinguished\_name

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_auth\_method\_certificate

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_encryption\_des

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_encryption\_triple\_des

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_encryption\_aes\_128

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_encryption\_aes\_192

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_encryption\_aes\_256

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_authentication\_md5

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_authentication\_sha\_1

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_authentication\_sha\_256

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_authentication\_sha\_384

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_authentication\_sha\_512

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_proposal\_ipsec\_authentication\_aes\_xcbc

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_require\_xauth

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_allow\_unauthenticated\_name

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_allow\_unauthenticated\_group

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_allow\_unauthenticated\_host

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_allow\_unauthenticated\_range

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_allow\_unauthenticated\_network

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_client\_authentication\_allow\_unauthenticated

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_ike\_mode\_configuration\_ip\_pool\_name

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_ike\_mode\_configuration\_ip\_pool\_host

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_ike\_mode\_configuration\_ip\_pool\_range

vpn\_policy\_ipv4\_group\_vpn\_ipv4\_group\_vpn\_ike\_mode\_configuration\_ip\_pool\_network

vpn\_policy\_ipv4\_group\_vpn

vpn\_policy\_ipv4\_group\_vpn\_collection

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_manual\_key

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_ipv4

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_domain\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_email\_address

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_firewall\_id

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_key\_id

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_ipv4

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_domain\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_email\_address

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_firewall\_id

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_key\_id

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_shared\_secret

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_distinguished\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_email\_id

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_domain\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_ip

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_auth\_method\_certificate

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_des

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_triple\_des

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_128

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_192

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_256

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gcm16\_128

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gcm16\_192

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gcm16\_256

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gmac\_128

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gmac\_192

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gmac\_256

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_authentication\_md5

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_1

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_256

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_384

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_512

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_proposal\_ipsec\_authentication\_aes\_xcbc

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_any

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_dhcp

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_group

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_host

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_range

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_local\_network

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_any

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_dhcp

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_ikev2\_ip\_pool\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_ikev2\_ip\_pool\_host

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_ikev2\_ip\_pool\_range

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_ikev2\_ip\_pool\_network

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_ikev2\_ip\_pool

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_destination\_network\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_destination\_network\_group

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_destination\_network\_host

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_destination\_network\_range

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_destination\_network\_network

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_network\_remote\_destination\_network

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_local\_original

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_local\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_local\_group

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_local\_host

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_local\_range

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_local\_network

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_remote\_original

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_remote\_name

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_remote\_group

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_remote\_host

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_remote\_range

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_translated\_network\_remote\_network

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_bound\_to\_zone

vpn\_policy\_ipv4\_site\_to\_site\_ipv4\_site\_to\_site\_bound\_to\_interface

vpn\_policy\_ipv4\_site\_to\_site

vpn\_policy\_ipv4\_site\_to\_site\_collection

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_manual\_key

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_local\_ipv4

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_local\_domain\_name

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_local\_email\_address

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_local\_firewall\_id

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_local\_key\_id

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_peer\_ipv4

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_peer\_domain\_name

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_peer\_email\_address

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_peer\_firewall\_id

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret\_ike\_id\_peer\_key\_id

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_shared\_secret

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_certificate\_ike\_id\_peer\_distinguished\_name

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_certificate\_ike\_id\_peer\_email\_id

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_certificate\_ike\_id\_peer\_domain\_name

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_certificate\_ike\_id\_peer\_ip

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_auth\_method\_certificate

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_des

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_triple\_des

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_128

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_192

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_256

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_gcm16\_128

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_gcm16\_192

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_gcm16\_256

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_gmac\_128

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_gmac\_192

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_encryption\_aes\_gmac\_256

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_authentication\_md5

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_authentication\_sha\_1

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_authentication\_sha\_256

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_authentication\_sha\_384

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_authentication\_sha\_512

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_proposal\_ipsec\_authentication\_aes\_xcbc

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_bound\_to\_zone

vpn\_policy\_ipv4\_tunnel\_interface\_ipv4\_tunnel\_interface\_bound\_to\_interface

vpn\_policy\_ipv4\_tunnel\_interface

vpn\_policy\_ipv4\_tunnel\_interface\_collection

vpn\_policy\_ipv4\_provision\_client\_ipv4\_provision\_client\_auth\_method\_shared\_secret

vpn\_policy\_ipv4\_provision\_client\_ipv4\_provision\_client\_auth\_method\_certificate

vpn\_policy\_ipv4\_provision\_client

vpn\_policy\_ipv4\_provision\_client\_collection

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_auth\_method\_shared\_secret

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_auth\_method\_certificate\_client\_id\_peer\_distinguished\_name

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_auth\_method\_certificate\_client\_id\_peer\_email\_id

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_auth\_method\_certificate\_client\_id\_peer\_domain\_name

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_auth\_method\_certificate\_client\_id\_peer\_ip

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_auth\_method\_certificate

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_require\_xauth

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_allow\_unauthenticated\_name

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_allow\_unauthenticated\_group

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_allow\_unauthenticated\_host

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_allow\_unauthenticated\_range

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_allow\_unauthenticated\_network

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_local\_allow\_unauthenticated

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_nat\_proxy

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_nat\_pool\_name

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_nat\_pool\_host

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_nat\_pool\_range

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_nat\_pool\_network

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_nat\_pool

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_destination\_network\_name

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_destination\_network\_group

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_destination\_network\_host

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_destination\_network\_range

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_destination\_network\_network

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_network\_remote\_destination\_network

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_des

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_triple\_des

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_128

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_192

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_256

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_gcm16\_128

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_gcm16\_192

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_gcm16\_256

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_gmac\_128

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_gmac\_192

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_encryption\_aes\_gmac\_256

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_authentication\_md5

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_authentication\_sha\_1

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_authentication\_sha\_256

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_authentication\_sha\_384

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_authentication\_sha\_512

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_proposal\_ipsec\_authentication\_aes\_xcbc

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_bound\_to\_zone

vpn\_policy\_ipv4\_provision\_server\_ipv4\_provision\_server\_bound\_to\_interface

vpn\_policy\_ipv4\_provision\_server

vpn\_policy\_ipv4\_provision\_server\_collection

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_manual\_key

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_ipv4

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_ipv6

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_domain\_name

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_email\_address

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_firewall\_id

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_local\_key\_id

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_ipv4

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_ipv6

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_domain\_name

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_email\_address

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_firewall\_id

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret\_ike\_id\_peer\_key\_id

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_shared\_secret

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_distinguished\_name

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_email\_id

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_domain\_name

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_certificate\_ike\_id\_peer\_ip

vpn\_policy\_ipv6\_site\_to\_site\_auth\_method\_certificate

vpn\_policy\_ipv6\_site\_to\_site\_network\_local\_name

vpn\_policy\_ipv6\_site\_to\_site\_network\_local\_group

vpn\_policy\_ipv6\_site\_to\_site\_network\_local\_host

vpn\_policy\_ipv6\_site\_to\_site\_network\_local\_range

vpn\_policy\_ipv6\_site\_to\_site\_network\_local\_network

vpn\_policy\_ipv6\_site\_to\_site\_network\_remote\_destination\_network\_name

vpn\_policy\_ipv6\_site\_to\_site\_network\_remote\_destination\_network\_group

vpn\_policy\_ipv6\_site\_to\_site\_network\_remote\_destination\_network\_host

vpn\_policy\_ipv6\_site\_to\_site\_network\_remote\_destination\_network\_range

vpn\_policy\_ipv6\_site\_to\_site\_network\_remote\_destination\_network\_network

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_des

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_triple\_des

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_128

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_192

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_256

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gcm16\_128

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gcm16\_192

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gcm16\_256

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gmac\_128

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gmac\_192

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_encryption\_aes\_gmac\_256

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_authentication\_md5

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_1

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_256

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_384

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_authentication\_sha\_512

vpn\_policy\_ipv6\_site\_to\_site\_proposal\_ipsec\_authentication\_aes\_xcbc

vpn\_policy\_ipv6\_site\_to\_site\_bound\_to\_zone

vpn\_policy\_ipv6\_site\_to\_site\_bound\_to\_interface

vpn\_policy\_ipv6\_site\_to\_site\_local\_ip\_primary

vpn\_policy\_ipv6\_site\_to\_site\_local\_ip\_custom

vpn\_policy\_ipv6

vpn\_policy\_ipv6\_collection

export\_group\_vpn\_policy\_spd

export\_group\_vpn\_policy\_rcf

vpn\_l2tp\_server\_l2tp\_server\_ip\_pool\_provided

vpn\_l2tp\_server\_l2tp\_server\_ip\_pool\_local

vpn\_l2tp\_server

vpn\_l2tp\_server\_ppp

vpn\_l2tp\_server\_ppp\_collection

dhcp\_over\_vpn\_global

dhcp\_over\_vpn\_base\_central

dhcp\_over\_vpn\_base\_remote

dhcp\_over\_vpn\_static\_devices

dhcp\_over\_vpn\_static\_devices\_collection

dhcp\_over\_vpn\_excluded\_devices

dhcp\_over\_vpn\_excluded\_devices\_collection

dhcp\_over\_vpn\_servers

dhcp\_over\_vpn\_servers\_collection

ssl\_control\_base

ssl\_control\_whitelist\_certificates

ssl\_control\_whitelist\_certificates\_collection

ssl\_control\_blacklist\_certificates

ssl\_control\_blacklist\_certificates\_collection

ssl\_vpn\_server\_logout\_action

ssl\_vpn\_logout\_action

ssl\_vpn\_server\_certificate\_use\_self\_signed

ssl\_vpn\_server\_certificate\_name

ssl\_vpn\_server\_use\_radius\_mschap

ssl\_vpn\_server\_use\_radius\_mschapv2

ssl\_vpn\_server\_download\_url\_default

ssl\_vpn\_server\_download\_url\_custom

ssl\_vpn\_server

ssl\_vpn\_server\_access

ssl\_vpn\_server\_access\_collection

ssl\_vpn\_portal\_home\_page\_message\_default

ssl\_vpn\_portal\_home\_page\_message\_custom

ssl\_vpn\_portal\_login\_message\_default

ssl\_vpn\_portal\_login\_message\_custom

ssl\_vpn\_portal\_logo\_default

ssl\_vpn\_portal\_logo\_custom

ssl\_vpn\_portal

ssl\_vpn\_device\_profile\_network\_address\_ipv6\_name

ssl\_vpn\_device\_profile\_network\_address\_ipv6\_host

ssl\_vpn\_device\_profile\_network\_address\_ipv6\_range

ssl\_vpn\_device\_profile\_network\_address\_ipv6\_network

ssl\_vpn\_device\_profile\_network\_address\_ipv4\_name

ssl\_vpn\_device\_profile\_network\_address\_ipv4\_host

ssl\_vpn\_device\_profile\_network\_address\_ipv4\_range

ssl\_vpn\_device\_profile\_network\_address\_ipv4\_network

ssl\_vpn\_device\_profile\_client\_cache\_user\_name\_only

ssl\_vpn\_device\_profile\_client\_cache\_credentials

ssl\_vpn\_device\_profile\_routes\_route\_ipv4\_name

ssl\_vpn\_device\_profile\_routes\_route\_ipv4\_group

ssl\_vpn\_device\_profile\_routes\_route\_ipv4

ssl\_vpn\_device\_profile\_routes\_route\_ipv6\_name

ssl\_vpn\_device\_profile\_routes\_route\_ipv6\_group

ssl\_vpn\_device\_profile\_routes\_route\_ipv6

ssl\_vpn\_device\_profile

ssl\_vpn\_device\_profile\_collection

ssl\_vpn\_device\_profile\_client\_dns\_inherit\_action

ssl\_vpn\_bookmark\_service\_rdp\_automatic\_login\_ssl\_vpn

ssl\_vpn\_bookmark\_service\_rdp\_automatic\_login\_custom

ssl\_vpn\_bookmark

ssl\_vpn\_bookmark\_collection

virtual\_assist

virtual\_assist\_deny\_requests\_host

virtual\_assist\_deny\_requests\_network

virtual\_assist\_deny\_requests

virtual\_assist\_deny\_requests\_collection

virtual\_assist\_logout\_action

voip\_sip\_transforms\_in\_service\_object\_name

voip\_sip\_transforms\_in\_service\_object\_group

voip

voip\_flush\_action

ha\_base\_mode\_active\_standby

ha\_base\_mode\_active\_active\_dpi

ha\_base

ha\_monitoring\_ipv4

ha\_monitoring\_ipv4\_collection

ha\_monitoring\_ipv6

ha\_monitoring\_ipv6\_collection

ha\_reporting

ha\_synchronize\_settings\_action

ha\_synchronize\_firmware\_action

ha\_force\_failover\_action

sdwan\_sla\_class\_objects

sdwan\_sla\_class\_objects\_collection

sdwan\_path\_selection\_profiles

sdwan\_path\_selection\_profiles\_collection

sdwan\_sla\_probe\_ipv4\_probe\_target\_name

sdwan\_sla\_probe\_ipv4\_probe\_target\_host

sdwan\_sla\_probe\_ipv4\_probe\_target\_fqdn

sdwan\_sla\_probe\_ipv4\_probe\_type\_ping

sdwan\_sla\_probe\_ipv4\_probe\_type\_tcp

sdwan\_sla\_probe\_ipv4

sdwan\_sla\_probe\_ipv4\_collection

sdwan\_group

sdwan\_group\_collection

threat

import\_packet\_replay

packet\_replay\_delete\_packet\_replay\_file\_action

packet\_replay\_replay

packet\_replay\_individual\_replay

packet\_replay\_replay\_mac

packet\_replay\_clear\_packets\_action

packet\_replay\_refresh\_packets\_action

packet\_replay\_packet\_crafting\_udp

packet\_replay\_packet\_crafting\_icmp

packet\_replay\_packet\_crafting\_igmp

packet\_replay\_packet\_crafting\_buffer

export\_replayed\_packets

amazon\_web\_services\_connection

amazon\_web\_services\_objects

amazon\_web\_services\_force\_sync

aws\_object\_address\_group\_mapping\_condition\_custom\_key

aws\_object\_address\_group\_mapping\_condition\_instance\_property

aws\_object\_address\_group\_mapping

aws\_object\_address\_group\_mapping\_collection

switch\_trunk\_ports

switch\_trunk\_ports\_collection

switch\_vlan\_trunk\_enable\_vlan\_action

switch\_portshield\_ports

switch\_portshield\_ports\_collection

switch\_l2\_discover\_interface

switch\_l2\_discover\_interface\_collection

switch\_lldp

switch\_lldp\_profiles\_admin\_status\_rx\_only

switch\_lldp\_profiles\_admin\_status\_tx\_only

switch\_lldp\_profiles\_admin\_status\_rx\_and\_tx

switch\_lldp\_profiles

switch\_lldp\_profiles\_collection

switch\_link\_aggregation\_ports\_key\_id

switch\_link\_aggregation\_ports\_load\_balance\_type\_source

switch\_link\_aggregation\_ports\_load\_balance\_type\_destination

switch\_link\_aggregation\_ports\_load\_balance\_type\_source\_destination

switch\_link\_aggregation\_ports

switch\_link\_aggregation\_ports\_collection

switch\_port\_mirrors

switch\_port\_mirrors\_collection

switch\_discover\_action

switch\_controller\_switch

switch\_controller\_switch\_collection

switch\_controller\_port\_link\_speed\_auto\_negotiate

switch\_controller\_port\_link\_speed\_half

switch\_controller\_port\_link\_speed\_full

switch\_controller\_port

switch\_controller\_port\_collection

switch\_controller\_voice\_vlan

switch\_controller\_voice\_vlan\_collection

switch\_controller\_switch\_info

switch\_controller\_switch\_info\_collection

switch\_controller\_authorize\_action

switch\_controller\_restart\_action

switch\_controller\_fw\_upgrade\_action

switch\_controller\_network\_ip\_dhcp

switch\_controller\_network\_ip\_static

switch\_controller\_network

switch\_controller\_network\_collection

switch\_controller\_radius

switch\_controller\_radius\_collection

switch\_controller\_route

switch\_controller\_route\_collection

switch\_controller\_user

switch\_controller\_user\_collection

switch\_controller\_arp

switch\_controller\_arp\_collection

switch\_controller\_arp\_aging\_time

switch\_controller\_arp\_aging\_time\_collection

switch\_controller\_qos

switch\_controller\_qos\_collection

switch\_controller\_qos\_dscp

switch\_controller\_qos\_dscp\_collection

switch\_controller\_qos\_cos

switch\_controller\_qos\_cos\_collection

switch\_controller\_statistics\_clear\_action

dell\_switch\_switch

dell\_switch\_switch\_collection

dell\_switch\_port\_link\_speed\_auto\_negotiate

dell\_switch\_port\_link\_speed\_half

dell\_switch\_port\_link\_speed\_full

dell\_switch\_port

dell\_switch\_port\_collection

dell\_switch\_restart\_action

dell\_switch\_statistics\_clear\_action

dell\_switch\_upload\_firmware

dell\_switch\_statistics\_reporting

dell\_switch\_firmware\_mgmt\_reporting

dell\_switch\_ports\_reporting

dell\_switch\_status\_reporting

dell\_switch\_product\_info\_reporting

portshield\_groups\_external\_switch

portshield\_groups\_external\_switch\_collection

diag\_advanced

diag\_advanced\_log

diag\_advanced\_threat\_api

diag\_advanced\_dpi\_stateful\_firewall\_security\_action

diag\_advanced\_stateful\_firewall\_security\_action

diag\_advanced\_arp

diag\_advanced\_preference

diag\_advanced\_user\_authentication\_advanced\_user\_authentication\_user\_ip\_all

diag\_advanced\_user\_authentication\_advanced\_user\_authentication\_user\_ip\_name

diag\_advanced\_user\_authentication\_advanced\_user\_authentication\_user\_ip\_group

diag\_advanced\_user\_authentication

diag\_advanced\_user\_authentication\_flush\_cached\_redirect\_files\_action

diag\_advanced\_user\_authentication\_logout\_users\_action

diag\_advanced\_user\_authentication\_kill\_all\_inactive\_users\_action

diag\_advanced\_arp\_send\_system\_arps\_action

diag\_advanced\_network

diag\_advanced\_dns

diag\_advanced\_dns\_proxy

diag\_advanced\_wan\_acceleration

diag\_advanced\_wan\_acceleration\_clear\_debug\_stats\_action

diag\_advanced\_wan\_acceleration\_clear\_tcp\_acceleration\_action

diag\_advanced\_flow\_reporting\_advanced\_flow\_reporting\_report\_server\_address\_sonicwall

diag\_advanced\_flow\_reporting\_advanced\_flow\_reporting\_report\_server\_address\_ip

diag\_advanced\_flow\_reporting

diag\_advanced\_flow\_reporting\_clear\_location\_map\_action

diag\_advanced\_flow\_reporting\_clear\_database\_tables\_action

diag\_advanced\_watchdog

diag\_advanced\_dns\_security

diag\_advanced\_pppoe

diag\_advanced\_dial\_up

diag\_advanced\_dial\_up\_reset\_action

diag\_advanced\_ssl\_vpn

diag\_advanced\_backend\_advanced\_backend\_force\_through\_any

diag\_advanced\_backend\_advanced\_backend\_force\_through\_interface

diag\_advanced\_backend

diag\_advanced\_wireless\_advanced\_wireless\_sonicpoint\_self\_maintenance\_daily

diag\_advanced\_wireless\_advanced\_wireless\_sonicpoint\_self\_maintenance\_weekly

diag\_advanced\_wireless\_advanced\_wireless\_sonicpointn\_noise\_security\_level\_extremely\_high

diag\_advanced\_wireless\_advanced\_wireless\_sonicpointn\_noise\_security\_level\_high

diag\_advanced\_wireless\_advanced\_wireless\_sonicpointn\_noise\_security\_level\_medium

diag\_advanced\_wireless\_advanced\_wireless\_sonicpointn\_noise\_security\_level\_low

diag\_advanced\_wireless\_advanced\_wireless\_sonicpointn\_noise\_security\_level\_extremely\_low

diag\_advanced\_wireless

diag\_advanced\_wireless\_sonicpoint\_firmware\_update\_action

diag\_advanced\_dhcp

diag\_advanced\_dhcp\_leases\_to\_flash\_action

diag\_advanced\_vpn

diag\_advanced\_management\_advanced\_management\_online\_help\_url\_default

diag\_advanced\_management\_advanced\_management\_online\_help\_url\_override

diag\_advanced\_management

diag\_advanced\_security\_service

diag\_advanced\_security\_service\_reset\_av\_info\_action

diag\_advanced\_security\_service\_reset\_ngav\_cache\_action

diag\_advanced\_security\_service\_reset\_licenses\_action

diag\_advanced\_security\_service\_reset\_client\_cfs\_info\_action

diag\_advanced\_security\_service\_reset\_client\_cfs\_cache\_action

diag\_advanced\_security\_service\_reset\_http\_clientless\_notification\_cache\_action

diag\_advanced\_security\_service\_reset\_cloud\_av\_cache\_action

diag\_advanced\_security\_service\_reset\_cfs\_memory\_cache\_action

diag\_advanced\_security\_service\_reset\_cfs\_persistent\_cache\_action

diag\_advanced\_security\_service\_reset\_client\_enforcement\_status\_info\_action

diag\_advanced\_security\_service\_reset\_registration\_log\_action

diag\_advanced\_voip

diag\_advanced\_voip\_reset\_sip\_database\_action

diag\_advanced\_anti\_spam\_advanced\_anti\_spam\_cass\_cloud\_service\_address\_auto\_resolve

diag\_advanced\_anti\_spam\_advanced\_anti\_spam\_cass\_cloud\_service\_address\_static\_ip

diag\_advanced\_anti\_spam

diag\_advanced\_anti\_spam\_reset\_grid\_name\_cache\_action

diag\_advanced\_firewall

diag\_advanced\_diagnostics

diag\_advanced\_encryption

diag\_advanced\_diagnostics\_wan\_connectivity\_test\_start\_action

diag\_advanced\_diagnostics\_wan\_connectivity\_test\_stop\_action

diag\_advanced\_diagnostics\_wan\_connectivity\_test\_send\_log\_action

diag\_advanced\_geoip\_location\_service\_advanced\_geoip\_location\_service\_remote\_geoip\_server\_failed\_resolution\_default

diag\_advanced\_geoip\_location\_service\_advanced\_geoip\_location\_service\_remote\_geoip\_server\_failed\_resolution\_ip

diag\_advanced\_geoip\_location\_service\_advanced\_geoip\_location\_service\_remote\_geoip\_server\_failed\_resolution

diag\_advanced\_geoip\_location\_service\_advanced\_geoip\_location\_service\_remote\_geoip\_server\_always\_default

diag\_advanced\_geoip\_location\_service\_advanced\_geoip\_location\_service\_remote\_geoip\_server\_always\_ip

diag\_advanced\_geoip\_location\_service\_advanced\_geoip\_location\_service\_remote\_geoip\_server\_always

diag\_advanced\_geoip\_location\_service

diag\_advanced\_geoip\_location\_service\_clear\_location\_cache\_action

diag\_advanced\_high\_availability

diag\_advanced\_dpi\_ssl

diag\_advanced\_dpi\_ssl\_update\_security\_services\_info\_action

diag\_advanced\_dpi\_ssl\_clear\_internal\_session\_and\_cache\_state\_action

diag\_advanced\_network\_fo\_lb

diag\_advanced\_trace\_log

diag\_advanced\_clear\_trace\_log\_action

diag\_advanced\_fqdn\_dyn\_addr\_obj

diag\_advanced\_cta\_report

diag\_advanced\_zero\_touch

diag\_advanced\_zero\_touch\_restart\_action

diag\_advanced\_zero\_touch\_enable\_action

diag\_advanced\_zero\_touch\_disable\_action

diag\_advanced\_analyzer\_next\_gen

diag\_advanced\_cloud\_backup

debug\_cmd

show\_status\_packet\_monitor\_detail

show\_status\_packet\_monitor\_trace\_config\_detail

show\_status\_schedule\_status\_list

show\_status\_zone\_status\_list

show\_status\_interface\_list

show\_status\_interface\_detail

show\_status\_interface\_ipv6\_list

show\_status\_interface\_ipv6\_detail

show\_status\_interface\_ip\_list

show\_status\_interface\_ip\_detail

show\_status\_interface\_status\_list

show\_status\_interface\_status\_detail

show\_status\_tunnel\_interface\_status\_detail

show\_status\_interface\_ip\_ipv6\_list

show\_status\_interface\_ip\_ipv6\_detail

show\_status\_interface\_mac\_list

show\_status\_interface\_mac\_detail

show\_status\_tunnel6\_interface\_mtu\_list

show\_status\_tunnel6\_interface\_mtu\_detail

show\_status\_arp\_cache\_list

show\_status\_arp\_cache\_detail

show\_status\_arp\_entries\_list

show\_status\_arp\_status\_show\_detail

show\_status\_dns\_wan\_detail

show\_status\_dns\_wan\_ipv6\_detail

show\_status\_dynamic\_dns\_status\_list

show\_status\_dhcp\_leases\_list

show\_status\_dhcp\_leases\_statistic\_detail

show\_status\_dhcps6\_leases\_list

show\_status\_dhcps6\_leases\_statistic\_detail

show\_status\_flb\_responder\_detail

show\_status\_flb\_group\_status\_list

show\_status\_flb\_group\_status\_detail

show\_status\_flb\_member\_status\_list

show\_status\_flb\_member\_status\_detail

show\_status\_flb\_statistics\_list

show\_status\_flb\_statistics\_detail

show\_status\_dhcp\_relay\_leases\_list

show\_status\_dhcpv6\_relay\_leases\_list

show\_status\_iph\_policy\_list

show\_status\_iph\_protocol\_list

show\_status\_mac\_anti\_spoof\_list

show\_status\_mac\_anti\_spoof\_lookup\_statistic\_detail

show\_status\_mac\_anti\_spoof\_cache\_list

show\_status\_nat\_policy\_list

show\_status\_nat\_policy\_detail

show\_status\_nat\_policy\_ipv6\_detail

show\_status\_netmon\_policy\_list

show\_status\_netmon\_policy\_detail

show\_status\_routing\_v4\_system\_list

show\_status\_routing\_v4\_dynamic\_list

show\_status\_routing\_v6\_system\_list

show\_status\_routing\_v6\_dynamic\_list

show\_status\_ndp\_cache\_list

show\_status\_ndp\_entries\_list

show\_status\_dns\_proxy\_server\_list

show\_status\_dns\_proxy\_split\_entries\_list

show\_status\_dns\_proxy\_cache\_list

show\_status\_vlan\_translation\_status\_list

show\_status\_dns\_security\_sinkhole\_statistical\_list

show\_status\_dns\_security\_tunnel\_clients\_list

show\_status\_portshield\_groups\_ext\_switch\_statistics\_list

show\_status\_portshield\_groups\_ext\_switch\_firmware\_management\_list

show\_status\_portshield\_port\_table\_list

show\_status\_firewall\_connections\_list

show\_status\_multicast\_state\_entry\_list

show\_status\_access\_rules\_v4\_status\_list

show\_status\_access\_rules\_v6\_status\_list

show\_status\_access\_rule\_conn\_limit\_source\_list

show\_status\_access\_rule\_conn\_limit\_dest\_list

show\_status\_tcp\_detail

show\_status\_cipher\_control\_tls\_cipher\_list

show\_status\_udpv6\_detail

show\_status\_udp\_detail

show\_status\_icmpv6\_detail

show\_status\_icmp\_detail

show\_status\_dynamic\_external\_object\_detail

show\_status\_firmware\_update\_detail

show\_status\_system\_detail

show\_status\_system\_guest\_admin\_detail

show\_status\_system\_storage\_detail

show\_status\_system\_security\_detail

show\_status\_system\_interfaces\_list

show\_status\_sysfile\_logs\_list

show\_status\_sysfile\_sysdata\_list

show\_status\_sysfile\_diagdata\_list

show\_status\_sysfile\_configbk\_list

show\_status\_ssh\_server\_sessions\_list

show\_status\_users\_quota\_list

show\_status\_user\_statistics\_list

show\_status\_radius\_server\_statistics\_list

show\_status\_radius\_accounting\_statistics\_list

show\_status\_ldap\_server\_statistics\_detail

show\_status\_ldap\_servers\_global\_statistics\_detail

show\_status\_ldap\_dynamic\_server\_status\_list

show\_status\_sso\_agent\_list

show\_status\_sso\_agent\_detail

show\_status\_sso\_tsa\_agent\_detail

show\_status\_sso\_tsa\_agent\_list

show\_status\_radius\_acct\_client\_detail

show\_status\_radius\_acct\_client\_list

show\_status\_third\_party\_api\_client\_detail

show\_status\_third\_party\_api\_client\_list

show\_status\_user\_guest\_users\_status\_list

show\_status\_user\_guest\_user\_byname\_statistic\_list

show\_status\_user\_guest\_user\_statistic\_detail

show\_status\_user\_guest\_user\_detail\_list

show\_status\_user\_guest\_user\_detail\_detail

show\_status\_tacacs\_server\_statistics\_list

show\_status\_tacacs\_accounting\_statistics\_list

show\_status\_appflow\_external\_detail

show\_status\_appflow\_internal\_detail

show\_status\_appflow\_ipfix\_detail

show\_status\_gms\_flow\_server\_detail

show\_status\_app\_flow\_server\_detail

show\_status\_cert\_detail

show\_status\_certs\_list

show\_status\_log\_view\_list

show\_status\_log\_view\_status\_list

show\_status\_log\_aws\_detail

show\_status\_log\_categories\_event\_count\_list

show\_status\_voip\_call\_list

show\_status\_wwan\_status\_list

show\_status\_cfs\_policies\_statistics\_list

show\_status\_cfs\_policies\_statistics\_detail

show\_status\_websense\_detail

show\_status\_cfs\_detail

show\_status\_endpoint\_security\_service\_list

show\_status\_anti\_spam\_probe\_stats\_list

show\_status\_anti\_spam\_general\_stats\_detail

show\_status\_anti\_spam\_threats\_stats\_detail

show\_status\_anti\_spam\_service\_status\_detail

show\_status\_anti\_spam\_monitor\_status\_list

show\_status\_anti\_spam\_pcap\_stats\_detail

show\_status\_ips\_detail

show\_status\_gav\_detail

show\_status\_match\_objects\_detail

show\_status\_action\_objects\_detail

show\_status\_action\_objects\_bwm\_usage\_list

show\_status\_email\_objects\_detail

show\_status\_app\_rules\_status\_detail

show\_status\_app\_rules\_statistics\_detail

show\_status\_ac\_detail

show\_status\_rbl\_list

show\_status\_dpi\_ssl\_client\_default\_exclusions\_detail

show\_status\_dpi\_ssl\_client\_connection\_failures\_list

show\_status\_dpi\_ssl\_client\_common\_name\_statistics\_list

show\_status\_geo\_ip\_resolved\_locations\_list

show\_status\_geo\_ip\_cache\_statistics\_detail

show\_status\_geo\_ip\_custom\_countries\_statistics\_detail

show\_status\_geo\_ip\_status\_detail

show\_status\_botnet\_resolved\_locations\_list

show\_status\_botnet\_cache\_statistics\_detail

show\_status\_botnet\_status\_detail

show\_status\_anti\_spyware\_detail

show\_status\_dhcp\_over\_vpn\_lease\_count\_detail

show\_status\_dhcp\_over\_vpn\_leases\_list

show\_status\_l2tp\_server\_sessions\_list

show\_status\_sslvpn\_session\_list

show\_status\_sslvpn\_bookmark\_list

show\_status\_sslvpn\_traffic\_detail

show\_status\_sdwan\_group\_member\_list

show\_status\_switch\_vlan\_reserved\_detail

show\_status\_switch\_l2\_vlan\_list

show\_status\_switch\_lag\_status\_list

show\_status\_dos\_policy\_status\_list

show\_status\_dos\_policy\_counters\_list

show\_status\_dos\_policy\_counter\_status\_detail

show\_status\_decryption\_policy\_ssh\_statistics\_list

show\_status\_decryption\_policy\_server\_statistics\_list

show\_status\_decryption\_policy\_client\_statistics\_list

show\_status\_security\_policies\_status\_list

show\_status\_security\_policies\_status\_detail

show\_status\_security\_policies\_v4\_status\_list

show\_status\_security\_policies\_v6\_status\_list

show\_status\_web\_category\_object\_list

show\_status\_wireless\_detected\_access\_point\_status\_list

show\_status\_wireless\_associated\_station\_status\_list

show\_status\_wireless\_statistics\_detail

show\_status\_wireless\_activities\_detail

show\_status\_wireless\_access\_point\_mode\_status\_detail

show\_status\_wireless\_wds\_station\_on\_mix\_mode\_status\_detail

show\_status\_sonicpoint\_station\_status\_list

show\_status\_sonicpoint\_station\_radio\_statistics\_list

show\_status\_sonicpoint\_station\_traffic\_statistics\_list

show\_status\_sonicpoint\_radio\_statistics\_list

show\_status\_sonicpoint\_traffic\_statistics\_list

show\_status\_sonicpoint\_status\_list

show\_status\_sonicpoint\_vap\_status\_list

show\_status\_sonicpoint\_ids\_list

show\_status\_sonicpoint\_widp\_sensor\_units\_list

show\_status\_sonicpoint\_rfm\_statistics\_detail

show\_status\_sonicpoint\_rfm\_station\_list

show\_status\_sonicpoint\_rfm\_station\_watch\_list

show\_status\_sonicpoint\_rf\_score\_list

show\_status\_sonicpoint\_rfa\_overloaded\_list

show\_status\_sonicpoint\_rfa\_interfered\_list

show\_status\_virtual\_assist\_sessions\_list