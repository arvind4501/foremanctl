import pytest

MIRROR_CONF = '/etc/containers/registries.conf.d/50-foremanctl-mirror.conf'

EXPECTED_PREFIXES = [
    'quay.io/foreman',
    'quay.io/sclorg',
]


def test_registry_mirror_file_exists(server):
    """Proxy/capsule deploy must generate a registries.conf.d mirror drop-in."""
    mirror = server.file(MIRROR_CONF)
    assert mirror.exists and mirror.is_file


@pytest.mark.parametrize('prefix', EXPECTED_PREFIXES)
def test_registry_mirror_contains_upstream_prefix(server, prefix):
    """Every upstream registry namespace used by deployed images must be redirected."""
    mirror = server.file(MIRROR_CONF)
    assert f'prefix = "{prefix}"' in mirror.content_string


def test_registry_mirror_location_points_to_parent_server(server, quadlet_fqdn):
    """The mirror must redirect pulls to the parent Foreman server, not upstream."""
    mirror = server.file(MIRROR_CONF)
    assert f'location = "{quadlet_fqdn}/Default_Organization"' in mirror.content_string
