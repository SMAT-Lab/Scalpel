proxies = proxies or {}
scheme = urlparse(request.url).scheme.lower()
proxy = proxies.get(scheme)

if proxy and scheme != 'https':
    url, _ = urldefrag(request.url)
else:
    url = request.path_url

