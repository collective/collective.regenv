from collective.regenv.settings import get_settings
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five import BrowserView


COLLECTIVE_REGENV_ACKNOWLEDGED = "collective_regenv_acknowledged"


def _all_paths() -> set[str]:
    """Get all paths from settings."""
    settings = get_settings()
    return settings.all_paths


class AcknowledgeCollectiveRegenv(BrowserView):
    def __call__(self):
        """When this is called set a cookie that will be used to hide the viewlet."""
        self.request.response.setCookie(
            COLLECTIVE_REGENV_ACKNOWLEDGED, "true", max_age=604800
        )
        api.portal.show_message(message="Ok!", request=self.request, type="info")
        return self.request.response.redirect(self.context.absolute_url())


class RegenvViewlet(ViewletBase):
    """Viewlet for rendering the registration environment."""

    def available(self):
        """Check if the viewlet should be displayed."""
        if not (paths := _all_paths()):
            return False

        if self.request.cookies.get(COLLECTIVE_REGENV_ACKNOWLEDGED):
            return False

        # Check if there is some override active on this site
        portal_path = "/".join(api.portal.get().getPhysicalPath())

        return any(key.startswith(portal_path) for key in paths)
