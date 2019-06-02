import json

in_file_path='D:\\News_Category_Dataset_v2.json' # Change me!
count = 0
fileno=1
with open(in_file_path,'r') as in_json_file:

    # Read the file and convert it to a dictionary
    json_obj_list = json.load(in_json_file)

    for json_obj in json_obj_list:
        count = count+1
        if count < 3:
            filename='D:\\split_'+str(fileno)+'.json'
            with open(filename, 'w') as out_json_file:
                json.dump(json_obj, out_json_file, indent=4)
        else:
            count = 0
            fileno=fileno +1

