"""Override registry settings in enhanced_templates."""
import os
from typing import Any, Dict, Union
from homeassistant.helpers.template import (
    _ENVIRONMENT,
    TemplateEnvironment,
)

from .const import DEFAULT_LANGUAGE, DOMAIN, JINJA_GLOBALS, TRANSLATIONS_PATH
from .share import get_configuration, get_hass, get_log

TranslationDict = Dict[str, Union[str, Dict[str, str]]]


async def setup_template() -> None:
    """Setup Jinja template for this integration."""

    # Add additional Jinja globals
    for jinja_global in JINJA_GLOBALS.items():
        add_template_global(*jinja_global)

    update_translations()


def update_translations() -> None:
    """Update the translation template variable."""

    # Add translations
    add_template_global("trans", load_translations())


def add_template_global(name: str, value: Any) -> None:
    """Add a global to the template."""

    jinja: TemplateEnvironment = get_hass().data[_ENVIRONMENT]

    jinja.globals[f"_{DOMAIN}_{name}"] = value


def load_translations() -> TranslationDict:
    """Load translation YAML files."""

    from custom_components.enhanced_templates.yaml_parser import parse_yaml

    # Always load the default language
    translations: TranslationDict = parse_yaml(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                TRANSLATIONS_PATH + DEFAULT_LANGUAGE + ".yaml",
            )
        )
    )

    language = get_configuration().language

    # Update with the selected language which allows for incomplete translations.
    if language != DEFAULT_LANGUAGE:
        try:
            translations.update(
                parse_yaml(
                    os.path.abspath(
                        os.path.join(
                            os.path.dirname(__file__),
                            TRANSLATIONS_PATH + language + ".yaml",
                        )
                    ),
                    skip_translations=True,
                )
            )
        except:
            get_log().warning(f"Translation doesn't exist for language '{language}.'")

    return translations
