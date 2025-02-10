#!/usr/bin/env python3 

from models.area import Area
from models.route import Route
from models.stage import Stage
from helpers import get_stages_in_area, get_stages_in_route, add_stage, remove_stage, create_route, exit_program, all_areas, all_routes

def display_menu():
    print("\n---- Saka Stage Management System ----")

    print("0. Exit")   
    print("1. List all areas")
    print("2. List all routes")
    print("3. List all stages within an area")
    print("4. List all stages within a route")
    print("5. Add stage")
    print("6. Remove stage in area/route")
    print("7. Create new route")

def main():
    Area.create_table()
    Route.create_table()
    Stage.create_table()
    
    while True:
        display_menu()
        choice = input("Enter option: ")

        if choice == "1":
            all_areas()
        elif choice == "2":
            all_routes()
        elif choice == "3":
            get_stages_in_area()
        elif choice == "4":
            get_stages_in_route()
        elif choice == "5":
            add_stage()
        elif choice == "6":
            remove_stage()
        elif choice == "7":
            create_route()
        elif choice == "0":
            exit_program()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':  
    main()  
