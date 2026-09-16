# Where the photographs come from

Both books' renders are served from a CloudFront host that some environments
block at the egress proxy. `fetch_photos.py` is the normal path and needs that
host; it reads the manifest for whichever book is being built
(`jobs.json` for Companion 01, `jobs_cp.json` for Companion 02).

When the host is blocked, do **not** tunnel around the proxy, and do not use a
third service as a relay -- the proxy README is explicit that a policy denial is
to be reported rather than routed around. The sanctioned path is Google Drive:
the renders are the account holder's own files, and the Drive connector is an
authorised channel that never touches the blocked host.

    Companion 01   SessionArc/OB1-CombinedRoutes/assets/photos
    Companion 02   SessionArc/OB2-Checkpoints/assets/photos

Download them there and drop them into `assets/photos/` under their slug.
`fetch_photos.py` skips any slug already on disk, so the rest of the build runs
unchanged, and `make.py` fails loudly rather than producing empty frames if any
are still missing.

`prompts_cp.py` carries the prompt behind every Companion 02 render, because a
job id points at an image that cannot be regenerated identically. If one has to
be remade, that file is what it was asked for.

The 58th file of Companion 01, `snap-ra05.jpg`, is not a render. `snap.py` cuts
it out of the freshly rendered A4 PDF so the reduced page on "Reading a route
page" can never disagree with the real route 05 spread.
