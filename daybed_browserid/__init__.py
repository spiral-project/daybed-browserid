"""

A BrowserID authentication plugin for Daybed:

    https://developer.mozilla.org/en-US/Persona/Protocol_Overview

"""
import pkg_resources
from pyramid.config import ConfigurationError
from pyramid.settings import aslist


#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version


def includeme(config):
    """Plug daybed-browserid to daybed"""
    settings = config.get_settings()
    if 'browserid.audiences' not in settings:
        raise ConfigurationError(
            'Missing browserid.audiences settings. This is needed for '
            'security reasons. See https://developer.mozilla.org/en-US/docs/'
            'Persona/Security_Considerations for details.')

    if 'browserid.trusted_issuers' not in settings:
        raise ConfigurationError(
            'Missing browserid.trusted_issuers settings. This is needed for '
            'security reasons. See https://developer.mozilla.org/en-US/docs/'
            'Persona/Security_Considerations for details.')

    verifier_url = settings.get("browserid.verifier_url", None)
    audiences = aslist(settings['browserid.audiences'])
    trusted_issuers = aslist(settings['browserid.trusted_issuers'])

    config.registry['browserid.verifier_url'] = verifier_url
    config.registry['browserid.audiences'] = audiences
    config.registry['browserid.trusted_issuers'] = trusted_issuers

    # Create a backend
    backend_class = config.maybe_dotted(
        settings.get(
            'browserid.backend',
            settings['daybed.backend'].replace('daybed', 'daybed_browserid')
        )
    )
    config.registry.browserid_db = backend_class.load_from_config(config)
    config.scan("daybed_browserid.views")
