from useragents import search_strings
import re

class Middleware(object):
    @staticmethod
    def process_request(request):
        """Adds a "mobile" attribute to the request which is True or False
           depending on whether the request should be considered to come from a
           small-screen device such as a phone or a PDA"""

        request.mobile = False

        if request.META.has_key("HTTP_X_OPERAMINI_FEATURES"):
            #Then it's running opera mini. 'Nuff said.
            #Reference from:
            # http://dev.opera.com/articles/view/opera-mini-request-headers/
            request.mobile = True

        if request.META.has_key("HTTP_ACCEPT"):
            s = request.META["HTTP_ACCEPT"].lower()
            if 'application/vnd.wap.xhtml+xml' in s:
                # Then it's a wap browser
                request.mobile = True


        request.devices = {}
        if request.META.has_key("HTTP_USER_AGENT"):
            # This takes the most processing. Surprisingly enough, when I
            # Experimented on my own machine, this was the most efficient
            # algorithm. Certainly more so than regexes.
            # Also, Caching didn't help much, with real-world caches.
            s = request.META["HTTP_USER_AGENT"].lower()
            for ua in search_strings:
                if ua in s:
                    request.mobile = True

            device = {}
            # also interested if it's a iPhone or Andriod, e.g. something common
            if s.find("iphone") > 0:
                device['iphone'] = "iphone" + re.search("iphone os (\d)", s).groups(0)[0]
                
            if s.find("ipad") > 0:
                device['ipad'] = "ipad"
                
            if s.find("android") > 0:
                device['android'] = "android" + re.search("android (\d\.\d)", s).groups(0)[0].translate(None, '.')

            if s.find("symbianOS/") > 0:
                device['nokia'] = "symbian" + re.search("symbianOS/(\d\.\d)", s).groups(0)[0]

            elif s.find("symbian/") > 0:
                device['nokia'] = "symbian" + re.search("symbianOS/(\d)", s).groups(0)[0]

            elif s.find("windows phone os 7") > 0:
                device['winphone7'] = "winphone7"

            elif s.find("nokia") > 0:
                device['nokia'] = "nokia" + re.search("nokia([a-z0-9]+)", s).groups(0)[0]
                
            if s.find("blackberry") > 0:
                device['blackberry'] = "blackberry"
                
            if s.find("iemobile") > 0:
                device['winmo'] = "winmo"
        
            # spits out device names for CSS targeting, to be applied to <html> or <body>.
            request.devices = " ".join(v for (k,v) in device.items())

        return None

def detect_mobile(view):
    """View Decorator that adds a "mobile" attribute to the request which is
       True or False depending on whether the request should be considered
       to come from a small-screen device such as a phone or a PDA"""

    def detected(request, *args, **kwargs):
        Middleware.process_request(request)
        return view(request, *args, **kwargs)
    detected.__doc__ = "%s\n[Wrapped by detect_mobile which detects if the request is from a phone]" % view.__doc__
    return detected


__all__ = ['Middleware', 'detect_mobile']
