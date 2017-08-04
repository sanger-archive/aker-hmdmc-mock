# aker-fake-hmdmc
Fake HMDMC validation for development.

You can set this running somewhere listening on some port, and then send get requests to it, e.g.

    GET http://my-server:1234/validate?hmdmc=17_999

You will get a different response depending on the hmdmc you send. OK (200) is expected to be the successful response.

The script reads a file at startup, called `HMDMCs.txt` by default.

The file should be formatted in the following way:

    [DEFAULT]
    17_000 = 200
    17_001 = 404
    default = 200

Any string given as an HMDMC that is not explicitly listed will get the 'default' response.

In the examples I'm assuming we're giving HMDMCs in the format `YY_NNN` rather than `YY/NNN`, since forward slashes are awkward in URLs. (This is the practice adopted by the CGAP LIMS.)

Usage:

To start a HTTP server:
    ./fake_hmdmc.py -p 3501  # run on port 3501 with default HMDMC file

To start a HTTPS server:
    ./fake_hmdmc.py -s 3501 -c /path/to/certfile -k /path/to/keyfile
