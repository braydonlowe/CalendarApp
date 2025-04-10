from sqLite import utils

def import_data_into_db(scheduledItems: dict) -> None:
    #Create class data and assocate it to a semester
    semester_id = utils.get_semester_id("Winter 2025")
    if semester_id == None:
        print("No semester was found when connecting to database. Returning to home.")
        return
    

    # Loop through classes and assignments and insert into DB
    for class_name, assignments in scheduledItems.items():
        class_id = utils.create_or_retrieve_class(semester_id, class_name)
        if class_id is None:
            print(f"Failed to create/retrieve class: {class_name}")
            continue

        for assignment in assignments:
            utils.create_or_retrieve_assignment(
                class_id=class_id,
                assignment_name=assignment["assignment"],
                due_date=assignment["due_date"],
                completed=assignment["completed"]
            )