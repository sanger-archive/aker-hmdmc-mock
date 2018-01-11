# aker-fake-hmdmc
Fake HMDMC validation for development.

You can set this running somewhere listening on some port, and then send get requests to it, e.g.

    GET http://my-server:1234/validateHMDMC?hmdmc=17_999

You should get an OK (200) response, along with a block of JSON. The JSON data includes keys `valid` (true or false) and `errorcode` (an integer). If the HMDMC is valid, the error code will be zero.

    {
        "valid": true,
        "errorcode": 0,
        "productclasses": []
    }

The script reads a file at startup, called `HMDMCs.txt` by default.

The file should be formatted in the following way:

    [DEFAULT]
    17_000 = 0
    17_001 = 3
    default = 0

The file describes the error codes for different HMDMC codes.

Any string given as an HMDMC that is not explicitly listed will get the `default` response.

In the examples I'm assuming we're giving HMDMCs in the format `YY_NNN` rather than `YY/NNN`, since forward slashes are awkward in URLs. (This is the practice adopted by the CGAP LIMS.)

####Usage

To start a HTTP server:

    # run HTTP on port 3501 with default HMDMC file
    ./fake_hmdmc.py 3501

To start a HTTPS server:

    # run HTTPS on port 3501 with default HMDMC file
    ./fake_hmdmc.py -c /path/to/certfile 3501
