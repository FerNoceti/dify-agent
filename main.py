import json

def main():
    data_json = {
        "TEXT": "**Short summary**  \nThe commit introduces changes to the repository as indicated by the commit message and the list of modified files.\n\n**Files affected**  \n- *[list of modified files from the metadata]*\n\n**Interpreted intent of the change**  \nBased on the filenames and the commit message, the change appears to implement a new feature, fix a bug, or refactor existing code to improve functionality or maintainability."
    }
    
    print(json.dumps(data_json, indent=4))

if __name__ == "__main__":
    main()
