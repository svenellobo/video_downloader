

class OutputParser():   
    
    @staticmethod
    def parse(json_dict) -> dict:
        metadata_dict = {}
        metadata_dict["title"] = json_dict.get("title") 
        metadata_dict["duration"] = json_dict.get("duration")
        metadata_dict["thumbnail"] = json_dict.get("thumbnail")
        metadata_dict["thumbnails"] = json_dict.get("thumbnails")
        metadata_dict["filesize_approx"] = json_dict.get("filesize_approx")
        return metadata_dict