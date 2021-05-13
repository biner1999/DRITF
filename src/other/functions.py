

def current_speed(rear_diff, gear_ratio, redline, tyre_diameter):
    return (redline*tyre_diameter) / (rear_diff * gear_ratio * 336)