#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray

class GridLabelsNode(Node):
    def __init__(self):
        super().__init__('grid_labels_node')
        self.publisher = self.create_publisher(MarkerArray, '/grid_labels', 10)
        self.timer = self.create_timer(1.0, self.publish_markers)
        self.get_logger().info("RViz Koordinat Yazıları (X,Y) Başlatıldı.")

    def publish_markers(self):
        marker_array = MarkerArray()
        id_counter = 0
        
        for x in range(-5, 6):
            for y in range(-5, 6):
                marker = Marker()
                marker.header.frame_id = "odom"
                marker.header.stamp = self.get_clock().now().to_msg()
                marker.ns = "grid_texts"
                marker.id = id_counter
                marker.type = Marker.TEXT_VIEW_FACING
                marker.action = Marker.ADD
                
                # Setup Position
                marker.pose.position.x = float(x)
                marker.pose.position.y = float(y)
                marker.pose.position.z = 0.2  # Slightly above the ground
                
                # Setup text and appearance
                marker.text = f"({x}, {y})"
                marker.scale.z = 0.3  # Text height
                
                # Green Color
                marker.color.a = 1.0 
                marker.color.r = 0.2
                marker.color.g = 1.0
                marker.color.b = 0.2
                
                marker_array.markers.append(marker)
                id_counter += 1
                
        self.publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = GridLabelsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
