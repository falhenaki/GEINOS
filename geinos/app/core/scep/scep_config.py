"""1. Configure SCEP server details
   2. Configure Certificate Authority (CA)
   3. Configure Client cert info"""


cert_server_config="""
<config>
    <pki xmlns="com:gemds:mds-certmgr">
        <certificate-servers>
            <certificate-server>
                <cert-server-identity>{}</cert-server-identity>
                <server-type>scep</server-type>
                <server-setting xmlns="com:gemds:mds-certmgr-servers">
                  <uri>{}</uri>
                  <digest-algo>{}</digest-algo>
                  <encrypt-algo>{}</encrypt-algo>
                </server-setting>
            </certificate-server>
        </certificate-servers>
    </pki>
</config>
"""

ca_server_config="""
<config>
  <pki xmlns="com:gemds:mds-certmgr">
  <ca-servers>
    <ca-server>
      <ca-issuer-identity>{}</ca-issuer-identity>
      <ca-fingerprint>{}</ca-fingerprint>
    </ca-server>
  </ca-servers>
  </pki>
</config>
"""

cert_info_config="""
<config>
  <pki xmlns="com:gemds:mds-certmgr">
  <cert-info>
    <certificate-info>
      <certificate-info-identity>{}</certificate-info-identity>
      <country-x509>{}</country-x509>
      <state-x509>{}</state-x509>
      <locale-x509>{}</locale-x509>
      <organization-x509>{}</organization-x509>
      <org-unit-x509>{}</org-unit-x509>
      <common-name-x509>{}</common-name-x509>
      <pkcs9-email-x509>{}</pkcs9-email-x509>
    </certificate-info>
  </cert-info>
  </pki>
</config>
"""


# TODO check for valid digest and encrypt algo, return error if invalid
def format_config_cert_server(server_name, cert_server, digest, encrypt):
    cfg = cert_server_config.format(server_name, cert_server, digest.lower(), encrypt.lower())
    return cfg


def format_config_ca_server(ca_name,thumbprint):

    cfg = ca_server_config.format(ca_name, thumbprint)
    return cfg


def format_config_cert_info(cert_name,serial,country,state,locale,organization,org_unit):
    cfg = cert_info_config.format(cert_name, country, state, locale, organization, org_unit, serial,
                                  "DEVICE-1@ge.com")
    return cfg

