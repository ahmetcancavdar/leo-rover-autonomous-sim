#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point, PoseStamped
from nav_msgs.msg import Odometry
import math
import transforms3d

class GoToGoalNode(Node):
    def __init__(self):
        super().__init__('go_to_goal_node')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom_true', self.odom_callback, 10)
        
        # Terminal Input
        self.goal_sub = self.create_subscription(Point, '/target_goal', self.goal_callback, 10)
        
        self.target_x = None
        self.target_y = None
        
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        
        # P control constants
        self.k_linear = 0.5
        self.k_angular = 1.2  # Smoother turning
        
        self.distance_tolerance = 0.05 # Increased slightly to prevent infinite spin at exact center
        self.angle_tolerance = 0.05
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Go To Goal Node Başlatıldı. Hedef Bekleniyor... (/target_goal)")

    def goal_callback(self, msg):
        self.target_x = msg.x
        self.target_y = msg.y
        self.get_logger().info(f"Terminalden Hedef Alındı: X={self.target_x}, Y={self.target_y}")

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        
        # Quaternion to Euler
        quat = [orientation_q.w, orientation_q.x, orientation_q.y, orientation_q.z]
        _, _, self.current_yaw = transforms3d.euler.quat2euler(quat)

    def control_loop(self):
        if self.target_x is None or self.target_y is None:
            return
            
        distance_to_goal = math.sqrt(
            math.pow((self.target_x - self.current_x), 2) +
            math.pow((self.target_y - self.current_y), 2)
        )
        
        angle_to_goal = math.atan2(self.target_y - self.current_y, self.target_x - self.current_x)
        
        # Angle normalization [-pi, pi]
        angle_error = angle_to_goal - self.current_yaw
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
        
        cmd = Twist()
        
        if distance_to_goal >= self.distance_tolerance:
            if abs(angle_error) > 0.1: # if orientation is way off, just turn
                cmd.angular.z = self.k_angular * angle_error
                cmd.angular.z = max(min(cmd.angular.z, 0.8), -0.8)
                cmd.linear.x = 0.0
            else:
                # move forward and correctly steer gently
                cmd.angular.z = self.k_angular * angle_error
                cmd.linear.x = self.k_linear * distance_to_goal
                cmd.linear.x = min(cmd.linear.x, 0.5)
                
            self.cmd_vel_pub.publish(cmd)
        else:
            # Reached goal
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_vel_pub.publish(cmd)
            self.get_logger().info(f"Hedefe Ulaşıldı! (Mevcut: {self.current_x:.2f}, {self.current_y:.2f})")
            # Hedefi sıfırla ki sürekli log atmasın
            self.target_x = None
            self.target_y = None

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoalNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node durduruluyor...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
