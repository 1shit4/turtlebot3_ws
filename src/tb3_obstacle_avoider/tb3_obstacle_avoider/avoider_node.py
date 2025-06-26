import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class AvoiderNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoider_node')
        
        # Create publisher for velocity commands
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Create subscriber to the laser scan data
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        
        # We will use a timer to control the robot's movement decisions
        timer_period = 0.1  # seconds (10 Hz)
        self.timer = self.create_timer(timer_period, self.move_robot)
        
        # State variable
        self.is_obstacle_in_front = False
        
        # Threshold for obstacle detection (in meters)
        self.obstacle_distance_threshold = 0.3 # 30 cm

        self.get_logger().info('Obstacle Avoider Node has been started.')

    def scan_callback(self, msg):
        # The laser scan data is an array of range measurements.
        # The element at index 0 is the measurement directly in front of the robot.
        front_distance = msg.ranges[0]
        
        # Check if the distance is finite (not 'inf' or 'nan') and below our threshold
        if front_distance > 0.0 and front_distance < self.obstacle_distance_threshold:
            self.is_obstacle_in_front = True
        else:
            self.is_obstacle_in_front = False

    def move_robot(self):
        # Create a new Twist message
        twist = Twist()
        
        # Decide on movement based on the obstacle state
        if self.is_obstacle_in_front:
            # Obstacle detected: stop moving forward and turn
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # Turn counter-clockwise
            self.get_logger().info('Obstacle detected! Turning...')
        else:
            # No obstacle: move forward
            twist.linear.x = 0.2  # Move forward at 0.2 m/s
            twist.angular.z = 0.0
            self.get_logger().info('Path is clear. Moving forward...')
            
        # Publish the movement command
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    avoider_node = AvoiderNode()
    rclpy.spin(avoider_node)
    
    # Destroy the node explicitly
    avoider_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()