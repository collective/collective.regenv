from collective.regenv import _
from collective.regenv import registry
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five import BrowserView


COLLECTIVE_REGENV_ACKNOWLEDGED = "collective_regenv_acknowledged"


class AcknowledgeCollectiveRegenv(BrowserView):
    def __call__(self):
        """When this is called set a cookie that will be used to hide the viewlet."""
        self.request.response.setCookie(
            COLLECTIVE_REGENV_ACKNOWLEDGED, "true", max_age=604800
        )
        api.portal.show_message(message=_("Ok!"), request=self.request, type="info")
        return self.request.response.redirect(self.context.absolute_url())


class RegenvViewlet(ViewletBase):
    """Viewlet for rendering the registration environment."""

    def available(self):
        """Check if the viewlet should be displayed."""
        if not registry:
            return False

        if self.request.cookies.get(COLLECTIVE_REGENV_ACKNOWLEDGED):
            return False

        # Check if there is some override active on this site
        portal_path = "/".join(api.portal.get().getPhysicalPath())
        for key in registry:
            if key.startswith(portal_path):
                return True

        return False
