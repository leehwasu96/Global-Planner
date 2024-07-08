# This function is a function that invokes a set grid map.
def load_grid_map(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            result = []
            for line in lines:
                row = list(map(int, line.strip().split()))
                result.insert(0, row)
            return result
        
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
