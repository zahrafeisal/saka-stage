# lib/helpers.py
from models.area import Area
from models.route import Route
from models.stage import Stage

def valid_id(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid ID. Please try an integer.")

def all_areas():
    areas = Area.get_all()
    if areas:
        for area in areas:
             print(f"{area.name}, Area ID: {area.id}")
    else:
        print("No areas found.")

def all_routes():
    routes = Route.get_all()
    if routes:
        for route in routes:
            print(f"{route.route}, Route ID: {route.id}")
    else:
        print("No routes found.")

def get_stages_in_area():
    area_id = valid_id("Enter Area ID: ")
    area = Area.find_by_id(area_id)

    if area:
        stages = area.stages()
        if stages:
            for stage in stages:
                print(f"{stage.name}")
        else:
            print("No stages found in this area.")
    else:
        print("No area found.")

def get_stages_in_route():
    route_id = valid_id("Enter Route ID: ")
    route = Route.find_by_id(route_id)

    if route:
        stages = route.stages()
        if stages:
            for stage in stages:
                print(f"{stage.name}")
        else:
            print("No stages found for this route.")
    else:
        print("No route found.")

def add_stage():
    stage_name = input("Enter stage name: ")
    route_id = valid_id("Enter Route ID: ")
    area_id = valid_id("Enter Area ID: ")
    Stage.create(stage_name, area_id, route_id)
    print(f"{stage_name} stage added successfully.")

def remove_stage():
    stage_id = valid_id("Enter stage ID: ")
    stage = Stage.find_by_id(stage_id)

    if stage:
        stage.delete()
        print(f"{stage.name} has been deleted successfully.")
    else:
        print("No stage found.")

def create_route():
    route_name = input("Enter route in format Place-Place: ")
    Route.create(route_name)

    print(f"{route_name} route added successfully.")

def exit_program():
    print("Exiting the program. Goodbye!")
    exit()
