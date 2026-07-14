#Each tuple contains: (Period Value, Column Index, label)
periods_to_plot = [
    (2.0, 0, "p2"),
    (3.0, 1, "p3"),
    (4.0, 2, "p4"),
    (5.0, 3, "p5"),
    (7.5, 4, "p7_5"),
    (10.0, 5, "p10")
]

#Metadata for earthquake_examples/plotting_examples.pth
example_metadata = [
    { # plotting_examples[0]
        "fault_lon": [-118.47449, -118.66749], "fault_lat": [34.70201, 34.746403],
        "event_lon": -118.50931, "event_lat": 34.70201,
        "sim_id": "(128,60,0)", "source_info": "S. San Andreas: M6.55, Depth = 6.8km"
    },
    { # plotting_examples[1]
        "fault_lon": [-118.26684, -117.98456], "fault_lat": [33.89529, 33.667397],
        "event_lon": -118.25589, "event_lat": 33.87971,
        "sim_id": "(219,78,0)", "source_info": "Newport Inglewood Connected alt 2: M6.75, Depth = 1.1km" 
    },
    { # plotting_examples[2]
        "fault_lon": [-117.58901, -117.00837], "fault_lat": [33.828526, 33.341652],
        "event_lon": -117.5614, "event_lat": 33.81376,
        "sim_id": "(8,0,0)", "source_info": "Elsinore;GI+T: M6.95, Depth = 3.3km " 
    },
    { # plotting_examples[3]
        "fault_lon": [-117.23616, -116.90387], "fault_lat": [34.016426, 33.756847],
        "event_lon": -117.20404, "event_lat": 34.00281,
        "sim_id": "(116,6,0)", "source_info": "San Jacinto;SJV: M7.25, Depth = 3.5km" 
    },
    { # plotting_examples[4]
        "fault_lon": [-117.56416, -115.9448], "fault_lat": [34.293026, 33.00176],
        "event_lon": -116.87798, "event_lat": 33.74463,
        "sim_id": "(114,0,128)", "source_info": "San Jacinto;SBV+SJV+A+CC+B: M7.55, Depth = 10.8km" 
    },
    { # plotting_examples[5]
        "fault_lon": [-116.35646, -118.04647], "fault_lat": [32.950275, 33.994457],
        "event_lon": -116.40266, "event_lat": 32.953,
        "sim_id": "(19,1,0)", "source_info": "Elsinore;W+GI+T+J: M7.55, Depth = 4.5km" 
    },
    { # plotting_examples[6]
        "fault_lon": [-116.262146, -117.60647], "fault_lat": [32.927917, 33.83696],
        "event_lon": -116.27712, "event_lat": 32.95924,
        "sim_id": "(124,419,0)", "source_info": "Elsinore: M7.65, Depth = 1.5km" 
    },
    { # plotting_examples[7]
        "fault_lon": [-117.14735, -118.38736], "fault_lat": [32.561203, 34.03932],
        "event_lon": -117.1636, "event_lat": 32.58761,
        "sim_id": "(218,267,0)", "source_info": "Newport Inglewood Connected alt 1: M7.75, Depth = 3.1km"
    },
    { # plotting_examples[8]
        "fault_lon": [-116.247185, -118.888336], "fault_lat": [33.788776, 34.80742],
        "event_lon": -116.2642, "event_lat": 33.83155,
        "sim_id": "(74,4,0)", "source_info": "S. San Andreas;NM+SM+NSB+SSB+BG: M7.95, Depth = 3.2km" 
    },
    { # plotting_examples[9]
        "fault_lon": [-120.56017, -117.22392], "fault_lat": [36.00196, 34.150867],
        "event_lon": -120.50703, "event_lat": 36.01471,
        "sim_id": "(86,6,0)", "source_info": "S. San Andreas;PK+CH+CC+BB+NM+SM+NSB: M8.25, Depth = 1.7km" 
    }
]
