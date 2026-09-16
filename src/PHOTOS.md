# Where the photographs come from

The 57 Higgsfield renders are served from a CloudFront host that some
environments block at the egress proxy. `fetch_photos.py` is the normal path
and needs that host.

When it is blocked, do **not** tunnel around the proxy. The photographs are
also in Google Drive, under `SessionArc/OB1-CombinedRoutes/assets/photos`, and
the Drive connector is an authorised channel that does not touch the blocked
host. Downloading them there and dropping them into `assets/photos/` is enough:
`fetch_photos.py` skips any slug already on disk, so the rest of the build runs
unchanged.

The 58th file, `snap-ra05.jpg`, is not a render. `snap.py` cuts it out of the
freshly rendered A4 PDF so the reduced page on "Reading a route page" can never
disagree with the real route 05 spread.
