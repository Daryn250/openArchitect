# save data using json
import json

# saves and loads settings and projects.
class SaveStructure:
    def __init__(self):
        # self is created.
        pass

    # updates per instance settings
    def settings_updated(self, settings): 
        pass
    
    # update settings on start
    def default_settings_updated(self, settings):
        pass
    
    # save the current project
    def save_project(self, project_data):
        pass
    
    # save the cache of the current project (list of modifications & the changes that they made to the project)
    def update_project_cache(self, cache):
        pass
