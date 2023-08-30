import json

test2_note_data = [
        {"number": 0, "color": "black", "lane": 0, "note_start_delays": 1200, "note_speed": 1/10},
        {"number": 1, "color": "black", "lane": 3, "note_start_delays": 1200, "note_speed": 1/10},
        {"number": 2, "color": "black", "lane": 2, "note_start_delays": 2200, "note_speed": 1/10},
        {"number": 3, "color": "black", "lane": 3, "note_start_delays": 2200, "note_speed": 1/10},
        {"number": 4, "color": "black", "lane": 3, "note_start_delays": 3200, "note_speed": 1/10},
        {"number": 5, "color": "black", "lane": 1, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 6, "color": "black", "lane": 2, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 7, "color": "black", "lane": 3, "note_start_delays": 4200, "note_speed": 1/10},
        {"number": 8, "color": "black", "lane": 1, "note_start_delays": 5200, "note_speed": 1/10},
        {"number": 9, "color": "black", "lane": 2, "note_start_delays": 6200, "note_speed": 1/10},
        {"number": 10, "color": "black", "lane": 3, "note_start_delays": 6200, "note_speed": 1/10}
]

with open("test2_note_data.json", "w") as file:
    json.dump(test2_note_data, file, indent=4)