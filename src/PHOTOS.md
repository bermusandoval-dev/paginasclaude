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

    Companion 01   Drive: "The Combined Routes | OB 1"      -> assets/photos
    Companion 02   Drive: "The Progress Checkpoints | OB 2"  -> assets/photos

Download them there and drop them into `assets/photos/<book>/` under their slug
(`routes/` for Companion 01, `checkpoints/` for Companion 02 -- the folders are
separate because both books wanted a slug called `h0-cover`, and while they
shared one directory the second book silently printed the first book’s cover).
`fetch_photos.py` skips any slug already on disk, so the rest of the build runs
unchanged, and `make.py` fails loudly rather than producing empty frames if any
are still missing.

`prompts_cp.py` carries the prompt behind every Companion 02 render, because a
job id points at an image that cannot be regenerated identically. If one has to
be remade, that file is what it was asked for.

The 58th file of Companion 01, `snap-ra05.jpg`, is not a render. `snap.py` cuts
it out of the freshly rendered A4 PDF so the reduced page on "Reading a route
page" can never disagree with the real route 05 spread.


## Companion 02: why the plates are drawn

The forty-six renders for The Progress Checkpoints were generated and are in
the Higgsfield account that ordered them. They could not be brought into the
build: they are served from `d8j0ntlcm91z4.cloudfront.net`, the egress policy
blocks it, and a second host found later (`d2ol7oe51mr4n9.cloudfront.net`) is
blocked too. Every channel that exists here was tried -- `jobs_wait`,
`show_generation_by_ids`, `show_medias`, the single-image widget, and the MCP
resource list, which serves only UI widgets. None returns bytes, only URLs.

So `art.py` draws the same forty-six compositions as vector plates and
`make_plates.py` rasterises them into `assets/photos/checkpoints/`, at the
sizes `fetch_photos.py` would have written. The book is complete either way.

`prompts_cp.py` still carries the prompt each plate was written from. To swap
the photographs back in: download them, rename them to the slugs in
`jobs_cp.json`, drop them over the files in `assets/photos/checkpoints/`, and
rebuild. Nothing else changes -- `make_plates.py` is the only step to skip.
