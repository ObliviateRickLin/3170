import mysql.connector
import numpy as np
import pandas as pd

def run_query(query, *args):
    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")
    cnx.reconnect()
    with cnx.cursor(buffered=True) as cur:
        cur.execute(query,*args)
        result = cur.fetchall()
    cnx.close()
    return result

def selectable_plants(plants, arg1, arg2, enough=True):
    """
    This is a function returns the selectable plants for a specific type of chip.

    Parameters:
    plants (list): all the plants 
    arg1 (type): Description of arg1
    arg2 (type): Description of arg2
    ...

    Returns:
    Selectable_plant_list (List): which plants can be selected to produce this chip
    """
    plant = np.random.choice(plants, size=3)
    #enough or not, we only choose 3
    # Assume `arg1` is the chip name, `arg2` is the chip version
    # Find all operation type needed
    if enough: return plant
    operation_name_ = run_query("SELECT operation_name FROM chip_type_with_operation_type WHERE CHIP_NAME = %s AND CHIP_VERSION = %s;",(arg1, arg2))
    operation_name = [i[0] for i in operation_name_]

    # Select all plants_id
    all_plant_id_ = run_query("SELECT plant_id FROM plant;")
    all_plant_id = [i[0] for i in all_plant_id_]
    # Select all plant
    all_plant_id_ = run_query("SELECT plant_id FROM plant;")
    all_plant_id = [i[0] for i in all_plant_id_]
    
    for id in all_plant_id:
        # Select all machines of the plant
        machine_info = run_query("SELECT machine_name, machine_version FROM machine WHERE plant_id = %s;", [id])
        machine_name, machine_version = [i[0] for i in machine_info], [i[1] for i in machine_info]
        # Record whether an operation name is included
        op_name_dict = dict()
        if enough: return plant
        # Find all operation types that could be processed
        for i in range(len(machine_name)):
            op_name_can_process_ = run_query("SELECT operation_name FROM machine_type_with_operation_type WHERE machine_name = %s AND machine_version = %s;", machine_info[i])
            op_name_can_process = [item[0] for item in op_name_can_process_]
            print(len(op_name_can_process))
            if len(op_name_can_process) != 0:
                break
            for op_name in op_name_can_process:
                op_name_dict[op_name] = 1
        # Determine whether all needed operation types are included
        feasible_plant = True
        for op_name in operation_name:
            if op_name not in op_name_dict:
                feasible_plant = False
                break
        if feasible_plant:
            plant.append(id)
    return plant

def select_plants_with_chip():
    plants_ = run_query("SELECT PLANT_NAME FROM plant")
    plants = [plant_[0] for plant_ in plants_]
    chip_type = pd.DataFrame(run_query("SELECT CHIP_NAME, CHIP_VERSION FROM chip_type"))
    chip_type.columns =["CHIP_NAME", "CHIP_VERSION"]
    chip_type["PLANTS"] = 0
    chip_type["PLANTS"] = chip_type.apply(lambda row: selectable_plants(plants, row["CHIP_NAME"], row['CHIP_VERSION']), axis=1)
    return chip_type

if __name__ == "__main__":
    print(select_plants_with_chip())
