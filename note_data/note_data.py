import json

original_note_data  = [
        {"number": 0, "color": "black", "lane": 0, "note_start_delays": 800, "note_speed": 1/10},
        
        {"number": 1, "color": "black", "lane": 0, "note_start_delays": 3400, "note_speed": 1/10},
        
        {"number": 2, "color": "black", "lane": 0, "note_start_delays": 6100, "note_speed": 1/10},
        
        {"number": 3, "color": "black", "lane": 0, "note_start_delays": 8800, "note_speed": 1/10},
        
        {"number": 4, "color": "black", "lane": 0, "note_start_delays": 11400, "note_speed": 1/10},
        
        {"number": 5, "color": "black", "lane": 0, "note_start_delays": 14000, "note_speed": 1/10},
        
        {"number": 6, "color": "black", "lane": 0, "note_start_delays": 16800, "note_speed": 1/10},

        {"number": 7, "color": "black", "lane": 0, "note_start_delays": 19400, "note_speed": 1/10},

        {"number": 8, "color": "black", "lane": 0, "note_start_delays": 22000, "note_speed": 1/10},

        {"number": 9, "color": "black", "lane": 0, "note_start_delays": 24900, "note_speed": 1/10},

        {"number": 10, "color": "black", "lane": 0, "note_start_delays": 27500, "note_speed": 1/10},

        {"number": 11, "color": "black", "lane": 0, "note_start_delays": 30200, "note_speed": 1/10},

        {"number": 12, "color": "black", "lane": 0, "note_start_delays": 32800, "note_speed": 1/10},

        {"number": 13, "color": "black", "lane": 0, "note_start_delays": 35500, "note_speed": 1/10},

        {"number": 14, "color": "black", "lane": 0, "note_start_delays": 38200, "note_speed": 1/10},


        {"number": 15, "color": "black", "lane": 0, "note_start_delays": 40800, "note_speed": 1/10},

        {"number": 16, "color": "black", "lane": 0, "note_start_delays": 43500, "note_speed": 1/10},

        {"number": 17, "color": "black", "lane": 0, "note_start_delays": 46200, "note_speed": 1/10},

        {"number": 18, "color": "black", "lane": 0, "note_start_delays": 48800, "note_speed": 1/10},

        {"number": 19, "color": "black", "lane": 0, "note_start_delays": 51500, "note_speed": 1/10},

        {"number": 20, "color": "black", "lane": 0, "note_start_delays": 54200, "note_speed": 1/10},

        {"number": 21, "color": "black", "lane": 0, "note_start_delays": 54500, "note_speed": 1/10},

        {"number": 22, "color": "black", "lane": 0, "note_start_delays": 54800, "note_speed": 1/10},


        {"number": 23, "color": "black", "lane": 0, "note_start_delays": 55200, "note_speed": 1/10},

        {"number": 24, "color": "black", "lane": 0, "note_start_delays": 55500, "note_speed": 1/10},

        {"number": 25, "color": "black", "lane": 0, "note_start_delays": 55800, "note_speed": 1/10},

        {"number": 26, "color": "black", "lane": 0, "note_start_delays": 56200, "note_speed": 1/10},

        {"number": 27, "color": "black", "lane": 0, "note_start_delays": 56500, "note_speed": 1/10},
         
        {"number": 28, "color": "black", "lane": 0, "note_start_delays": 56800, "note_speed": 1/10},

        {"number": 29, "color": "black", "lane": 0, "note_start_delays": 57100, "note_speed": 1/10},
        
        {"number": 30, "color": "black", "lane": 0, "note_start_delays": 57500, "note_speed": 1/10},

        {"number": 31, "color": "black", "lane": 0, "note_start_delays": 57800, "note_speed": 1/10},

        {"number": 32, "color": "black", "lane": 0, "note_start_delays": 58200, "note_speed": 1/10},

        {"number": 33, "color": "black", "lane": 0, "note_start_delays": 58500, "note_speed": 1/10},

        {"number": 34, "color": "black", "lane": 0, "note_start_delays": 58800, "note_speed": 1/10},

        {"number": 0, "color": "black", "lane": 0, "note_start_delays": 1000000, "note_speed": 1/10},
]

with open("test1_note_data.json", "w") as file:
    json.dump(original_note_data, file, indent=4)