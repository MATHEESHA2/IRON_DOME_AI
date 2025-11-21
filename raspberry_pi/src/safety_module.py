class SafetyModule:
    def __init__(self, min_safe_distance_cm=10, max_safe_distance_cm=200):
        self.min_safe = min_safe_distance_cm
        self.max_safe = max_safe_distance_cm

    def is_safe_to_fire(self, depth_cm, resp=None):
        if depth_cm is None:
            return False
        return (self.min_safe < depth_cm < self.max_safe)
