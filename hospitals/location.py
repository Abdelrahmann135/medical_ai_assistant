from winsdk.windows.devices.geolocation import Geolocator

async def get_coords():
    locator = Geolocator()
    pos = await locator.get_geoposition_async()
    return pos.coordinate.point.position.latitude, pos.coordinate.point.position.longitude