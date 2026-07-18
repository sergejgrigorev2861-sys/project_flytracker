from src.aeroplane import Aeroplane


def test_aeroplane_from_dict():
    data = [
        "abc123",  # icao24
        "TEST  ",  # callsign (с пробелом)
        "US",  # country
        123456,  # time_position
        123456,  # last_contact
        10.0,  # longitude
        50.0,  # latitude
        5000.0,  # baro_altitude
        False,  # on_ground
        100.0,  # velocity
        120.0,  # true_track
        0.0,  # vertical_rate
        None,  # sensors
        0.0,  # geo_altitude
        "0",  # squawk
        False,  # spi
        0  # position_source
    ]
    plane = Aeroplane.from_dict(data)
    assert plane.icao24 == "abc123"
    assert plane.callsign == "TEST"
    assert plane.country == "US"
    assert plane.velocity == 100.0
    assert plane.altitude == 5000.0


def test_cast_to_object_list():
    data = {
        "states": [
            ["abc123", "TEST", "US", 0, 0, 0, 0, 5000, False, 100, 0, 0, None, 0, "0", False, 0]
        ]
    }
    planes = Aeroplane.cast_to_object_list(data)
    assert len(planes) == 1
    assert planes[0].callsign == "TEST"


def test_aeroplane_comparison():
    p1 = Aeroplane("a", "A", "US", 100, 5000)
    p2 = Aeroplane("b", "B", "US", 100, 6000)
    assert p1 < p2
    assert p2 > p1
    assert p1 != p2


def test_cast_to_object_list_empty():
    data = {}
    planes = Aeroplane.cast_to_object_list(data)
    assert planes == []
