
for (prefix, adapter) in self.adapters.items():

    if url.lower().startswith(prefix):
        return adapter

# Nothing matches :-/
raise InvalidSchema("No connection adapters were found for '%s'" % url)

