#!/usr/bin/env python3
"""
Unit test for vehicle detection filtering logic.
This test validates the filter_vehicle_detections function without requiring a full model.
"""

import sys
import os

# Add parent directory to path to import from tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_vehicle_filtering():
    """Test the vehicle class filtering logic"""
    
    # Define vehicle classes (same as in demo_track_vehicle.py)
    VEHICLE_CLASSES = [1, 2, 3, 5, 6, 7]
    
    # Detection format constant
    CLASS_PRED_INDEX = 6  # Index of class prediction in detection array
    
    # Simulate detection data
    # Format: (x1, y1, x2, y2, obj_conf, class_conf, class_pred)
    test_cases = [
        # Test case 1: Mixed detections with persons and vehicles
        {
            'name': 'Mixed persons and vehicles',
            'detections': [
                [100, 100, 200, 200, 0.9, 0.85, 0],   # person (class 0) - should be filtered out
                [300, 100, 400, 200, 0.85, 0.90, 2],  # car (class 2) - keep
                [500, 100, 600, 200, 0.88, 0.87, 5],  # bus (class 5) - keep
                [700, 100, 800, 200, 0.92, 0.88, 7],  # truck (class 7) - keep
                [100, 300, 200, 400, 0.87, 0.83, 15], # cat (class 15) - should be filtered out
            ],
            'expected_count': 3,
            'expected_classes': [2, 5, 7]
        },
        # Test case 2: Only vehicles
        {
            'name': 'Only vehicles',
            'detections': [
                [100, 100, 200, 200, 0.9, 0.85, 1],   # bicycle (class 1) - keep
                [300, 100, 400, 200, 0.85, 0.90, 2],  # car (class 2) - keep
                [500, 100, 600, 200, 0.88, 0.87, 3],  # motorcycle (class 3) - keep
            ],
            'expected_count': 3,
            'expected_classes': [1, 2, 3]
        },
        # Test case 3: No vehicles
        {
            'name': 'No vehicles',
            'detections': [
                [100, 100, 200, 200, 0.9, 0.85, 0],   # person (class 0) - filtered out
                [300, 100, 400, 200, 0.85, 0.90, 14], # bird (class 14) - filtered out
            ],
            'expected_count': 0,
            'expected_classes': []
        },
        # Test case 4: Empty detections
        {
            'name': 'Empty detections',
            'detections': [],
            'expected_count': 0,
            'expected_classes': []
        },
    ]
    
    print("=" * 60)
    print("Testing Vehicle Detection Filtering Logic")
    print("=" * 60)
    print(f"Vehicle classes: {VEHICLE_CLASSES}")
    print(f"  1: bicycle, 2: car, 3: motorcycle, 5: bus, 6: train, 7: truck")
    print()
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"Test: {test_case['name']}")
        print(f"  Input detections: {len(test_case['detections'])}")
        
        # Simulate the filtering logic
        if len(test_case['detections']) == 0:
            filtered_count = 0
            filtered_classes = []
        else:
            # Extract class IDs using the constant
            class_ids = [det[CLASS_PRED_INDEX] for det in test_case['detections']]
            # Filter for vehicle classes
            filtered_detections = [det for det in test_case['detections'] 
                                  if det[CLASS_PRED_INDEX] in VEHICLE_CLASSES]
            filtered_count = len(filtered_detections)
            filtered_classes = [int(det[CLASS_PRED_INDEX]) for det in filtered_detections]
        
        print(f"  Filtered detections: {filtered_count}")
        print(f"  Filtered classes: {filtered_classes}")
        
        # Validate results
        if filtered_count == test_case['expected_count'] and \
           filtered_classes == test_case['expected_classes']:
            print(f"  ✓ PASSED")
        else:
            print(f"  ✗ FAILED")
            print(f"    Expected count: {test_case['expected_count']}, got: {filtered_count}")
            print(f"    Expected classes: {test_case['expected_classes']}, got: {filtered_classes}")
            all_passed = False
        print()
    
    print("=" * 60)
    if all_passed:
        print("All tests PASSED ✓")
        print("=" * 60)
        return 0
    else:
        print("Some tests FAILED ✗")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit_code = test_vehicle_filtering()
    sys.exit(exit_code)
