import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        """Instantiate the restaurant manager.

        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """
        self.staff = {}
        self.special = {}


    async def __call__(self, request: Request):
        
        server = request.scope



        if server["type"] == "staff.offduty":
            self.staff.pop(server["id"])
        



        elif server["type"] == "staff.onduty":

            self.staff[server["id"]] = request
            for s in server["speciality"]:
                try:
                    self.special[s].append(server["id"])
                except:
                    self.special[s] = [server["id"]]
        



        elif server["type"] == "order":

            try:
                found = self.staff[self.special[server["speciality"]][0]]

            except IndexError:
                found = self.staff[list(self.staff.keys())[0]]

            full_order = await request.receive()

            await found.send(full_order)

            result = await found.receive()
            await request.send(result)
            