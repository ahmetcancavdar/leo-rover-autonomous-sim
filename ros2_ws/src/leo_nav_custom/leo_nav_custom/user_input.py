#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
import threading

class UserInputNode(Node):
    def __init__(self):
        super().__init__('user_input_node')
        self.publisher_ = self.create_publisher(Point, '/target_goal', 10)
        self.get_logger().info("Kullanıcı Giriş Ekranı Başlatıldı.")
        
        self.input_thread = threading.Thread(target=self.ask_for_input)
        self.input_thread.daemon = True
        self.input_thread.start()

    def ask_for_input(self):
        while rclpy.ok():
            try:
                print("\n=== LEO ROVER YENİ HEDEF ===")
                x_str = input("Gitmek istediğiniz X koordinatını girin: ")
                y_str = input("Gitmek istediğiniz Y koordinatını girin: ")
                
                x = float(x_str)
                y = float(y_str)
                
                msg = Point()
                msg.x = x
                msg.y = y
                msg.z = 0.0
                
                self.publisher_.publish(msg)
                self.get_logger().info(f"Hedef gönderildi: X={x}, Y={y}")
                
            except ValueError:
                print("Hata! Lütfen sadece sayısal (float/int) değerler giriniz.")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")
                break

def main(args=None):
    rclpy.init(args=args)
    node = UserInputNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Kullanıcı ekranı kapatılıyor...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
