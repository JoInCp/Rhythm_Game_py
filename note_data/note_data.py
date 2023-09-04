import json

original_note_data  = [
        {"number": 0, "color": "black", "lane": 0, "note_start_delays": 800, "note_speed": 1/10},
        {"number": 1, "color": "black", "lane": 1, "note_start_delays": 800, "note_speed": 1/10},
        
        {"number": 2, "color": "black", "lane": 0, "note_start_delays": 3400, "note_speed": 1/10},
        {"number": 3, "color": "black", "lane": 1, "note_start_delays": 3400, "note_speed": 1/10},
        
        {"number": 4, "color": "black", "lane": 0, "note_start_delays": 6100, "note_speed": 1/10},
        {"number": 5, "color": "black", "lane": 1, "note_start_delays": 6100, "note_speed": 1/10},

        {"number": 6, "color": "black", "lane": 0, "note_start_delays": 8800, "note_speed": 1/10},
        {"number": 7, "color": "black", "lane": 1, "note_start_delays": 8800, "note_speed": 1/10},
        
        {"number": 8, "color": "black", "lane": 0, "note_start_delays": 11400, "note_speed": 1/10},
        {"number": 9, "color": "black", "lane": 1, "note_start_delays": 11400, "note_speed": 1/10},
        
        {"number": 10, "color": "black", "lane": 2, "note_start_delays": 14000, "note_speed": 1/10},
        {"number": 11, "color": "black", "lane": 3, "note_start_delays": 14000, "note_speed": 1/10},
        
        {"number": 12, "color": "black", "lane": 2, "note_start_delays": 16800, "note_speed": 1/10},
        {"number": 13, "color": "black", "lane": 3, "note_start_delays": 16800, "note_speed": 1/10},

        {"number": 14, "color": "black", "lane": 2, "note_start_delays": 19400, "note_speed": 1/10},
        {"number": 15, "color": "black", "lane": 3, "note_start_delays": 19400, "note_speed": 1/10},

        {"number": 16, "color": "black", "lane": 2, "note_start_delays": 22000, "note_speed": 1/10},
        {"number": 17, "color": "black", "lane": 3, "note_start_delays": 22000, "note_speed": 1/10},

        {"number": 18, "color": "black", "lane": 2, "note_start_delays": 24900, "note_speed": 1/10},
        {"number": 19, "color": "black", "lane": 3, "note_start_delays": 24900, "note_speed": 1/10},

        {"number": 20, "color": "black", "lane": 0, "note_start_delays": 27500, "note_speed": 1/10},
        {"number": 21, "color": "black", "lane": 1, "note_start_delays": 27500, "note_speed": 1/10},

        {"number": 22, "color": "black", "lane": 2, "note_start_delays": 30200, "note_speed": 1/10},
        {"number": 23, "color": "black", "lane": 3, "note_start_delays": 30200, "note_speed": 1/10},

        {"number": 24, "color": "black", "lane": 0, "note_start_delays": 32800, "note_speed": 1/10},
        {"number": 25, "color": "black", "lane": 1, "note_start_delays": 32800, "note_speed": 1/10},

        {"number": 26, "color": "black", "lane": 2, "note_start_delays": 35500, "note_speed": 1/10},
        {"number": 27, "color": "black", "lane": 3, "note_start_delays": 35500, "note_speed": 1/10},

        {"number": 28, "color": "black", "lane": 0, "note_start_delays": 38200, "note_speed": 1/10},
        {"number": 29, "color": "black", "lane": 1, "note_start_delays": 38200, "note_speed": 1/10},

        {"number": 30, "color": "black", "lane": 0, "note_start_delays": 40800, "note_speed": 1/10},
        {"number": 31, "color": "black", "lane": 1, "note_start_delays": 40800, "note_speed": 1/10},

        {"number": 32, "color": "black", "lane": 0, "note_start_delays": 43500, "note_speed": 1/10},
        {"number": 33, "color": "black", "lane": 1, "note_start_delays": 43500, "note_speed": 1/10},

        {"number": 34, "color": "black", "lane": 0, "note_start_delays": 46200, "note_speed": 1/10},
        {"number": 35, "color": "black", "lane": 1, "note_start_delays": 46200, "note_speed": 1/10},

        {"number": 36, "color": "black", "lane": 0, "note_start_delays": 48800, "note_speed": 1/10},
        {"number": 37, "color": "black", "lane": 3, "note_start_delays": 48800, "note_speed": 1/10},

        {"number": 38, "color": "black", "lane": 1, "note_start_delays": 51500, "note_speed": 1/10},
        {"number": 39, "color": "black", "lane": 2, "note_start_delays": 51500, "note_speed": 1/10},

        {"number": 40, "color": "black", "lane": 0, "note_start_delays": 54200, "note_speed": 1/10},
        {"number": 41, "color": "black", "lane": 1, "note_start_delays": 54200, "note_speed": 1/10},
         
        {"number": 42, "color": "black", "lane": 0, "note_start_delays": 54500, "note_speed": 1/10},
        {"number": 43, "color": "black", "lane": 1, "note_start_delays": 54500, "note_speed": 1/10},
         
        {"number": 44, "color": "black", "lane": 0, "note_start_delays": 54800, "note_speed": 1/10},
        {"number": 45, "color": "black", "lane": 1, "note_start_delays": 54800, "note_speed": 1/10},
         
        {"number": 46, "color": "black", "lane": 0, "note_start_delays": 55200, "note_speed": 1/10},
        {"number": 47, "color": "black", "lane": 1, "note_start_delays": 55200, "note_speed": 1/10},
         
        {"number": 48, "color": "black", "lane": 0, "note_start_delays": 55500, "note_speed": 1/10},
        {"number": 49, "color": "black", "lane": 1, "note_start_delays": 55500, "note_speed": 1/10},

        {"number": 50, "color": "black", "lane": 0, "note_start_delays": 55800, "note_speed": 1/10},
        {"number": 51, "color": "black", "lane": 1, "note_start_delays": 55800, "note_speed": 1/10},

        {"number": 52, "color": "black", "lane": 0, "note_start_delays": 56200, "note_speed": 1/10},
        {"number": 53, "color": "black", "lane": 1, "note_start_delays": 56200, "note_speed": 1/10},
         
        {"number": 54, "color": "black", "lane": 0, "note_start_delays": 56500, "note_speed": 1/10},
        {"number": 55, "color": "black", "lane": 1, "note_start_delays": 56500, "note_speed": 1/10},
         
        {"number": 56, "color": "black", "lane": 0, "note_start_delays": 56800, "note_speed": 1/10},
        {"number": 57, "color": "black", "lane": 1, "note_start_delays": 56800, "note_speed": 1/10},
         
        {"number": 58, "color": "black", "lane": 0, "note_start_delays": 57100, "note_speed": 1/10},
        {"number": 59, "color": "black", "lane": 1, "note_start_delays": 57100, "note_speed": 1/10},
        
        {"number": 60, "color": "black", "lane": 2, "note_start_delays": 57500, "note_speed": 1/10},
        {"number": 61, "color": "black", "lane": 3, "note_start_delays": 57500, "note_speed": 1/10},
         
        {"number": 62, "color": "black", "lane": 2, "note_start_delays": 57800, "note_speed": 1/10},
        {"number": 63, "color": "black", "lane": 3, "note_start_delays": 57800, "note_speed": 1/10},
         
        {"number": 64, "color": "black", "lane": 2, "note_start_delays": 58200, "note_speed": 1/10},
        {"number": 65, "color": "black", "lane": 3, "note_start_delays": 58200, "note_speed": 1/10}, 
         
        {"number": 66, "color": "black", "lane": 2, "note_start_delays": 58500, "note_speed": 1/10},
        {"number": 67, "color": "black", "lane": 3, "note_start_delays": 58500, "note_speed": 1/10},
         
        {"number": 68, "color": "black", "lane": 2, "note_start_delays": 58800, "note_speed": 1/10},
        {"number": 69, "color": "black", "lane": 3, "note_start_delays": 58800, "note_speed": 1/10},

        {"number": 70, "color": "black", "lane": 2, "note_start_delays": 59200, "note_speed": 1/10},
        {"number": 71, "color": "black", "lane": 3, "note_start_delays": 59200, "note_speed": 1/10}, 
         
        {"number": 72, "color": "black", "lane": 2, "note_start_delays": 59500, "note_speed": 1/10},
        {"number": 73, "color": "black", "lane": 3, "note_start_delays": 59500, "note_speed": 1/10},
         
        {"number": 74, "color": "black", "lane": 2, "note_start_delays": 59800, "note_speed": 1/10},
        {"number": 75, "color": "black", "lane": 3, "note_start_delays": 59800, "note_speed": 1/10},
         
        {"number": 76, "color": "black", "lane": 2, "note_start_delays": 60200, "note_speed": 1/10},
        {"number": 77, "color": "black", "lane": 3, "note_start_delays": 60200, "note_speed": 1/10},
         
        {"number": 78, "color": "black", "lane": 2, "note_start_delays": 60500, "note_speed": 1/10},
        {"number": 79, "color": "black", "lane": 3, "note_start_delays": 60500, "note_speed": 1/10},
         
        {"number": 80, "color": "black", "lane": 0, "note_start_delays": 60800, "note_speed": 1/10},
        {"number": 81, "color": "black", "lane": 1, "note_start_delays": 60800, "note_speed": 1/10},
         
        {"number": 82, "color": "black", "lane": 0, "note_start_delays": 61200, "note_speed": 1/10},
        {"number": 83, "color": "black", "lane": 1, "note_start_delays": 61200, "note_speed": 1/10},
         
        {"number": 84, "color": "black", "lane": 0, "note_start_delays": 61500, "note_speed": 1/10},
        {"number": 85, "color": "black", "lane": 1, "note_start_delays": 61500, "note_speed": 1/10},
         
        {"number": 86, "color": "black", "lane": 0, "note_start_delays": 61800, "note_speed": 1/10},
        {"number": 87, "color": "black", "lane": 1, "note_start_delays": 61800, "note_speed": 1/10},
          
        {"number": 88, "color": "black", "lane": 0, "note_start_delays": 62200, "note_speed": 1/10},
        {"number": 89, "color": "black", "lane": 1, "note_start_delays": 62200, "note_speed": 1/10},
          
        {"number": 90, "color": "black", "lane": 0, "note_start_delays": 62500, "note_speed": 1/10},
        {"number": 91, "color": "black", "lane": 1, "note_start_delays": 62500, "note_speed": 1/10},
          
        {"number": 92, "color": "black", "lane": 0, "note_start_delays": 62800, "note_speed": 1/10},
        {"number": 93, "color": "black", "lane": 1, "note_start_delays": 62800, "note_speed": 1/10},
         
        {"number": 94, "color": "black", "lane": 0, "note_start_delays": 63200, "note_speed": 1/10},
        {"number": 95, "color": "black", "lane": 1, "note_start_delays": 63200, "note_speed": 1/10},
         
        {"number": 96, "color": "black", "lane": 0, "note_start_delays": 63500, "note_speed": 1/10},
        {"number": 97, "color": "black", "lane": 1, "note_start_delays": 63500, "note_speed": 1/10},
         
        {"number": 98, "color": "black", "lane": 0, "note_start_delays": 63800, "note_speed": 1/10},
        {"number": 99, "color": "black", "lane": 1, "note_start_delays": 63800, "note_speed": 1/10},
         
        {"number": 100, "color": "black", "lane": 2, "note_start_delays": 64200, "note_speed": 1/10},
        {"number": 101, "color": "black", "lane": 3, "note_start_delays": 64200, "note_speed": 1/10},
         
        {"number": 102, "color": "black", "lane": 2, "note_start_delays": 64500, "note_speed": 1/10},
        {"number": 103, "color": "black", "lane": 3, "note_start_delays": 64500, "note_speed": 1/10},
         
        {"number": 104, "color": "black", "lane": 2, "note_start_delays": 64800, "note_speed": 1/10},
        {"number": 105, "color": "black", "lane": 3, "note_start_delays": 64800, "note_speed": 1/10},
         
        {"number": 106, "color": "black", "lane": 2, "note_start_delays": 65200, "note_speed": 1/10},
        {"number": 107, "color": "black", "lane": 3, "note_start_delays": 65200, "note_speed": 1/10},
         
        {"number": 108, "color": "black", "lane": 2, "note_start_delays": 65500, "note_speed": 1/10},
        {"number": 109, "color": "black", "lane": 3, "note_start_delays": 65500, "note_speed": 1/10},
         
        {"number": 110, "color": "black", "lane": 2, "note_start_delays": 65800, "note_speed": 1/10},
        {"number": 111, "color": "black", "lane": 3, "note_start_delays": 65800, "note_speed": 1/10},
         
        {"number": 112, "color": "black", "lane": 2, "note_start_delays": 66200, "note_speed": 1/10},
        {"number": 113, "color": "black", "lane": 3, "note_start_delays": 66200, "note_speed": 1/10},
          
        {"number": 114, "color": "black", "lane": 2, "note_start_delays": 66500, "note_speed": 1/10},
        {"number": 115, "color": "black", "lane": 3, "note_start_delays": 66500, "note_speed": 1/10},
         
        {"number": 116, "color": "black", "lane": 2, "note_start_delays": 66800, "note_speed": 1/10},
        {"number": 117, "color": "black", "lane": 3, "note_start_delays": 66800, "note_speed": 1/10},
          
        {"number": 118, "color": "black", "lane": 2, "note_start_delays": 67100, "note_speed": 1/10},
        {"number": 119, "color": "black", "lane": 3, "note_start_delays": 67100, "note_speed": 1/10},
         
        {"number": 120, "color": "black", "lane": 0, "note_start_delays": 67500, "note_speed": 1/10},
        {"number": 121, "color": "black", "lane": 1, "note_start_delays": 67500, "note_speed": 1/10},
         
        {"number": 122, "color": "black", "lane": 0, "note_start_delays": 67800, "note_speed": 1/10},
        {"number": 123, "color": "black", "lane": 1, "note_start_delays": 67800, "note_speed": 1/10},
          
        {"number": 124, "color": "black", "lane": 0, "note_start_delays": 68200, "note_speed": 1/10},
        {"number": 125, "color": "black", "lane": 1, "note_start_delays": 68200, "note_speed": 1/10},
         
        {"number": 126, "color": "black", "lane": 0, "note_start_delays": 68500, "note_speed": 1/10},
        {"number": 127, "color": "black", "lane": 1, "note_start_delays": 68500, "note_speed": 1/10},
         
        {"number": 128, "color": "black", "lane": 0, "note_start_delays": 68800, "note_speed": 1/10},
        {"number": 129, "color": "black", "lane": 1, "note_start_delays": 68800, "note_speed": 1/10},
         
        {"number": 130, "color": "black", "lane": 0, "note_start_delays": 69200, "note_speed": 1/10},
        {"number": 131, "color": "black", "lane": 1, "note_start_delays": 69200, "note_speed": 1/10},
         
        {"number": 132, "color": "black", "lane": 0, "note_start_delays": 69500, "note_speed": 1/10},
        {"number": 133, "color": "black", "lane": 1, "note_start_delays": 69500, "note_speed": 1/10},
         
        {"number": 134, "color": "black", "lane": 0, "note_start_delays": 69800, "note_speed": 1/10},
        {"number": 135, "color": "black", "lane": 1, "note_start_delays": 69800, "note_speed": 1/10},
         
        {"number": 136, "color": "black", "lane": 0, "note_start_delays": 70200, "note_speed": 1/10},
        {"number": 137, "color": "black", "lane": 1, "note_start_delays": 70200, "note_speed": 1/10},
         
        {"number": 138, "color": "black", "lane": 0, "note_start_delays": 70500, "note_speed": 1/10},
        {"number": 139, "color": "black", "lane": 1, "note_start_delays": 70500, "note_speed": 1/10},
         
        {"number": 140, "color": "black", "lane": 2, "note_start_delays": 70800, "note_speed": 1/10},
        {"number": 141, "color": "black", "lane": 3, "note_start_delays": 70800, "note_speed": 1/10},
          
        {"number": 142, "color": "black", "lane": 2, "note_start_delays": 71200, "note_speed": 1/10},
        {"number": 143, "color": "black", "lane": 3, "note_start_delays": 71200, "note_speed": 1/10},
         
        {"number": 144, "color": "black", "lane": 2, "note_start_delays": 71500, "note_speed": 1/10},
        {"number": 145, "color": "black", "lane": 3, "note_start_delays": 71500, "note_speed": 1/10},
         
        {"number": 146, "color": "black", "lane": 2, "note_start_delays": 71800, "note_speed": 1/10},
        {"number": 147, "color": "black", "lane": 3, "note_start_delays": 71800, "note_speed": 1/10},
         
        {"number": 148, "color": "black", "lane": 2, "note_start_delays": 72200, "note_speed": 1/10},
        {"number": 149, "color": "black", "lane": 3, "note_start_delays": 72200, "note_speed": 1/10},
         
        {"number": 150, "color": "black", "lane": 2, "note_start_delays": 72500, "note_speed": 1/10},
        {"number": 151, "color": "black", "lane": 3, "note_start_delays": 72500, "note_speed": 1/10},
         
        {"number": 152, "color": "black", "lane": 2, "note_start_delays": 72800, "note_speed": 1/10},
        {"number": 153, "color": "black", "lane": 3, "note_start_delays": 72800, "note_speed": 1/10},
         
        {"number": 154, "color": "black", "lane": 2, "note_start_delays": 73200, "note_speed": 1/10},
        {"number": 155, "color": "black", "lane": 3, "note_start_delays": 73200, "note_speed": 1/10},
         
        {"number": 156, "color": "black", "lane": 2, "note_start_delays": 73500, "note_speed": 1/10},
        {"number": 157, "color": "black", "lane": 3, "note_start_delays": 73500, "note_speed": 1/10},
         
        {"number": 158, "color": "black", "lane": 2, "note_start_delays": 73800, "note_speed": 1/10},
        {"number": 159, "color": "black", "lane": 3, "note_start_delays": 73800, "note_speed": 1/10},
         
        {"number": 160, "color": "black", "lane": 1, "note_start_delays": 74200, "note_speed": 1/10},
        {"number": 161, "color": "black", "lane": 2, "note_start_delays": 74200, "note_speed": 1/10},
         
        {"number": 162, "color": "black", "lane": 1, "note_start_delays": 74500, "note_speed": 1/10},
        {"number": 163, "color": "black", "lane": 2, "note_start_delays": 74500, "note_speed": 1/10},
         
        {"number": 164, "color": "black", "lane": 1, "note_start_delays": 74800, "note_speed": 1/10},
        {"number": 165, "color": "black", "lane": 2, "note_start_delays": 74800, "note_speed": 1/10},
          
        {"number": 166, "color": "black", "lane": 1, "note_start_delays": 75200, "note_speed": 1/10},
        {"number": 167, "color": "black", "lane": 2, "note_start_delays": 75200, "note_speed": 1/10},
         
        {"number": 168, "color": "black", "lane": 1, "note_start_delays": 75500, "note_speed": 1/10},
        {"number": 169, "color": "black", "lane": 2, "note_start_delays": 75500, "note_speed": 1/10},
          
        {"number": 170, "color": "black", "lane": 0, "note_start_delays": 78200, "note_speed": 1/10},
        {"number": 171, "color": "black", "lane": 1, "note_start_delays": 78200, "note_speed": 1/10},
        {"number": 172, "color": "black", "lane": 2, "note_start_delays": 78200, "note_speed": 1/10},

        {"number": 173, "color": "black", "lane": 1, "note_start_delays": 80800, "note_speed": 1/10},
        {"number": 174, "color": "black", "lane": 2, "note_start_delays": 80800, "note_speed": 1/10},
        {"number": 175, "color": "black", "lane": 3, "note_start_delays": 80800, "note_speed": 1/10},
          
        {"number": 176, "color": "black", "lane": 0, "note_start_delays": 83500, "note_speed": 1/10},
        {"number": 177, "color": "black", "lane": 1, "note_start_delays": 83500, "note_speed": 1/10},
        {"number": 178, "color": "black", "lane": 2, "note_start_delays": 83500, "note_speed": 1/10},
        {"number": 179, "color": "black", "lane": 3, "note_start_delays": 83500, "note_speed": 1/10},

    ]

with open("test1_note_data.json", "w") as file:
    json.dump(original_note_data, file, indent=4)